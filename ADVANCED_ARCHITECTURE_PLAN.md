# MC AI Advanced Architecture Plan
**Scalable Architecture for High-Process Loads**

## Executive Summary

The current lazy loading fix is a band-aid solution. To scale MC AI beyond 10,000+ examples and handle increasing process loads, we need a comprehensive architectural upgrade with:

1. **Centralized Knowledge Service** - Shared dataset management across workers
2. **Database-Backed Datasets** - Move from files to PostgreSQL for scalability
3. **Async Task Queue** - Offload heavy operations to background workers
4. **Shared Caching** - Redis/KeyDB for cross-worker cache efficiency
5. **Memory Optimization** - Reduce per-worker memory from 2.4MB to shared pools

**Goal:** Maintain <2s mobile load times while scaling to 100k+ examples

---

## Current Architecture Issues

### 🔴 Critical Bottlenecks

| Issue | Current State | Impact |
|-------|--------------|---------|
| **Memory Duplication** | Each of 4 workers loads 2.4MB cache | 9.6MB total, grows linearly |
| **Cold Start Latency** | Python imports + heavy constructors | Multi-second delays on worker spawn |
| **File-Based Datasets** | 5,012 examples in JSON/TXT files | Slow I/O, no pagination, no querying |
| **Sequential Processing** | Heavy operations block request thread | Poor concurrency for art/music/cymatic |
| **Per-Instance Cache** | LRU cache not shared across workers | Duplicate API calls, higher costs |
| **Dataset Growth Limit** | File-based system won't scale past ~15k | Eventual performance collapse |

### 📊 Current Performance

- **Workers:** 4 Gunicorn sync workers
- **Memory per worker:** 2.4MB cache + engine overhead
- **Total memory:** ~10MB across workers (duplicated)
- **Cold start:** 1s (with lazy loading)
- **Dataset size:** 5,012 examples
- **Cache strategy:** Pickle file per worker

---

## Proposed Architecture: Tiered Knowledge Service

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      MOBILE/WEB CLIENT                       │
│                     <2s Initial Load ✅                      │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌──────▼─────┐  ┌──────▼─────┐
│   Worker 1   │  │  Worker 2  │  │  Worker 3  │  (Gunicorn)
│  (Thin Web)  │  │ (Thin Web) │  │ (Thin Web) │
└──────┬───────┘  └──────┬─────┘  └──────┬─────┘
       │                 │                │
       └─────────────────┼────────────────┘
                         │
        ┌────────────────▼────────────────┐
        │    KNOWLEDGE SERVICE LAYER      │
        │  (Shared Memory / Redis Cache)  │
        │                                 │
        │  • Dataset Index (versioned)    │
        │  • Embedding Cache              │
        │  • LLM Response Cache           │
        │  • Frequency Mappings           │
        └────────┬────────────────────────┘
                 │
        ┌────────┼────────────────┐
        │        │                │
┌───────▼─────┐  │  ┌─────────────▼─────────┐
│ PostgreSQL  │  │  │   ASYNC TASK QUEUE    │
│             │  │  │  (Redis Queue / PG)   │
│ • datasets  │  │  │                       │
│ • examples  │  │  │  • Art Generation     │
│ • embeddings│  │  │  • Music Synthesis    │
│ • metadata  │  │  │  • Cymatic Analysis   │
│ • feedback  │  │  │  • Video Generation   │
└─────────────┘  │  └───────────────────────┘
                 │
        ┌────────▼────────┐
        │  STATIC CACHE   │
        │  (File System)  │
        │                 │
        │ • Compiled FFT  │
        │ • Model Weights │
        │ • Game Assets   │
        └─────────────────┘
```

---

## Phase 1: Knowledge Service (Shared Cache)

### 1.1 Shared Memory Dataset Cache

**Current:** Each worker loads 2.4MB pickle cache
**Proposed:** Single shared cache across all workers

#### Option A: Redis/KeyDB (Recommended)
```python
# src/knowledge_service.py
import redis
import json
import pickle

