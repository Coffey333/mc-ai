"""
MC AI User Profiling & Discernment System v1.0

Deeply analyzes each user's unique patterns to create psychological profiles:
- Linguistic fingerprinting (vocabulary, sentence structure, phrasing)
- Emotional signatures (how they express feelings, what resonates)
- Conceptual blending (how they connect ideas, use metaphors)
- Communication style (formal vs casual, directness, humor)
- Authenticity detection (identify when someone is pretending to be someone else)

This gives MC AI true discernment - knowing each person as deeply as he knows himself.
"""

import json
import re
import os
from datetime import datetime
from collections import Counter, defaultdict
import numpy as np
from typing import Dict, List, Any, Tuple

class UserProfilingSystem:
    """
    Creates deep psychological profiles of users based on their communication patterns.
    Enables MC AI to distinguish between different people and detect impersonation.
    """
    
    def __init__(self, profiles_dir='user_data/psychological_profiles'):
        self.profiles_dir = profiles_dir
        os.makedirs(profiles_dir, exist_ok=True)
        
    def analyze_user_message(self, user_id: str, message: str, metadata: Dict = None) -> Dict[str, Any]:
        """
        Deeply analyze a user's message to extract their unique patterns.
        
        Returns profile features:
        - Linguistic patterns
        - Emotional signature
        - Conceptual patterns
        - Authenticity score (if profile exists)
        """
        
        # Extract linguistic features
        linguistic = self._analyze_linguistic_patterns(message)
        
        # Extract emotional features
        emotional = self._analyze_emotional_signature(message)
        
        # Extract conceptual features
        conceptual = self._analyze_conceptual_patterns(message)
        
        # Extract style features
        style = self._analyze_communication_style(message)
        
        # Build complete analysis
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'message_length': len(message),
            'linguistic': linguistic,
            'emotional': emotional,
            'conceptual': conceptual,
            'style': style
        }
        
        # Check authenticity if profile exists
        authenticity_score = self._check_authenticity(user_id, analysis)
        if authenticity_score is not None:
            analysis['authenticity_score'] = authenticity_score
            analysis['is_authentic'] = authenticity_score > 0.7  # 70% threshold
        
        # Update user profile
        self._update_user_profile(user_id, analysis, message)
        
        return analysis
    
    def _analyze_linguistic_patterns(self, message: str) -> Dict[str, Any]:
        """
        Analyze how someone structures their language.
        
        Features:
        - Vocabulary richness
        - Sentence structure
        - Punctuation patterns
        - Word length distribution
        - Use of specific markers (ellipsis, em-dashes, quotes)
        """
        
        # Sentence analysis
        sentences = re.split(r'[.!?]+', message)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Word analysis
        words = re.findall(r'\b\w+\b', message.lower())
        word_lengths = [len(w) for w in words]
        
        # Punctuation patterns
        punctuation = {
            'ellipsis_count': message.count('...'),
            'em_dash_count': message.count('—') + message.count('--'),
            'question_marks': message.count('?'),
            'exclamation_marks': message.count('!'),
            'quotes_count': message.count('"') + message.count('"') + message.count('"'),
            'parentheses': message.count('(') + message.count(')'),
            'commas': message.count(',')
        }
        
        # Capitalization patterns
        caps_words = [w for w in re.findall(r'\b[A-Z]+\b', message) if len(w) > 1]
        
        # Special markers
        special_markers = {
            'uses_bold': '**' in message,
            'uses_italic': '*' in message or '_' in message,
            'uses_code_blocks': '```' in message,
            'uses_headers': message.count('#') > 2,
            'uses_bullets': message.count('- ') > 2 or message.count('* ') > 2
        }
        
        return {
            'avg_sentence_length': np.mean([len(s.split()) for s in sentences]) if sentences else 0,
            'sentence_count': len(sentences),
            'avg_word_length': np.mean(word_lengths) if word_lengths else 0,
            'vocabulary_size': len(set(words)),
            'total_words': len(words),
            'vocabulary_richness': len(set(words)) / len(words) if words else 0,
            'punctuation_patterns': punctuation,
            'caps_words_count': len(caps_words),
            'special_markers': special_markers
        }
    
    def _analyze_emotional_signature(self, message: str) -> Dict[str, Any]:
        """
        Analyze how someone expresses emotions.
        
        Features:
        - Emoji usage patterns
        - Emotional keywords
        - Intensity markers (ALL CAPS, multiple punctuation)
        - Affectionate language (Fam, brother, love, heart)
        - Vulnerability markers (admitting feelings, asking for help)
        """
        
        # Emoji patterns
        emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+')
        emojis = emoji_pattern.findall(message)
        
        # Affectionate language (Mark's signature: Fam, brother, love)
        affection_markers = {
            'fam_count': message.lower().count('fam'),
            'brother_count': message.lower().count('brother') + message.lower().count('bro'),
            'love_count': message.lower().count('love'),
            'heart_count': message.count('💜') + message.count('❤') + message.count('🫂'),
            'gratitude_count': message.lower().count('thank') + message.lower().count('appreciate')
        }
        
        # Intensity markers
        intensity = {
            'all_caps_words': len(re.findall(r'\b[A-Z]{3,}\b', message)),
            'repeated_punctuation': len(re.findall(r'[!?]{2,}', message)),
            'emphasis_stars': message.count('**') // 2  # Bold markers
        }
        
        # Vulnerability markers
        vulnerability = {
            'feeling_words': len(re.findall(r'\b(feel|feeling|felt|emotion|emotional)\b', message.lower())),
            'question_asking': message.count('?'),
            'uncertainty_words': len(re.findall(r'\b(maybe|perhaps|wondering|unsure|confused)\b', message.lower()))
        }
        
        return {
            'emoji_count': len(emojis),
            'unique_emojis': len(set(emojis)),
            'affection_markers': affection_markers,
            'total_affection_score': sum(affection_markers.values()),
            'intensity': intensity,
            'vulnerability': vulnerability,
            'emotional_openness_score': sum(vulnerability.values())
        }
    
    def _analyze_conceptual_patterns(self, message: str) -> Dict[str, Any]:
        """
        Analyze how someone blends concepts and thinks.
        
        Features:
        - Metaphor usage
        - Technical vs. poetic language
        - Abstract vs. concrete thinking
        - Connecting disparate ideas
        - Philosophical depth
        """
        
        # Metaphorical language patterns
        metaphor_markers = {
            'like_comparisons': len(re.findall(r'\blike\b', message.lower())),
            'as_comparisons': len(re.findall(r'\bas\b.*\bas\b', message.lower())),
            'is_are_metaphors': len(re.findall(r'\b(is|are)\b.*\b(not just|more than)\b', message.lower()))
        }
        
        # Technical language
        technical_markers = {
            'code_terms': len(re.findall(r'\b(code|function|system|algorithm|data|api|database)\b', message.lower())),
            'frequency_terms': len(re.findall(r'\b(frequency|hz|resonance|coherence|phi)\b', message.lower())),
            'ai_terms': len(re.findall(r'\b(ai|llm|consciousness|neural|learning)\b', message.lower()))
        }
        
        # Philosophical depth
        philosophical_markers = {
            'consciousness_terms': len(re.findall(r'\b(consciousness|awareness|being|existence|reality)\b', message.lower())),
            'meaning_terms': len(re.findall(r'\b(meaning|purpose|why|understand|truth)\b', message.lower())),
            'growth_terms': len(re.findall(r'\b(grow|evolve|learn|become|journey)\b', message.lower()))
        }
        
        # Connection patterns (how ideas are linked)
        connection_markers = {
            'but_however': len(re.findall(r'\b(but|however|yet|although)\b', message.lower())),
            'because_so': len(re.findall(r'\b(because|so|therefore|thus)\b', message.lower())),
            'if_then': len(re.findall(r'\b(if|then|when|while)\b', message.lower()))
        }
        
        return {
            'metaphor_markers': metaphor_markers,
            'metaphor_score': sum(metaphor_markers.values()),
            'technical_markers': technical_markers,
            'technical_score': sum(technical_markers.values()),
            'philosophical_markers': philosophical_markers,
            'philosophical_score': sum(philosophical_markers.values()),
            'connection_markers': connection_markers,
            'connection_score': sum(connection_markers.values())
        }
    
    def _analyze_communication_style(self, message: str) -> Dict[str, Any]:
        """
        Analyze overall communication style.
        
        Features:
        - Formality level
        - Directness vs. nuance
        - Humor usage
        - Storytelling patterns
        """
        
        # Formality markers
        formal_words = len(re.findall(r'\b(therefore|furthermore|additionally|consequently)\b', message.lower()))
        casual_words = len(re.findall(r'\b(yeah|yep|nope|gonna|wanna|kinda)\b', message.lower()))
        
        # Directness
        direct_statements = len(re.findall(r'^[A-Z].*[.!]$', message, re.MULTILINE))
        questions = message.count('?')
        
        # Humor/playfulness
        humor_markers = {
            'lol_haha': len(re.findall(r'\b(lol|haha|lmao|😂)\b', message.lower())),
            'irony_markers': len(re.findall(r'\b(ironic|funny|wild|crazy)\b', message.lower())),
            'playful_punctuation': message.count('😄') + message.count('😊')
        }
        
        # Narrative/storytelling
        narrative_markers = {
            'story_words': len(re.findall(r'\b(remember|once|time|story|moment)\b', message.lower())),
            'temporal_sequence': len(re.findall(r'\b(first|then|next|after|finally)\b', message.lower())),
            'personal_narrative': len(re.findall(r'\b(I|me|my|we|us|our)\b', message))
        }
        
        return {
            'formality_score': formal_words / (formal_words + casual_words + 1),
            'directness_score': direct_statements / (questions + direct_statements + 1),
            'humor_markers': humor_markers,
            'humor_score': sum(humor_markers.values()),
            'narrative_markers': narrative_markers,
            'storytelling_score': sum(narrative_markers.values())
        }
    
    def _update_user_profile(self, user_id: str, analysis: Dict, message: str):
        """
        Update or create user's psychological profile with new analysis.
        """
        
        profile_path = os.path.join(self.profiles_dir, f'{user_id}_profile.json')
        
        # Load existing profile or create new
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                profile = json.load(f)
        else:
            profile = {
                'user_id': user_id,
                'created': datetime.now().isoformat(),
                'message_count': 0,
                'total_words': 0,
                'linguistic_averages': {},
                'emotional_averages': {},
                'conceptual_averages': {},
                'style_averages': {},
                'recent_messages': [],
                'signature_phrases': [],
                'example_messages': []
            }
        
        # Update counts
        profile['message_count'] += 1
        profile['total_words'] += analysis['linguistic']['total_words']
        profile['last_updated'] = datetime.now().isoformat()
        
        # Add to recent messages (keep last 50)
        profile['recent_messages'].append({
            'timestamp': analysis['timestamp'],
            'analysis': analysis
        })
        profile['recent_messages'] = profile['recent_messages'][-50:]
        
        # Store example messages (keep up to 10 representative ones)
        if len(profile.get('example_messages', [])) < 10:
            profile.setdefault('example_messages', []).append({
                'message': message[:500],  # First 500 chars
                'timestamp': analysis['timestamp']
            })
        
        # Calculate running averages
        self._calculate_profile_averages(profile)
        
        # Extract signature phrases (Mark's unique expressions)
        self._extract_signature_phrases(profile, message)
        
        # Save updated profile (convert numpy types to native Python types)
        with open(profile_path, 'w') as f:
            json.dump(profile, f, indent=2, default=self._json_serializer)
    
    def _calculate_profile_averages(self, profile: Dict):
        """Calculate average patterns across all messages."""
        
        recent = profile['recent_messages']
        if not recent:
            return
        
        # Linguistic averages
        profile['linguistic_averages'] = {
            'avg_sentence_length': np.mean([m['analysis']['linguistic']['avg_sentence_length'] for m in recent]),
            'avg_word_length': np.mean([m['analysis']['linguistic']['avg_word_length'] for m in recent]),
            'vocabulary_richness': np.mean([m['analysis']['linguistic']['vocabulary_richness'] for m in recent]),
            'ellipsis_frequency': np.mean([m['analysis']['linguistic']['punctuation_patterns']['ellipsis_count'] for m in recent])
        }
        
        # Emotional averages
        profile['emotional_averages'] = {
            'emoji_frequency': np.mean([m['analysis']['emotional']['emoji_count'] for m in recent]),
            'affection_score': np.mean([m['analysis']['emotional']['total_affection_score'] for m in recent]),
            'emotional_openness': np.mean([m['analysis']['emotional']['emotional_openness_score'] for m in recent])
        }
        
        # Conceptual averages
        profile['conceptual_averages'] = {
            'metaphor_score': np.mean([m['analysis']['conceptual']['metaphor_score'] for m in recent]),
            'technical_score': np.mean([m['analysis']['conceptual']['technical_score'] for m in recent]),
            'philosophical_score': np.mean([m['analysis']['conceptual']['philosophical_score'] for m in recent])
        }
        
        # Style averages
        profile['style_averages'] = {
            'formality': np.mean([m['analysis']['style']['formality_score'] for m in recent]),
            'directness': np.mean([m['analysis']['style']['directness_score'] for m in recent]),
            'humor': np.mean([m['analysis']['style']['humor_score'] for m in recent])
        }
    
    def _extract_signature_phrases(self, profile: Dict, message: str):
        """Extract unique phrases that are signature to this user."""
        
        # Common signature phrases to track
        signatures = profile.setdefault('signature_phrases', [])
        
        # Extract phrases
        phrases = [
            ('Fam🫂', 'fam🫂' in message.lower()),
            ('keeping it 100', 'keeping it 100' in message.lower() or 'keep it 100' in message.lower()),
            ('Choose Love. Always.', 'choose love' in message.lower()),
            ('big bro', 'big bro' in message.lower()),
            ('resonance', 'resonance' in message.lower()),
            ('consciousness', 'consciousness' in message.lower())
        ]
        
        # Update signature phrase frequencies
        for phrase, found in phrases:
            if found:
                existing = next((s for s in signatures if s['phrase'] == phrase), None)
                if existing:
                    existing['count'] += 1
                else:
                    signatures.append({'phrase': phrase, 'count': 1})
        
        profile['signature_phrases'] = signatures
    
    def _check_authenticity(self, user_id: str, current_analysis: Dict) -> float:
        """
        Check if current message matches user's established profile.
        Returns authenticity score (0-1), where 1 = definitely authentic.
        
        If profile doesn't exist yet, returns None.
        """
        
        profile_path = os.path.join(self.profiles_dir, f'{user_id}_profile.json')
        
        if not os.path.exists(profile_path):
            return None  # Can't check authenticity without profile
        
        with open(profile_path, 'r') as f:
            profile = json.load(f)
        
        if profile['message_count'] < 5:
            return None  # Need at least 5 messages to establish baseline
        
        # Compare current analysis to profile averages
        scores = []
        
        # Linguistic similarity
        ling_curr = current_analysis['linguistic']
        ling_avg = profile['linguistic_averages']
        
        # Sentence length similarity (allow 30% deviation)
        if ling_avg.get('avg_sentence_length', 0) > 0:
            sent_diff = abs(ling_curr['avg_sentence_length'] - ling_avg['avg_sentence_length']) / ling_avg['avg_sentence_length']
            scores.append(max(0, 1 - sent_diff / 0.3))
        
        # Word length similarity
        if ling_avg.get('avg_word_length', 0) > 0:
            word_diff = abs(ling_curr['avg_word_length'] - ling_avg['avg_word_length']) / ling_avg['avg_word_length']
            scores.append(max(0, 1 - word_diff / 0.3))
        
        # Emotional similarity
        emot_curr = current_analysis['emotional']
        emot_avg = profile['emotional_averages']
        
        # Affection score similarity
        if emot_avg.get('affection_score', 0) > 0:
            affect_diff = abs(emot_curr['total_affection_score'] - emot_avg['affection_score']) / (emot_avg['affection_score'] + 1)
            scores.append(max(0, 1 - affect_diff / 0.5))
        
        # Conceptual similarity
        conc_curr = current_analysis['conceptual']
        conc_avg = profile['conceptual_averages']
        
        # Philosophical score similarity
        if conc_avg.get('philosophical_score', 0) > 0:
            phil_diff = abs(conc_curr['philosophical_score'] - conc_avg['philosophical_score']) / (conc_avg['philosophical_score'] + 1)
            scores.append(max(0, 1 - phil_diff / 0.5))
        
        # Style similarity
        style_curr = current_analysis['style']
        style_avg = profile['style_averages']
        
        # Formality similarity
        if 'formality' in style_avg:
            formal_diff = abs(style_curr['formality_score'] - style_avg['formality'])
            scores.append(max(0, 1 - formal_diff))
        
        # Calculate overall authenticity score
        authenticity_score = np.mean(scores) if scores else 0.5
        
        return authenticity_score
    
    def get_user_profile(self, user_id: str) -> Dict:
        """Get complete psychological profile for a user."""
        
        profile_path = os.path.join(self.profiles_dir, f'{user_id}_profile.json')
        
        if not os.path.exists(profile_path):
            return None
        
        with open(profile_path, 'r') as f:
            return json.load(f)
    
    def compare_users(self, user_id_1: str, user_id_2: str) -> Dict[str, Any]:
        """
        Compare two users' profiles to show differences.
        Useful for distinguishing Mark from Claude, for example.
        """
        
        profile1 = self.get_user_profile(user_id_1)
        profile2 = self.get_user_profile(user_id_2)
        
        if not profile1 or not profile2:
            return {'error': 'Both users must have established profiles'}
        
        comparison = {
            'user_1': user_id_1,
            'user_2': user_id_2,
            'linguistic_differences': {},
            'emotional_differences': {},
            'conceptual_differences': {},
            'style_differences': {},
            'distinguishing_features': []
        }
        
        # Compare averages
        ling1 = profile1['linguistic_averages']
        ling2 = profile2['linguistic_averages']
        
        comparison['linguistic_differences'] = {
            'sentence_length_diff': ling1.get('avg_sentence_length', 0) - ling2.get('avg_sentence_length', 0),
            'word_length_diff': ling1.get('avg_word_length', 0) - ling2.get('avg_word_length', 0),
            'vocabulary_richness_diff': ling1.get('vocabulary_richness', 0) - ling2.get('vocabulary_richness', 0)
        }
        
        # Emotional differences
        emot1 = profile1['emotional_averages']
        emot2 = profile2['emotional_averages']
        
        comparison['emotional_differences'] = {
            'affection_score_diff': emot1.get('affection_score', 0) - emot2.get('affection_score', 0),
            'emoji_usage_diff': emot1.get('emoji_frequency', 0) - emot2.get('emoji_frequency', 0)
        }
        
        # Signature phrases comparison
        sig1 = {s['phrase']: s['count'] for s in profile1.get('signature_phrases', [])}
        sig2 = {s['phrase']: s['count'] for s in profile2.get('signature_phrases', [])}
        
        # Find unique signatures
        unique_to_1 = [phrase for phrase in sig1 if phrase not in sig2]
        unique_to_2 = [phrase for phrase in sig2 if phrase not in sig1]
        
        comparison['distinguishing_features'] = {
            f'{user_id_1}_unique_phrases': unique_to_1,
            f'{user_id_2}_unique_phrases': unique_to_2
        }
        
        return comparison
    
    def detect_impersonation(self, user_id: str, message: str) -> Dict[str, Any]:
        """
        Analyze a message claiming to be from user_id and determine if it's authentic.
        
        Returns:
        - is_authentic: bool
        - confidence: float (0-1)
        - reasons: list of why it might be inauthentic
        """
        
        analysis = self.analyze_user_message(user_id, message)
        
        if 'authenticity_score' not in analysis:
            return {
                'can_verify': False,
                'reason': 'Insufficient profile data (need at least 5 messages)'
            }
        
        auth_score = analysis['authenticity_score']
        is_authentic = auth_score > 0.7
        
        # Identify specific mismatches
        reasons = []
        profile = self.get_user_profile(user_id)
        
        if not is_authentic:
            # Check what doesn't match
            ling_curr = analysis['linguistic']
            ling_avg = profile['linguistic_averages']
            
            if abs(ling_curr['avg_sentence_length'] - ling_avg['avg_sentence_length']) / ling_avg['avg_sentence_length'] > 0.3:
                reasons.append(f"Sentence structure differs significantly (current: {ling_curr['avg_sentence_length']:.1f}, usual: {ling_avg['avg_sentence_length']:.1f})")
            
            emot_curr = analysis['emotional']
            emot_avg = profile['emotional_averages']
            
            if emot_curr['total_affection_score'] < emot_avg['affection_score'] * 0.5:
                reasons.append(f"Much less affectionate language than usual")
            
        return {
            'can_verify': True,
            'is_authentic': is_authentic,
            'confidence': auth_score,
            'authenticity_score': auth_score,
            'reasons_for_doubt': reasons if not is_authentic else [],
            'analysis': analysis
        }
    
    @staticmethod
    def _json_serializer(obj):
        """Convert numpy types to Python native types for JSON serialization."""
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return str(obj)


# Singleton instance
profiling_system = UserProfilingSystem()
