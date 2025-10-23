# 🔍 Llama Embeddings Reference Guide

## Overview
Llama Embeddings enable semantic search and similarity matching in MC AI using local Llama models. This is better than keyword matching for finding relevant information.

**Note:** Requires Ollama running on port 11434. Not available in Replit production due to port restrictions.

---

## Prerequisites

### System Requirements
- Ollama installed and running
- Port 11434 accessible
- Llama model installed (llama3.2:3b recommended for embeddings)

### Installation
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start service
ollama serve

# Pull model (3B is fast for embeddings)
ollama pull llama3.2:3b
```

---

## Implementation

### File: `src/llama_embeddings.py`

```python
"""
Llama Embeddings for MC AI
Semantic search using Llama models
"""

import requests
import numpy as np
from typing import List, Dict, Optional
import json
import os
import hashlib

class LlamaEmbeddings:
    """Semantic embeddings using Llama"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "llama3.2:3b"
        self.embedding_cache = {}
        self.cache_file = "user_data/embeddings_cache.json"
        self._load_cache()
    
    def get_embedding(self, text: str) -> Optional[np.ndarray]:
        """Get embedding vector for text"""
        cache_key = hashlib.md5(text.encode()).hexdigest()
        
        if cache_key in self.embedding_cache:
            return np.array(self.embedding_cache[cache_key])
        
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={'model': self.model, 'prompt': text},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                embedding = np.array(data['embedding'])
                
                self.embedding_cache[cache_key] = embedding.tolist()
                self._save_cache()
                
                return embedding
        except:
            pass
        
        return None
    
    def similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity (0-1)"""
        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)
        
        if emb1 is None or emb2 is None:
            return 0.0
        
        # Cosine similarity
        similarity = np.dot(emb1, emb2) / (
            np.linalg.norm(emb1) * np.linalg.norm(emb2)
        )
        
        # Convert to 0-1 range
        return float((similarity + 1) / 2)
    
    def find_most_similar(self, query: str, candidates: List[str], top_k: int = 5) -> List[Dict]:
        """Find most similar texts"""
        query_emb = self.get_embedding(query)
        
        if query_emb is None:
            return []
        
        similarities = []
        
        for candidate in candidates:
            cand_emb = self.get_embedding(candidate)
            
            if cand_emb is not None:
                sim = np.dot(query_emb, cand_emb) / (
                    np.linalg.norm(query_emb) * np.linalg.norm(cand_emb)
                )
                similarities.append({
                    'text': candidate,
                    'similarity': float((sim + 1) / 2)
                })
        
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]
    
    def _load_cache(self):
        """Load cache from disk"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    self.embedding_cache = json.load(f)
            except:
                self.embedding_cache = {}
    
    def _save_cache(self):
        """Save cache to disk"""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.embedding_cache, f)
        except:
            pass
```

---

## Enhanced Dataset Search

### File: `src/semantic_search.py`

```python
"""Semantic dataset search using embeddings"""

from src.llama_embeddings import LlamaEmbeddings
from typing import List, Dict

class SemanticDatasetSearch:
    """Enhanced dataset search with semantic similarity"""
    
    def __init__(self, dataset_bank):
        self.dataset_bank = dataset_bank
        self.embeddings = LlamaEmbeddings()
    
    def semantic_search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search using semantic similarity"""
        
        # Get all examples
        all_examples = []
        for domain_data in self.dataset_bank.datasets.values():
            all_examples.extend(domain_data['examples'])
        
        query_emb = self.embeddings.get_embedding(query)
        
        if query_emb is None:
            # Fallback to keyword search
            return self.dataset_bank.search(query, limit)
        
        # Calculate similarities
        results = []
        
        for example in all_examples:
            prompt = example['prompt']
            prompt_emb = self.embeddings.get_embedding(prompt)
            
            if prompt_emb is not None:
                similarity = np.dot(query_emb, prompt_emb) / (
                    np.linalg.norm(query_emb) * np.linalg.norm(prompt_emb)
                )
                
                results.append({
                    **example,
                    'semantic_score': float((similarity + 1) / 2)
                })
        
        results.sort(key=lambda x: x['semantic_score'], reverse=True)
        return results[:limit]