class KnowledgeService:
    """Centralized knowledge service with shared caching"""
    
    def __init__(self):
        self.redis = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=False,  # Binary for pickle
            max_connections=20
        )
        self.version = self._get_dataset_version()
    
    def get_dataset(self, domain: str, cache=True):
        """Get dataset from cache or load"""
        cache_key = f"dataset:{self.version}:{domain}"
        
        if cache:
            cached = self.redis.get(cache_key)
            if cached:
                return pickle.loads(cached)
        
        # Load from PostgreSQL or files
        dataset = self._load_dataset(domain)
        
        # Cache with TTL (24 hours)
        self.redis.setex(
            cache_key,
            86400,
            pickle.dumps(dataset)
        )
        
        return dataset
    
    def query_knowledge(self, query: str, cache=True):
        """Query with shared LRU cache"""
        cache_key = f"query:{hash(query)}"
        
        if cache:
            result = self.redis.get(cache_key)
            if result:
                return json.loads(result)
        
        # Generate response
        result = self._query_llm(query)
        
        # Cache for 1 hour
        self.redis.setex(cache_key, 3600, json.dumps(result))
        
        return result

# Global singleton
knowledge_service = KnowledgeService()
```

**Benefits:**
- ✅ Single cache shared across all workers
- ✅ Memory usage: 2.4MB total (vs 9.6MB currently)
- ✅ Redis is fast (microsecond access)
- ✅ Built-in TTL and eviction policies
- ✅ Can scale horizontally later

#### Option B: Shared Memory (Alternative)
```python
# src/knowledge_service_shm.py
from multiprocessing import shared_memory
import numpy as np

class SharedKnowledgeService:
    """Process-shared memory for datasets"""
    
    def __init__(self):
        try:
            self.shm = shared_memory.SharedMemory(name="mc_ai_datasets")
        except FileNotFoundError:
            # First worker creates shared memory
            self.shm = shared_memory.SharedMemory(
                name="mc_ai_datasets",
                create=True,
                size=10_000_000  # 10MB
            )
            self._initialize_shared_data()
```

**Trade-offs:**
- ✅ No external dependency (Redis)
- ❌ More complex to manage
- ❌ Fixed size allocation
- ⚠️ Best for read-only data

### 1.2 Gunicorn Post-Fork Warmup

**Warm shared cache on first worker spawn to avoid cold start spikes**

```python
# app.py
def on_starting(server):
    """Called before workers are spawned"""
    print("🔄 Initializing shared knowledge service...")
    from src.knowledge_service import knowledge_service
    knowledge_service.warmup()
    print("✅ Knowledge service ready")

# gunicorn.conf.py
on_starting = on_starting
workers = 4
worker_class = 'sync'
preload_app = True  # Share memory across workers
```

**Benefits:**
- First worker primes the cache
- Other workers connect to warm cache
- No simultaneous spikes

---

## Phase 2: Database-Backed Datasets

### 2.1 PostgreSQL Schema

**Current:** 5,012 examples in 48+ JSON/TXT files
**Proposed:** Normalized relational schema with versioning

```sql
-- Dataset domains
CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    domain_name VARCHAR(100) UNIQUE NOT NULL,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    example_count INTEGER DEFAULT 0,
    metadata JSONB
);

