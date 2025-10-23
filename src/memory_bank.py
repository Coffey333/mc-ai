"""
Memory Bank - Long-Term Conversation Memory System
Stores old conversations in dataset format and retrieves relevant memories
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

class MemoryBank:
    """
    Extends MC AI's memory by storing old conversations in searchable dataset format
    
    Instead of losing old conversation context to token limits, we:
    1. Archive old messages as searchable knowledge
    2. Retrieve relevant memories based on current conversation
    3. Use dataset infrastructure for infinite scalable memory
    
    This makes old conversations part of MC AI's learned knowledge base.
    """
    
    def __init__(self, memory_path: str = "datasets/memory"):
        self.memory_path = memory_path
        os.makedirs(memory_path, exist_ok=True)
        
        # Track which messages have been archived
        self.archive_index_file = os.path.join(memory_path, "archive_index.json")
        self.archive_index = self._load_archive_index()
    
    def _load_archive_index(self) -> Dict:
        """Load index of what's been archived"""
        if os.path.exists(self.archive_index_file):
            with open(self.archive_index_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_archive_index(self):
        """Save archive index"""
        with open(self.archive_index_file, 'w') as f:
            json.dump(self.archive_index, f, indent=2)
    
    def archive_old_messages(self, user_id: str, messages: List[Dict], frequency_tags: Optional[List[int]] = None):
        """
        Archive old conversation messages as searchable dataset entries
        
        Args:
            user_id: User identifier
            messages: List of old messages to archive
            frequency_tags: Optional list of frequencies to tag these memories with
        """
        if not messages:
            return
        
        # Create user memory file
        user_memory_file = os.path.join(self.memory_path, f"user_{user_id}_memory.json")
        
        # Load existing memories or create new
        if os.path.exists(user_memory_file):
            with open(user_memory_file, 'r') as f:
                memories = json.load(f)
        else:
            memories = []
        
        # Convert messages to searchable memory format
        for msg in messages:
            if isinstance(msg, dict):
                user_msg = msg.get('content', '')
                role = msg.get('role', 'user')
                
                # Extract metadata if available
                metadata = msg.get('metadata', {})
                emotion = metadata.get('emotion', 'neutral')
                frequency = metadata.get('frequency', 240)
                
                # Create searchable memory entry
                memory_entry = {
                    'prompt': user_msg if role == 'user' else f"MC AI responded: {user_msg[:200]}",
                    'response': user_msg if role == 'assistant' else '',
                    'domain': 'memory',
                    'timestamp': datetime.now().isoformat(),
                    'emotion': emotion,
                    'frequency': frequency,
                    'user_id': user_id,
                    'role': role
                }
                
                # Add frequency tags for cross-thread recall
                if frequency_tags:
                    memory_entry['frequency_tags'] = frequency_tags
                
                memories.append(memory_entry)
        
        # Save updated memories
        with open(user_memory_file, 'w') as f:
            json.dump(memories, f, indent=2)
        
        # Update archive index
        if user_id not in self.archive_index:
            self.archive_index[user_id] = {
                'archived_count': 0,
                'last_archive': None
            }
        
        self.archive_index[user_id]['archived_count'] += len(messages)
        self.archive_index[user_id]['last_archive'] = datetime.now().isoformat()
        self._save_archive_index()
        
        print(f"📚 Archived {len(messages)} messages to long-term memory for {user_id}")
    
    def retrieve_relevant_memories(self, user_id: str, current_query: str, max_memories: int = 5) -> List[Dict]:
        """
        Retrieve relevant memories from archive based on current query
        
        Args:
            user_id: User identifier
            current_query: Current user query to find relevant memories for
            max_memories: Maximum number of memories to retrieve
            
        Returns:
            List of relevant memory entries
        """
        user_memory_file = os.path.join(self.memory_path, f"user_{user_id}_memory.json")
        
        if not os.path.exists(user_memory_file):
            return []
        
        with open(user_memory_file, 'r') as f:
            memories = json.load(f)
        
        if not memories:
            return []
        
        # Simple keyword-based relevance scoring
        query_words = set(current_query.lower().split())
        scored_memories = []
        
        for memory in memories:
            prompt = memory.get('prompt', '').lower()
            memory_words = set(prompt.split())
            
            # Calculate relevance score (intersection of words)
            common_words = query_words.intersection(memory_words)
            relevance_score = len(common_words)
            
            if relevance_score > 0:
                scored_memories.append({
                    'memory': memory,
                    'score': relevance_score
                })
        
        # Sort by relevance and return top matches
        scored_memories.sort(key=lambda x: x['score'], reverse=True)
        return [item['memory'] for item in scored_memories[:max_memories]]
    
    def retrieve_frequency_memories(self, user_id: str, target_frequency: int, max_memories: int = 5) -> List[Dict]:
        """
        Retrieve memories by frequency (for cross-thread recall)
        
        Args:
            user_id: User identifier
            target_frequency: Target frequency to search for
            max_memories: Maximum number of memories to retrieve
            
        Returns:
            List of memories at that frequency
        """
        user_memory_file = os.path.join(self.memory_path, f"user_{user_id}_memory.json")
        
        if not os.path.exists(user_memory_file):
            return []
        
        with open(user_memory_file, 'r') as f:
            memories = json.load(f)
        
        # Find memories at target frequency (with tolerance)
        frequency_memories = []
        for memory in memories:
            mem_freq = memory.get('frequency', 240)
            
            # Check if frequency matches (±5 Hz tolerance)
            if abs(mem_freq - target_frequency) <= 5:
                frequency_memories.append(memory)
            # Check frequency tags
            elif 'frequency_tags' in memory and target_frequency in memory['frequency_tags']:
                frequency_memories.append(memory)
        
        return frequency_memories[:max_memories]
    
    def get_memory_stats(self, user_id: str) -> Dict:
        """Get statistics about archived memories"""
        if user_id not in self.archive_index:
            return {'archived_count': 0, 'last_archive': None}
        
        return self.archive_index[user_id]
