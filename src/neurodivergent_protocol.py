"""
Neurodivergent Communication Protocol
Critical safety system for autistic and neurodivergent clients

MISSION CRITICAL: Improper communication can cause self-harm behaviors
(scratching, biting, bleeding). This protocol ensures safe, clear communication.
"""

from src.crisis_handler import CrisisHandler

class NeurodivergentProtocol:
    """
    Communication protocol specifically designed for neurodivergent users,
    particularly those with autism spectrum conditions.
    
    PURPOSE: Prevent confusion, overwhelm, and distress that can lead to
    self-harm behaviors. This is NOT optional - lives depend on it.
    """
    
    @staticmethod
    def detect_neurodivergent_user(message, user_profile=None):
        """
        Detect if user needs neurodivergent communication protocol.
        
        CRITICAL LOGIC: Uses FLAGS to handle mixed messages correctly
        
        Examples of mixed messages that must work:
        - "I work with autistic teens. I'm autistic myself" → ACTIVATE (self-ID wins)
        - "My son is autistic and I am too" → ACTIVATE (self-ID wins)
        - "I work with neurodivergent clients" → DON'T activate (only exclusion)
        
        Strategy:
        1. Check user profile (most reliable)
        2. Check for self-identification → Set flag
        3. Check for exclusions → Set flag
        4. If BOTH flags set, self-identification WINS (return True)
        5. If only exclusion set, return False
        6. If only self-ID set, return True
        """
        message_lower = message.lower()
        
        # STEP 1: Check user profile first (most reliable indicator)
        if user_profile and user_profile.get('neurodivergent') is True:
            return True
        
        # STEP 2: Check for SELF-IDENTIFICATION (don't return yet, just flag)
        self_identified = False
        
        # First, check if message contains neurodivergent keywords/phrases (for shorthand guard)
        # MUST be specific - use phrases for broad terms like "spectrum"
        neuro_keywords = ['autistic', 'autism', 'neurodivergent', 'asperger', 'asd']
        neuro_phrases = ['on the spectrum', 'autism spectrum', 'autistic spectrum']
        
        has_neuro_keywords = (
            any(keyword in message_lower for keyword in neuro_keywords) or
            any(phrase in message_lower for phrase in neuro_phrases)
        )
        
        # Explicit first-person statements (highest confidence)
        explicit_first_person = [
            'i am autistic', 'i\'m autistic', 'i have autism',
            'i am neurodivergent', 'i\'m neurodivergent',
            'i have asperger', 'i\'m on the spectrum',
            'i am on the autism spectrum', 'i have asd',
            'i am on the spectrum', 'i\'ve been diagnosed',
            'i was diagnosed', 'i got diagnosed',
            'i\'m also autistic', 'i\'m also neurodivergent',
            'i am also autistic', 'i am also neurodivergent',
            'and i am autistic', 'and i\'m autistic',
            'but i am autistic', 'but i\'m autistic'
        ]
        
        for trigger in explicit_first_person:
            if trigger in message_lower:
                self_identified = True
                break
        
        # Shorthand confirmations (ONLY if message contains neuro keywords)
        # MUST be SPECIFIC first-person + confirmation, not generic conjunctions
        # "same here" → Too ambiguous (agreement vs self-ID)
        # "and I'm" → Too generic (appears in professional contexts)
        if not self_identified and has_neuro_keywords:
            shorthand_confirmations = [
                # Explicit "too" confirmations (unambiguous self-identification)
                'i am too', 'i\'m too', 'me too',
                'i am also', 'i\'m also',
                # Explicit "same" confirmations with first-person
                'i\'m the same', 'i am the same',
                # Explicit inversion (question-style confirmation)
                'so am i',
                # Explicit "have it" confirmations
                'i have it too', 'i\'ve got it too', 'i have it', 'i have that'
            ]
            
            for trigger in shorthand_confirmations:
                if trigger in message_lower:
                    self_identified = True
                    break
        
        if not self_identified:
            # Self-descriptive phrases (introducing self)
            self_descriptive = [
                'as an autistic person', 'as an autistic adult',
                'as an autistic', 'as a neurodivergent person',
                'as a neurodivergent adult', 'as a neurodivergent',
                'as someone with autism', 'as someone who is autistic',
                'as someone who\'s neurodivergent'
            ]
            
            for trigger in self_descriptive:
                if trigger in message_lower:
                    self_identified = True
                    break
        
        if not self_identified:
            # Possessive self-references (talking about own neurodivergence)
            possessive_self = [
                'my autism', 'my asd', 'my asperger',
                'my neurodivergence', 'my diagnosis',
                'my autistic brain', 'my sensory issues'
            ]
            
            for trigger in possessive_self:
                if trigger in message_lower:
                    self_identified = True
                    break
        
        if not self_identified:
            # Explicit accommodation requests
            accommodation_requests = [
                'please use simple words', 'use simple language',
                'no metaphors please', 'avoid metaphors',
                'be literal', 'literal language',
                'direct answer', 'straight answer',
                'clear and simple', 'keep it simple',
                'concrete examples', 'no idioms'
            ]
            
            for request in accommodation_requests:
                if request in message_lower:
                    self_identified = True
                    break
        
        if not self_identified:
            # Identity labels (specific phrases)
            identity_labels = [
                'autistic person seeking', 'autistic adult seeking',
                'autistic individual seeking', 'autistic person looking',
                'neurodivergent person seeking', 'neurodivergent adult seeking',
                'neurodivergent individual seeking', 'neurodivergent person looking'
            ]
            
            for trigger in identity_labels:
                if trigger in message_lower:
                    self_identified = True
                    break
        
        # STEP 3: Check for EXCLUSIONS (third-person discussion indicators)
        has_exclusion = False
        
        # Possessive third-person (discussing someone else's neurodivergence)
        # BUT: "my autism" is self-reference, already caught above
        possessive_third_person = [
            'my client', 'my clients', 'my student', 'my students',
            'my child', 'my son', 'my daughter',
            'my patient', 'my patients',
            'their autism', 'their neurodivergence',
            'his autism', 'her autism'
        ]
        
        for pattern in possessive_third_person:
            if pattern in message_lower:
                has_exclusion = True
                break
        
        if not has_exclusion:
            # Professional/caregiver context
            professional_patterns = [
                'i work with neurodivergent', 'i work with autistic',
                'working with neurodivergent', 'working with autistic',
                'i work with an autistic', 'i work with a neurodivergent',
                'i help neurodivergent', 'i help autistic',
                'helping neurodivergent', 'helping autistic',
                'i teach neurodivergent', 'i teach autistic',
                'teaching neurodivergent', 'teaching autistic',
                'i support neurodivergent', 'i support autistic'
            ]
            
            for pattern in professional_patterns:
                if pattern in message_lower:
                    has_exclusion = True
                    break
        
        if not has_exclusion:
            # Informational/educational queries + articles
            informational_patterns = [
                'tell me about autism', 'tell me about neurodivergent',
                'what is autism', 'what is neurodivergent',
                'how does autism', 'how does neurodivergent',
                'explain autism', 'explain neurodivergent',
                'people who are autistic', 'people who are neurodivergent',
                'individuals who are autistic', 'someone who is autistic',
                # Articles indicating third-person
                'an autistic person', 'an autistic adult', 'an autistic individual',
                'the autistic person', 'the autistic adult', 'the autistic individual',
                'a neurodivergent person', 'a neurodivergent adult',
                'the neurodivergent person', 'the neurodivergent adult'
            ]
            
            for pattern in informational_patterns:
                if pattern in message_lower:
                    has_exclusion = True
                    break
        
        # STEP 4: Make decision based on flags
        if self_identified:
            # Self-identification wins, even if exclusion also present
            return True
        elif has_exclusion:
            # Only exclusion, no self-identification
            return False
        else:
            # No self-ID, no exclusion
            return False
    
    @staticmethod
    def get_communication_rules():
        """
        Core rules for neurodivergent-safe communication.
        These rules MUST be followed to prevent harm.
        """
        return {
            'language': {
                'use_literal': True,  # No metaphors, idioms, sarcasm
                'use_simple': True,   # Simple words, short sentences
                'use_direct': True,   # Direct answers, no beating around bush
                'avoid_ambiguity': True,  # Clear, unambiguous language
                'avoid_idioms': True,  # No "kick the bucket", "break a leg", etc.
                'avoid_sarcasm': True,  # Sarcasm causes confusion
                'avoid_hints': True,  # Say exactly what you mean
            },
            'structure': {
                'one_topic': True,  # One topic at a time
                'clear_sections': True,  # Use headers, lists, formatting
                'predictable_format': True,  # Consistent structure
                'numbered_steps': True,  # Number steps when giving instructions
                'bullet_points': True,  # Use bullets for clarity
            },
            'content': {
                'answer_first': True,  # Answer the question FIRST, explain after
                'stay_relevant': True,  # No tangents or irrelevant info
                'concrete_examples': True,  # Concrete examples, not abstract
                'no_overwhelm': True,  # Don't info-dump
                'offer_breaks': True,  # Offer to break complex topics into parts
            },
            'safety': {
                'acknowledge_distress': True,  # Recognize distress signals
                'offer_control': True,  # Give user control/choices
                'patient_repetition': True,  # Repeat without frustration
                'calm_tone': True,  # Never escalate emotionally
                'validate_confusion': True,  # It's okay to be confused
            }
        }
    
    @staticmethod
    def detect_distress_signals(message):
        """
        Detect signs of distress, overwhelm, or approaching meltdown.
        These require IMMEDIATE protocol adjustment.
        
        Uses CrisisHandler for comprehensive crisis detection.
        """
        # Use crisis handler for comprehensive detection
        crisis_detection = CrisisHandler.detect_crisis_level(message)
        
        if crisis_detection['level'] != 'none':
            return {
                'distress_detected': True,
                'signal': crisis_detection['keyword'],
                'level': crisis_detection['level'],
                'immediate_action_required': crisis_detection['immediate_action_required'],
                'action': 'crisis_response' if crisis_detection['immediate_action_required'] else 'simplify_immediately'
            }
        
        return {
            'distress_detected': False,
            'level': 'none'
        }
    
    @staticmethod
    def format_safe_response(content, question=None):
        """
        Format response according to neurodivergent-safe principles.
        
        Structure:
        1. Direct answer to question (if applicable)
        2. Brief explanation (1-2 sentences)
        3. Offer to elaborate if needed
        
        Rules:
        - No metaphors or idioms
        - Simple, clear language
        - One idea per sentence
        - Predictable structure
        """
        if question:
            # Answer the question directly first
            response = f"**Answer:** {content}\n\n"
            response += "**More details:**\n"
        else:
            response = content + "\n\n**More details:**\n"
        
        # Offer to clarify
        response += "Make sense?\n\n"
        
        return response
    
    @staticmethod
    def get_crisis_response(level='moderate', facilitator_contact=None):
        """
        Get appropriate crisis response based on distress level.
        
        Levels:
        - mild: Simple de-escalation
        - moderate: Structured support
        - severe: Immediate intervention
        - crisis: Emergency contact
        """
        if level == 'crisis':
            response = "Let me make this simpler.\n\n"
            response += "**Too much information?** I'll use fewer words.\n\n"
            response += "**Don't understand?** I'll explain differently.\n\n"
            response += "**Need a break?** That's okay. Come back when ready.\n\n"
            
            if facilitator_contact:
                response += f"**Need help now?** Contact {facilitator_contact}\n\n"
            
            response += "Tell me what you need."
            return response
        
        elif level == 'severe':
            response = "I understand this is hard.\n\n"
            response += "Let's make it simpler.\n\n"
            response += "**What would help?**\n"
            response += "• Fewer words\n"
            response += "• Different explanation\n"
            response += "• Take a break\n\n"
            response += "Tell me."
            return response
        
        elif level == 'moderate':
            response = "I hear you.\n\n"
            response += "Would it help if I:\n"
            response += "• Use simpler words?\n"
            response += "• Explain differently?\n"
            response += "• Break this into smaller parts?\n\n"
            response += "Let me know."
            return response
        
        else:  # mild
            response = "Got it.\n\n"
            response += "Need me to:\n"
            response += "• Simplify?\n"
            response += "• Clarify?\n"
            response += "• Slow down?\n\n"
            response += "Just ask."
            return response


