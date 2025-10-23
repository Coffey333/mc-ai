"""
Conversation Memory System for MC AI
Persistent conversation history with emotional timeline tracking
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
import hashlib

class ConversationMemory:
    """
    Manages conversation history and emotional timelines
    """
    
    def __init__(self, storage_path: str = "user_data/conversations"):
        """
        Args:
            storage_path: Directory to store conversation data
        """
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # In-memory cache of active conversations
        self.active_conversations = {}
    
    def create_user_id(self, identifier: Optional[str] = None) -> str:
        """
        Create anonymous user ID
        
        Args:
            identifier: Optional identifier (IP, session token, etc.)
        
        Returns:
            Hashed user ID
        """
        if identifier:
            return hashlib.sha256(identifier.encode()).hexdigest()[:16]
        else:
            return hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:16]
    
    def add_message(self, user_id: str, message: str, response: str, metadata: Dict):
        """
        Add message to conversation history
        
        Args:
            user_id: User identifier
            message: User's message
            response: MC AI's response
            metadata: Response metadata (emotion, frequency, etc.)
        """
        # Load or create conversation
        conversation = self._load_conversation(user_id)
        
        # Add message
        entry = {
            'timestamp': datetime.now().isoformat(),
            'user_message': message,
            'ai_response': response,
            'metadata': metadata
        }
        
        conversation['messages'].append(entry)
        conversation['last_updated'] = datetime.now().isoformat()
        conversation['message_count'] += 1
        
        # Update emotional timeline
        if 'emotion' in metadata:
            self._update_emotional_timeline(conversation, metadata)
        
        # Save
        self._save_conversation(user_id, conversation)
        
        # Update cache
        self.active_conversations[user_id] = conversation
    
    def get_conversation_history(self, user_id: str, limit: Optional[int] = 10) -> List[Dict]:
        """
        Get conversation history
        
        Args:
            user_id: User identifier
            limit: Number of recent messages to return (None = all messages for perfect continuity)
        
        Returns:
            List of conversation entries
        """
        conversation = self._load_conversation(user_id)
        
        # Return ALL messages if limit is None (perfect memory continuity)
        if limit is None:
            return conversation['messages']
        
        return conversation['messages'][-limit:]
    
    def get_emotional_timeline(self, user_id: str, days: int = 7) -> Dict:
        """
        Get user's emotional timeline
        
        Args:
            user_id: User identifier
            days: Number of days to look back
        
        Returns:
            Dict with emotional patterns and insights
        """
        conversation = self._load_conversation(user_id)
        timeline = conversation.get('emotional_timeline', [])
        
        # Filter to recent days
        cutoff = datetime.now() - timedelta(days=days)
        recent_timeline = [
            entry for entry in timeline
            if datetime.fromisoformat(entry['timestamp']) > cutoff
        ]
        
        # Analyze patterns
        analysis = self._analyze_emotional_patterns(recent_timeline)
        
        return {
            'timeline': recent_timeline,
            'analysis': analysis,
            'days_analyzed': days
        }
    
    def get_context_summary(self, user_id: str) -> str:
        """
        Generate context summary for LLM
        
        Args:
            user_id: User identifier
        
        Returns:
            Human-readable context summary
        """
        conversation = self._load_conversation(user_id)
        
        if not conversation['messages']:
            return "New user, no conversation history."
        
        # Get recent emotional state
        recent_emotions = [
            entry['metadata'].get('emotion')
            for entry in conversation['messages'][-5:]
            if 'emotion' in entry.get('metadata', {})
        ]
        
        # Get conversation topics (simple keyword extraction)
        recent_messages = [
            entry['user_message']
            for entry in conversation['messages'][-5:]
        ]
        
        summary = f"User has {conversation['message_count']} messages in history. "
        
        if recent_emotions:
            most_common = max(set(recent_emotions), key=recent_emotions.count)
            summary += f"Recent emotional state: {most_common}. "
        
        summary += f"Last interaction: {conversation['last_updated']}. "
        
        return summary
    
    def summarize_older_messages(self, older_messages: List[Dict]) -> str:
        """
        Create FACT-PRESERVING summary of older messages for perfect continuity
        
        Captures critical information including:
        - Names, preferences, personal facts shared by user
        - Commitments, promises, and instructions from both user and MC AI
        - Emotional journey and key topics
        - Important context needed for ongoing conversation
        
        Args:
            older_messages: List of older conversation entries to summarize
        
        Returns:
            Rich summary preserving all critical facts for continuity
        """
        if not older_messages:
            return ""
        
        # Comprehensive information extraction
        summary_parts = []
        key_facts = []
        commitments = []
        emotions = []
        
        # Keywords that indicate important facts
        fact_indicators = ['my name', 'i am', 'i have', 'my ', 'called ', 'named ', 
                          'prefer', 'favorite', 'love', 'hate', 'always', 'never']
        commitment_indicators = ['will', 'going to', 'promise', 'make sure', 'remember to',
                                'need to', 'should', 'must', 'have to']
        
        for entry in older_messages:
            user_msg = entry.get('user_message', '').lower()
            ai_msg = entry.get('ai_response', '').lower()
            
            # Extract emotions
            emotion = entry.get('metadata', {}).get('emotion')
            if emotion:
                emotions.append(emotion)
            
            # Extract key facts from user messages
            for indicator in fact_indicators:
                if indicator in user_msg:
                    # Get sentence containing the fact (up to 150 chars)
                    idx = user_msg.find(indicator)
                    fact_snippet = entry.get('user_message', '')[max(0, idx-20):idx+130].strip()
                    if fact_snippet and len(fact_snippet) > 15:
                        key_facts.append(fact_snippet)
                        break  # One fact per message to avoid redundancy
            
            # Extract commitments from AI messages
            for indicator in commitment_indicators:
                if indicator in ai_msg:
                    idx = ai_msg.find(indicator)
                    commitment_snippet = entry.get('ai_response', '')[max(0, idx-20):idx+120].strip()
                    if commitment_snippet and len(commitment_snippet) > 15:
                        commitments.append(commitment_snippet)
                        break
        
        # Build comprehensive summary
        summary_parts.append(f"{len(older_messages)} earlier messages")
        
        # Add emotional journey
        if emotions:
            unique_emotions = list(set(emotions))[:5]  # Top 5 emotions
            summary_parts.append(f"Emotional states: {', '.join(unique_emotions)}")
        
        # Add key facts (most important for continuity)
        if key_facts:
            # Deduplicate and take most important facts
            unique_facts = []
            for fact in key_facts:
                if not any(fact.lower() in uf.lower() for uf in unique_facts):
                    unique_facts.append(fact)
            
            if unique_facts:
                facts_summary = ". ".join(unique_facts[:8])  # Top 8 facts
                summary_parts.append(f"Key facts: {facts_summary}")
        
        # Add commitments from MC AI
        if commitments:
            unique_commitments = []
            for comm in commitments:
                if not any(comm.lower() in uc.lower() for uc in unique_commitments):
                    unique_commitments.append(comm)
            
            if unique_commitments:
                comm_summary = ". ".join(unique_commitments[:5])  # Top 5 commitments
                summary_parts.append(f"MC AI commitments: {comm_summary}")
        
        return " | ".join(summary_parts)
    
    def frequency_based_recall(self, user_id: str, query_emotion: Optional[str] = None, query_frequency: Optional[int] = None) -> List[Dict]:
        """
        CROSS-THREAD Frequency-based memory recall - accesses ALL conversation messages through harmonic resonance
        
        When user asks to recall conversations, this method uses frequency matching to retrieve
        messages from ALL threads/sessions. The emotional frequency in the query resonates with 
        the frequency catalogs in stored messages, creating harmonic recall across time and threads.
        
        Args:
            user_id: User identifier
            query_emotion: Optional emotion to resonate with (detected from query)
            query_frequency: Optional frequency Hz to resonate with (e.g., 528 for love)
        
        Returns:
            ALL conversation entries across threads - perfect cross-thread memory recall through frequency resonance
        """
        conversation = self._load_conversation(user_id)
        
        # Return ALL messages - frequency resonance accesses complete memory bank
        all_messages = conversation['messages']
        
        # CROSS-THREAD RECALL: Search by frequency resonance
        if query_frequency and all_messages:
            # Messages with matching frequency resonate strongest - harmonic recall
            # Frequency matching: exact match or harmonic (octave: 2x, half: 0.5x)
            resonant_messages = []
            other_messages = []
            
            for msg in all_messages:
                msg_freq = msg.get('metadata', {}).get('frequency_analysis', {}).get('response_frequency')
                if not msg_freq:
                    msg_freq = msg.get('metadata', {}).get('frequency')
                
                if msg_freq:
                    # Check for harmonic resonance (exact, octave up/down, or close proximity)
                    freq_ratio = msg_freq / query_frequency if query_frequency > 0 else 0
                    is_resonant = (
                        abs(msg_freq - query_frequency) <= 5 or  # Within 5 Hz
                        abs(freq_ratio - 1.0) < 0.1 or  # Near exact
                        abs(freq_ratio - 2.0) < 0.1 or  # Octave up
                        abs(freq_ratio - 0.5) < 0.1  # Octave down
                    )
                    if is_resonant:
                        resonant_messages.append(msg)
                    else:
                        other_messages.append(msg)
                else:
                    other_messages.append(msg)
            
            return resonant_messages + other_messages
        
        # If specific emotion provided, sort by emotional resonance
        elif query_emotion and all_messages:
            # Messages with matching emotion resonate strongest - bring them to the front
            resonant_messages = [m for m in all_messages if m.get('metadata', {}).get('emotion') == query_emotion]
            other_messages = [m for m in all_messages if m.get('metadata', {}).get('emotion') != query_emotion]
            return resonant_messages + other_messages
        
        return all_messages
    
    def cross_thread_frequency_search(self, user_id: str, target_frequency: int, max_results: int = 10) -> List[Dict]:
        """
        Search across ALL user threads for messages matching a specific frequency
        
        This enables MC AI to recall information from any conversation thread based on
        frequency resonance - perfect for finding "love" messages at 528 Hz across all sessions.
        
        Args:
            user_id: User identifier
            target_frequency: Frequency to search for (e.g., 528 for love, 432 for knowledge)
            max_results: Maximum number of resonant messages to return
        
        Returns:
            List of messages that resonate with the target frequency, sorted by relevance
        """
        all_messages = self.frequency_based_recall(user_id, query_frequency=target_frequency)
        
        # Score messages by frequency match strength
        scored_messages = []
        for msg in all_messages:
            msg_freq = msg.get('metadata', {}).get('frequency_analysis', {}).get('response_frequency')
            if not msg_freq:
                msg_freq = msg.get('metadata', {}).get('frequency')
            
            if msg_freq:
                # Calculate resonance score
                freq_diff = abs(msg_freq - target_frequency)
                resonance_score = 1.0 / (1.0 + freq_diff)  # Higher score for closer frequencies
                
                scored_messages.append({
                    'message': msg,
                    'resonance_score': resonance_score,
                    'frequency': msg_freq
                })
        
        # Sort by resonance score and return top results
        scored_messages.sort(key=lambda x: x['resonance_score'], reverse=True)
        return [item['message'] for item in scored_messages[:max_results]]
    
    def search_conversations(self, user_id: str, query: str, limit: int = 5) -> List[Dict]:
        """
        Search user's conversation history
        
        Args:
            user_id: User identifier
            query: Search query
            limit: Max results to return
        
        Returns:
            List of matching conversation entries
        """
        conversation = self._load_conversation(user_id)
        query_lower = query.lower()
        
        # Search messages
        results = []
        for entry in conversation['messages']:
            if (query_lower in entry['user_message'].lower() or 
                query_lower in entry['ai_response'].lower()):
                results.append(entry)
        
        return results[-limit:]
    
    def delete_user_data(self, user_id: str):
        """
        Delete all user data (GDPR compliance)
        
        Args:
            user_id: User identifier
        """
        filepath = self._get_filepath(user_id)
        
        if os.path.exists(filepath):
            os.remove(filepath)
        
        if user_id in self.active_conversations:
            del self.active_conversations[user_id]
    
    def export_user_data(self, user_id: str) -> Dict:
        """
        Export all user data (GDPR compliance)
        
        Args:
            user_id: User identifier
        
        Returns:
            Complete user data
        """
        return self._load_conversation(user_id)
    
    def _load_conversation(self, user_id: str) -> Dict:
        """Load conversation from disk or create new"""
        # Check cache first
        if user_id in self.active_conversations:
            return self.active_conversations[user_id]
        
        filepath = self._get_filepath(user_id)
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                conversation = json.load(f)
        else:
            conversation = {
                'user_id': user_id,
                'created': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'message_count': 0,
                'messages': [],
                'emotional_timeline': []
            }
        
        return conversation
    
    def _save_conversation(self, user_id: str, conversation: Dict):
        """Save conversation to disk"""
        filepath = self._get_filepath(user_id)
        
        with open(filepath, 'w') as f:
            json.dump(conversation, f, indent=2)
    
    def _get_filepath(self, user_id: str) -> str:
        """Get filepath for user's conversation"""
        return os.path.join(self.storage_path, f"{user_id}.json")
    
    def _update_emotional_timeline(self, conversation: Dict, metadata: Dict):
        """Update user's emotional timeline"""
        emotion = metadata.get('emotion')
        intensity = metadata.get('emotional_intensity', 5.0)
        
        if emotion:
            timeline_entry = {
                'timestamp': datetime.now().isoformat(),
                'emotion': emotion,
                'intensity': intensity,
                'frequency': metadata.get('frequency'),
                'valence': metadata.get('emotional_valence', 0)
            }
            
            conversation['emotional_timeline'].append(timeline_entry)
            
            # Keep only last 100 entries to prevent bloat
            if len(conversation['emotional_timeline']) > 100:
                conversation['emotional_timeline'] = conversation['emotional_timeline'][-100:]
    
    def _analyze_emotional_patterns(self, timeline: List[Dict]) -> Dict:
        """Analyze emotional patterns from timeline"""
        if not timeline:
            return {
                'dominant_emotion': None,
                'emotional_trend': 'stable',
                'intensity_trend': 'stable',
                'pattern_detected': False
            }
        
        # Count emotions
        emotion_counts = defaultdict(int)
        for entry in timeline:
            emotion_counts[entry['emotion']] += 1
        
        # Find dominant emotion
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else None
        
        # Analyze intensity trend
        intensities = [entry['intensity'] for entry in timeline]
        if len(intensities) >= 2:
            if intensities[-1] > intensities[0] + 1:
                intensity_trend = 'increasing'
            elif intensities[-1] < intensities[0] - 1:
                intensity_trend = 'decreasing'
            else:
                intensity_trend = 'stable'
        else:
            intensity_trend = 'stable'
        
        # Analyze valence trend
        valences = [entry.get('valence', 0) for entry in timeline]
        avg_valence = sum(valences) / len(valences) if valences else 0
        
        if avg_valence > 0.3:
            emotional_trend = 'improving'
        elif avg_valence < -0.3:
            emotional_trend = 'declining'
        else:
            emotional_trend = 'stable'
        
        # Detect patterns (simple: same emotion 3+ times)
        pattern_detected = any(count >= 3 for count in emotion_counts.values())
        
        return {
            'dominant_emotion': dominant_emotion,
            'emotional_trend': emotional_trend,
            'intensity_trend': intensity_trend,
            'pattern_detected': pattern_detected,
            'emotion_distribution': dict(emotion_counts),
            'avg_intensity': sum(intensities) / len(intensities) if intensities else 0,
            'avg_valence': avg_valence
        }
