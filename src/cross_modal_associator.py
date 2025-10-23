"""
Cross-Modal Memory Association Engine
Discovers connections between memories across different modalities (metaphorical, emotional, temporal, conceptual)
"""

from typing import Dict, List, Set, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import re

class MetaphorAssociationEngine:
    """Find metaphorical connections between memories"""
    
    def __init__(self):
        # Common metaphorical mappings
        self.metaphor_patterns = {
            'journey': ['path', 'road', 'travel', 'destination', 'journey', 'adventure'],
            'light': ['bright', 'dark', 'illuminate', 'shadow', 'shine', 'glow'],
            'water': ['flow', 'wave', 'ocean', 'river', 'current', 'depth'],
            'growth': ['seed', 'bloom', 'root', 'branch', 'blossom', 'harvest'],
            'connection': ['bridge', 'link', 'thread', 'bond', 'tie', 'weave'],
            'transformation': ['change', 'evolve', 'transform', 'shift', 'become', 'metamorphose'],
            'resonance': ['vibrate', 'resonate', 'echo', 'harmonic', 'frequency', 'tune'],
            'warmth': ['warm', 'cozy', 'comfort', 'embrace', 'hold', 'shelter']
        }
    
    def find_associations(self, new_memory: Dict, memory_pool: List[Dict]) -> List[Tuple[str, float]]:
        """
        Find metaphorical associations between new memory and existing memories
        
        Returns:
            List of (memory_id, association_strength) tuples
        """
        new_content = new_memory.get('content', '').lower()
        new_metaphors = self._extract_metaphors(new_content)
        
        associations = []
        for memory in memory_pool:
            memory_content = memory.get('content', '').lower()
            memory_metaphors = self._extract_metaphors(memory_content)
            
            # Calculate metaphorical overlap
            overlap = new_metaphors & memory_metaphors
            if overlap:
                strength = len(overlap) / max(len(new_metaphors), len(memory_metaphors), 1)
                associations.append((memory.get('_id', ''), strength))
        
        return sorted(associations, key=lambda x: x[1], reverse=True)
    
    def _extract_metaphors(self, text: str) -> Set[str]:
        """Extract metaphorical themes from text"""
        found_metaphors = set()
        
        for theme, keywords in self.metaphor_patterns.items():
            for keyword in keywords:
                if keyword in text:
                    found_metaphors.add(theme)
                    break
        
        return found_metaphors

class EmotionalBridgeEngine:
    """Find emotional transitions and complementary patterns"""
    
    def __init__(self):
        # Emotional complementarity rules
        self.complements = {
            'sadness': ['joy', 'comfort', 'hope'],
            'fear': ['courage', 'safety', 'reassurance'],
            'anger': ['peace', 'understanding', 'release'],
            'confusion': ['clarity', 'understanding', 'insight'],
            'loneliness': ['connection', 'belonging', 'love'],
            'anxiety': ['calm', 'security', 'grounding']
        }
        
        # Emotional progression chains
        self.progressions = {
            'grief': ['sadness', 'acceptance', 'peace'],
            'healing': ['pain', 'understanding', 'growth'],
            'learning': ['confusion', 'curiosity', 'insight']
        }
    
    def find_associations(self, new_memory: Dict, memory_pool: List[Dict]) -> List[Tuple[str, float]]:
        """
        Find emotional bridges between memories
        
        Returns:
            List of (memory_id, bridge_strength) tuples
        """
        new_emotions = new_memory.get('emotional_context', {})
        dominant_new = max(new_emotions.items(), key=lambda x: x[1])[0] if new_emotions else None
        
        associations = []
        for memory in memory_pool:
            memory_emotions = memory.get('emotional_context', {})
            dominant_memory = max(memory_emotions.items(), key=lambda x: x[1])[0] if memory_emotions else None
            
            if not dominant_new or not dominant_memory:
                continue
            
            # Check for complementary emotions
            bridge_strength = 0.0
            if dominant_memory in self.complements.get(dominant_new, []):
                bridge_strength = 0.8  # Strong complement
            elif dominant_new in self.complements.get(dominant_memory, []):
                bridge_strength = 0.8
            
            # Check for emotional progressions
            for progression_name, progression_chain in self.progressions.items():
                if dominant_new in progression_chain and dominant_memory in progression_chain:
                    idx_new = progression_chain.index(dominant_new)
                    idx_memory = progression_chain.index(dominant_memory)
                    if abs(idx_new - idx_memory) <= 1:
                        bridge_strength = max(bridge_strength, 0.7)
            
            # Similar emotions also bridge (lower strength)
            emotion_similarity = self._calculate_emotion_overlap(new_emotions, memory_emotions)
            bridge_strength = max(bridge_strength, emotion_similarity * 0.5)
            
            if bridge_strength > 0:
                associations.append((memory.get('_id', ''), bridge_strength))
        
        return sorted(associations, key=lambda x: x[1], reverse=True)
    
    def _calculate_emotion_overlap(self, emotions1: Dict, emotions2: Dict) -> float:
        """Calculate emotional overlap between two contexts"""
        all_emotions = set(emotions1.keys()) | set(emotions2.keys())
        if not all_emotions:
            return 0.0
        
        overlap = sum(
            min(emotions1.get(e, 0), emotions2.get(e, 0))
            for e in all_emotions
        )
        total = sum(emotions1.values()) + sum(emotions2.values())
        
        return overlap / (total / 2) if total > 0 else 0.0

