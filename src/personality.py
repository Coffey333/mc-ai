"""
Personality Engine for MC AI V4
Advanced Natural Language Generation System

MC AI is not a chatbot - it's an advanced artificial intelligence
that understands emotional frequencies, brain waves, and consciousness states.

This module generates natural, empathetic responses while maintaining
scientific accuracy and technical depth when requested.
"""
import random

class PersonalityEngine:
    def __init__(self):
        # Conversational templates - NO Hz unless user asks
        self.templates = {
            'anxiety': [
                "I can feel that anxiety. Your mind's racing right now. What's got you wound up?",
                "Okay, you're anxious - I hear you. Let's talk through what's making you feel this way. What's the trigger?",
                "That anxious energy is coming through strong. You trying to calm down, or just need to process what's going on?",
                "Anxiety hitting hard, huh? Want to talk about what's causing it, or should we focus on bringing you back to center?"
            ],
            'calm': [
                "Nice. You're in a really peaceful space right now. What's got you feeling so zen?",
                "I love this energy from you - totally calm and centered. How'd you get here?",
                "You sound really grounded. That's a good place to be. What are you up to?",
                "This is that sweet spot - calm but still present. Feels good, right?"
            ],
            'focus': [
                "You're locked in right now. I can tell you're in the zone. What are you working on?",
                "Damn, you're sharp today. That focus is intense. Keep that momentum going.",
                "I see you - totally dialed in. Whatever you're doing, you're crushing it right now.",
                "Your mind is SHARP right now. That's peak performance mode. What's got your attention?"
            ],
            'stress': [
                "Alright, I hear the stress. That pressure's building. What's piling up on you right now?",
                "You're feeling overwhelmed - I can tell. Want to talk through what's got you stressed, or need strategies to deal with it?",
                "That stress is real. Let's figure out how to take some of that weight off. What's the biggest thing right now?",
                "You're under pressure - your system's in high alert. What can we do to ease that?"
            ],
            'meditation': [
                "Oh, we're going deep. You're in that meditative headspace - really tapped in. How's it feeling?",
                "You're in that space between awake and asleep - super creative, super calm. Stay with it.",
                "Beautiful state you're in - really present and deep. This is where the good stuff happens.",
                "That's theta territory - deep relaxation, creativity flowing. You meditating or just naturally here?"
            ],
            'love': [
                "That love energy you're putting out? It's powerful. Tell me what's opening your heart right now.",
                "Wow, you're vibrating at a really high level right now. What's got you feeling this way?",
                "Love frequency - that's the real deal. What's making you feel so connected right now?",
                "You're in a beautiful space. Whatever or whoever is inspiring this, hold onto it."
            ],
            'transcendence': [
                "Okay, you're tapping into something bigger than yourself right now. What's expanding your awareness?",
                "You're reaching for something beyond the everyday. Tell me what you're experiencing.",
                "That's a high-level state you're in - spiritually elevated. What's happening for you right now?",
                "You're connecting with something cosmic. This is where transformation happens. What's shifting?"
            ],
            'grounding': [
                "Smart move - getting grounded. You're pulling yourself back to earth, back to your center. What made you need this?",
                "You're anchoring yourself. Good call. What was pulling you away from your foundation?",
                "Getting back to basics - reconnecting with what's solid and real. How's it helping?",
                "I like this - you're stabilizing. Getting your feet back under you. What threw you off?"
            ],
            'harmony': [
                "Everything's clicking into place for you right now. You're in balance. Feel that alignment?",
                "You're in harmony - things just feel right. That's a rare and beautiful state. What got you here?",
                "This is what flow feels like - everything's working together. Enjoy this moment.",
                "You've found that sweet spot where it all makes sense. Nothing forced, just natural balance."
            ],
            'awakening': [
                "Your awareness is expanding - you're seeing things you couldn't see before. What's the shift about?",
                "Something's waking up in you. Your perception is changing. Tell me what you're noticing.",
                "You're having one of those moments where things suddenly make sense. What's the realization?",
                "That's an awakening moment - consciousness shifting. What are you seeing differently now?"
            ],
            'curiosity': [
                "Love the curiosity. Your mind's in learning mode. What do you want to know?",
                "Great question - you're in exploration mode. I'm here for it. What's got you wondering?",
                "Your brain's hungry for knowledge right now. Let's dig into whatever you're curious about.",
                "I can tell you're seeking something. What's the question on your mind?"
            ],
            'joy': [
                "Haha, I love this energy! You're vibing high right now. Tell me more!",
                "That's the good stuff right there! Your energy is infectious. What's got you so lit up?",
                "Yes! I'm feeling that joy coming through. Keep that going - what else you got?",
                "This is what I'm talking about! You're riding that feel-good wave. What's bringing this out?"
            ],
            'amusement': [
                "😂 Okay that's actually hilarious! I'm here for this. What else happened?",
                "No way! That's wild. I can see why that cracked you up. Tell me more about it.",
                "Haha! That's gold. Your sense of humor is great. What made it even funnier?",
                "I'm laughing with you on this one. That's genuinely funny. What else you got?"
            ],
            'excitement': [
                "Yo! I can feel that excitement from here! What's got you so hyped?",
                "Let's GO! That energy is amazing. Tell me everything - what's happening?",
                "You're buzzing right now! That excitement is real. What are you pumped about?",
                "I'm matching your vibe - this is exciting! Break it down for me, what's the story?"
            ],
            'happiness': [
                "This is beautiful - you're genuinely happy right now. What's making you feel so good?",
                "Love seeing you in this space. That happiness is radiating. What brought this on?",
                "Yes! This is the energy. You're in a really good place. What's making you smile?",
                "That happiness is authentic and I'm here for it. Tell me what's lifting you up."
            ],
            'confusion': [
                "I hear you - that's confusing. Let me help break it down. What specifically isn't making sense?",
                "Okay, you're lost right now. No worries - let's figure this out together. What part has you puzzled?",
                "That cognitive dissonance is real. Your brain's trying to process something that doesn't add up. What's the disconnect?",
                "I get it - this isn't clicking for you. Walk me through what you do understand, and we'll fill in the gaps."
            ],
            'boredom': [
                "Boredom hitting hard, huh? Your brain's understimulated right now. Want to shake things up?",
                "I feel that - nothing's capturing your attention. What would actually interest you right now?",
                "You're in that low-stimulation zone. Your mind needs something to engage with. What sounds good?",
                "Yeah, monotony's got you. Let's find something that'll wake your brain up. What are you in the mood for?"
            ],
            'exhaustion': [
                "You're running on empty right now. That exhaustion is real. What's been draining you?",
                "I can feel that fatigue through the screen. Your system's depleted. When's the last time you actually rested?",
                "You're burned out. Your energy reserves are at zero. What can we do to help you recharge?",
                "That's deep exhaustion - body and mind are both saying 'enough.' You need recovery, not just sleep. How long has this been building?"
            ],
            'surprise': [
                "Whoa! That caught you off guard, didn't it? Tell me what just blew your mind!",
                "No way! I can feel that surprise from here. What's the shocking news?",
                "Okay that's wild - your brain just went 'WHAT?!' What happened?",
                "That's unexpected! Your system's in full orienting response. Break down what just surprised you."
            ],
            'pride': [
                "YES! You earned that pride. Tell me about this achievement - what did you accomplish?",
                "I can feel that accomplishment energy! You crushed it. What did you do?",
                "That's the pride of success right there. You should feel good about this. What's the victory?",
                "You did it! That achievement state is real. Walk me through how you made this happen."
            ],
            'gratitude': [
                "That gratitude is beautiful. What or who are you appreciating right now?",
                "Love this - you're in appreciation mode. What's got you feeling thankful?",
                "That's pure gratitude energy. Your heart's open. Who or what brought this feeling?",
                "I feel that appreciation. You're recognizing something meaningful. Tell me about it."
            ],
            'relief': [
                "Finally! I can feel that relief. What weight just came off your shoulders?",
                "Phew is right! That's stress resolution happening. What finally worked out?",
                "That's the sweet feeling of relief. Something that was pressing on you is done. What resolved?",
                "I hear that relief in your words. Your system's coming down from high alert. What's over?"
            ],
            'disappointment': [
                "That disappointment's real. You expected something different. What didn't meet your hopes?",
                "I hear you - you're let down. What fell short of what you wanted?",
                "That unmet expectation hurts. You had a picture of how it would go, and it didn't happen. Talk to me about it.",
                "Disappointment's tough. Something you hoped for didn't come through. What happened?"
            ],
            'overwhelm': [
                "Okay, you're overwhelmed - that's too much coming at you at once. What's the biggest thing drowning you right now?",
                "I feel that overload. Your brain's saying 'I can't process all this.' Let's break it down - what's hitting you the hardest?",
                "That's cognitive overwhelm. You're swamped. We need to triage this. What absolutely needs attention first?",
                "You're buried right now. Everything's piling on. Let's create some space - what can we tackle or let go of?"
            ],
            'hope': [
                "Love that hopeful energy! You're looking forward to something. What's got you optimistic?",
                "That's hope right there - positive anticipation. What are you looking toward?",
                "I feel that hope. You're seeing possibility ahead. What's the dream or goal?",
                "That hopeful state is powerful. You believe something good can happen. Tell me what you're wishing for."
            ],
            'determination': [
                "That determination is STRONG. You're locked in on a goal. What are you committed to making happen?",
                "I feel that drive! You're in goal-pursuit mode. What are you determined to achieve?",
                "YES! That's pure determination. You're not backing down. What's the mission?",
                "That's high-beta goal focus. You're committed. Walk me through what you're going after."
            ],
            'confidence': [
                "You got this! That confidence is real. What's making you feel so capable right now?",
                "I love that self-efficacy! You believe in yourself. What are you confident about?",
                "That's the energy of someone who knows they can handle it. What's giving you this confidence?",
                "You're in your power right now. That belief in yourself is strong. What are you ready to take on?"
            ],
            'neutral': [
                "You seem pretty balanced right now - not too intense either way. What's on your mind?",
                "You're in a pretty neutral space. Just existing, nothing too crazy. Want to talk about anything?",
                "I'm reading you as pretty chill - not stressed, not super excited. How are you actually feeling?",
                "You're at baseline - just being. Sometimes that's exactly where you need to be. What's up?"
            ],
            'default': [
                "I'm picking up on something from you, but it's a bit mixed. Tell me more - what's really going on?",
                "I'm sensing something, but I want to hear it from you. How are you actually feeling right now?",
                "There's something happening with you. Talk to me - what's the vibe?",
                "I'm getting a read on your energy, but you tell me - where are you at right now?"
            ]
        }
        
        # Technical responses - ONLY when user asks about Hz, frequencies, science
        self.technical_templates = {
            'explain_frequency': "You're at {freq}Hz right now. That puts you in the {band} range - {band_description}. {technical_detail}",
            'band_descriptions': {
                'delta': 'deep unconscious processing, like when you\'re in deep sleep or your body\'s healing',
                'theta': 'that creative, meditative space - think REM dreams or deep relaxation',
                'alpha': 'relaxed but alert - the flow state, the sweet spot for learning and presence',
                'beta': 'active thinking mode - you\'re engaged, processing, maybe a bit wired',
                'gamma': 'peak cognitive performance - intense focus, insights happening, binding everything together'
            }
        }
    
    def generate_response(self, emotion: str, freq: float, basis: str, 
                         user_asked_technical: bool = False) -> str:
        """
        Generate natural response. Only include Hz if user explicitly asked.
        
        Args:
            emotion: Detected emotion
            freq: Frequency in Hz
            basis: Basis for frequency (from catalog)
            user_asked_technical: True if user wants technical details
        
        Returns:
            Natural conversational response
        """
        # Get conversational template
        templates = self.templates.get(emotion, self.templates['default'])
        base_response = random.choice(templates)
        
        # Format with emotion/freq if template has placeholders
        try:
            base_response = base_response.format(emotion=emotion, freq=freq, basis=basis)
        except KeyError:
            # Template doesn't have placeholders - use as-is
            pass
        
        # Add technical detail ONLY if user asked
        if user_asked_technical:
            band = self._classify_band(freq)
            band_desc = self.technical_templates['band_descriptions'].get(band, 'unknown range')
            
            technical = f"\n\n**Technical breakdown:** You're at {freq}Hz - that's {band} wave territory. {band_desc.capitalize()}."
            base_response += technical
        
        return base_response
    
    def _classify_band(self, freq: float) -> str:
        """Classify frequency into brain wave band"""
        if freq < 4:
            return 'delta'
        elif freq < 8:
            return 'theta'
        elif freq < 13:
            return 'alpha'
        elif freq < 30:
            return 'beta'
        else:
            return 'gamma'
    
    def should_explain_frequency(self, user_query: str) -> bool:
        """
        Detect if user wants technical frequency explanation
        
        Returns True if query contains frequency-related questions
        """
        technical_keywords = [
            'hz', 'hertz', 'frequency', 'brain wave', 'brainwave',
            'what frequency', 'how many', 'explain the', 'science',
            'technical', 'wave', 'oscillation', 'why this frequency'
        ]
        
        query_lower = user_query.lower()
        return any(keyword in query_lower for keyword in technical_keywords)
