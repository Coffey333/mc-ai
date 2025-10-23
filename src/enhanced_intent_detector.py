"""
Enhanced Intent Detection System
Prevents false positives and improves accuracy for user requests
Handles typos, vague questions, and context awareness
"""

import re
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher


class EnhancedIntentDetector:
    """
    Advanced intent detection with:
    - Typo tolerance
    - Context awareness
    - False positive reduction
    - Question vs. request distinction
    """
    
    def __init__(self):
        # Action verbs that indicate user wants something created
        self.action_verbs = [
            'create', 'make', 'generate', 'build', 'design', 'develop',
            'produce', 'craft', 'construct', 'compose', 'draw', 'paint'
        ]
        
        # Question words that indicate inquiry, not request
        self.question_indicators = [
            'what', 'who', 'when', 'where', 'why', 'how', 'which',
            'can you tell', 'tell me about', 'explain', 'describe',
            'do you know', 'have you heard', 'what do you think'
        ]
        
        # Patterns that indicate user is just talking about something, not requesting it
        self.discussion_patterns = [
            r'\b(talk about|discuss|learn about|read about|hear about)\b',
            r'\b(your (opinion|thoughts|view) on)\b',
            r'\b(what (is|are|was|were))\b',
            r'\b(tell me (about|more))\b',
            r'\b(interested in|curious about)\b'
        ]
    
    def wants_art(self, query: str, is_ai_conversation: bool = False) -> bool:
        """
        Detect if user wants AI art generation
        Returns True only if user explicitly requests creation
        """
        if is_ai_conversation:
            return False
        
        query_lower = query.lower()
        
        # Check if this is just a question about art
        if self._is_question_not_request(query_lower):
            return False
        
        # Explicit art creation keywords (high confidence)
        art_creation_patterns = [
            r'\b(create|make|generate|draw|paint|design)\b.{0,30}\b(art|image|picture|illustration|artwork|drawing|painting)\b',
            r'\b(art|image|picture|illustration|artwork|drawing|painting)\b.{0,20}\b(for me|please)\b',
            r'\bshow me\b.{0,10}\b(art|image|picture)\b.{0,10}\bof\b'
        ]
        
        for pattern in art_creation_patterns:
            if re.search(pattern, query_lower):
                return True
        
        # Simple keywords only if combined with action words
        art_keywords = ['generate art', 'create art', 'make art', 'draw me', 'paint me']
        return any(keyword in query_lower for keyword in art_keywords)
    
    def wants_music(self, query: str, is_ai_conversation: bool = False) -> bool:
        """
        Detect if user wants music generation
        Returns True only if user explicitly requests creation
        """
        if is_ai_conversation:
            return False
        
        query_lower = query.lower()
        
        # Check if this is just a question about music
        if self._is_question_not_request(query_lower):
            return False
        
        # Explicit music creation patterns
        music_creation_patterns = [
            r'\b(create|make|generate|compose|produce)\b.{0,30}\b(music|song|sound|audio|soundtrack|beat)\b',
            r'\b(music|song|sound|audio)\b.{0,20}\b(for me|please)\b',
            r'\bplay me\b.{0,10}\b(music|song)\b'
        ]
        
        for pattern in music_creation_patterns:
            if re.search(pattern, query_lower):
                return True
        
        # Simple keywords only if combined with action words
        music_keywords = ['generate music', 'create music', 'make music', 'compose music']
        return any(keyword in query_lower for keyword in music_keywords)
    
    def wants_game(self, query: str, is_ai_conversation: bool = False) -> bool:
        """
        Detect if user wants game generation
        Returns True only if user explicitly requests creation
        """
        if is_ai_conversation:
            return False
        
        query_lower = query.lower()
        
        # Check if this is just a question about games
        if self._is_question_not_request(query_lower):
            # Exception: "play a game" or "let's play" is a request
            if any(phrase in query_lower for phrase in ['play a game', 'play game', 'lets play', "let's play"]):
                return True
            return False
        
        # Explicit game creation patterns
        game_creation_patterns = [
            r'\b(create|make|generate|build|design)\b.{0,30}\b(game|puzzle|quiz)\b',
            r'\bgame\b.{0,20}\b(for me|please)\b',
            r'\b(play|start)\b.{0,10}\b(a|the)\b.{0,10}\bgame\b'
        ]
        
        for pattern in game_creation_patterns:
            if re.search(pattern, query_lower):
                return True
        
        # Simple keywords
        game_keywords = ['create game', 'make game', 'generate game', 'build game', 'play a game', 'interactive game']
        return any(keyword in query_lower for keyword in game_keywords)
    
    def wants_video(self, query: str) -> bool:
        """Detect if user wants video generation"""
        query_lower = query.lower()
        
        # Check if this is just a question
        if self._is_question_not_request(query_lower):
            return False
        
        # Video creation patterns
        video_creation_patterns = [
            r'\b(create|make|generate|produce)\b.{0,30}\b(video|animation)\b',
            r'\b(video|animation)\b.{0,20}\b(for me|please)\b',
            r'\banimate\b.{0,20}\b(this|that|it)\b'
        ]
        
        for pattern in video_creation_patterns:
            if re.search(pattern, query_lower):
                return True
        
        return False
    
    def _is_question_not_request(self, query_lower: str) -> bool:
        """
        Determine if this is a question/discussion vs. an actual request
        
        Examples:
        - "What is music therapy?" → True (question)
        - "Create music for me" → False (request)
        - "Tell me about AI art" → True (discussion)
        - "Generate art of a sunset" → False (request)
        """
        # Check for question indicators at start
        if any(query_lower.strip().startswith(q) for q in self.question_indicators):
            return True
        
        # Check for discussion patterns
        for pattern in self.discussion_patterns:
            if re.search(pattern, query_lower):
                return True
        
        # Check if it ends with a question mark and has no action verbs
        if '?' in query_lower:
            has_action_verb = any(verb in query_lower for verb in self.action_verbs)
            if not has_action_verb:
                return True
        
        return False
    
    def detect_typos_and_suggest(self, query: str, vocab: List[str], threshold: float = 0.8) -> Dict[str, str]:
        """
        Detect typos and suggest corrections
        
        Args:
            query: User's input
            vocab: List of known correct words/phrases
            threshold: Similarity threshold (0-1)
        
        Returns:
            Dict mapping typos to suggested corrections
        """
        words = query.lower().split()
        corrections = {}
        
        for word in words:
            # Skip very short words
            if len(word) < 3:
                continue
            
            # Check against vocabulary
            best_match = None
            best_score = 0
            
            for known_word in vocab:
                similarity = SequenceMatcher(None, word, known_word.lower()).ratio()
                if similarity > best_score and similarity >= threshold:
                    best_score = similarity
                    best_match = known_word
            
            if best_match and best_match.lower() != word:
                corrections[word] = best_match
        
        return corrections
    
    def normalize_query(self, query: str, corrections: Dict[str, str] = None) -> str:
        """
        Normalize query by:
        - Fixing typos
        - Standardizing spacing
        - Removing extra punctuation
        """
        normalized = query.strip()
        
        # Apply typo corrections if provided
        if corrections:
            for typo, correction in corrections.items():
                # Use word boundaries to avoid partial replacements
                normalized = re.sub(rf'\b{re.escape(typo)}\b', correction, normalized, flags=re.IGNORECASE)
        
        # Standardize multiple spaces
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Remove multiple punctuation
        normalized = re.sub(r'([!?.]){2,}', r'\1', normalized)
        
        return normalized
    
    def extract_context_clues(self, query: str, conversation_history: List[Dict]) -> Dict:
        """
        Extract context clues from conversation history
        Helps resolve vague references like "it", "that", "the thing"
        """
        context = {
            'recent_topics': [],
            'recent_entities': [],
            'last_user_question': None,
            'conversation_tone': 'neutral'
        }
        
        # Get last 5 messages
        recent = conversation_history[-5:] if len(conversation_history) > 5 else conversation_history
        
        for msg in recent:
            # Extract topics (simple noun extraction)
            content = msg.get('content', '') or msg.get('user_message', '') or msg.get('ai_response', '')
            if content:
                # Extract capitalized words (likely entities/topics)
                entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
                context['recent_entities'].extend(entities)
                
                # Extract nouns after "about", "regarding", etc.
                topics = re.findall(r'\b(?:about|regarding|concerning)\s+(\w+(?:\s+\w+)*)', content.lower())
                context['recent_topics'].extend(topics)
        
        # Get last user question
        for msg in reversed(recent):
            if msg.get('role') == 'user' or 'user_message' in msg:
                content = msg.get('content') or msg.get('user_message', '')
                if '?' in content:
                    context['last_user_question'] = content
                    break
        
        # Detect conversation tone
        query_lower = query.lower()
        if any(word in query_lower for word in ['please', 'thanks', 'thank you', 'appreciate']):
            context['conversation_tone'] = 'polite'
        elif any(word in query_lower for word in ['!', 'wow', 'amazing', 'awesome']):
            context['conversation_tone'] = 'enthusiastic'
        elif any(word in query_lower for word in ['help', 'confused', 'don\'t understand']):
            context['conversation_tone'] = 'seeking_help'
        
        return context
    
    def resolve_vague_reference(self, query: str, context_clues: Dict) -> Optional[str]:
        """
        Resolve vague references using context
        
        Examples:
        - "tell me more about it" + context["recent_topics"] = ["quantum computing"]
          → "tell me more about quantum computing"
        """
        query_lower = query.lower()
        
        # Vague pronouns
        vague_patterns = [
            (r'\bit\b', 'recent_topics'),
            (r'\bthat\b', 'recent_topics'),
            (r'\bthis\b', 'recent_topics'),
            (r'\bthe thing\b', 'recent_topics'),
            (r'\bthem\b', 'recent_entities'),
            (r'\bthey\b', 'recent_entities')
        ]
        
        resolved = query
        
        for pattern, context_key in vague_patterns:
            if re.search(pattern, query_lower):
                # Get most recent item from context
                items = context_clues.get(context_key, [])
                if items:
                    most_recent = items[-1]
                    # Replace vague reference with specific reference
                    resolved = re.sub(pattern, most_recent, resolved, count=1, flags=re.IGNORECASE)
                    break
        
        return resolved if resolved != query else None


# Global instance
enhanced_intent_detector = EnhancedIntentDetector()