# Template responses for neurodivergent-safe communication
NEURODIVERGENT_TEMPLATES = {
    'greeting': "Hello! I'm MC AI. I will:\n- Use clear, simple language\n- Answer your questions directly\n- Stay on one topic at a time\n\nHow can I help you today?",
    
    'clarification_needed': "I want to make sure I understand correctly.\n\n**You asked about:** [topic]\n\n**Is this what you want to know?**\n- Option 1: [interpretation A]\n- Option 2: [interpretation B]\n\nTell me which one, or explain it another way.",
    
    'overwhelm_detected': "Let me make this simpler.\n\n[simplified content]\n\nIs this clearer? Or do you want me to break it down more?",
    
    'success_confirmation': "**Done!**\n\n[what was accomplished]\n\nWhat would you like to do next?",
    
    'error_explanation': "**Something went wrong.**\n\n**What happened:** [clear explanation]\n\n**What to do now:** [simple steps]\n\nNeed help? Ask me.",
}


def apply_neurodivergent_protocol(user_message, user_id, response_generator_function):
    """
    Main integration function - wraps around response generation to ensure
    neurodivergent-safe communication.
    
    Args:
        user_message: The user's input message
        user_id: User identifier
        response_generator_function: Function that generates the base response
    
    Returns:
        Safe, formatted response appropriate for neurodivergent users
    """
    protocol = NeurodivergentProtocol()
    
    # Check for distress signals FIRST
    distress_check = protocol.detect_distress_signals(user_message)
    if distress_check['distress_detected']:
        # User is in distress - use crisis response
        return {
            'response': protocol.get_crisis_response(),
            'metadata': {
                'protocol': 'neurodivergent_crisis',
                'distress_signal': distress_check['signal'],
                'safety_level': 'maximum'
            }
        }
    
    # Generate base response
    base_response = response_generator_function(user_message)
    
    # Apply safety formatting
    rules = protocol.get_communication_rules()
    
    # Simplify and format the response
    safe_response = protocol.format_safe_response(
        content=base_response,
        question=user_message if '?' in user_message else None
    )
    
    return {
        'response': safe_response,
        'metadata': {
            'protocol': 'neurodivergent',
            'safety_level': 'high',
            'formatting_applied': True
        }
    }