-- Dataset examples
CREATE TABLE examples (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER REFERENCES datasets(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    response TEXT,
    metadata JSONB,
    embedding VECTOR(1536),  -- For semantic search
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_dataset_id (dataset_id),
    INDEX idx_embedding USING ivfflat (embedding vector_cosine_ops)
);

-- Emotion catalog
CREATE TABLE emotions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    neuroscience_freq FLOAT,
    metaphysical_freq FLOAT,
    personality_template JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Knowledge cache
CREATE TABLE knowledge_cache (
    id SERIAL PRIMARY KEY,
    query_hash VARCHAR(64) UNIQUE NOT NULL,
    query_text TEXT NOT NULL,
    response JSONB NOT NULL,
    source VARCHAR(50),  -- 'dataset', 'wikipedia', 'web', 'llm'
    created_at TIMESTAMP DEFAULT NOW(),
    accessed_at TIMESTAMP DEFAULT NOW(),
    access_count INTEGER DEFAULT 1,
    ttl INTERVAL DEFAULT '1 hour'
);

-- Indexes
CREATE INDEX idx_knowledge_hash ON knowledge_cache(query_hash);
CREATE INDEX idx_knowledge_ttl ON knowledge_cache(created_at, ttl);
```

### 2.2 Dataset Migration Strategy

```python
# scripts/migrate_datasets_to_db.py
"""Migrate file-based datasets to PostgreSQL"""
import psycopg2
import json
from pathlib import Path

def migrate_datasets():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    
    dataset_dir = Path('datasets')
    
    for domain_file in dataset_dir.glob('*.json'):
        domain_name = domain_file.stem
        
        # Skip archive
        if domain_name == 'archive':
            continue
        
        # Create dataset entry
        cur.execute(
            "INSERT INTO datasets (domain_name) VALUES (%s) "
            "ON CONFLICT (domain_name) DO UPDATE SET updated_at = NOW() "
            "RETURNING id",
            (domain_name,)
        )
        dataset_id = cur.fetchone()[0]
        
        # Load examples
        with open(domain_file) as f:
            data = json.load(f)
            examples = data.get('examples', [])
        
        # Insert examples
        for example in examples:
            content = example.get('content', example.get('completion', ''))
            response = example.get('response', '')
            
            cur.execute(
                "INSERT INTO examples (dataset_id, content, response, metadata) "
                "VALUES (%s, %s, %s, %s)",
                (dataset_id, content, response, json.dumps(example))
            )
        
        # Update count
        cur.execute(
            "UPDATE datasets SET example_count = "
            "(SELECT COUNT(*) FROM examples WHERE dataset_id = %s) "
            "WHERE id = %s",
            (dataset_id, dataset_id)
        )
        
        print(f"✅ Migrated {domain_name}: {len(examples)} examples")
    
    conn.commit()
    conn.close()
```

### 2.3 Database-Backed DatasetBank

```python
# src/dataset_bank_v2.py
import psycopg2.pool

class DatasetBankV2:
    """Database-backed dataset management"""
    
    def __init__(self):
        self.pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=os.environ['DATABASE_URL']
        )
    
    def query(self, domain: str = None, limit: int = 100, offset: int = 0):
        """Paginated query with optional domain filter"""
        conn = self.pool.getconn()
        try:
            cur = conn.cursor()
            
            if domain:
                cur.execute(
                    "SELECT e.content, e.response, e.metadata "
                    "FROM examples e "
                    "JOIN datasets d ON e.dataset_id = d.id "
                    "WHERE d.domain_name = %s "
                    "LIMIT %s OFFSET %s",
                    (domain, limit, offset)
                )
            else:
                cur.execute(
                    "SELECT content, response, metadata "
                    "FROM examples "
                    "LIMIT %s OFFSET %s",
                    (limit, offset)
                )
            
            return cur.fetchall()
        
        finally:
            self.pool.putconn(conn)
    
    def semantic_search(self, query_embedding, top_k=10):
        """Vector similarity search"""
        conn = self.pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT content, response, "
                "embedding <=> %s AS distance "
                "FROM examples "
                "WHERE embedding IS NOT NULL "
                "ORDER BY distance "
                "LIMIT %s",
                (query_embedding, top_k)
            )
            return cur.fetchall()
        finally:
            self.pool.putconn(conn)
```

**Benefits:**
- ✅ Pagination: Load 100 examples at a time (not 5,012!)
- ✅ Filtering: Query by domain, date, frequency
- ✅ Semantic search: Vector embeddings for relevance
- ✅ Versioning: Track dataset changes
- ✅ Scalability: Can handle 1M+ examples
- ✅ Backups: PostgreSQL replication built-in

---

## Phase 3: Async Task Queue

### 3.1 Background Task Architecture

**Current:** Heavy operations block web request thread
**Proposed:** Offload to async workers

```python
# src/task_queue.py
import redis
from rq import Queue, Worker
from rq.job import Job

# Connect to Redis
redis_conn = redis.Redis(host='localhost', port=6379)

# Task queues
art_queue = Queue('art', connection=redis_conn)
music_queue = Queue('music', connection=redis_conn)
cymatic_queue = Queue('cymatic', connection=redis_conn)
emotion_queue = Queue('emotion', connection=redis_conn)

# Task functions
def generate_art_task(prompt: str, style: str, options: dict):
    """Background art generation"""
    from src.art_generator import ArtGenerator
    generator = ArtGenerator()
    return generator.generate(prompt, style, **options)

