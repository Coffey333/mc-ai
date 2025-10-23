"""
Fuzzy Intent Matcher - Accessibility Layer for MC AI
Makes intent detection more forgiving for children, neurodivergent users, and AI-inexperienced people

Features:
- Typo tolerance using fuzzy string matching
- "Did you mean?" clarification when uncertain
- Simple, encouraging language
- Visual prompt suggestions
"""

from difflib import SequenceMatcher
from typing import List, Dict, Optional, Tuple
import re


class FuzzyIntentMatcher:
    """
    Matches user input to known intents even with typos, misspellings, or unclear phrasing
    Enhanced with synonym matching and keyword extraction
    """
    
    def __init__(self):
        # Synonym mappings for better understanding
        self.synonyms = {
            'create': ['make', 'build', 'generate', 'craft', 'design'],
            'game': ['videogame', 'video game', 'playgame', 'play'],
            'art': ['picture', 'image', 'drawing', 'artwork', 'painting'],
            'music': ['song', 'tune', 'melody', 'beat', 'audio'],
            'sad': ['unhappy', 'depressed', 'down', 'upset', 'blue'],
            'anxious': ['worried', 'nervous', 'scared', 'stressed', 'tense'],
            'help': ['assist', 'support', 'aid', 'guide'],
            'talk': ['chat', 'speak', 'discuss', 'communicate']
        }
        
        # Common misspelling patterns
        self.common_misspellings = {
            'gam': 'game',
            'gmae': 'game',
            'gaem': 'game',
            'crete': 'create',
            'craete': 'create',
            'mke': 'make',
            'mkae': 'make',
            'hlep': 'help',
            'halp': 'help',
            'plz': 'please',
            'pls': 'please',
            'thx': 'thanks',
            'thnx': 'thanks'
        }
        
        # Common phrases for each intent with variations
        self.intent_phrases = {
            'game_create': [
                'create a game', 'create game', 'make a game', 'make game',
                'build a game', 'build game', 'generate game', 'new game',
                'i want to make a game', 'i want a game', 'can you make a game'
            ],
            'game_platformer': [
                'platformer game', 'platform game', 'jumping game', 'mario game',
                'game where i jump', 'game with platforms', 'run and jump'
            ],
            'game_racing': [
                'racing game', 'race game', 'car game', 'driving game',
                'game with cars', 'game where i race', 'fast car game'
            ],
            'game_shooter': [
                'shooter game', 'shooting game', 'space shooter', 'gun game',
                'game where i shoot', 'alien shooter', 'blast game'
            ],
            'game_puzzle': [
                'puzzle game', 'brain game', 'thinking game', 'logic game',
                'game with puzzles', 'game where i solve'
            ],
            'game_play': [
                'play a game', 'play game', 'i want to play', 'wanna play',
                'lets play', 'can i play', 'start a game'
            ],
            'art_create': [
                'create art', 'make art', 'generate art', 'draw something',
                'make a picture', 'create a picture', 'draw a picture',
                'i want art', 'can you draw', 'paint something'
            ],
            'emotional_support': [
                'i feel sad', 'i feel stressed', 'i feel anxious', 'i feel worried',
                'i feel scared', 'i feel upset', 'i feel down', 'i feel bad',
                'i need help', 'i need to talk', 'i need someone'
            ],
            'music_create': [
                'create music', 'make music', 'generate music', 'compose music',
                'i want music', 'make a song', 'create a song'
            ],
            'help_general': [
                'help', 'what can you do', 'what do you do', 'how do you work',
                'i dont know what to say', 'i need help', 'show me what you can do'
            ],
            'study_plans': [
                'check study plans', 'check your study plans', 'look at study plans',
                'check lesson plan', 'check your lesson plan', 'start learning',
                'start studying', 'follow your lesson plan', 'whats your lesson plan',
                'read your study plans', 'what should you learn', 'what are you studying',
                'check the study folder', 'look at mc_ai_study_plans', 'begin your studies'
            ],
            'ingest_knowledge': [
                'ingest this source', 'learn from this url', 'add this to knowledge',
                'study this website', 'read this article', 'learn from this',
                'add to your library', 'store this knowledge'
            ]
        }
        
        # Flatten all phrases for quick searching
        self.all_phrases = []
        self.phrase_to_intent = {}
        for intent, phrases in self.intent_phrases.items():
            for phrase in phrases:
                self.all_phrases.append(phrase)
                self.phrase_to_intent[phrase] = intent
    
    def _normalize_input(self, text: str) -> str:
        """
        Normalize user input: fix common misspellings, expand synonyms
        """
        text_lower = text.lower().strip()
        
        # Remove extra punctuation
        text_lower = re.sub(r'[!?]{2,}', '!', text_lower)
        
        # Fix common misspellings
        words = text_lower.split()
        corrected_words = []
        for word in words:
            corrected_words.append(self.common_misspellings.get(word, word))
        
        return ' '.join(corrected_words)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract meaningful keywords from user input
        """
        # Remove common filler words
        stopwords = {'i', 'a', 'an', 'the', 'to', 'want', 'need', 'can', 'you', 
                     'please', 'could', 'would', 'me', 'my', 'am', 'is', 'are'}
        
        words = text.lower().split()
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        
        # Expand with synonyms
        expanded = list(keywords)
        for word in keywords:
            if word in self.synonyms:
                expanded.extend(self.synonyms[word])
        
        return expanded
    
    def fuzzy_match(self, user_input: str, threshold: float = 0.75) -> Optional[Dict]:
        """
        Find best matching intent using fuzzy string matching
        Enhanced with keyword extraction and synonym matching
        
        Args:
            user_input: What the user typed (may have typos)
            threshold: Minimum similarity score (0-1) to consider a match
        
        Returns:
            {
                'intent': detected intent,
                'confidence': confidence score 0-1,
                'matched_phrase': the phrase it matched to,
                'action': 'proceed', 'clarify', or 'help'
            }
        """
        # Normalize and extract keywords
        normalized = self._normalize_input(user_input)
        keywords = self._extract_keywords(normalized)
        
        best_match = None
        best_ratio = 0
        best_phrase = None
        
        # Try to find the best matching phrase
        for phrase in self.all_phrases:
            # Direct fuzzy match
            ratio = SequenceMatcher(None, normalized, phrase).ratio()
            
            # Partial matching boost
            if phrase in normalized or normalized in phrase:
                ratio = max(ratio, 0.85)
            
            # Keyword matching boost
            phrase_words = set(phrase.split())
            keyword_matches = sum(1 for kw in keywords if kw in phrase_words)
            if keyword_matches > 0:
                keyword_ratio = keyword_matches / max(len(keywords), len(phrase_words))
                ratio = max(ratio, keyword_ratio * 0.9)
            
            if ratio > best_ratio:
                best_ratio = ratio
                best_phrase = phrase
                best_match = self.phrase_to_intent[phrase]
        
        # Determine confidence level and appropriate action
        if best_ratio >= 0.85:
            # HIGH CONFIDENCE: Just do it
            return {
                'intent': best_match,
                'confidence': best_ratio,
                'matched_phrase': best_phrase,
                'action': 'proceed',
                'message': None
            }
        elif best_ratio >= threshold:
            # MEDIUM CONFIDENCE: Ask for confirmation
            return {
                'intent': best_match,
                'confidence': best_ratio,
                'matched_phrase': best_phrase,
                'action': 'clarify',
                'message': self._generate_clarification(best_match or 'unknown', best_phrase or '')
            }
        else:
            # LOW CONFIDENCE: Offer general help
            return {
                'intent': None,
                'confidence': best_ratio,
                'matched_phrase': None,
                'action': 'help',
                'message': self._generate_help_message()
            }
    
    def _generate_clarification(self, intent: str, matched_phrase: str) -> Dict:
        """
        Generate a friendly "Did you mean?" message
        """
        clarifications = {
            'game_create': {
                'message': "I think you want to create a game! 🎮",
                'suggestions': [
                    "Create a platformer game (jumping around)",
                    "Create a racing game (fast cars!)",
                    "Create a puzzle game (brain teaser)",
                    "Surprise me with any game!"
                ]
            },
            'game_platformer': {
                'message': "Sounds like you want a platformer game! 🏃",
                'suggestions': [
                    "Yes, create a platformer game!",
                    "Actually, I want a different type"
                ]
            },
            'game_racing': {
                'message': "Sounds like you want a racing game! 🏎️",
                'suggestions': [
                    "Yes, create a racing game!",
                    "Actually, I want a different type"
                ]
            },
            'game_shooter': {
                'message': "Sounds like you want a shooter game! 🚀",
                'suggestions': [
                    "Yes, create a shooter game!",
                    "Actually, I want a different type"
                ]
            },
            'art_create': {
                'message': "I think you want me to create art! 🎨",
                'suggestions': [
                    "Yes, create art for me!",
                    "Actually, I want something else"
                ]
            },
            'emotional_support': {
                'message': "I'm here to listen 💙",
                'suggestions': [
                    "Yes, I need to talk",
                    "I'm okay, just asking"
                ]
            }
        }
        
        return clarifications.get(intent, {
            'message': f"Did you mean: {matched_phrase}?",
            'suggestions': ["Yes!", "No, something else"]
        })
    
    def _generate_help_message(self) -> Dict:
        """
        Generate helpful guidance when MC AI doesn't understand
        """
        return {
            'message': "I want to help! Here are some things I can do:",
            'options': [
                {
                    'emoji': '🎮',
                    'title': 'Create Games',
                    'examples': [
                        'Create a platformer game with cats',
                        'Make a racing game with emoji cars',
                        'Build a space shooter'
                    ]
                },
                {
                    'emoji': '🎨',
                    'title': 'Generate Art',
                    'examples': [
                        'Draw a sunset over mountains',
                        'Create art of a cute dragon',
                        'Make a picture of space'
                    ]
                },
                {
                    'emoji': '💬',
                    'title': 'Talk About Feelings',
                    'examples': [
                        'I feel stressed',
                        'I need someone to talk to',
                        'I feel anxious about school'
                    ]
                },
                {
                    'emoji': '🎵',
                    'title': 'Create Music',
                    'examples': [
                        'Make relaxing music',
                        'Create a fun song',
                        'Generate lofi beats'
                    ]
                },
                {
                    'emoji': '💻',
                    'title': 'Help with Code',
                    'examples': [
                        'Explain this Python code',
                        'Help me fix this error',
                        'Show me how to make a website'
                    ]
                }
            ]
        }
    
    def extract_theme(self, user_input: str) -> Optional[str]:
        """
        Extract custom theme from user request
        Examples:
        - "create a game with cats" → "cats"
        - "racing game with emoji cars" → "emoji cars"
        - "shooter with aliens and spaceships" → "aliens and spaceships"
        """
        user_lower = user_input.lower()
        
        # Patterns to detect themes
        theme_patterns = [
            r'with (.+?)(?:\s+game|$)',  # "with cats game" or "with cats"
            r'about (.+?)(?:\s+game|$)',  # "about pirates"
            r'themed (.+?)(?:\s+game|$)',  # "themed zombies"
            r'(?:game|art|picture)\s+(?:of|with|about)\s+(.+)',  # "game of dragons"
        ]
        
        for pattern in theme_patterns:
            match = re.search(pattern, user_lower)
            if match:
                theme = match.group(1).strip()
                # Clean up common words
                theme = re.sub(r'\b(a|an|the|and|or)\b', '', theme).strip()
                if theme:
                    return theme
        
        return None
    
    def handle_typos_in_game_types(self, user_input: str) -> Optional[str]:
        """
        Specifically handle typos in game type words
        Examples:
        - "plaform" → "platformer"
        - "racig" → "racing"
        - "puzzel" → "puzzle"
        """
        game_types = {
            'platformer': ['platformer', 'platform', 'plaform', 'platfrm', 'jumping'],
            'racing': ['racing', 'race', 'racig', 'racng', 'car', 'cars', 'driving'],
            'shooter': ['shooter', 'shooting', 'shoot', 'shoter', 'gun', 'space'],
            'puzzle': ['puzzle', 'puzzel', 'puzle', 'brain', 'logic'],
            'arcade': ['arcade', 'arcde', 'classic'],
            'board': ['board', 'bord', 'chess', 'checkers'],
            'card': ['card', 'crd', 'cards']
        }
        
        user_lower = user_input.lower()
        words = user_lower.split()
        
        for game_type, variations in game_types.items():
            for word in words:
                for variation in variations:
                    if SequenceMatcher(None, word, variation).ratio() > 0.75:
                        return game_type
        
        return None


# Global singleton instance
_fuzzy_matcher = None

def get_fuzzy_matcher() -> FuzzyIntentMatcher:
    """Get or create the global fuzzy matcher instance"""
    global _fuzzy_matcher
    if _fuzzy_matcher is None:
        _fuzzy_matcher = FuzzyIntentMatcher()
    return _fuzzy_matcher