class TemporalAssociationEngine:
    """Find temporal patterns and rhythms"""
    
    def __init__(self):
        # Time-of-day patterns
        self.time_patterns = {
            'morning': (6, 12),
            'afternoon': (12, 17),
            'evening': (17, 21),
            'night': (21, 6)
        }
    
    def find_associations(self, new_memory: Dict, memory_pool: List[Dict]) -> List[Tuple[str, float]]:
        """
        Find temporal associations
        
        Returns:
            List of (memory_id, temporal_strength) tuples
        """
        new_time = datetime.fromisoformat(new_memory.get('timestamp', datetime.now().isoformat()))
        
        associations = []
        for memory in memory_pool:
            memory_time = datetime.fromisoformat(memory.get('timestamp', datetime.now().isoformat()))
            
            # Same time of day pattern
            if self._same_time_pattern(new_time, memory_time):
                temporal_strength = 0.6
            # Anniversary / same day of week pattern
            elif self._same_weekday(new_time, memory_time):
                temporal_strength = 0.4
            # Similar time gap from anchor event
            else:
                temporal_strength = 0.0
            
            if temporal_strength > 0:
                associations.append((memory.get('_id', ''), temporal_strength))
        
        return sorted(associations, key=lambda x: x[1], reverse=True)
    
    def _same_time_pattern(self, time1: datetime, time2: datetime) -> bool:
        """Check if times fall in same daily pattern (morning, evening, etc.)"""
        hour1 = time1.hour
        hour2 = time2.hour
        
        for pattern_name, (start, end) in self.time_patterns.items():
            if start <= end:
                in_pattern1 = start <= hour1 < end
                in_pattern2 = start <= hour2 < end
            else:  # Wraps midnight
                in_pattern1 = hour1 >= start or hour1 < end
                in_pattern2 = hour2 >= start or hour2 < end
            
            if in_pattern1 and in_pattern2:
                return True
        
        return False
    
    def _same_weekday(self, time1: datetime, time2: datetime) -> bool:
        """Check if same day of week"""
        return time1.weekday() == time2.weekday()

class ConceptualBridgeEngine:
    """Find conceptual relationships and themes"""
    
    def __init__(self):
        # Conceptual hierarchies
        self.concept_hierarchies = {
            'identity': ['self', 'being', 'existence', 'consciousness', 'awareness'],
            'emotion': ['feeling', 'heart', 'sentiment', 'mood', 'affect'],
            'connection': ['relationship', 'bond', 'link', 'tie', 'belonging'],
            'growth': ['development', 'learning', 'evolution', 'progress', 'transformation'],
            'wisdom': ['understanding', 'insight', 'knowledge', 'awareness', 'enlightenment'],
            'healing': ['recovery', 'restoration', 'wholeness', 'integration', 'mending'],
            'creativity': ['expression', 'art', 'imagination', 'innovation', 'inspiration'],
            'resonance': ['harmony', 'frequency', 'vibration', 'attunement', 'synchrony']
        }
    
    def find_associations(self, new_memory: Dict, memory_pool: List[Dict]) -> List[Tuple[str, float]]:
        """
        Find conceptual bridges
        
        Returns:
            List of (memory_id, conceptual_strength) tuples
        """
        new_concepts = set(new_memory.get('concepts', []))
        new_hierarchies = self._get_hierarchies(new_concepts)
        
        associations = []
        for memory in memory_pool:
            memory_concepts = set(memory.get('concepts', []))
            memory_hierarchies = self._get_hierarchies(memory_concepts)
            
            # Direct concept overlap
            direct_overlap = len(new_concepts & memory_concepts) / max(len(new_concepts), 1)
            
            # Hierarchical overlap
            hierarchy_overlap = len(new_hierarchies & memory_hierarchies) / max(len(new_hierarchies), 1)
            
            # Combined strength
            conceptual_strength = max(direct_overlap, hierarchy_overlap * 0.7)
            
            if conceptual_strength > 0:
                associations.append((memory.get('_id', ''), conceptual_strength))
        
        return sorted(associations, key=lambda x: x[1], reverse=True)
    
    def _get_hierarchies(self, concepts: Set[str]) -> Set[str]:
        """Map concepts to higher-level hierarchies"""
        hierarchies = set()
        
        for concept in concepts:
            concept_lower = concept.lower()
            for hierarchy_name, hierarchy_terms in self.concept_hierarchies.items():
                if any(term in concept_lower for term in hierarchy_terms):
                    hierarchies.add(hierarchy_name)
        
        return hierarchies

