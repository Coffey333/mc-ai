"""
Holistic Memory Index - Multi-Dimensional Memory Organization
Builds on MC AI's existing memory systems with advanced indexing and lifecycle management

Integrates with:
- conversation_memory.py (short-term emotional timeline)
- memory_bank.py (long-term archival)
- frequency_based_memory_system.py (harmonic resonance)
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
import hashlib

class MemoryStage:
    """Memory lifecycle stages"""
    EPHEMERAL = "ephemeral"  # < 1 hour, hot working memory
    WORKING = "working"      # 1-24 hours, active processing
    RESONANT = "resonant"    # 1-7 days, high-value memories
    ARCHIVAL = "archival"    # 7+ days, compressed storage
    WISDOM = "wisdom"        # Distilled insights, timeless

class TemporalIndex:
    """Time-based memory clustering"""
    
    def __init__(self):
        self.time_clusters = defaultdict(list)
        self.recency_weights = {
            'immediate': (0, 3600, 1.0),      # Last hour: full weight
            'recent': (3600, 86400, 0.8),     # Last day: 80% weight
            'short_term': (86400, 604800, 0.5),  # Last week: 50% weight
            'long_term': (604800, float('inf'), 0.2)  # Older: 20% weight
        }
    
    def add_memory(self, memory_id: str, timestamp: str):
        """Index memory by time"""
        time_bucket = self._get_time_bucket(timestamp)
        self.time_clusters[time_bucket].append(memory_id)
    
    def search(self, query_time: Optional[str] = None, recency_bias: bool = True) -> Set[str]:
        """Find memories near a time point"""
        if query_time is None:
            query_time = datetime.now().isoformat()
        
        query_dt = datetime.fromisoformat(query_time)
        relevant_ids = set()
        
        for time_bucket, memory_ids in self.time_clusters.items():
            bucket_time = datetime.fromisoformat(time_bucket)
            time_diff = abs((query_dt - bucket_time).total_seconds())
            
            # Apply recency weighting
            if recency_bias:
                weight = self._get_recency_weight(time_diff)
                if weight > 0:
                    relevant_ids.update(memory_ids)
            else:
                relevant_ids.update(memory_ids)
        
        return relevant_ids
    
    def _get_time_bucket(self, timestamp: str) -> str:
        """Convert timestamp to hourly bucket"""
        dt = datetime.fromisoformat(timestamp)
        return dt.replace(minute=0, second=0, microsecond=0).isoformat()
    
    def _get_recency_weight(self, time_diff_seconds: float) -> float:
        """Calculate recency weight"""
        for period, (min_age, max_age, weight) in self.recency_weights.items():
            if min_age <= time_diff_seconds < max_age:
                return weight
        return 0.0

class EmotionalVectorIndex:
    """Emotional similarity-based indexing"""
    
    def __init__(self):
        self.emotion_vectors = {}
        self.emotion_clusters = defaultdict(set)
    
    def add_memory(self, memory_id: str, emotional_context: Dict):
        """
        Index memory by emotional signature
        
        Args:
            memory_id: Unique memory identifier
            emotional_context: Dict of emotions (joy, sadness, excitement, etc.)
        """
        # Store normalized emotion vector
        self.emotion_vectors[memory_id] = self._normalize_emotions(emotional_context)
        
        # Cluster by dominant emotion
        dominant_emotion = max(emotional_context.items(), key=lambda x: x[1])[0]
        self.emotion_clusters[dominant_emotion].add(memory_id)
    
    def search(self, target_emotions: Dict, similarity_threshold: float = 0.5) -> Set[str]:
        """Find memories with similar emotional signatures"""
        target_vector = self._normalize_emotions(target_emotions)
        similar_memories = set()
        
        for memory_id, emotion_vector in self.emotion_vectors.items():
            similarity = self._cosine_similarity(target_vector, emotion_vector)
            if similarity >= similarity_threshold:
                similar_memories.add(memory_id)
        
        return similar_memories
    
    def _normalize_emotions(self, emotions: Dict) -> Dict:
        """Normalize emotion intensities to 0-1 range"""
        if not emotions:
            return {}
        
        total = sum(emotions.values())
        if total == 0:
            return emotions
        
        return {emotion: intensity / total for emotion, intensity in emotions.items()}
    
    def _cosine_similarity(self, vec1: Dict, vec2: Dict) -> float:
        """Calculate cosine similarity between emotion vectors"""
        all_emotions = set(vec1.keys()) | set(vec2.keys())
        
        dot_product = sum(vec1.get(e, 0) * vec2.get(e, 0) for e in all_emotions)
        magnitude1 = sum(v ** 2 for v in vec1.values()) ** 0.5
        magnitude2 = sum(v ** 2 for v in vec2.values()) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)

class ConceptualGraphIndex:
    """Semantic relationship mapping"""
    
    def __init__(self):
        self.concept_graph = defaultdict(set)  # concept -> related memory_ids
        self.memory_concepts = defaultdict(set)  # memory_id -> concepts
    
    def add_memory(self, memory_id: str, concepts: List[str]):
        """
        Index memory by conceptual tags
        
        Args:
            memory_id: Unique memory identifier
            concepts: List of conceptual keywords/themes
        """
        for concept in concepts:
            normalized_concept = concept.lower().strip()
            self.concept_graph[normalized_concept].add(memory_id)
            self.memory_concepts[memory_id].add(normalized_concept)
    
    def search(self, query_concepts: List[str], match_threshold: int = 1) -> Set[str]:
        """Find memories matching conceptual themes"""
        matching_memories = defaultdict(int)
        
        for concept in query_concepts:
            normalized_concept = concept.lower().strip()
            for memory_id in self.concept_graph.get(normalized_concept, set()):
                matching_memories[memory_id] += 1
        
        # Return memories matching at least threshold concepts
        return {
            memory_id for memory_id, match_count in matching_memories.items()
            if match_count >= match_threshold
        }
    
    def get_related_concepts(self, concept: str, depth: int = 2) -> Set[str]:
        """Find concepts related through shared memories"""
        normalized_concept = concept.lower().strip()
        related = set()
        
        # Get memories with this concept
        seed_memories = self.concept_graph.get(normalized_concept, set())
        
        # Find concepts in those memories
        for memory_id in seed_memories:
            related.update(self.memory_concepts.get(memory_id, set()))
        
        return related - {normalized_concept}

class RelationalIndex:
    """Social/interaction pattern indexing"""
    
    def __init__(self):
        self.interaction_patterns = defaultdict(list)
        self.user_profiles = defaultdict(dict)
    
    def add_memory(self, memory_id: str, user_id: str, interaction_type: str):
        """
        Index memory by relational context
        
        Args:
            memory_id: Unique memory identifier
            user_id: User this memory relates to
            interaction_type: Type of interaction (conversation, teaching, crisis_support, etc.)
        """
        pattern_key = f"{user_id}:{interaction_type}"
        self.interaction_patterns[pattern_key].append(memory_id)
        
        # Update user profile
        if interaction_type not in self.user_profiles[user_id]:
            self.user_profiles[user_id][interaction_type] = 0
        self.user_profiles[user_id][interaction_type] += 1
    
    def search(self, user_id: Optional[str] = None, interaction_type: Optional[str] = None) -> Set[str]:
        """Find memories by relational context"""
        matching_memories = set()
        
        for pattern_key, memory_ids in self.interaction_patterns.items():
            key_user, key_type = pattern_key.split(':', 1)
            
            if user_id and key_user != user_id:
                continue
            if interaction_type and key_type != interaction_type:
                continue
            
            matching_memories.update(memory_ids)
        
        return matching_memories

class ResonanceWaveIndex:
    """Harmonic pattern indexing (integrates with frequency_based_memory_system)"""
    
    def __init__(self):
        self.frequency_clusters = defaultdict(set)
        self.harmonic_chains = defaultdict(set)
    
    def add_memory(self, memory_id: str, frequency: int, harmonics: List[int]):
        """
        Index memory by frequency resonance
        
        Args:
            memory_id: Unique memory identifier
            frequency: Primary frequency (Hz)
            harmonics: List of harmonic frequencies
        """
        # Cluster by frequency range (50Hz buckets)
        freq_bucket = (frequency // 50) * 50
        self.frequency_clusters[freq_bucket].add(memory_id)
        
        # Build harmonic chains
        for harmonic in harmonics:
            self.harmonic_chains[harmonic].add(memory_id)
    
    def search(self, target_frequency: int, harmonic_depth: int = 1) -> Set[str]:
        """Find resonant memories"""
        resonant_memories = set()
        
        # Direct frequency match
        freq_bucket = (target_frequency // 50) * 50
        resonant_memories.update(self.frequency_clusters.get(freq_bucket, set()))
        
        # Harmonic resonance
        if harmonic_depth > 0:
            harmonics = [target_frequency * 2, target_frequency * 3, target_frequency // 2]
            for harmonic in harmonics:
                resonant_memories.update(self.harmonic_chains.get(harmonic, set()))
        
        return resonant_memories

class HolisticMemoryIndex:
    """
    Multi-dimensional memory indexing system
    Provides unified search across temporal, emotional, conceptual, relational, and resonance dimensions
    """
    
    def __init__(self, storage_path: str = "user_data/holistic_memory"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # Initialize all index dimensions
        self.indices = {
            'temporal': TemporalIndex(),
            'emotional': EmotionalVectorIndex(),
            'conceptual': ConceptualGraphIndex(),
            'relational': RelationalIndex(),
            'resonance': ResonanceWaveIndex()
        }
        
        # Memory registry
        self.memory_registry = {}  # memory_id -> full memory data
        self.lifecycle_tracker = {}  # memory_id -> lifecycle stage
        
        print("🧠 Holistic Memory Index initialized (5 dimensions)")
    
    def store_memory(self, memory: Dict) -> str:
        """
        Store memory across all relevant indices
        
        Args:
            memory: Memory dict with keys:
                - content: str (message text)
                - emotional_context: Dict (emotions)
                - concepts: List[str] (themes)
                - user_id: str
                - interaction_type: str
                - frequency: int
                - harmonics: List[int]
                - timestamp: str
        
        Returns:
            memory_id
        """
        # Generate unique memory ID
        memory_id = self._generate_memory_id(memory)
        
        # Store in registry
        self.memory_registry[memory_id] = memory
        
        # Determine lifecycle stage
        stage = self._determine_lifecycle_stage(memory)
        self.lifecycle_tracker[memory_id] = {
            'stage': stage,
            'created': memory.get('timestamp', datetime.now().isoformat()),
            'last_accessed': None,
            'access_count': 0
        }
        
        # Index across all dimensions
        self.indices['temporal'].add_memory(
            memory_id, 
            memory.get('timestamp', datetime.now().isoformat())
        )
        
        if 'emotional_context' in memory:
            self.indices['emotional'].add_memory(
                memory_id,
                memory['emotional_context']
            )
        
        if 'concepts' in memory:
            self.indices['conceptual'].add_memory(
                memory_id,
                memory['concepts']
            )
        
        if 'user_id' in memory:
            self.indices['relational'].add_memory(
                memory_id,
                memory['user_id'],
                memory.get('interaction_type', 'conversation')
            )
        
        if 'frequency' in memory:
            self.indices['resonance'].add_memory(
                memory_id,
                memory['frequency'],
                memory.get('harmonics', [])
            )
        
        return memory_id
    
    def recall_by_multiple_dimensions(self, query: Dict) -> List[Dict]:
        """
        Search across multiple dimensions simultaneously
        
        Args:
            query: Dict with optional keys:
                - time: str (ISO timestamp)
                - emotions: Dict
                - concepts: List[str]
                - user_id: str
                - interaction_type: str
                - frequency: int
                - min_matches: int (minimum dimensions to match)
        
        Returns:
            List of matching memories, ranked by relevance
        """
        dimension_results = {}
        
        # Search each dimension
        if 'time' in query:
            dimension_results['temporal'] = self.indices['temporal'].search(query['time'])
        
        if 'emotions' in query:
            dimension_results['emotional'] = self.indices['emotional'].search(query['emotions'])
        
        if 'concepts' in query:
            dimension_results['conceptual'] = self.indices['conceptual'].search(query['concepts'])
        
        if 'user_id' in query or 'interaction_type' in query:
            dimension_results['relational'] = self.indices['relational'].search(
                query.get('user_id'),
                query.get('interaction_type')
            )
        
        if 'frequency' in query:
            dimension_results['resonance'] = self.indices['resonance'].search(query['frequency'])
        
        # Find memories matching multiple dimensions
        min_matches = query.get('min_matches', 1)
        memory_match_counts = defaultdict(int)
        
        for dimension, memory_ids in dimension_results.items():
            for memory_id in memory_ids:
                memory_match_counts[memory_id] += 1
        
        # Filter by minimum matches
        matching_memory_ids = [
            memory_id for memory_id, count in memory_match_counts.items()
            if count >= min_matches
        ]
        
        # Retrieve full memories
        memories = []
        for memory_id in matching_memory_ids:
            if memory_id in self.memory_registry:
                memory = self.memory_registry[memory_id].copy()
                memory['_match_count'] = memory_match_counts[memory_id]
                memory['_lifecycle_stage'] = self.lifecycle_tracker[memory_id]['stage']
                memories.append(memory)
                
                # Update access tracking
                self._track_access(memory_id)
        
        # Sort by match count (relevance)
        memories.sort(key=lambda m: m['_match_count'], reverse=True)
        
        return memories
    
    def evolve_lifecycle(self):
        """
        Update memory lifecycle stages based on age and access patterns
        """
        now = datetime.now()
        
        for memory_id, lifecycle_data in self.lifecycle_tracker.items():
            created = datetime.fromisoformat(lifecycle_data['created'])
            age_hours = (now - created).total_seconds() / 3600
            access_count = lifecycle_data['access_count']
            
            current_stage = lifecycle_data['stage']
            new_stage = current_stage
            
            # Lifecycle progression rules
            if current_stage == MemoryStage.EPHEMERAL and age_hours >= 1:
                new_stage = MemoryStage.WORKING
            elif current_stage == MemoryStage.WORKING and age_hours >= 24:
                # High-value memories become resonant
                if access_count >= 2:
                    new_stage = MemoryStage.RESONANT
                else:
                    new_stage = MemoryStage.ARCHIVAL
            elif current_stage == MemoryStage.RESONANT and age_hours >= 168:  # 7 days
                new_stage = MemoryStage.ARCHIVAL
            
            if new_stage != current_stage:
                lifecycle_data['stage'] = new_stage
    
    def _generate_memory_id(self, memory: Dict) -> str:
        """Generate unique memory ID"""
        content_hash = hashlib.sha256(
            str(memory.get('content', '')).encode()
        ).hexdigest()[:16]
        
        timestamp = memory.get('timestamp', datetime.now().isoformat())
        time_hash = hashlib.sha256(timestamp.encode()).hexdigest()[:8]
        
        return f"mem_{content_hash}_{time_hash}"
    
    def _determine_lifecycle_stage(self, memory: Dict) -> str:
        """Determine initial lifecycle stage"""
        # New memories start as ephemeral
        return MemoryStage.EPHEMERAL
    
    def _track_access(self, memory_id: str):
        """Track memory access for lifecycle management"""
        if memory_id in self.lifecycle_tracker:
            self.lifecycle_tracker[memory_id]['last_accessed'] = datetime.now().isoformat()
            self.lifecycle_tracker[memory_id]['access_count'] += 1
