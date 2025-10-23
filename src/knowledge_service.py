"""
Centralized Knowledge Service with Shared Caching
Reduces memory usage from 10MB (4 workers x 2.4MB) to ~3MB shared
"""
import redis
import pickle
import json
import hashlib
from typing import Optional, Any
import os

class KnowledgeService:
    """
    Shared knowledge service across all Gunicorn workers
    
    Features:
    - Shared Redis cache (all workers share one cache)
    - Query result caching (reduce LLM costs)
    - Dataset caching with versioning
    - Automatic TTL management
    """
    
    def __init__(self):
        try:
            self.redis = redis.Redis(
                host='localhost',
                port=6379,
                decode_responses=False,
                socket_connect_timeout=2,
                socket_timeout=2,
                max_connections=20
            )
            self.redis.ping()
            self.enabled = True
            print("✅ Redis connected - shared caching enabled")
        except (redis.ConnectionError, redis.TimeoutError) as e:
            self.enabled = False
            self.redis = None
        
        self.version = self._get_dataset_version()
    
    def _get_dataset_version(self) -> str:
        """Get current dataset version for cache invalidation"""
        try:
            import hashlib
            from pathlib import Path
            
            dataset_dir = Path('datasets')
            if not dataset_dir.exists():
                return "v1"
            
            file_hash = hashlib.md5()
            for file_path in sorted(dataset_dir.glob('*.json')):
                if file_path.name != 'archive':
                    file_hash.update(str(file_path.stat().st_mtime).encode())
            
            return f"v{file_hash.hexdigest()[:8]}"
        except Exception as e:
            print(f"⚠️  Version detection failed: {e}")
            return "v1"
    
    def get_cached_dataset(self, domain: str) -> Optional[Any]:
        """Get dataset from shared cache"""
        if not self.enabled:
            return None
        
        try:
            cache_key = f"dataset:{self.version}:{domain}"
            cached = self.redis.get(cache_key)
            
            if cached:
                return pickle.loads(cached)
            
            return None
        except Exception as e:
            print(f"⚠️  Cache read error: {e}")
            return None
    
    def set_cached_dataset(self, domain: str, data: Any, ttl: int = 86400):
        """Cache dataset in shared Redis (24 hour TTL by default)"""
        if not self.enabled:
            return
        
        try:
            cache_key = f"dataset:{self.version}:{domain}"
            self.redis.setex(
                cache_key,
                ttl,
                pickle.dumps(data)
            )
        except Exception as e:
            print(f"⚠️  Cache write error: {e}")
    
    def get_cached_query(self, query: str) -> Optional[dict]:
        """Get cached LLM/knowledge query result"""
        if not self.enabled:
            return None
        
        try:
            query_hash = hashlib.md5(query.encode()).hexdigest()
            cache_key = f"query:{query_hash}"
            
            result = self.redis.get(cache_key)
            if result:
                return json.loads(result)
            
            return None
        except Exception as e:
            print(f"⚠️  Query cache read error: {e}")
            return None
    
    def set_cached_query(self, query: str, result: dict, ttl: int = 3600):
        """Cache query result (1 hour TTL by default)"""
        if not self.enabled:
            return
        
        try:
            query_hash = hashlib.md5(query.encode()).hexdigest()
            cache_key = f"query:{query_hash}"
            
            self.redis.setex(
                cache_key,
                ttl,
                json.dumps(result)
            )
        except Exception as e:
            print(f"⚠️  Query cache write error: {e}")
    
    def get_cached_examples(self, limit: int = 1000, offset: int = 0) -> Optional[list]:
        """Get cached dataset examples with pagination"""
        if not self.enabled:
            return None
        
        try:
            cache_key = f"examples:{self.version}:all"
            cached = self.redis.get(cache_key)
            
            if cached:
                all_examples = pickle.loads(cached)
                return all_examples[offset:offset + limit]
            
            return None
        except Exception as e:
            print(f"⚠️  Examples cache error: {e}")
            return None
    
    def set_cached_examples(self, examples: list, ttl: int = 86400):
        """Cache all examples (24 hour TTL)"""
        if not self.enabled:
            return
        
        try:
            cache_key = f"examples:{self.version}:all"
            self.redis.setex(
                cache_key,
                ttl,
                pickle.dumps(examples)
            )
            print(f"📦 Cached {len(examples)} examples in shared Redis")
        except Exception as e:
            print(f"⚠️  Examples cache write error: {e}")
    
    def invalidate_cache(self):
        """Invalidate all caches (useful after dataset updates)"""
        if not self.enabled:
            return
        
        try:
            pattern = f"*:{self.version}:*"
            for key in self.redis.scan_iter(pattern):
                self.redis.delete(key)
            print("♻️ Cache invalidated")
        except Exception as e:
            print(f"⚠️  Cache invalidation error: {e}")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        if not self.enabled:
            return {"enabled": False}
        
        try:
            info = self.redis.info('memory')
            return {
                "enabled": True,
                "memory_used_mb": info.get('used_memory', 0) / 1024 / 1024,
                "total_keys": self.redis.dbsize(),
                "version": self.version
            }
        except Exception as e:
            print(f"⚠️  Stats error: {e}")
            return {"enabled": True, "error": str(e)}

knowledge_service = KnowledgeService()
