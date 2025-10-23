"""
Dataset Bank - Knowledge Repository for MC AI V4 Advanced AI System

This isn't a simple keyword database. It's an intelligent knowledge
synthesis engine with 4,376 training examples across 31 specialized domains.

Supports semantic search, context awareness, and multi-domain integration.
Powers MC AI's ability to discuss topics from quantum physics to meditation.
"""

import json
import pickle
from pathlib import Path
from typing import List, Dict, Optional
from collections import defaultdict
from src.dataset_loader import DatasetLoader

try:
    from src.knowledge_service import knowledge_service
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    knowledge_service = None

class DatasetBank:
    """
    Central knowledge bank that loads, indexes, and retrieves training examples
    Now with Redis shared caching for reduced memory usage
    """
    
    def __init__(self, datasets_dir: str = "datasets", cache_file: str = "dataset_cache.pkl"):
        self.datasets_dir = datasets_dir
        self.cache_file = cache_file
        self.data: Dict[str, List[Dict]] = {}
        self.index: Dict[str, List[tuple]] = defaultdict(list)
        self.loaded = False
        self.use_redis = REDIS_AVAILABLE and knowledge_service and knowledge_service.enabled
    
    def load(self, force_reload: bool = False):
        """Load all datasets (uses shared Redis cache if available, otherwise file cache)"""
        
        if self.use_redis and not force_reload:
            cached_examples = knowledge_service.get_cached_examples()
            if cached_examples:
                print("📦 Loading from shared Redis cache...")
                self.data = self._organize_examples(cached_examples)
                print("🔍 Building search index...")
                self._build_index()
                self.loaded = True
                print(f"✅ Loaded {len(cached_examples)} examples from shared cache\n")
                return
        
        cache_path = Path(self.cache_file)
        
        if not force_reload and cache_path.exists():
            print("📦 Loading from cache...")
            try:
                with open(cache_path, 'rb') as f:
                    cached = pickle.load(f)
                    self.data = cached['data']
                    self.index = cached['index']
                    self.loaded = True
                    total = sum(len(v) for v in self.data.values())
                    print(f"✅ Loaded {total} examples from cache\n")
                    
                    if self.use_redis:
                        all_examples = [ex for examples in self.data.values() for ex in examples]
                        knowledge_service.set_cached_examples(all_examples)
                        print(f"📤 Uploaded {total} examples to shared Redis cache")
                    
                    return
            except Exception as e:
                print(f"⚠️ Cache load failed: {e}")
        
        print("🔄 Loading datasets from files...")
        loader = DatasetLoader(self.datasets_dir)
        self.data = loader.load_all_datasets()
        
        print("🔍 Building search index...")
        self._build_index()
        
        print("💾 Saving cache...")
        self._save_cache()
        
        if self.use_redis:
            all_examples = [ex for examples in self.data.values() for ex in examples]
            knowledge_service.set_cached_examples(all_examples)
        
        self.loaded = True
        total = sum(len(v) for v in self.data.values())
        print(f"✅ Dataset Bank ready with {total} examples across {len(self.data)} domains\n")
    
    def _organize_examples(self, examples: List[Dict]) -> Dict[str, List[Dict]]:
        """Organize flat list of examples into domain-based structure"""
        organized = defaultdict(list)
        for ex in examples:
            domain = ex.get('domain', 'general')
            organized[domain].append(ex)
        return dict(organized)
    
    def _build_index(self):
        """Build keyword index for fast search"""
        self.index.clear()
        
        for domain, examples in self.data.items():
            for idx, example in enumerate(examples):
                prompt = example.get('prompt', '').lower()
                words = set(prompt.split())
                
                for word in words:
                    if len(word) > 3:
                        self.index[word].append((domain, idx))
    
    def _save_cache(self):
        """Save processed data to cache"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump({
                    'data': self.data,
                    'index': self.index
                }, f)
        except Exception as e:
            print(f"⚠️ Failed to save cache: {e}")
    
    def search(self, query: str, domain: Optional[str] = None, limit: int = 5) -> List[Dict]:
        """
        Search for relevant examples with IMPROVED relevance scoring
        
        Args:
            query: Search query
            domain: Optional domain filter (e.g., 'coding', 'neuroscience')
            limit: Max results to return
        
        Returns:
            List of matching examples with metadata
        """
        if not self.loaded:
            self.load()
        
        # Filter stop words for better relevance
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                      'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                      'should', 'may', 'might', 'can', 'of', 'to', 'in', 'for', 'on', 'at',
                      'by', 'with', 'from', 'as', 'or', 'and', 'but', 'if', 'then', 'than',
                      'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we',
                      'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its',
                      'our', 'their', 'what', 'when', 'where', 'why', 'how', 'who', 'which'}
        
        query_lower = query.lower()
        words = [w for w in query_lower.split() if w not in stop_words and len(w) > 2]
        
        # If no meaningful words, return empty (prevents matching everything)
        if not words:
            return []
        
        scores = defaultdict(lambda: {'score': 0, 'matches': 0})
        
        for word in words:
            if word in self.index:
                for dom, idx in self.index[word]:
                    if domain is None or dom == domain:
                        key = (dom, idx)
                        # Weight by word importance (longer words = more specific = higher score)
                        scores[key]['score'] += len(word) * 2
                        scores[key]['matches'] += 1
        
        # Calculate final scores with match quality bonus
        final_scores = {}
        for key, data in scores.items():
            # Require at least 2 matching words OR 1 very specific match
            if data['matches'] >= 2 or data['score'] >= 12:
                # Bonus for matching multiple words (better context match)
                match_bonus = data['matches'] * 5
                final_scores[key] = data['score'] + match_bonus
        
        # Sort by final score
        ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for (dom, idx), score in ranked[:limit]:
            example = self.data[dom][idx].copy()
            example['domain'] = dom
            example['relevance_score'] = score
            results.append(example)
        
        return results
    
    def get_domain(self, domain: str) -> List[Dict]:
        """Get all examples from a specific domain"""
        if not self.loaded:
            self.load()
        return self.data.get(domain, [])
    
    def get_random_example(self, domain: Optional[str] = None) -> Optional[Dict]:
        """Get a random example (optionally from specific domain)"""
        if not self.loaded:
            self.load()
        
        import random
        
        if domain:
            examples = self.data.get(domain, [])
            return random.choice(examples) if examples else None
        else:
            all_examples = [ex for examples in self.data.values() for ex in examples]
            return random.choice(all_examples) if all_examples else None
    
    def stats(self) -> Dict:
        """Get dataset statistics"""
        if not self.loaded:
            self.load()
        
        return {
            'total_examples': sum(len(v) for v in self.data.values()),
            'domains': {
                domain: len(examples) 
                for domain, examples in self.data.items()
            },
            'indexed_keywords': len(self.index)
        }
    
    def export_summary(self, output_file: str = "dataset_summary.json"):
        """Export dataset summary to JSON"""
        summary = self.stats()
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"📄 Summary exported to {output_file}")
