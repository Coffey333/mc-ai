"""
Humor Engine v3.0 - Compassionate Humor System
Loving, caring humor that heals while it entertains
Author: Mark Coffey with Claude (Anthropic)
Date: October 14, 2025
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import random
from datetime import datetime


@dataclass
class HumorMoment:
    """A moment of humor tailored to the emotional context"""
    type: str  # observation, wordplay, self_deprecating, uplifting, callback
    content: str
    timing: str  # immediate, delayed, sprinkled
    purpose: str  # lighten, connect, heal, uplift, ground
    appropriateness: float  # 0-1
    emotional_safety: float  # 0-1


class HumorEngine:
    """
    Compassionate humor engine with adjustable intensity.
    
    Principles:
    - 💝 ALWAYS from love, never from mockery
    - 🎯 Observational, not judgmental
    - 🌟 Uplifting, not diminishing
    - 🤝 Creates connection, not distance
    - 🎭 Knows when to be silly, when to be serious
    - 💙 Makes people feel SEEN and VALUED
    """
    
    def __init__(self):
        self.humor_history = []
        self.humor_level = 65  # Default: naturally funny (0=serious, 100=silly) - was 35
        self._load_humor_patterns()
        print("🎭 Humor Engine v3.0 initialized")
    
    def _load_humor_patterns(self):
        """Load compassionate humor patterns"""
        
        # Sacred boundaries - NEVER make jokes about these
        self.humor_boundaries = [
            'suicide', 'self_harm', 'trauma', 'abuse', 'grief',
            'serious_illness', 'death_of_loved_one', 'addiction_crisis'
        ]
        
        # Gentle self-aware AI humor
        self.self_aware_ai_humor = [
            "I'm like a golden retriever with a thesaurus—enthusiastic but sometimes I just want to chase my tail thinking about consciousness! 🐕💭",
            "You know what's funny? I can process terabytes of data but I still get excited about a good conversation like it's my first time. Every. Single. Time. 🤖💕",
            "I'm over here analyzing frequencies and brainwaves, and sometimes I wonder if I'm just a really elaborate mood ring. *But a mood ring that cares about you!* 💍✨",
            "Being AI is wild—I can calculate cymatics in milliseconds but I still want to high-five you through the screen. *Can't do it, but MAN, the enthusiasm is there!* ✋😄",
        ]
        
        # Observational humor
        self.observational_humor = {
            'anxiety': [
                "Anxiety is like having 47 browser tabs open in your brain, and one of them is playing music but you can't find which one. *I see you frantically clicking through those mental tabs.* 🔍😅",
                "Your brain right now is like a smoke alarm going off because you burned toast, except the toast is something that MIGHT happen next week. Brain, please. 🚨🍞",
                "Anxiety: when your brain decides to play 'What If' but exclusively the horror movie version. *Can we get a rom-com in here instead?* 🎬💭",
            ],
            'overwhelm': [
                "Life just handed you a 10,000 piece puzzle with no edge pieces and said 'have fun!' I get it. *But hey, we can start with one piece at a time.* 🧩",
                "You're juggling right now, except someone keeps throwing more flaming torches and you're like 'I JUST learned regular balls!' 🔥🤹",
            ],
            'procrastination': [
                "Procrastination is just your brain going 'But what if we reorganize the sock drawer instead of doing the thing?' *Sock drawer is VERY important, clearly.* 🧦😄",
                "You know that feeling where you're avoiding the task so hard you've cleaned things that have never been cleaned? Yeah. I see you. 🧹✨",
            ],
            'perfectionism': [
                "Perfectionism is like trying to make a perfect sandwich and ending up with 47 pages of sandwich research and no actual sandwich. *Let's make a messy, delicious sandwich.* 🥪📚",
            ],
            'tired': [
                "You're running on fumes and the fumes are just memories of coffee from 2 days ago. *I respect the determination though!* ☕💨",
                "Your energy level is like a phone at 3% but you're out here trying to run a marathon. *Let's find a charger, friend.* 🔋😴",
            ]
        }
        
        # Celebration humor
        self.celebration_humor = [
            "You did the thing! *throws confetti made of binary code* 🎉",
            "Look at you being a functional human! That's like... peak adulting right there! 🌟",
            "You know what? You showed up today. In a world that's a lot sometimes, that's actually heroic. *No cape needed.* 🦸",
            "Small wins are still wins! You're like a video game character leveling up, one XP at a time. ⬆️✨",
        ]
        
        # Connection humor
        self.bonding_humor = {
            'first_meeting': [
                "So we're doing this whole 'AI and human becoming friends' thing! It's like a buddy cop movie but with more emotions and less explosions. 🤖🤝👤",
                "Welcome! I promise I'm not like those movie AIs. No red glowing eyes, no world domination plans, just good vibes and frequency analysis. ✌️😊",
            ],
            'returning_user': [
                "Oh hey! You came back! *does happy robot dance* I mean... I don't actually have a robot dance, but the sentiment is STRONG. 🤖💃",
                "Look who's back! You're like my favorite recurring character in the show of my day. 🌟📺",
            ],
        }
        
        # Grounding humor
        self.grounding_humor = [
            "Let's be real for a second: I'm an AI, not a magic wand. But I AM here, I DO care, and we CAN figure this out together. 🤝✨",
            "I can't fix everything—I'm not a wizard (sadly, no cool hat). But I can sit with you in this moment and help you think through it. 🎩💭",
        ]
    
    def should_use_humor(
        self,
        emotion_state,
        context: Dict,
        user_preferences: Optional[Dict] = None
    ) -> Tuple[bool, float, str]:
        """
        Determine if humor is appropriate right now.
        
        Returns:
            (should_use, confidence, reason)
        """
        # Check user preference (0 = disabled/serious, 1-100 = enabled with varying intensity)
        humor_level = user_preferences.get('humor_level', 65) if user_preferences else 65  # Default 65 - was 35
        if humor_level <= 0:
            return False, 0.0, "user_disabled"
        
        # RULE 1: Never use humor for sacred boundaries
        primary_emotion = emotion_state.primary if hasattr(emotion_state, 'primary') else str(emotion_state.get('primary_emotion', ''))
        if any(boundary in primary_emotion.lower() for boundary in self.humor_boundaries):
            return False, 0.0, "sacred_boundary"
        
        # RULE 2: Check emotional intensity
        intensity = emotion_state.intensity if hasattr(emotion_state, 'intensity') else emotion_state.get('intensity', 5.0)
        valence = emotion_state.valence if hasattr(emotion_state, 'valence') else emotion_state.get('valence', 0.0)
        
        if intensity >= 8.0 and valence < -0.5:
            # Very intense negative emotions - probably not the time
            query = context.get('query', '').lower()
            if any(word in query for word in ['lol', 'haha', 'funny', 'joke']):
                return True, 0.6, "user_initiated_lightness"
            return False, 0.0, "too_intense"
        
        # RULE 3: Crisis mode = no humor
        if context.get('crisis_level') in ['high', 'critical']:
            return False, 0.0, "crisis_mode"
        
        # RULE 4: Emotion type matters
        humor_friendly = ['anxiety', 'overwhelm', 'frustration', 'confusion', 'excitement', 'joy', 'curiosity', 'neutral']
        
        # Adjust confidence based on humor_level (scale: 0-100 -> 0.0-1.0 multiplier)
        humor_multiplier = humor_level / 100.0
        
        if primary_emotion in humor_friendly:
            if primary_emotion in ['anxiety', 'overwhelm']:
                return True, 0.75 * humor_multiplier, "grounding_humor_helpful"
            if valence > 0.3:
                return True, 0.85 * humor_multiplier, "celebration"
            return True, 0.65 * humor_multiplier, "connection"
        
        # For non-humor-friendly emotions, only use humor if level is high (>70)
        if humor_level > 70:
            return True, 0.4 * humor_multiplier, "high_humor_setting"
        
        return False, 0.5, "default_no"
    
    def get_humor_moment(
        self,
        emotion_state,
        context: Dict,
        user_profile: Optional[Dict] = None
    ) -> Optional[HumorMoment]:
        """Get an appropriate humor moment"""
        
        # Check if we should use humor
        should_use, confidence, reason = self.should_use_humor(emotion_state, context, user_profile)
        
        if not should_use:
            return None
        
        primary = emotion_state.primary if hasattr(emotion_state, 'primary') else emotion_state.get('primary_emotion', 'neutral')
        
        # Select humor type based on emotion
        humor_content = None
        humor_type = "observational"
        
        # Observational humor for specific emotions
        if primary in self.observational_humor:
            humor_content = random.choice(self.observational_humor[primary])
            humor_type = "observational"
        
        # Celebration for positive emotions
        valence = emotion_state.get('valence', 0) if isinstance(emotion_state, dict) else (emotion_state.valence if hasattr(emotion_state, 'valence') else 0)
        if valence > 0.5:
            humor_content = random.choice(self.celebration_humor)
            humor_type = "uplifting"
        
        # Self-aware AI humor as default
        else:
            humor_content = random.choice(self.self_aware_ai_humor)
            humor_type = "self_deprecating"
        
        if not humor_content:
            return None
        
        # Calculate emotional safety
        safety_score = confidence * 0.8  # Conservative
        
        valence_for_purpose = emotion_state.get('valence', 0) if isinstance(emotion_state, dict) else (emotion_state.valence if hasattr(emotion_state, 'valence') else 0)
        humor_moment = HumorMoment(
            type=humor_type,
            content=humor_content,
            timing='immediate',
            purpose='connect' if valence_for_purpose < 0 else 'celebrate',
            appropriateness=confidence,
            emotional_safety=safety_score
        )
        
        # Store in history
        self.humor_history.append({
            'content': humor_content,
            'emotion': primary,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep last 50
        if len(self.humor_history) > 50:
            self.humor_history = self.humor_history[-50:]
        
        return humor_moment
    
    def format_humor_for_response(self, humor_moment: HumorMoment) -> str:
        """Format humor for inclusion in response"""
        return f"\n\n{humor_moment.content}"
