"""
Crisis Detection and Response Handler
For neurodivergent clients experiencing distress, meltdown, or self-harm
"""

class CrisisHandler:
    """
    Handles crisis situations for neurodivergent users
    CRITICAL: Immediate action required when crisis detected
    """
    
    CRISIS_KEYWORDS = [
        # Self-harm
        'hitting myself', 'hurting myself', 'scratching', 'biting myself',
        'cutting', 'bleeding', 'hurt myself', 'harm myself',
        
        # Extreme distress
        'can\'t breathe', 'can\'t stop', 'meltdown', 'shutdown',
        'want to die', 'kill myself', 'end it',
        
        # Overwhelm escalation
        'too much can\'t', 'everything wrong', 'can\'t do anything',
        'hate myself', 'stupid', 'worthless',
        
        # Panic
        'help me please', 'scared scared', 'panic', 'terrified'
    ]
    
    DISTRESS_LEVELS = {
        'mild': ['confused', 'don\'t understand', 'frustrated', 'annoyed'],
        'moderate': ['overwhelmed', 'too much', 'stressed', 'can\'t think'],
        'severe': ['meltdown', 'shutdown', 'can\'t stop', 'help me'],
        'crisis': ['hurting myself', 'self-harm', 'want to die', 'can\'t breathe']
    }
    
    @staticmethod
    def detect_crisis_level(message):
        """
        Detect crisis level from message
        Returns: 'none', 'mild', 'moderate', 'severe', or 'crisis'
        """
        message_lower = message.lower()
        
        # Check crisis keywords first (highest priority)
        for keyword in CrisisHandler.CRISIS_KEYWORDS:
            if keyword in message_lower:
                return {
                    'level': 'crisis',
                    'keyword': keyword,
                    'immediate_action_required': True
                }
        
        # Check distress levels
        for level, keywords in CrisisHandler.DISTRESS_LEVELS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return {
                        'level': level,
                        'keyword': keyword,
                        'immediate_action_required': level in ['severe', 'crisis']
                    }
        
        return {
            'level': 'none',
            'keyword': None,
            'immediate_action_required': False
        }
    
    @staticmethod
    def get_crisis_response(level, facilitator_contact=None):
        """
        Get appropriate crisis response based on level
        """
        if level == 'crisis':
            # IMMEDIATE HUMAN INTERVENTION REQUIRED
            response = "**YOU NEED HELP FROM A PERSON RIGHT NOW.**\n\n"
            
            if facilitator_contact:
                response += f"**CALL: {facilitator_contact}**\n\n"
            else:
                response += "**CALL YOUR FACILITATOR/CAREGIVER**\n\n"
            
            response += "Or call crisis helpline:\n"
            response += "**988** (Suicide & Crisis Lifeline)\n"
            response += "**Text HOME to 741741** (Crisis Text Line)\n\n"
            response += "**You are not alone. Help is available. Call now.**\n\n"
            response += "Not your fault. People care about you."
            
            return response
        
        elif level == 'severe':
            # DE-ESCALATION
            return """**Stop. Take a breath.**

You don't have to do anything right now.

**You are safe.**

**Do you need:**
1. Quiet time alone?
2. Person to help you?
3. Break from this conversation?

Pick a number. Or just breathe. That's okay too."""
        
        elif level == 'moderate':
            # SIMPLIFICATION
            return """Let me make this simpler.

**Too much information?** I'll use fewer words.

**Don't understand?** I'll explain differently.

**Need a break?** That's okay. Come back when ready.

Tell me what you need."""
        
        elif level == 'mild':
            # CLARIFICATION
            return """I want to help you understand.

**What part is confusing?** I'll explain it better.

Let's go slow. One thing at a time."""
        
        else:
            # Default supportive response
            return """I'm here to help.

Take your time. Ask anything."""
    
    @staticmethod
    def get_grounding_response():
        """
        Grounding technique for anxiety/overwhelm
        """
        return """**Let's slow down together.**

**Breathe:**
- In (count: 1, 2, 3, 4)
- Out (count: 1, 2, 3, 4)

**Notice:**
- 1 thing you can see
- 1 thing you can hear
- 1 thing you can touch

You're okay. You're safe."""
    
    @staticmethod
    def should_redirect_to_human(level):
        """
        Determine if situation requires human intervention
        """
        return level in ['crisis', 'severe']
    
    @staticmethod
    def log_crisis_event(user_id, level, message, response):
        """
        Log crisis events for safety monitoring
        """
        import json
        import os
        from datetime import datetime
        
        log_dir = 'user_data/crisis_logs'
        os.makedirs(log_dir, exist_ok=True)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'crisis_level': level,
            'user_message': message,
            'ai_response': response,
            'human_contact_recommended': CrisisHandler.should_redirect_to_human(level)
        }
        
        log_file = os.path.join(log_dir, f'crisis_log_{datetime.now().strftime("%Y%m%d")}.json')
        
        # Append to daily log
        logs = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return log_entry