def generate_music_task(prompt: str, duration: int, options: dict):
    """Background music generation"""
    from src.music_generator import MusicGenerator
    generator = MusicGenerator()
    return generator.generate(prompt, duration, **options)

def analyze_cymatic_task(frequencies: list, options: dict):
    """Background cymatic analysis"""
    from src.advanced_cymatics import AdvancedCymaticEngine
    engine = AdvancedCymaticEngine()
    return engine.analyze(frequencies, **options)
```

### 3.2 API Integration

```python
# app.py - Async endpoints
from src.task_queue import art_queue, music_queue

@app.route('/api/art/generate-async', methods=['POST'])
def api_art_generate_async():
    """Submit art generation job"""
    data = request.get_json()
    
    # Enqueue task
    job = art_queue.enqueue(
        'src.task_queue.generate_art_task',
        data['prompt'],
        data.get('style', 'abstract'),
        data.get('options', {}),
        job_timeout='5m'
    )
    
    return jsonify({
        'job_id': job.id,
        'status': 'queued',
        'poll_url': f'/api/job/{job.id}'
    })

@app.route('/api/job/<job_id>', methods=['GET'])
def api_job_status(job_id):
    """Poll job status"""
    job = Job.fetch(job_id, connection=redis_conn)
    
    if job.is_finished:
        return jsonify({
            'status': 'completed',
            'result': job.result
        })
    elif job.is_failed:
        return jsonify({
            'status': 'failed',
            'error': str(job.exc_info)
        })
    else:
        return jsonify({
            'status': 'processing',
            'progress': job.meta.get('progress', 0)
        })
```

### 3.3 Worker Deployment

```bash
# Start background workers
rq worker art music cymatic emotion --with-scheduler
```

**Benefits:**
- ✅ Web workers stay responsive
- ✅ Heavy tasks don't block requests
- ✅ Can scale workers independently
- ✅ Job retry and failure handling
- ✅ Progress tracking for long jobs

---

## Phase 4: Memory Optimization

### 4.1 Lazy Engine Factories

**Current:** All engines initialized on worker startup
**Proposed:** Factory pattern with lazy loading

```python
# src/engine_factory.py
class EngineFactory:
    """Lazy engine initialization"""
    
    def __init__(self):
        self._engines = {}
    
    def get_cymatic_engine(self):
        if 'cymatic' not in self._engines:
            from src.cymatic import CymaticTransformer
            self._engines['cymatic'] = CymaticTransformer(use_advanced=True)
        return self._engines['cymatic']
    
    def get_art_generator(self):
        if 'art' not in self._engines:
            from src.art_generator import ArtGenerator
            self._engines['art'] = ArtGenerator()
        return self._engines['art']
    
    # ... other engines

# Global factory
engine_factory = EngineFactory()
```

### 4.2 Memory-Mapped Cymatic Buffers

**Current:** Large arrays in RAM
**Proposed:** Memory-mapped files for intermediate results

```python
# src/cymatic_v2.py
import numpy as np
import tempfile

class CymaticTransformerV2:
    """Memory-efficient cymatic analysis"""
    
    def analyze(self, frequency: float):
        # Use memory-mapped file for large array
        with tempfile.NamedTemporaryFile() as tmp:
            # Create memory-mapped array
            mmap_array = np.memmap(
                tmp.name,
                dtype='float64',
                mode='w+',
                shape=(1000, 1000)
            )
            
            # Compute directly into mmap
            self._compute_pattern(frequency, mmap_array)
            
            # Only load final result into RAM
            result = mmap_array[:100, :100].copy()
            
            del mmap_array
            return result
```

### 4.3 Compiled FFT Kernel Pool

**Reuse compiled kernels across requests**

```python
# src/fft_pool.py
import numpy as np
from scipy import fft
from functools import lru_cache

@lru_cache(maxsize=16)
def get_fft_plan(size: int):
    """Get cached FFT plan for size"""
    # scipy.fft automatically caches plans
    # This just ensures we reuse common sizes
    return fft.rfft(np.zeros(size))