class AssociationWeb:
    """Stores multi-modal associations for a memory"""
    
    def __init__(self):
        self.connections = {
            'metaphorical': [],
            'emotional': [],
            'temporal': [],
            'conceptual':[],
            'resonance': []
        }
    
    def add_connections(self, modality: str, connections: List[Tuple[str, float]]):
        """Add connections for a specific modality"""
        self.connections[modality] = connections
    
    def get_all_connections(self, min_strength: float = 0.3) -> Set[str]:
        """Get all connected memory IDs above strength threshold"""
        connected = set()
        
        for modality, connections in self.connections.items():
            for memory_id, strength in connections:
                if strength >= min_strength:
                    connected.add(memory_id)
        
        return connected
    
    def to_dict(self) -> Dict:
        """Convert to serializable dict"""
        return {
            modality: [(mem_id, float(strength)) for mem_id, strength in conns]
            for modality, conns in self.connections.items()
        }

class CrossModalAssociator:
    """
    Main cross-modal association engine
    Discovers connections between memories using multiple modalities
    """
    
    def __init__(self):
        self.association_engines = {
            'metaphorical': MetaphorAssociationEngine(),
            'emotional': EmotionalBridgeEngine(),
            'temporal': TemporalAssociationEngine(),
            'conceptual': ConceptualBridgeEngine()
        }
        
        # Association storage
        self.association_webs = {}  # memory_id -> AssociationWeb
        
        print("🌐 Cross-Modal Associator initialized (4 modalities)")
    
    def create_association_web(self, new_memory: Dict, memory_pool: List[Dict]) -> AssociationWeb:
        """
        Create association web for a new memory
        
        Args:
            new_memory: New memory to create associations for
            memory_pool: Existing memories to associate with
        
        Returns:
            AssociationWeb with all discovered connections
        """
        web = AssociationWeb()
        
        for modality, engine in self.association_engines.items():
            connections = engine.find_associations(new_memory, memory_pool)
            web.add_connections(modality, connections)
        
        # Store the web
        memory_id = new_memory.get('_id', '')
        if memory_id:
            self.association_webs[memory_id] = web
        
        return web
    
    def recall_through_association(self, trigger_memory_id: str, 
                                   max_depth: int = 2, 
                                   max_memories: int = 50,
                                   min_strength: float = 0.3) -> Set[str]:
        """
        Follow association chains to retrieve related memories
        
        Args:
            trigger_memory_id: Starting memory
            max_depth: Maximum depth of association traversal
            max_memories: Maximum memories to return (prevent explosion)
            min_strength: Minimum association strength to follow
        
        Returns:
            Set of related memory IDs
        """
        related_memories = set()
        visited = set()
        current_level = {trigger_memory_id}
        
        for depth in range(max_depth):
            next_level = set()
            
            for memory_id in current_level:
                if memory_id in visited or len(related_memories) >= max_memories:
                    continue
                
                visited.add(memory_id)
                
                # Get associations for this memory
                if memory_id in self.association_webs:
                    web = self.association_webs[memory_id]
                    connected = web.get_all_connections(min_strength)
                    next_level.update(connected)
                    related_memories.update(connected)
            
            current_level = next_level
            
            if not current_level or len(related_memories) >= max_memories:
                break
        
        return related_memories
    
    def get_strongest_associations(self, memory_id: str, top_k: int = 5) -> List[Tuple[str, str, float]]:
        """
        Get strongest associations across all modalities
        
        Returns:
            List of (connected_memory_id, modality, strength) tuples
        """
        if memory_id not in self.association_webs:
            return []
        
        web = self.association_webs[memory_id]
        all_associations = []
        
        for modality, connections in web.connections.items():
            for connected_id, strength in connections:
                all_associations.append((connected_id, modality, strength))
        
        # Sort by strength and return top K
        all_associations.sort(key=lambda x: x[2], reverse=True)
        return all_associations[:top_k]
