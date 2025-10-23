"""
Context-Aware Memory Recall with Predictive Preloading
Anticipates needed memories based on conversation patterns and context
"""

from typing import Dict, List, Optional, Set
from datetime import datetime
from collections import defaultdict, deque
import re

class ConversationPatternAnalyzer:
    """Analyzes conversation patterns to predict memory needs"""
    
    def __init__(self):
        # Track conversation flow patterns
        self.topic_transitions = defaultdict(lambda: defaultdict(int))
        self.emotional_transitions = defaultdict(lambda: defaultdict(int))
        self.conversation_rhythms = {}
    
    def extract_pattern(self, dialogue: List[Dict]) -> Dict:
        """
        Extract patterns from current dialogue
        
        Args:
            dialogue: List of conversation messages
        
        Returns:
            Pattern dict with topics, emotions, rhythm
        """
        if not dialogue:
            return {}
        
        # Extract topics
        topics = []
        emotions = []
        timestamps = []
        
        for msg in dialogue[-10:]:  # Last 10 messages
            # Extract concepts/topics
            content = msg.get('content', '')
            msg_topics = self._extract_topics(content)
            topics.extend(msg_topics)
            
            # Extract emotions
            if 'emotional_context' in msg:
                dominant_emotion = max(
                    msg['emotional_context'].items(),
                    key=lambda x: x[1]
                )[0]
                emotions.append(dominant_emotion)
            
            # Track timing
            if 'timestamp' in msg:
                timestamps.append(msg['timestamp'])
        
        # Analyze topic flow
        topic_sequence = self._get_sequence(topics)
        emotion_sequence = self._get_sequence(emotions)
        
        # Calculate conversation rhythm
        rhythm = self._calculate_rhythm(timestamps)
        
        return {
            'topics': topics,
            'topic_sequence': topic_sequence,
            'emotions': emotions,
            'emotion_sequence': emotion_sequence,
            'rhythm': rhythm,
            'depth': len(dialogue),
            'current_phase': self._determine_conversation_phase(dialogue)
        }
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract key topics from text"""
        # Simple keyword extraction (could be enhanced with NLP)
        keywords = re.findall(r'\b[A-Za-z]{4,}\b', text.lower())
        
        # Filter common words
        stopwords = {'this', 'that', 'with', 'from', 'about', 'have', 'been', 'were', 'does'}
        topics = [word for word in keywords if word not in stopwords]
        
        return topics[:5]  # Top 5 keywords
    
    def _get_sequence(self, items: List) -> List:
        """Get unique sequence of items"""
        seen = set()
        sequence = []
        for item in items:
            if item and item not in seen:
                sequence.append(item)
                seen.add(item)
        return sequence
    
    def _calculate_rhythm(self, timestamps: List[str]) -> str:
        """Determine conversation rhythm (fast/medium/slow)"""
        if len(timestamps) < 2:
            return 'unknown'
        
        # Calculate average time between messages
        diffs = []
        for i in range(1, len(timestamps)):
            t1 = datetime.fromisoformat(timestamps[i-1])
            t2 = datetime.fromisoformat(timestamps[i])
            diffs.append((t2 - t1).total_seconds())
        
        avg_diff = sum(diffs) / len(diffs)
        
        if avg_diff < 30:  # < 30 seconds
            return 'fast'
        elif avg_diff < 120:  # < 2 minutes
            return 'medium'
        else:
            return 'slow'
    
    def _determine_conversation_phase(self, dialogue: List[Dict]) -> str:
        """Determine current conversation phase"""
        if len(dialogue) < 3:
            return 'opening'
        elif len(dialogue) < 10:
            return 'building'
        elif len(dialogue) < 30:
            return 'deep'
        else:
            return 'extended'

class MemoryNeedPredictor:
    """Predicts which memories will be needed next"""
    
    def __init__(self):
        self.prediction_rules = {
            'emotional_support': {
                'triggers': ['sadness', 'fear', 'anxiety', 'loneliness'],
                'needed_memories': ['positive_experiences', 'coping_strategies', 'support_moments']
            },
            'learning': {
                'triggers': ['curiosity', 'confusion', 'interest'],
                'needed_memories': ['related_topics', 'previous_explanations', 'insights']
            },
            'reflection': {
                'triggers': ['contemplation', 'wonder', 'introspection'],
                'needed_memories': ['past_reflections', 'wisdom_moments', 'growth_experiences']
            },
            'celebration': {
                'triggers': ['joy', 'excitement', 'accomplishment'],
                'needed_memories': ['achievements', 'happy_moments', 'shared_joys']
            }
        }
    
    def predict_memory_needs(self, conversation_pattern: Dict) -> Dict:
        """
        Predict which memories will likely be needed
        
        Args:
            conversation_pattern: Pattern from ConversationPatternAnalyzer
        
        Returns:
            Dict with high_probability and medium_probability memory IDs
        """
        predictions = {
            'high_probability': [],
            'medium_probability': [],
            'context': {}
        }
        
        # Analyze emotional context
        emotions = conversation_pattern.get('emotions', [])
        if emotions:
            recent_emotion = emotions[-1] if emotions else None
            
            for pattern_name, pattern_data in self.prediction_rules.items():
                if recent_emotion in pattern_data['triggers']:
                    predictions['context']['pattern'] = pattern_name
                    predictions['context']['needed_types'] = pattern_data['needed_memories']
                    break
        
        # Analyze topic continuity
        topics = conversation_pattern.get('topics', [])
        if len(topics) >= 2:
            # Predict continuation of current topic thread
            recent_topics = topics[-3:]
            predictions['context']['topic_thread'] = recent_topics
        
        # Analyze conversation phase
        phase = conversation_pattern.get('current_phase', 'opening')
        if phase == 'deep' or phase == 'extended':
            # Deep conversations likely need historical context
            predictions['context']['depth_context'] = True
        
        return predictions

class PredictiveCache:
    """Fast-access cache for preloaded memories"""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.cache = {}  # memory_id -> memory_data
        self.access_order = deque()  # LRU tracking
        self.relevance_scores = {}  # memory_id -> score
    
    def prefetch(self, memory: Dict, relevance_score: float = 1.0):
        """Preload memory into cache"""
        memory_id = memory.get('_id', '')
        if not memory_id:
            return
        
        # Add to cache
        self.cache[memory_id] = memory
        self.relevance_scores[memory_id] = relevance_score
        
        # Update LRU
        if memory_id in self.access_order:
            self.access_order.remove(memory_id)
        self.access_order.append(memory_id)
        
        # Evict if over capacity
        while len(self.cache) > self.max_size:
            # Remove least recently used, lowest relevance
            oldest_id = self.access_order.popleft()
            if oldest_id in self.cache:
                del self.cache[oldest_id]
                del self.relevance_scores[oldest_id]
    
    def get_relevant_memories(self, context: Dict, max_memories: int = 10) -> List[Dict]:
        """
        Retrieve preloaded memories relevant to context
        
        Args:
            context: Current context (topics, emotions, etc.)
            max_memories: Maximum memories to return
        
        Returns:
            List of relevant memories from cache
        """
        relevant = []
        
        context_topics = set(context.get('topics', []))
        context_emotions = set(context.get('emotions', []))
        
        for memory_id, memory in self.cache.items():
            # Calculate relevance to current context
            relevance = 0.0
            
            # Topic match
            memory_concepts = set(memory.get('concepts', []))
            topic_overlap = len(context_topics & memory_concepts)
            if topic_overlap > 0:
                relevance += topic_overlap * 0.5
            
            # Emotional match
            memory_emotions = set(memory.get('emotional_context', {}).keys())
            emotion_overlap = len(context_emotions & memory_emotions)
            if emotion_overlap > 0:
                relevance += emotion_overlap * 0.3
            
            # Pre-computed relevance score
            relevance += self.relevance_scores.get(memory_id, 0) * 0.2
            
            if relevance > 0:
                memory_copy = memory.copy()
                memory_copy['_cache_relevance'] = relevance
                relevant.append(memory_copy)
        
        # Sort by relevance
        relevant.sort(key=lambda m: m['_cache_relevance'], reverse=True)
        
        return relevant[:max_memories]
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.access_order.clear()
        self.relevance_scores.clear()

class ContextAwareRecall:
    """
    Main context-aware memory recall system
    Intelligently retrieves memories based on conversation context and predictive analysis
    """
    
    def __init__(self, memory_index=None):
        self.pattern_analyzer = ConversationPatternAnalyzer()
        self.predictor = MemoryNeedPredictor()
        self.cache = PredictiveCache(max_size=100)
        self.memory_index = memory_index
        
        print("🔮 Context-Aware Recall initialized")
    
    def recall_with_context(self, query: str, conversation_history: List[Dict], 
                           user_id: str, max_memories: int = 10) -> List[Dict]:
        """
        Recall memories with full context awareness
        
        Args:
            query: Current query
            conversation_history: Recent conversation
            user_id: User identifier
            max_memories: Maximum memories to return
        
        Returns:
            List of contextually relevant memories
        """
        # Analyze conversation pattern
        pattern = self.pattern_analyzer.extract_pattern(conversation_history)
        
        # Build context weights
        context_weights = self._calculate_context_weights(pattern, query)
        
        # Check cache first (fast path)
        cached_memories = self.cache.get_relevant_memories(
            {
                'topics': pattern.get('topics', []),
                'emotions': pattern.get('emotions', []),
                'query': query
            },
            max_memories
        )
        
        if cached_memories and len(cached_memories) >= max_memories // 2:
            # Cache hit - supplement with fresh search if needed
            memories = cached_memories
        else:
            # Cache miss - full search
            if self.memory_index:
                search_query = {
                    'user_id': user_id,
                    'concepts': pattern.get('topics', [])[:5],
                    'emotions': self._build_emotion_query(pattern),
                    'min_matches': 1
                }
                memories = self.memory_index.recall_by_multiple_dimensions(search_query)
            else:
                memories = []
        
        # Apply context weighting
        memories = self._reweight_by_context(memories, context_weights)
        
        # Filter by coherence
        memories = self._filter_by_coherence(memories, pattern)
        
        # Rank by final relevance
        memories = self._rank_by_relevance(memories, query, pattern)
        
        return memories[:max_memories]
    
    def preload_predicted_memories(self, conversation_history: List[Dict], 
                                   user_id: str, memory_pool: List[Dict]):
        """
        Preload memories that will likely be needed next
        
        Args:
            conversation_history: Recent conversation
            user_id: User identifier
            memory_pool: Available memories to preload from
        """
        # Analyze conversation
        pattern = self.pattern_analyzer.extract_pattern(conversation_history)
        
        # Predict needs
        predictions = self.predictor.predict_memory_needs(pattern)
        
        # Identify relevant memories from pool
        needed_types = predictions['context'].get('needed_types', [])
        topic_thread = predictions['context'].get('topic_thread', [])
        
        preload_candidates = []
        for memory in memory_pool:
            relevance_score = 0.0
            
            # Match needed types
            memory_type = memory.get('interaction_type', '')
            if any(needed_type in memory_type for needed_type in needed_types):
                relevance_score += 0.5
            
            # Match topic thread
            memory_concepts = set(memory.get('concepts', []))
            topic_overlap = len(set(topic_thread) & memory_concepts)
            if topic_overlap > 0:
                relevance_score += topic_overlap * 0.3
            
            if relevance_score > 0.2:  # Threshold
                preload_candidates.append((memory, relevance_score))
        
        # Preload top candidates
        preload_candidates.sort(key=lambda x: x[1], reverse=True)
        for memory, score in preload_candidates[:20]:
            self.cache.prefetch(memory, score)
    
    def _calculate_context_weights(self, pattern: Dict, query: str) -> Dict:
        """Calculate weighting based on context"""
        weights = {
            'temporal': 0.3,    # Default weights
            'emotional': 0.3,
            'conceptual': 0.3,
            'resonance': 0.1
        }
        
        # Adjust based on conversation phase
        phase = pattern.get('current_phase', 'opening')
        if phase == 'deep' or phase == 'extended':
            weights['temporal'] = 0.4  # History more important in deep convos
            weights['emotional'] = 0.4
            weights['conceptual'] = 0.15
            weights['resonance'] = 0.05
        
        # Adjust based on emotional intensity
        emotions = pattern.get('emotions', [])
        if emotions:
            weights['emotional'] = 0.5  # Boost emotional weighting
            weights['conceptual'] = 0.2
        
        return weights
    
    def _build_emotion_query(self, pattern: Dict) -> Dict:
        """Build emotion query from pattern"""
        emotions = pattern.get('emotions', [])
        if not emotions:
            return {}
        
        # Use recent emotion as query
        recent_emotion = emotions[-1] if emotions else None
        return {recent_emotion: 1.0} if recent_emotion else {}
    
    def _reweight_by_context(self, memories: List[Dict], weights: Dict) -> List[Dict]:
        """Apply context weights to memories"""
        for memory in memories:
            if '_match_count' in memory:
                # Apply weighting (simplified - full version would be more nuanced)
                memory['_context_score'] = memory['_match_count']
        
        return memories
    
    def _filter_by_coherence(self, memories: List[Dict], pattern: Dict) -> List[Dict]:
        """Filter memories by coherence with conversation"""
        # Simple coherence check - ensure memories aren't contradictory
        # Full implementation would check for logical consistency
        return memories
    
    def _rank_by_relevance(self, memories: List[Dict], query: str, pattern: Dict) -> List[Dict]:
        """Final relevance ranking"""
        memories.sort(
            key=lambda m: m.get('_context_score', m.get('_match_count', 0)),
            reverse=True
        )
        return memories