class FFTPool:
    """Reusable FFT computation pool"""
    
    def compute(self, signal: np.ndarray):
        """Compute FFT using cached plan"""
        # scipy.fft will reuse plan for same size
        return fft.rfft(signal)
```

---

## Phase 5: Monitoring & Guardrails

### 5.1 Performance Monitoring

```python
# src/monitoring.py
import time
import psutil
from prometheus_client import Counter, Histogram, Gauge

# Metrics
request_duration = Histogram(
    'mc_ai_request_duration_seconds',
    'Request duration',
    ['endpoint']
)

cache_hits = Counter(
    'mc_ai_cache_hits_total',
    'Cache hit count',
    ['cache_type']
)

worker_memory = Gauge(
    'mc_ai_worker_memory_mb',
    'Worker memory usage'
)

def monitor_request(func):
    """Decorator to monitor request performance"""
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start
            request_duration.labels(endpoint=func.__name__).observe(duration)
            
            # Update memory gauge
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            worker_memory.set(memory_mb)
    
    return wrapper
```

### 5.2 Dataset Size Guardrails

```python
# src/dataset_rotator_v2.py
class DatasetRotatorV2:
    """Automatic dataset rotation with DB support"""
    
    def __init__(self, max_examples_per_domain=1000):
        self.max_examples = max_examples_per_domain
    
    def rotate_if_needed(self):
        """Archive old examples when domain exceeds limit"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Find domains over limit
        cur.execute("""
            SELECT id, domain_name, example_count 
            FROM datasets 
            WHERE example_count > %s
        """, (self.max_examples,))
        
        for dataset_id, domain_name, count in cur.fetchall():
            # Archive oldest examples
            archive_count = count - self.max_examples
            
            cur.execute("""
                WITH archived AS (
                    DELETE FROM examples 
                    WHERE dataset_id = %s 
                    AND id IN (
                        SELECT id FROM examples 
                        WHERE dataset_id = %s 
                        ORDER BY created_at ASC 
                        LIMIT %s
                    )
                    RETURNING *
                )
                INSERT INTO examples_archive 
                SELECT * FROM archived
            """, (dataset_id, dataset_id, archive_count))
            
            print(f"♻️ Rotated {archive_count} examples from {domain_name}")
        
        conn.commit()
```

---

## Implementation Roadmap

### Sprint 1: Foundation (Week 1-2)
**Goal:** Shared caching infrastructure

- [ ] Install and configure Redis/KeyDB
- [ ] Create KnowledgeService module
- [ ] Implement shared dataset cache
- [ ] Add Gunicorn post_fork warmup
- [ ] Update ResponseGenerator to use KnowledgeService
- [ ] Test memory usage (target: <5MB total vs 10MB)

**Success Metrics:**
- Memory usage reduced by 50%
- Cache hit rate >80%
- Cold start <1s maintained

### Sprint 2: Database Migration (Week 3-4)
**Goal:** Move datasets to PostgreSQL

- [ ] Create database schema (datasets, examples, embeddings)
- [ ] Write migration script
- [ ] Migrate current 5,012 examples
- [ ] Implement DatasetBankV2 with pagination
- [ ] Add semantic search with vector embeddings
- [ ] Update KnowledgeEngine to query database

**Success Metrics:**
- All datasets migrated successfully
- Query latency <50ms for 100 examples
- Pagination working correctly
- Can handle 10k+ examples without slowdown

### Sprint 3: Async Task Queue (Week 5-6)
**Goal:** Offload heavy operations

- [ ] Set up Redis Queue (RQ) or PostgreSQL-based queue
- [ ] Create task workers for art/music/cymatic
- [ ] Update API endpoints for async generation
- [ ] Implement job polling/streaming
- [ ] Add progress tracking
- [ ] Deploy background workers

**Success Metrics:**
- Web workers respond in <100ms
- Background jobs complete successfully
- Can handle 10 concurrent art generations
- No request timeouts

### Sprint 4: Memory Optimization (Week 7-8)
**Goal:** Reduce memory footprint

- [ ] Implement EngineFactory with lazy loading
- [ ] Add memory-mapped buffers for cymatic
- [ ] Create FFT kernel pool
- [ ] Optimize emotion engine memory
- [ ] Add memory monitoring

**Success Metrics:**
- Worker RSS <200MB per worker
- Cymatic analysis uses <50MB peak
- FFT kernel reuse >90%

### Sprint 5: Monitoring & Polish (Week 9-10)
**Goal:** Production-ready observability

- [ ] Add Prometheus metrics
- [ ] Create performance dashboard
- [ ] Implement dataset rotation guardrails
- [ ] Add circuit breakers for external APIs
- [ ] Load testing (simulate 100+ concurrent users)
- [ ] Documentation updates

**Success Metrics:**
- All metrics collecting correctly
- System handles 100 concurrent requests
- Dataset rotation working automatically
- <2s mobile load maintained under load

---

## Quick Wins (Can Implement Now)

### 1. Redis Shared Cache (2 hours)
```bash
# Install Redis
nix-env -iA nixpkgs.redis

# Start Redis
redis-server --daemonize yes

# Update Python requirements
pip install redis
```

### 2. Gunicorn Warmup Hook (30 mins)
```python
# gunicorn.conf.py
def on_starting(server):
    print("🔥 Warming shared cache...")
    # Pre-load critical datasets
    
workers = 4
preload_app = True
```

### 3. Database Schema Setup (1 hour)
```python
# scripts/create_schema.py
# Run PostgreSQL migrations
```

### 4. Memory Monitoring (1 hour)
```python
# Add psutil monitoring to existing endpoints
import psutil

@app.before_request
def log_memory():
    memory_mb = psutil.Process().memory_info().rss / 1024 / 1024
    if memory_mb > 500:
        print(f"⚠️ High memory: {memory_mb:.1f}MB")
```

---

## Expected Outcomes

### Before (Current State)
- **Memory:** 10MB (4 workers × 2.4MB each)
- **Cold start:** 1s (with lazy loading)
- **Dataset limit:** ~15k examples before degradation
- **Concurrent heavy ops:** 1-2 (blocks web workers)
- **Cache efficiency:** Low (duplicated across workers)

### After (Fully Implemented)
- **Memory:** 3-5MB shared (80% reduction)
- **Cold start:** <500ms (pre-warmed cache)
- **Dataset limit:** 100k+ examples (database pagination)
- **Concurrent heavy ops:** 20+ (async workers)
- **Cache efficiency:** High (shared + Redis)
- **Mobile load:** <2s even with 100k examples
- **Scalability:** Can add more workers/machines

---

## Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| **Redis dependency** | Use PostgreSQL as fallback cache |
| **Database migration complexity** | Migrate incrementally, keep files as backup |
| **Async queue learning curve** | Start with simple RQ, well-documented |
| **Memory-mapped file bugs** | Extensive testing, fallback to RAM |
| **Over-engineering** | Implement in sprints, measure ROI |

---

## Decision Points

### Choose Cache Backend

**Option A: Redis (Recommended)**
- ✅ Fast, battle-tested, simple
- ✅ Built-in TTL and eviction
- ❌ External dependency

**Option B: PostgreSQL JSONB**
- ✅ No extra dependency
- ✅ ACID guarantees
- ❌ Slower than Redis

**Option C: Shared Memory**
- ✅ No dependency, fastest
- ❌ Complex management, fixed size

**Recommendation:** Redis for speed and simplicity

### Choose Task Queue

**Option A: Redis Queue (RQ)**
- ✅ Simple Python API
- ✅ Great for most use cases
- ❌ Requires Redis

**Option B: PostgreSQL + Custom**
- ✅ No extra dependency
- ❌ More code to maintain

**Option C: Celery**
- ✅ Feature-rich, mature
- ❌ Heavy, overkill for our needs

**Recommendation:** RQ for simplicity

---

## Conclusion

This architecture upgrade transforms MC AI from a monolithic file-based system to a scalable, distributed architecture that:

1. **Eliminates memory duplication** - Shared cache across workers
2. **Scales datasets** - PostgreSQL handles 100k+ examples
3. **Improves concurrency** - Async workers for heavy tasks
4. **Maintains performance** - <2s mobile loads even under load
5. **Enables horizontal scaling** - Can add more machines later

**Next Step:** Start with Sprint 1 (Redis shared cache) as a quick win to validate the approach.

---

**Status:** 📋 **PLANNING COMPLETE - READY FOR IMPLEMENTATION**
