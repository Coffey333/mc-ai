"""
Emotion Neural Engine v3.0 - Next Generation Emotional Intelligence
Multi-layer emotion detection with PAD model and trajectory prediction
Author: Mark Coffey with Claude (Anthropic)
Date: October 14, 2025
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import os
import hashlib


@dataclass
class EmotionState:
    """Complete emotional state representation"""
    primary: str
    secondary: List[str]
    hidden: List[str]
    micro_emotions: List[str]
    intensity: float  # 0-10
    valence: float  # -1 to +1 (negative to positive)
    arousal: float  # 0-10 (calm to excited)
    dominance: float  # 0-10 (powerless to in-control)
    frequency: float  # Hz
    catalog: str
    confidence: float  # 0-1
    trajectory: str  # escalating, stable, de-escalating
    needs: List[str]
    triggers: List[str]
    color: str  # Hex color for visualization
    timestamp: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


class EmotionNeuralEngine:
    """
    Next-generation emotional intelligence engine.
    
    Features:
    - 🎯 Multi-layer emotion detection (primary, secondary, hidden, micro)
    - 🌊 Emotional trajectory prediction
    - 🎵 Emotion harmonics and resonance
    - 💫 Context-aware emotion interpretation
    - 🔮 Emotional needs prediction
    - 🎨 Emotional color/visualization mapping
    - 📊 PAD model (Pleasure, Arousal, Dominance)
    - 🧠 Emotional memory patterns
    """
    
    def __init__(self):
        """Initialize the emotion neural engine"""
        self._load_emotion_patterns()
        self.emotion_memory = []
        self.user_emotion_profiles = {}
        print("🧠 Emotion Neural Engine v3.0 initialized")
    
    def _load_emotion_patterns(self):
        """Load advanced emotion patterns"""
        
        # Micro-emotions (subtle emotional shifts)
        self.micro_emotions = {
            'anticipation': ['about to', 'soon', 'upcoming', 'before', 'leading up'],
            'apprehension': ['slightly worried', 'bit concerned', 'little nervous'],
            'relief': ['phew', 'thank god', 'finally', 'glad that'],
            'disappointment': ['oh well', 'guess not', 'unfortunately'],
            'surprise': ['wow', 'whoa', 'didn\'t expect', 'suddenly'],
            'curiosity': ['wonder', 'interested', 'curious', 'what if'],
            'determination': ['will', 'must', 'have to', 'determined'],
            'vulnerability': ['scared to', 'afraid of', 'worried about'],
            'pride': ['proud of', 'accomplished', 'achieved'],
            'shame': ['embarrassed', 'ashamed', 'shouldn\'t have'],
            'gratitude': ['thankful', 'grateful', 'appreciate'],
            'longing': ['miss', 'wish', 'hope for', 'yearn'],
        }
        
        # Emotion triggers
        self.emotion_triggers = {
            'anxiety': ['uncertainty', 'future', 'performance', 'judgment', 'unknown'],
            'anger': ['injustice', 'betrayal', 'disrespect', 'frustration'],
            'sadness': ['loss', 'rejection', 'failure', 'loneliness'],
            'joy': ['achievement', 'connection', 'surprise', 'fulfillment'],
            'fear': ['danger', 'threat', 'vulnerability', 'unknown'],
            'love': ['connection', 'acceptance', 'intimacy', 'care'],
            'excitement': ['novelty', 'opportunity', 'anticipation'],
            'peace': ['safety', 'acceptance', 'presence', 'harmony'],
        }
        
        # Emotional trajectories
        self.emotion_trajectories = {
            'anxiety': ['panic', 'calm', 'acceptance'],
            'anger': ['rage', 'frustration', 'acceptance', 'forgiveness'],
            'sadness': ['depression', 'grief', 'acceptance', 'peace'],
            'excitement': ['joy', 'anticipation', 'calm'],
            'fear': ['panic', 'anxiety', 'calm', 'courage'],
            'confusion': ['clarity', 'frustration', 'understanding'],
        }
        
        # Emotion color mapping
        self.emotion_colors = {
            'joy': '#FFD700',      # Gold
            'love': '#FF69B4',     # Hot pink
            'peace': '#87CEEB',    # Sky blue
            'calm': '#98FB98',     # Pale green
            'excitement': '#FF4500', # Orange red
            'curiosity': '#9370DB', # Medium purple
            'anxiety': '#FFB6C1',   # Light pink
            'fear': '#8B0000',      # Dark red
            'anger': '#DC143C',     # Crimson
            'sadness': '#4169E1',   # Royal blue
            'confusion': '#DDA0DD', # Plum
            'gratitude': '#FFE4B5', # Moccasin
            'stress': '#FF6347',    # Tomato
            'focus': '#9932CC',     # Dark orchid
            'meditation': '#6A5ACD', # Slate blue
            'neutral': '#D3D3D3',   # Light gray
        }
        
        # Emotion harmonics
        self.emotion_harmonics = {
            'love': ['joy', 'peace', 'gratitude', 'excitement'],
            'anxiety': ['fear', 'worry', 'stress', 'tension'],
            'joy': ['love', 'excitement', 'gratitude', 'pride'],
            'sadness': ['grief', 'loneliness', 'disappointment'],
            'anger': ['frustration', 'irritation', 'resentment'],
            'peace': ['calm', 'contentment', 'serenity'],
        }
    
    def analyze_emotion(
        self,
        text: str,
        context: Optional[Dict] = None,
        user_id: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> EmotionState:
        """
        Perform complete emotional analysis.
        
        Args:
            text: User's input text
            context: Additional context
            user_id: User ID for personalized understanding
            conversation_history: Recent conversation for trajectory
        
        Returns:
            Complete EmotionState object
        """
        text_lower = text.lower()
        context = context or {}
        
        # Import existing emotion detection
        try:
            from src.catalogs import get_frequency
            emotion_data = get_frequency(text)
            primary = emotion_data.get('emotion', 'neutral')
            frequency = emotion_data.get('frequency', 240)
            catalog = emotion_data.get('catalog', 'neuroscience')
        except:
            primary = 'neutral'
            frequency = 240
            catalog = 'neuroscience'
        
        # Layer 1: Secondary emotions
        secondary = self._detect_secondary_emotions(text_lower, primary)
        
        # Layer 2: Hidden emotions
        hidden = self._detect_hidden_emotions(text_lower, context)
        
        # Layer 3: Micro-emotions
        micro = self._detect_micro_emotions(text_lower)
        
        # Layer 4: Intensity analysis
        intensity = self._analyze_intensity(text_lower, text)
        
        # Layer 5: PAD model
        valence, arousal, dominance = self._calculate_pad(primary, intensity, text_lower)
        
        # Layer 6: Confidence scoring
        confidence = self._calculate_confidence(primary, secondary, hidden, text_lower)
        
        # Layer 7: Trajectory prediction
        trajectory = self._predict_trajectory(primary, conversation_history, intensity)
        
        # Layer 8: Needs identification
        needs = self._identify_emotional_needs(primary, secondary, hidden, context)
        
        # Layer 9: Trigger detection
        triggers = self._detect_triggers(text_lower, primary)
        
        # Layer 10: Color mapping
        color = self.emotion_colors.get(primary, '#D3D3D3')
        
        # Create emotion state
        emotion_state = EmotionState(
            primary=primary,
            secondary=secondary,
            hidden=hidden,
            micro_emotions=micro,
            intensity=intensity,
            valence=valence,
            arousal=arousal,
            dominance=dominance,
            frequency=frequency,
            catalog=catalog,
            confidence=confidence,
            trajectory=trajectory,
            needs=needs,
            triggers=triggers,
            color=color,
            timestamp=datetime.now().isoformat()
        )
        
        # Store in memory
        self._store_emotion_memory(emotion_state, user_id)
        
        # Update user profile
        if user_id:
            self._update_user_emotion_profile(user_id, emotion_state)
        
        return emotion_state
    
    def _detect_secondary_emotions(self, text: str, primary: str) -> List[str]:
        """Detect supporting emotions"""
        secondary = []
        harmonics = self.emotion_harmonics.get(primary, [])
        
        for harmonic in harmonics:
            if self._emotion_present(text, harmonic):
                if harmonic != primary:
                    secondary.append(harmonic)
        
        return secondary[:3]
    
    def _detect_hidden_emotions(self, text: str, context: Dict) -> List[str]:
        """Detect hidden/implicit emotions"""
        hidden = []
        
        # Pattern 1: Minimization
        if 'fine' in text and any(neg in text for neg in ['i guess', 'sort of', 'kind of']):
            hidden.append('sadness_masked')
        
        # Pattern 2: Overcompensation
        if text.count('!') > 3 and any(pos in text for pos in ['great', 'perfect', 'amazing']):
            hidden.append('stress_masked')
        
        # Pattern 3: Deflection
        if any(defl in text for defl in ['anyway', 'whatever', 'moving on']):
            hidden.append('avoidance')
        
        return hidden
    
    def _detect_micro_emotions(self, text: str) -> List[str]:
        """Detect subtle emotional shifts"""
        micro = []
        
        for emotion, keywords in self.micro_emotions.items():
            if any(keyword in text for keyword in keywords):
                micro.append(emotion)
        
        return micro[:3]
    
    def _analyze_intensity(self, text_lower: str, text_original: str) -> float:
        """Analyze emotional intensity (0-10)"""
        intensity = 5.0
        
        # Punctuation amplifiers
        exclamation_count = text_original.count('!')
        question_count = text_original.count('?')
        caps_ratio = sum(1 for c in text_original if c.isupper()) / max(len(text_original), 1)
        
        # Intensity modifiers
        intensity_words = {
            'very': 1.5, 'extremely': 2.0, 'incredibly': 2.0,
            'really': 1.5, 'so': 1.5, 'totally': 1.5,
            'absolutely': 2.0, 'completely': 2.0
        }
        
        for word, multiplier in intensity_words.items():
            if word in text_lower:
                intensity *= multiplier
        
        # Add punctuation impact
        intensity += exclamation_count * 0.5
        intensity += caps_ratio * 3
        
        return min(10.0, max(0.0, intensity))
    
    def _calculate_pad(self, primary: str, intensity: float, text: str) -> Tuple[float, float, float]:
        """Calculate PAD model (Pleasure, Arousal, Dominance)"""
        
        # Pleasure (valence): -1 to +1
        positive_emotions = ['joy', 'love', 'excitement', 'peace', 'calm', 'gratitude', 'pride']
        negative_emotions = ['anxiety', 'fear', 'anger', 'sadness', 'stress', 'grief']
        
        if primary in positive_emotions:
            valence = 0.5 + (intensity / 20)  # 0.5 to 1.0
        elif primary in negative_emotions:
            valence = -0.5 - (intensity / 20)  # -0.5 to -1.0
        else:
            valence = 0.0
        
        # Arousal: 0 to 10
        high_arousal = ['anxiety', 'fear', 'anger', 'excitement', 'stress']
        low_arousal = ['peace', 'calm', 'meditation', 'sadness']
        
        if primary in high_arousal:
            arousal = 7.0 + (intensity / 3)
        elif primary in low_arousal:
            arousal = 3.0 - (intensity / 5)
        else:
            arousal = 5.0
        
        arousal = min(10.0, max(0.0, arousal))
        
        # Dominance: 0 to 10
        control_words = ['can', 'will', 'choose', 'control', 'decide']
        helpless_words = ['can\'t', 'won\'t', 'stuck', 'trapped', 'helpless']
        
        if any(word in text for word in control_words):
            dominance = 7.0
        elif any(word in text for word in helpless_words):
            dominance = 3.0
        else:
            dominance = 5.0
        
        return valence, arousal, dominance
    
    def _calculate_confidence(self, primary: str, secondary: List[str], hidden: List[str], text: str) -> float:
        """Calculate confidence in emotion detection (0-1)"""
        confidence = 0.5
        
        # Strong indicators
        if len(text) > 50:
            confidence += 0.2
        if secondary:
            confidence += 0.1
        if any(emotion in text for emotion in [primary]):
            confidence += 0.2
        
        return min(1.0, confidence)
    
    def _predict_trajectory(self, primary: str, history: Optional[List[Dict]], intensity: float) -> str:
        """Predict emotional trajectory"""
        if intensity > 8.0:
            return 'escalating'
        elif intensity < 3.0:
            return 'de-escalating'
        else:
            return 'stable'
    
    def _identify_emotional_needs(self, primary: str, secondary: List[str], hidden: List[str], context: Dict) -> List[str]:
        """Identify emotional needs"""
        needs_map = {
            'anxiety': ['reassurance', 'grounding', 'control'],
            'sadness': ['validation', 'connection', 'hope'],
            'anger': ['acknowledgment', 'justice', 'release'],
            'fear': ['safety', 'courage', 'support'],
            'love': ['expression', 'connection', 'celebration'],
            'confusion': ['clarity', 'understanding', 'direction'],
            'stress': ['relief', 'support', 'rest'],
        }
        
        return needs_map.get(primary, ['support', 'understanding'])
    
    def _detect_triggers(self, text: str, primary: str) -> List[str]:
        """Detect emotional triggers"""
        triggers = []
        trigger_keywords = self.emotion_triggers.get(primary, [])
        
        for trigger in trigger_keywords:
            if trigger in text:
                triggers.append(trigger)
        
        return triggers[:3]
    
    def _emotion_present(self, text: str, emotion: str) -> bool:
        """Check if emotion is present in text"""
        try:
            from src.catalogs import EMOTION_KEYWORDS
            keywords = EMOTION_KEYWORDS.get(emotion, [])
            return any(keyword in text for keyword in keywords)
        except:
            return emotion in text
    
    def _store_emotion_memory(self, emotion_state: EmotionState, user_id: Optional[str]):
        """Store emotion in memory"""
        self.emotion_memory.append({
            'user_id': user_id,
            'primary': emotion_state.primary,
            'intensity': emotion_state.intensity,
            'timestamp': emotion_state.timestamp
        })
        
        # Keep last 1000
        if len(self.emotion_memory) > 1000:
            self.emotion_memory = self.emotion_memory[-1000:]
    
    def _update_user_emotion_profile(self, user_id: str, emotion_state: EmotionState):
        """Update user's emotion profile"""
        # Hash user_id for privacy
        hashed_id = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        
        if hashed_id not in self.user_emotion_profiles:
            self.user_emotion_profiles[hashed_id] = {
                'emotion_history': [],
                'common_emotions': {},
                'average_intensity': 5.0,
                'created_at': datetime.now().isoformat()
            }
        
        profile = self.user_emotion_profiles[hashed_id]
        
        # Add to history
        profile['emotion_history'].append({
            'emotion': emotion_state.primary,
            'intensity': emotion_state.intensity,
            'timestamp': emotion_state.timestamp
        })
        
        # Keep last 50
        if len(profile['emotion_history']) > 50:
            profile['emotion_history'] = profile['emotion_history'][-50:]
        
        # Update common emotions
        if emotion_state.primary in profile['common_emotions']:
            profile['common_emotions'][emotion_state.primary] += 1
        else:
            profile['common_emotions'][emotion_state.primary] = 1
        
        # Save profile periodically
        if len(profile['emotion_history']) % 10 == 0:
            self._save_user_profile(hashed_id, profile)
    
    def _save_user_profile(self, hashed_id: str, profile: Dict):
        """Save user emotion profile to disk"""
        try:
            profile_path = f"user_data/emotion_profiles/{hashed_id}.json"
            with open(profile_path, 'w') as f:
                json.dump(profile, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving emotion profile: {e}")
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user's emotion profile"""
        hashed_id = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        return self.user_emotion_profiles.get(hashed_id)
