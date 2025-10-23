"""
Enhanced Memory Manager - Unified Interface
Integrates all memory systems (existing + new) with backward compatibility

Coordinates:
- conversation_memory.py (existing short-term)
- memory_bank.py (existing long-term archive)
- frequency_based_memory_system.py (existing frequency recall)
- holistic_memory_index.py (NEW multi-dimensional)
- cross_modal_associator.py (NEW associations)
- context_aware_recall.py (NEW predictive)
"""

import json
from typing import Dict, List, Optional
from datetime import datetime

# Existing systems
from src.conversation_memory import ConversationMemory
from src.memory_bank import MemoryBank
from src.frameworks.frequency_based_memory_system import FrequencyBasedMemorySystem

# New systems
from src.holistic_memory_index import HolisticMemoryIndex
from src.cross_modal_associator import CrossModalAssociator
from src.context_aware_recall import ContextAwareRecall

class EnhancedMemoryManager:
    """
    Unified memory management system
    Seamlessly integrates existing and new memory capabilities
    """
    
    def __init__(self):
        # Initialize existing systems (backward compatible)
        self.conversation_memory = ConversationMemory()
        self.memory_bank = MemoryBank()
        self.frequency_memory = FrequencyBasedMemorySystem()
        
        # Initialize new systems (enhanced capabilities)
        self.holistic_index = HolisticMemoryIndex()
        self.associator = CrossModalAssociator()
        self.context_recall = ContextAwareRecall(memory_index=self.holistic_index)
        
        print("✨ Enhanced Memory Manager initialized (6 systems integrated)")
    
    def add_message(self, user_id: str, message: str, response: str, metadata: Dict):
        """
        Add message to ALL memory systems
        
        This is the main entry point - it coordinates storage across all systems
        
        Args:
            user_id: User identifier
            message: User's message
            response: MC AI's response
            metadata: Response metadata (emotion, frequency, etc.)
        """
        # 1. Store in existing conversation memory (backward compatible)
        self.conversation_memory.add_message(user_id, message, response, metadata)
        
        # 2. Store in frequency-based memory (existing)
        frequency = metadata.get('frequency', 240)
        timestamp = datetime.now().isoformat()
        memory_id = f"{user_id}_{timestamp}"
        self.frequency_memory.store_memory(
            memory_id,
            f"User: {message}\nMC AI: {response[:200]}",
            frequency,
            timestamp
        )
        
        # 3. Extract concepts for new systems
        concepts = self._extract_concepts(message, response)
        
        # 4. Build enhanced memory object for new systems
        enhanced_memory = {
            'content': f"User: {message}\nMC AI: {response}",
            'user_message': message,
            'ai_response': response,
            'emotional_context': self._extract_emotions(metadata),
            'concepts': concepts,
            'user_id': user_id,
            'interaction_type': metadata.get('type', 'conversation'),
            'frequency': frequency,
            'harmonics': self._calculate_harmonics(frequency),
            'timestamp': timestamp,
            '_id': memory_id
        }
        
        # 5. Store in holistic index (NEW)
        self.holistic_index.store_memory(enhanced_memory)
        
        # 6. Create association web (NEW)
        # Get recent memories for association
        recent_memories = self.get_recent_memories_for_association(user_id, limit=50)
        if recent_memories:
            enhanced_memory['_id'] = memory_id
            self.associator.create_association_web(enhanced_memory, recent_memories)
        
        # 7. Trigger predictive preloading (NEW)
        conversation_history = self.get_conversation_history(user_id, limit=10)
        if conversation_history:
            formatted_history = self._format_history_for_prediction(conversation_history)
            self.context_recall.preload_predicted_memories(
                formatted_history,
                user_id,
                recent_memories
            )
    
    def get_conversation_history(self, user_id: str, limit: Optional[int] = 10) -> List[Dict]:
        """
        Get conversation history (uses existing system)
        
        Args:
            user_id: User identifier
            limit: Number of recent messages
        
        Returns:
            List of conversation entries
        """
        return self.conversation_memory.get_conversation_history(user_id, limit)
    
    def recall_relevant_memories(self, user_id: str, query: str, 
                                conversation_history: List[Dict],
                                max_memories: int = 10,
                                use_enhanced: bool = True) -> List[Dict]:
        """
        Intelligent memory recall with context awareness
        
        Args:
            user_id: User identifier
            query: Current query
            conversation_history: Recent conversation
            max_memories: Maximum memories to return
            use_enhanced: Use enhanced context-aware recall (True) or basic (False)
        
        Returns:
            List of relevant memories
        """
        if use_enhanced:
            # NEW: Context-aware recall with predictive preloading
            formatted_history = self._format_history_for_prediction(conversation_history)
            return self.context_recall.recall_with_context(
                query,
                formatted_history,
                user_id,
                max_memories
            )
        else:
            # FALLBACK: Use existing memory bank (backward compatible)
            return self.memory_bank.retrieve_relevant_memories(user_id, query, max_memories)
    
    def recall_by_frequency(self, target_frequency: int, tolerance: int = 50) -> List[Dict]:
        """
        Recall memories by frequency resonance (existing system)
        
        Args:
            target_frequency: Target frequency in Hz
            tolerance: Frequency tolerance
        
        Returns:
            List of resonant memories
        """
        return self.frequency_memory.recall_by_frequency(target_frequency, tolerance)
    
    def find_associated_memories(self, memory_id: str, max_depth: int = 2, 
                                max_memories: int = 20) -> List[str]:
        """
        Follow association chains to find related memories (NEW)
        
        Args:
            memory_id: Starting memory
            max_depth: Maximum association depth
            max_memories: Maximum memories to return
        
        Returns:
            List of related memory IDs
        """
        related_ids = self.associator.recall_through_association(
            memory_id,
            max_depth,
            max_memories
        )
        return list(related_ids)
    
    def get_strongest_associations(self, memory_id: str, top_k: int = 5) -> List[tuple]:
        """
        Get strongest cross-modal associations (NEW)
        
        Args:
            memory_id: Memory to get associations for
            top_k: Number of top associations to return
        
        Returns:
            List of (connected_memory_id, modality, strength) tuples
        """
        return self.associator.get_strongest_associations(memory_id, top_k)
    
    def evolve_memory_lifecycle(self):
        """
        Update memory lifecycle stages (NEW)
        
        Should be called periodically (e.g., hourly) to evolve memory stages
        """
        self.holistic_index.evolve_lifecycle()
    
    def archive_old_messages(self, user_id: str, conversation_history: List[Dict]):
        """
        Archive old messages to long-term storage (existing system)
        
        Args:
            user_id: User identifier
            conversation_history: Full conversation history
        """
        # Determine which messages to archive (keep recent 30, archive older)
        if len(conversation_history) > 30:
            to_archive = conversation_history[:-30]
            
            # Extract frequency tags for cross-thread recall
            frequency_tags = []
            for msg in to_archive:
                if 'metadata' in msg and 'frequency' in msg['metadata']:
                    frequency_tags.append(msg['metadata']['frequency'])
            
            # Archive using existing memory bank
            self.memory_bank.archive_old_messages(user_id, to_archive, frequency_tags)
            
            print(f"📚 Archived {len(to_archive)} messages to long-term memory")
            return len(to_archive)
        
        return 0
    
    def get_memory_stats(self, user_id: str) -> Dict:
        """
        Get comprehensive memory statistics
        
        Args:
            user_id: User identifier
        
        Returns:
            Dict with memory statistics across all systems
        """
        conversation = self.conversation_memory._load_conversation(user_id)
        
        stats = {
            'total_messages': conversation.get('message_count', 0),
            'conversation_started': conversation.get('created', None),
            'last_updated': conversation.get('last_updated', None),
            'archived_count': 0,
            'frequency_clusters': len(self.frequency_memory.frequency_memory),
            'holistic_memories': len(self.holistic_index.memory_registry),
            'association_webs': len(self.associator.association_webs)
        }
        
        # Get archive stats
        archive_index = self.memory_bank.archive_index
        if user_id in archive_index:
            stats['archived_count'] = archive_index[user_id].get('archived_count', 0)
        
        return stats
    
    def get_recent_memories_for_association(self, user_id: str, limit: int = 50) -> List[Dict]:
        """
        Get recent memories formatted for association building
        
        Args:
            user_id: User identifier
            limit: Number of recent memories
        
        Returns:
            List of memory dicts
        """
        # Get from holistic index
        memories = []
        for memory_id, memory in self.holistic_index.memory_registry.items():
            if memory.get('user_id') == user_id:
                memories.append(memory)
        
        # Sort by timestamp (most recent first)
        memories.sort(
            key=lambda m: m.get('timestamp', ''),
            reverse=True
        )
        
        return memories[:limit]
    
    def _extract_concepts(self, message: str, response: str) -> List[str]:
        """Extract key concepts from message and response"""
        import re
        
        combined_text = f"{message} {response}".lower()
        
        # Extract keywords (4+ letter words, excluding common words)
        keywords = re.findall(r'\b[a-z]{4,}\b', combined_text)
        
        # Filter stopwords
        stopwords = {
            'this', 'that', 'with', 'from', 'about', 'have', 'been', 
            'were', 'does', 'your', 'what', 'when', 'where', 'which',
            'there', 'their', 'would', 'could', 'should'
        }
        
        concepts = [word for word in keywords if word not in stopwords]
        
        # Return unique concepts (top 10)
        seen = set()
        unique_concepts = []
        for concept in concepts:
            if concept not in seen:
                unique_concepts.append(concept)
                seen.add(concept)
                if len(unique_concepts) >= 10:
                    break
        
        return unique_concepts
    
    def _extract_emotions(self, metadata: Dict) -> Dict:
        """Extract emotional context from metadata"""
        emotions = {}
        
        # Primary emotion
        if 'emotion' in metadata:
            emotions[metadata['emotion']] = 0.8
        
        # Additional emotions from enhanced analysis
        if 'emotional_context' in metadata:
            emotions.update(metadata['emotional_context'])
        
        return emotions
    
    def _calculate_harmonics(self, frequency: int) -> List[int]:
        """Calculate harmonic frequencies"""
        return [
            frequency * 2,      # Second harmonic
            frequency * 3,      # Third harmonic
            frequency // 2,     # Subharmonic
            int(frequency * 1.618)  # Phi harmonic
        ]
    
    def _format_history_for_prediction(self, conversation_history: List[Dict]) -> List[Dict]:
        """Format conversation history for predictive analysis"""
        formatted = []
        
        for entry in conversation_history:
            formatted_entry = {
                'content': entry.get('user_message', ''),
                'timestamp': entry.get('timestamp', datetime.now().isoformat()),
                'metadata': entry.get('metadata', {})
            }
            
            # Extract emotional context
            if 'metadata' in entry and 'emotion' in entry['metadata']:
                formatted_entry['emotional_context'] = {
                    entry['metadata']['emotion']: 1.0
                }
            
            formatted.append(formatted_entry)
        
        return formatted


# Global instance for easy import
enhanced_memory = EnhancedMemoryManager()
