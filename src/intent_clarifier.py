"""
Intent Clarifier for MC AI
Helps understand unclear, vague, or incomplete user requests
Interprets user intent even when they can't express themselves clearly
"""

import re
from typing import Dict, List, Optional, Tuple

class IntentClarifier:
    """
    Interprets unclear user requests by analyzing patterns, context, and common usage
    Helps users who struggle to express themselves clearly
    """
    
    def __init__(self):
        # Common incomplete/vague patterns and their likely meanings
        self.vague_patterns = {
            # Emotional distress signals
            r'\b(hurt|hurts|hurting)\b': {
                'likely_intent': 'emotional_support',
                'interpretation': 'experiencing emotional or physical pain',
                'suggested_response': 'emotional support and understanding'
            },
            r'\b(help|help me)\b(?!\s+with\s+\w+)': {
                'likely_intent': 'seeking_help',
                'interpretation': 'needs assistance but unclear with what',
                'suggested_response': 'ask about what kind of help or infer from context'
            },
            r'\b(idk|dunno|don\'t know)\s+(what|how)': {
                'likely_intent': 'confusion_indecision',
                'interpretation': 'feeling confused or indecisive',
                'suggested_response': 'offer guidance or options'
            },
            r'\b(the thing|that thing|this)\b(?!\s+\w+)': {
                'likely_intent': 'unclear_reference',
                'interpretation': 'referring to something from context',
                'suggested_response': 'use conversation history to identify referent'
            },
            r'\b(can you|could you|will you)\s*$': {
                'likely_intent': 'incomplete_request',
                'interpretation': 'incomplete question/request',
                'suggested_response': 'offer common completions based on MC AI capabilities'
            },
            r'^\s*\w{1,3}\s*$': {
                'likely_intent': 'very_short_input',
                'interpretation': 'extremely brief message, needs context interpretation',
                'suggested_response': 'interpret based on conversation flow'
            },
            r'\b(why|how come)\s*$': {
                'likely_intent': 'incomplete_why_question',
                'interpretation': 'asking "why" about previous topic',
                'suggested_response': 'explain the last discussed topic'
            },
            r'\b(what about|how about)\s+\w+\s*$': {
                'likely_intent': 'topic_shift',
                'interpretation': 'shifting to related topic',
                'suggested_response': 'discuss the new topic mentioned'
            }
        }
        
        # Common emotional markers in unclear speech
        self.emotional_markers = {
            'distress': ['help', 'cant', "can't", 'stuck', 'confused', 'lost', 'scared', 'worried'],
            'pain': ['hurt', 'hurts', 'painful', 'ache', 'suffering'],
            'uncertainty': ['idk', 'dunno', "don't know", 'unsure', 'maybe', 'not sure'],
            'overwhelm': ['too much', 'cant handle', 'overwhelmed', 'stressed'],
            'seeking': ['need', 'want', 'looking for', 'trying to']
        }
        
        # Context clues for inference
        self.context_keywords = {
            'code_related': ['code', 'program', 'function', 'error', 'bug', 'python', 'javascript'],
            'art_related': ['draw', 'create', 'art', 'image', 'picture', 'generate'],
            'emotion_related': ['feel', 'feeling', 'emotion', 'mood', 'anxiety', 'happy', 'sad'],
            'analysis_related': ['analyze', 'data', 'pattern', 'understand', 'explain']
        }
    
    def clarify_intent(self, query: str, conversation_history: Optional[List] = None) -> Dict:
        """
        Analyze unclear query and infer likely intent
        
        Args:
            query: User's message (potentially unclear/vague)
            conversation_history: Previous messages for context
            
        Returns:
            Dict with interpretation, suggested_intent, confidence, and context_clues
        """
        query_lower = query.lower().strip()
        
        # Check for vague patterns
        detected_patterns = []
        for pattern, info in self.vague_patterns.items():
            if re.search(pattern, query_lower):
                detected_patterns.append(info)
        
        # Detect emotional state
        emotional_state = self._detect_emotional_markers(query_lower)
        
        # Extract context from conversation history
        context_clues = self._extract_context(query_lower, conversation_history)
        
        # Build interpretation
        interpretation = self._build_interpretation(
            query, 
            detected_patterns, 
            emotional_state, 
            context_clues,
            conversation_history
        )
        
        return interpretation
    
    def _detect_emotional_markers(self, query: str) -> List[str]:
        """Detect emotional markers in text"""
        found_emotions = []
        for emotion, markers in self.emotional_markers.items():
            if any(marker in query for marker in markers):
                found_emotions.append(emotion)
        return found_emotions
    
    def _extract_context(self, query: str, conversation_history: Optional[List]) -> Dict:
        """Extract contextual clues from query and history"""
        clues = {
            'query_length': len(query.split()),
            'is_very_short': len(query.split()) <= 3,
            'is_question': '?' in query or query.startswith(('what', 'how', 'why', 'when', 'where', 'who', 'can', 'could', 'would')),
            'recent_topics': []
        }
        
        # Analyze recent conversation for context
        if conversation_history and len(conversation_history) > 0:
            # Get last few messages for context
            recent_messages = conversation_history[-5:] if len(conversation_history) >= 5 else conversation_history
            
            # Identify topics discussed recently
            for domain, keywords in self.context_keywords.items():
                for msg in recent_messages:
                    msg_content = msg.get('content', '') if isinstance(msg, dict) else str(msg)
                    if any(kw in msg_content.lower() for kw in keywords):
                        if domain not in clues['recent_topics']:
                            clues['recent_topics'].append(domain)
        
        return clues
    
    def _build_interpretation(self, query: str, patterns: List, emotions: List, 
                            context: Dict, history: Optional[List]) -> Dict:
        """Build final interpretation of user intent"""
        
        # Default interpretation
        interpretation = {
            'original_query': query,
            'is_unclear': False,
            'likely_intent': 'general_conversation',
            'interpretation': query,  # Default: use as-is
            'confidence': 1.0,  # High confidence if clear
            'suggestions': [],
            'emotional_state': emotions,
            'context_clues': context
        }
        
        # Check if query is unclear/vague
        is_unclear = (
            context['is_very_short'] or 
            len(patterns) > 0 or 
            len(emotions) > 0 or
            query.strip().endswith(('...', '..'))
        )
        
        if is_unclear:
            interpretation['is_unclear'] = True
            interpretation['confidence'] = 0.6  # Lower confidence for unclear requests
            
            # Build interpretation based on patterns and context
            if patterns:
                # Use first detected pattern
                primary_pattern = patterns[0]
                interpretation['likely_intent'] = primary_pattern['likely_intent']
                interpretation['interpretation'] = primary_pattern['interpretation']
                interpretation['suggestions'].append(primary_pattern['suggested_response'])
            
            # Add emotional context
            if emotions:
                interpretation['likely_intent'] = 'emotional_support'
                emotional_desc = ', '.join(emotions)
                interpretation['interpretation'] = f"User expressing {emotional_desc}"
                interpretation['suggestions'].append(f"Respond with empathy to their {emotional_desc}")
            
            # Use recent topics for context
            if context['recent_topics']:
                topic_desc = ' or '.join(context['recent_topics'])
                interpretation['suggestions'].append(f"Likely related to recent {topic_desc} discussion")
                # Upgrade confidence if we have strong context
                interpretation['confidence'] = min(0.8, interpretation['confidence'] + 0.2)
        
        return interpretation
    
    def suggest_clarification_questions(self, interpretation: Dict) -> List[str]:
        """Generate clarification questions if needed"""
        if not interpretation['is_unclear']:
            return []
        
        questions = []
        intent = interpretation['likely_intent']
        
        if intent == 'seeking_help':
            questions.append("What kind of help do you need?")
            questions.append("Can you tell me more about what you're working on?")
        elif intent == 'unclear_reference':
            questions.append("What are you referring to?")
            questions.append("Can you be more specific?")
        elif intent == 'incomplete_request':
            questions.append("I can help with code analysis, creating art, emotional support, or answering questions. What would you like?")
        elif intent == 'confusion_indecision':
            questions.append("What are you trying to decide?")
            questions.append("What options are you considering?")
        
        return questions