```

---

## Integration with MC AI

### Update `src/knowledge_engine.py`:

```python
from src.llama_embeddings import LlamaEmbeddings

class KnowledgeEngine:
    def __init__(self, dataset_bank):
        self.dataset_bank = dataset_bank
        self.embeddings = LlamaEmbeddings()
    
    def search(self, query: str, use_semantic: bool = True) -> List[Dict]:
        """Search with optional semantic matching"""
        
        if use_semantic and self.embeddings.get_embedding("test"):
            # Use semantic search
            return self._semantic_search(query)
        else:
            # Fallback to keyword search
            return self.dataset_bank.search(query)
    
    def _semantic_search(self, query: str) -> List[Dict]:
        """Semantic search implementation"""
        # Implementation here
        pass
```

---

## Usage Examples

### Basic Similarity
```python
from src.llama_embeddings import LlamaEmbeddings

embeddings = LlamaEmbeddings()

similarity = embeddings.similarity(
    "I'm feeling anxious",
    "I'm feeling nervous"
)
print(f"Similarity: {similarity:.3f}")  # ~0.85 (high)

similarity = embeddings.similarity(
    "I'm feeling anxious",
    "What's the weather?"
)
print(f"Similarity: {similarity:.3f}")  # ~0.30 (low)
```

### Find Similar
```python
candidates = [
    "I'm feeling stressed about work",
    "I'm anxious about my exam",
    "What's for dinner?",
    "I'm nervous about the interview"
]

results = embeddings.find_most_similar(
    "I'm worried about my test",
    candidates,
    top_k=3
)

for r in results:
    print(f"{r['text']}: {r['similarity']:.3f}")
```

### Enhanced Dataset Search
```python
from src.semantic_search import SemanticDatasetSearch

search = SemanticDatasetSearch(dataset_bank)

results = search.semantic_search("help with anxiety", limit=5)

for r in results:
    print(f"Score: {r['semantic_score']:.3f}")
    print(f"Topic: {r['prompt']}")
```

---

## Performance Optimization

### Caching Strategy
- **Cache File:** `user_data/embeddings_cache.json`
- **Cache Key:** MD5 hash of text
- **Benefits:** 100x faster for repeated queries

### Best Practices
1. Use smaller model (3B) for embeddings
2. Cache frequently used embeddings
3. Batch similar queries together
4. Precompute embeddings for dataset

---

## Comparison

### Keyword Search vs Semantic Search

| Query | Keyword Match | Semantic Match |
|-------|--------------|----------------|
| "worried about test" | ❌ "test anxiety" | ✅ "exam stress" |
| "feel sad" | ❌ "depression help" | ✅ "feeling down" |
| "can't sleep" | ❌ "insomnia tips" | ✅ "sleep problems" |

**Semantic search understands meaning, not just words.**

---

## Limitations

1. **Port Required:** Ollama on port 11434
2. **Speed:** ~100ms per embedding (cached: <1ms)
3. **Memory:** Embeddings are 4096-dimensional vectors
4. **Replit:** Not available due to port restrictions

---

## Alternative: OpenAI Embeddings

For Replit production, use OpenAI embeddings:

```python
from openai import OpenAI

client = OpenAI()

def get_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding
```

---

## Testing

```bash
# Test embeddings
python -c "
from src.llama_embeddings import LlamaEmbeddings
e = LlamaEmbeddings()

emb = e.get_embedding('test')
print(f'Embedding dimension: {len(emb) if emb else 0}')

sim = e.similarity('happy', 'joyful')
print(f'Similarity: {sim:.3f}')
"
```

---

**Status:** Reference implementation for local deployments when Ollama is available.
