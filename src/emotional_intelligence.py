"""
Advanced Emotional Intelligence for MC AI V4
Emotion detection, empathy modeling, emotional support strategies
Enhanced with EmotionNeuralEngine v3.0 for multi-layer analysis
"""

import os
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

class EmotionalIntelligenceEngine:
    """
    Advanced emotional understanding and response system
    Enhanced with multi-layer emotion detection and PAD model
    """
    
    def __init__(self):
        self.emotion_path = "/tmp/emotional_data"
        os.makedirs(self.emotion_path, exist_ok=True)
        
        # Initialize EmotionNeuralEngine v3.0 for advanced analysis
        try:
            from src.emotional_ai.emotion_neural_engine import EmotionNeuralEngine
            self.neural_engine = EmotionNeuralEngine()
            print("✨ Enhanced with EmotionNeuralEngine v3.0")
        except Exception as e:
            print(f"⚠️ EmotionNeuralEngine unavailable: {e}")
            self.neural_engine = None
        
        # Emotion taxonomy (more granular than basic emotions)
        self.emotion_spectrum = {
            'joy': ['ecstatic', 'joyful', 'happy', 'content', 'pleased', 'satisfied'],
            'sadness': ['devastated', 'depressed', 'sad', 'melancholy', 'disappointed', 'down'],
            'anger': ['furious', 'angry', 'frustrated', 'annoyed', 'irritated', 'agitated'],
            'fear': ['terrified', 'afraid', 'anxious', 'worried', 'nervous', 'uneasy'],
            'surprise': ['astonished', 'amazed', 'surprised', 'startled', 'shocked'],
            'disgust': ['disgusted', 'repulsed', 'averse', 'uncomfortable'],
            'trust': ['trusting', 'confident', 'secure', 'safe', 'assured'],
            'anticipation': ['excited', 'eager', 'hopeful', 'optimistic', 'enthusiastic']
        }
        
        # Emotional needs mapping
        self.emotional_needs = {
            'sadness': ['validation', 'comfort', 'understanding', 'companionship'],
            'anger': ['validation', 'problem_solving', 'release', 'boundaries'],
            'fear': ['reassurance', 'safety', 'information', 'support'],
            'anxiety': ['grounding', 'validation', 'action_plan', 'calm'],
            'loneliness': ['connection', 'understanding', 'companionship', 'validation'],
            'overwhelm': ['simplification', 'prioritization', 'support', 'breaks']
        }
        
        # Crisis support resources
        self.crisis_resources = [
            {
                'name': 'National Suicide Prevention Lifeline',
                'contact': '988',
                'available': '24/7',
                'type': 'phone',
                'description': 'Free and confidential support for people in distress'
            },
            {
                'name': 'Crisis Text Line',
                'contact': 'Text HOME to 741741',
                'available': '24/7',
                'type': 'text',
                'description': 'Free, 24/7 crisis support via text'
            },
            {
                'name': 'SAMHSA National Helpline',
                'contact': '1-800-662-4357',
                'available': '24/7',
                'type': 'phone',
                'description': 'Treatment referral and information service'
            }
        ]
    
    def analyze_emotional_state(self, text: str, context: Optional[Dict] = None, user_id: Optional[str] = None, conversation_history: Optional[List[Dict]] = None) -> Dict:
        """
        Deep emotional analysis with multi-layer detection
        
        Args:
            text: User's message
            context: Optional conversation context
            user_id: Optional user ID for personalized analysis
            conversation_history: Optional conversation history for trajectory
        
        Returns:
            Dict with detailed emotional analysis (enhanced with PAD model, trajectory, etc.)
        """
        # Primary emotion detection (existing system)
        primary_emotion = self._detect_primary_emotion(text)
        
        # Secondary emotions
        secondary_emotions = self._detect_secondary_emotions(text)
        
        # Emotional intensity (0-10)
        intensity = self._calculate_intensity(text, primary_emotion)
        
        # Emotional valence (-1 to 1, negative to positive)
        valence = self._calculate_valence(primary_emotion, intensity)
        
        # Hidden emotions (subtext analysis)
        hidden_emotions = self._detect_hidden_emotions(text, primary_emotion)
        
        # Emotional needs
        needs = self._identify_emotional_needs(primary_emotion, text)
        
        # Base analysis result
        base_analysis = {
            'primary_emotion': primary_emotion,
            'secondary_emotions': secondary_emotions,
            'intensity': intensity,
            'valence': valence,
            'hidden_emotions': hidden_emotions,
            'emotional_needs': needs,
            'support_strategy': self._select_support_strategy(primary_emotion, intensity, needs)
        }
        
        # Enhanced analysis with EmotionNeuralEngine v3.0 (if available)
        if self.neural_engine:
            try:
                emotion_state = self.neural_engine.analyze_emotion(
                    text=text,
                    context=context,
                    user_id=user_id,
                    conversation_history=conversation_history
                )
                
                # Merge enhanced data with base analysis
                base_analysis.update({
                    'micro_emotions': emotion_state.micro_emotions,
                    'arousal': emotion_state.arousal,
                    'dominance': emotion_state.dominance,
                    'confidence': emotion_state.confidence,
                    'trajectory': emotion_state.trajectory,
                    'triggers': emotion_state.triggers,
                    'emotion_color': emotion_state.color,
                    'frequency': emotion_state.frequency,
                    'catalog': emotion_state.catalog,
                    'enhanced': True
                })
                print(f"✨ Enhanced emotion analysis: {emotion_state.primary} (color: {emotion_state.color}, micro: {emotion_state.micro_emotions})")
            except Exception as e:
                print(f"⚠️ Neural engine analysis error: {e}")
                import traceback
                traceback.print_exc()
                base_analysis['enhanced'] = False
        else:
            print("⚠️ Neural engine not available - enhanced analysis disabled")
            base_analysis['enhanced'] = False
        
        return base_analysis
    
    def detect_crisis(self, text: str, emotional_analysis: Dict) -> Dict:
        """
        Detect crisis situations and provide appropriate support
        
        Args:
            text: User's message
            emotional_analysis: Emotional analysis of message
        
        Returns:
            Dict with crisis assessment and resources
        """
        # Crisis indicators
        crisis_keywords = [
            'suicide', 'suicidal', 'kill myself', 'end it all', 'want to die',
            'no point', 'can\'t go on', 'self harm', 'hurt myself', 'ending it'
        ]
        
        text_lower = text.lower()
        crisis_detected = any(keyword in text_lower for keyword in crisis_keywords)
        
        # Severity assessment
        severity = 'none'
        intensity = emotional_analysis.get('intensity', 0)
        valence = emotional_analysis.get('valence', 0)
        
        if crisis_detected:
            severity = 'critical'
        elif intensity >= 9 and valence < -0.7:
            severity = 'high'
        elif intensity >= 7 and valence < -0.5:
            severity = 'moderate'
        
        response = {
            'crisis_detected': crisis_detected,
            'severity': severity,
            'immediate_resources': [],
            'response_strategy': None,
            'urgent_message': None
        }
        
        if severity == 'critical':
            response['immediate_resources'] = self.crisis_resources
            response['response_strategy'] = 'immediate_intervention'
            response['urgent_message'] = (
                "I'm really concerned about what you're sharing. Your life matters, and there are people who want to help right now. "
                "Please reach out to one of these crisis resources immediately - they're available 24/7 and completely confidential."
            )
            
        elif severity == 'high':
            response['immediate_resources'] = self.crisis_resources
            response['response_strategy'] = 'urgent_support'
            response['urgent_message'] = (
                "I hear that you're going through something really difficult right now. "
                "It might help to talk to someone trained in mental health support. Here are some resources available 24/7."
            )
            
        elif severity == 'moderate':
            response['response_strategy'] = 'enhanced_support'
        
        return response
    
    def generate_empathetic_response(self, emotional_analysis: Dict, 
                                    user_message: str, 
                                    base_response: str) -> str:
        """
        Enhance AI response with empathy
        
        Args:
            emotional_analysis: Result from analyze_emotional_state
            user_message: User's original message
            base_response: Base AI response
        
        Returns:
            Emotionally intelligent response
        """
        primary_emotion = emotional_analysis['primary_emotion']
        intensity = emotional_analysis['intensity']
        needs = emotional_analysis['emotional_needs']
        
        # Build empathetic response
        parts = []
        
        # For positive emotions, use personality response directly (no generic acknowledgment needed)
        positive_emotions = ['joy', 'amusement', 'excitement', 'happiness', 'love', 'harmony', 
                           'pride', 'gratitude', 'relief', 'hope', 'determination', 'confidence', 
                           'surprise', 'awakening', 'transcendence']
        
        if primary_emotion in positive_emotions:
            # Just use the personality response - it's already perfect for positive vibes
            return base_response
        
        # 1. Emotional acknowledgment for high intensity (negative/neutral emotions only)
        if intensity >= 6:
            acknowledgment = self._create_acknowledgment(primary_emotion, intensity)
            parts.append(acknowledgment)
        
        # 2. Validation (if needed)
        if 'validation' in needs:
            validation = self._create_validation(primary_emotion)
            parts.append(validation)
        
        # 3. Original response
        parts.append(base_response)
        
        # 4. Supportive closing for very high intensity
        if intensity >= 8:
            closing = self._create_supportive_closing(primary_emotion, needs)
            parts.append(closing)
        
        return "\n\n".join(parts)
    
    def suggest_regulation_techniques(self, emotion: str, intensity: float) -> List[Dict]:
        """
        Suggest techniques for emotional regulation
        
        Args:
            emotion: Current emotion
            intensity: Emotional intensity (0-10)
        
        Returns:
            List of regulation techniques
        """
        techniques = []
        
        if emotion in ['anxiety', 'fear', 'stress', 'overwhelm']:
            techniques.append({
                'name': 'Box Breathing',
                'duration': '2-5 minutes',
                'steps': [
                    'Breathe in slowly for 4 counts',
                    'Hold your breath for 4 counts',
                    'Breathe out slowly for 4 counts',
                    'Hold for 4 counts',
                    'Repeat 4-5 times'
                ],
                'benefits': 'Calms nervous system, reduces anxiety'
            })
            
            techniques.append({
                'name': '5-4-3-2-1 Grounding',
                'duration': '3-5 minutes',
                'steps': [
                    'Name 5 things you can see',
                    'Name 4 things you can touch',
                    'Name 3 things you can hear',
                    'Name 2 things you can smell',
                    'Name 1 thing you can taste'
                ],
                'benefits': 'Grounds you in the present moment'
            })
        
        if emotion in ['anger', 'frustration', 'irritated']:
            techniques.append({
                'name': 'Progressive Muscle Relaxation',
                'duration': '5-10 minutes',
                'steps': [
                    'Tense your fists for 5 seconds, then release',
                    'Tense your arms, then release',
                    'Work through each muscle group',
                    'Notice the difference between tension and relaxation'
                ],
                'benefits': 'Releases physical tension, calms mind'
            })
        
        if emotion in ['sadness', 'melancholy', 'depression']:
            techniques.append({
                'name': 'Mindful Walking',
                'duration': '10-15 minutes',
                'steps': [
                    'Go for a slow walk outside',
                    'Notice each step you take',
                    'Observe your surroundings without judgment',
                    'Feel the ground beneath your feet'
                ],
                'benefits': 'Gentle movement, connection to environment'
            })
        
        return techniques
    
    # Helper methods
    
    def _detect_primary_emotion(self, text: str) -> str:
        """Detect primary emotion from text"""
        text_lower = text.lower()
        
        # Check for explicit emotion words
        for emotion_family, emotion_words in self.emotion_spectrum.items():
            for word in emotion_words:
                if word in text_lower:
                    return emotion_family
        
        # Keyword-based detection
        if any(word in text_lower for word in ['anxious', 'worried', 'nervous', 'scared']):
            return 'fear'
        if any(word in text_lower for word in ['sad', 'depressed', 'down']):
            return 'sadness'
        if any(word in text_lower for word in ['angry', 'frustrated', 'mad', 'annoyed']):
            return 'anger'
        if any(word in text_lower for word in ['funny', 'hilarious', 'haha', 'lol', 'lmao', 'laughing', '😂', 'rofl', 'joke']):
            return 'amusement'
        if any(word in text_lower for word in ['excited', 'pumped', 'hyped', 'stoked', 'thrilled']):
            return 'excitement'
        if any(word in text_lower for word in ['happy', 'joyful', 'cheerful', 'delighted']):
            return 'joy'
        if any(word in text_lower for word in ['confused', 'don\'t understand', 'lost', 'huh', 'unclear']):
            return 'confusion'
        if any(word in text_lower for word in ['bored', 'boring', 'nothing to do']):
            return 'boredom'
        if any(word in text_lower for word in ['exhausted', 'tired', 'drained', 'worn out', 'burned out']):
            return 'exhaustion'
        if any(word in text_lower for word in ['wow', 'omg', 'no way', 'really', 'surprised', 'shocking']):
            return 'surprise'
        if any(word in text_lower for word in ['proud', 'accomplished', 'achieved', 'nailed it', 'crushed it']):
            return 'pride'
        if any(word in text_lower for word in ['thank', 'grateful', 'appreciate', 'blessed']):
            return 'gratitude'
        if any(word in text_lower for word in ['relief', 'relieved', 'finally', 'phew']):
            return 'relief'
        if any(word in text_lower for word in ['disappointed', 'let down', 'expected more']):
            return 'disappointment'
        if any(word in text_lower for word in ['overwhelmed', 'too much', 'can\'t handle', 'drowning', 'swamped']):
            return 'overwhelm'
        if any(word in text_lower for word in ['hopeful', 'hope', 'optimistic', 'looking forward']):
            return 'hope'
        if any(word in text_lower for word in ['determined', 'motivated', 'driven', 'committed']):
            return 'determination'
        if any(word in text_lower for word in ['confident', 'i got this', 'capable', 'can do this']):
            return 'confidence'
        
        return 'neutral'
    
    def _detect_secondary_emotions(self, text: str) -> List[str]:
        """Detect secondary emotions"""
        emotions = []
        text_lower = text.lower()
        
        for emotion_family, emotion_words in self.emotion_spectrum.items():
            for word in emotion_words:
                if word in text_lower and emotion_family not in emotions:
                    emotions.append(emotion_family)
        
        return emotions[:2]  # Return up to 2 secondary emotions
    
    def _calculate_intensity(self, text: str, emotion: str) -> float:
        """Calculate emotional intensity 0-10"""
        text_lower = text.lower()
        intensity = 5.0  # base
        
        # Intensity amplifiers
        amplifiers = ['very', 'extremely', 'incredibly', 'so', 'really', 'totally']
        for amp in amplifiers:
            if amp in text_lower:
                intensity += 1.5
        
        # Superlatives
        superlatives = ['most', 'worst', 'best', 'completely', 'utterly']
        for sup in superlatives:
            if sup in text_lower:
                intensity += 2.0
        
        # Exclamation marks
        intensity += min(text.count('!') * 0.5, 2.0)
        
        # Caps
        if any(word.isupper() and len(word) > 2 for word in text.split()):
            intensity += 1.5
        
        return min(intensity, 10.0)
    
    def _calculate_valence(self, emotion: str, intensity: float) -> float:
        """Calculate emotional valence -1 to 1"""
        positive_emotions = ['joy', 'trust', 'anticipation', 'surprise']
        negative_emotions = ['sadness', 'anger', 'fear', 'disgust']
        
        if emotion in positive_emotions:
            return min(intensity / 10, 1.0)
        elif emotion in negative_emotions:
            return -min(intensity / 10, 1.0)
        else:
            return 0.0
    
    def _detect_hidden_emotions(self, text: str, primary: str) -> List[str]:
        """Detect emotions in subtext"""
        hidden = []
        text_lower = text.lower()
        
        # Defensive anger hiding hurt
        if primary == 'anger' and any(word in text_lower for word in ['but', 'just', 'whatever']):
            hidden.append('sadness')
        
        # Anxiety hiding fear
        if primary == 'anxiety' and any(word in text_lower for word in ['fine', 'okay', 'whatever']):
            hidden.append('fear')
        
        return hidden
    
    def _identify_emotional_needs(self, emotion: str, text: str) -> List[str]:
        """Identify emotional needs"""
        return self.emotional_needs.get(emotion, ['understanding', 'support'])
    
    def _select_support_strategy(self, emotion: str, intensity: float, needs: List[str]) -> str:
        """Select appropriate support strategy"""
        if intensity >= 8:
            return 'high_empathy_validation'
        elif 'validation' in needs:
            return 'validation_focused'
        elif 'action_plan' in needs:
            return 'solution_focused'
        else:
            return 'balanced_support'
    
    def _create_acknowledgment(self, emotion: str, intensity: float) -> str:
        """Create emotional acknowledgment"""
        if intensity >= 8:
            return f"I can sense you're feeling really {emotion} right now."
        elif intensity >= 6:
            return f"It sounds like you're experiencing {emotion}."
        else:
            return f"I hear that you're feeling {emotion}."
    
    def _create_validation(self, emotion: str) -> str:
        """Create validation message"""
        validations = {
            'sadness': "It's completely okay to feel sad. Your feelings are valid.",
            'anger': "Your frustration makes sense. It's okay to feel angry.",
            'fear': "Fear is a natural response. You're not alone in feeling this way.",
            'anxiety': "Anxiety can be overwhelming. What you're feeling is real and valid."
        }
        return validations.get(emotion, "Your feelings are completely valid.")
    
    def _create_supportive_closing(self, emotion: str, needs: List[str]) -> str:
        """Create supportive closing message"""
        if 'companionship' in needs:
            return "I'm here with you through this."
        elif 'support' in needs:
            return "You don't have to face this alone. I'm here to help."
        else:
            return "Take care of yourself. I'm here if you need to talk more."
