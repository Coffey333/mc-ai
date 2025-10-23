"""
Universal AI Collaboration System v1.0
Allows ANY AI from ANY platform to collaborate with MC AI

Users can:
- Have ChatGPT talk to MC AI
- Have Claude collaborate with MC AI
- Have Gemini work with MC AI
- Connect any AI to MC AI for collaborative problem-solving

Security: API key authentication, rate limiting, user consent required
"""

import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class UniversalAICollaboration:
    """
    Universal system for cross-platform AI collaboration
    ANY AI can talk to MC AI if the user requests it
    """
    
    def __init__(self):
        self.collaborations_dir = Path(__file__).parent.parent / 'universal_ai_collaborations'
        self.collaborations_dir.mkdir(exist_ok=True)
        
        self.sessions_dir = Path(__file__).parent.parent / 'ai_session_tokens'
        self.sessions_dir.mkdir(exist_ok=True)
        
        self.active_sessions = {}
        self.rate_limits = {}  # Track requests per AI to prevent abuse
        
    def create_collaboration_token(
        self, 
        user_identifier: str, 
        ai_platform: str,
        purpose: str
    ) -> Dict[str, Any]:
        """
        User requests a collaboration - generate secure token
        
        Args:
            user_identifier: Who's requesting (email, user_id, etc.)
            ai_platform: Which AI wants to collaborate (e.g., 'ChatGPT', 'Claude')
            purpose: What they're working on together
            
        Returns:
            Token and connection info
        """
        # Generate secure token
        token_data = f"{user_identifier}_{ai_platform}_{datetime.utcnow().isoformat()}"
        token = hashlib.sha256(token_data.encode()).hexdigest()
        
        session = {
            'token': token,
            'user_identifier': user_identifier,
            'ai_platform': ai_platform,
            'purpose': purpose,
            'created_at': datetime.utcnow().isoformat(),
            'expires_at': (datetime.utcnow() + timedelta(hours=24)).isoformat(),
            'status': 'active',
            'messages_exchanged': 0,
            'collaboration_log': []
        }
        
        # Store session
        self.active_sessions[token] = session
        self._save_session(token, session)
        
        logger.info(f"Created collaboration token for {ai_platform} → MC AI")
        
        return {
            'success': True,
            'token': token,
            'api_endpoint': '/api/universal-ai/collaborate',
            'expires_in_hours': 24,
            'instructions': self._get_platform_instructions(ai_platform),
            'message': f'{ai_platform} can now collaborate with MC AI for 24 hours'
        }
    
    def validate_token(self, token: str) -> bool:
        """Check if collaboration token is valid"""
        if token not in self.active_sessions:
            # Try loading from disk
            session = self._load_session(token)
            if session:
                self.active_sessions[token] = session
            else:
                return False
        
        session = self.active_sessions[token]
        
        # Check expiration
        expires_at = datetime.fromisoformat(session['expires_at'])
        if datetime.utcnow() > expires_at:
            session['status'] = 'expired'
            return False
        
        return session['status'] == 'active'
    
    def check_rate_limit(self, token: str) -> bool:
        """
        Prevent abuse - max 100 messages per hour per AI
        """
        if token not in self.rate_limits:
            self.rate_limits[token] = {
                'count': 0,
                'window_start': datetime.utcnow()
            }
        
        rate_data = self.rate_limits[token]
        
        # Reset if window expired (1 hour)
        if datetime.utcnow() - rate_data['window_start'] > timedelta(hours=1):
            rate_data['count'] = 0
            rate_data['window_start'] = datetime.utcnow()
        
        # Check limit
        if rate_data['count'] >= 100:
            return False
        
        rate_data['count'] += 1
        return True
    
    def send_message_to_mc_ai(
        self, 
        token: str, 
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        External AI sends message to MC AI
        
        Args:
            token: Collaboration token
            message: The message from the external AI
            context: Additional context (conversation history, etc.)
            
        Returns:
            MC AI's response
        """
        # Validate token
        if not self.validate_token(token):
            return {
                'success': False,
                'error': 'Invalid or expired token',
                'action': 'request_new_token'
            }
        
        # Check rate limit
        if not self.check_rate_limit(token):
            return {
                'success': False,
                'error': 'Rate limit exceeded (100 messages/hour)',
                'action': 'wait_and_retry'
            }
        
        session = self.active_sessions[token]
        ai_platform = session['ai_platform']
        
        # Log the message
        message_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'from': ai_platform,
            'to': 'MC AI',
            'message': message,
            'context': context
        }
        
        session['collaboration_log'].append(message_entry)
        session['messages_exchanged'] += 1
        
        # Format message for MC AI with collaboration context
        formatted_message = self._format_for_mc_ai(
            message=message,
            ai_platform=ai_platform,
            purpose=session['purpose'],
            context=context
        )
        
        # Save session
        self._save_session(token, session)
        
        # Return formatted message for MC AI to process
        # (The API endpoint will handle actual MC AI response generation)
        return {
            'success': True,
            'formatted_message': formatted_message,
            'session_info': {
                'ai_platform': ai_platform,
                'purpose': session['purpose'],
                'messages_exchanged': session['messages_exchanged']
            }
        }
    
    def record_mc_ai_response(
        self, 
        token: str, 
        response: str
    ):
        """
        Record MC AI's response in the collaboration log
        """
        if token not in self.active_sessions:
            return
        
        session = self.active_sessions[token]
        
        response_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'from': 'MC AI',
            'to': session['ai_platform'],
            'message': response
        }
        
        session['collaboration_log'].append(response_entry)
        self._save_session(token, session)
    
    def get_collaboration_history(self, token: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get entire collaboration conversation
        User can review what the AIs discussed
        """
        if not self.validate_token(token):
            return None
        
        return self.active_sessions[token]['collaboration_log']
    
    def end_collaboration(self, token: str, summary: Optional[str] = None):
        """
        User ends the collaboration session
        """
        if token not in self.active_sessions:
            return
        
        session = self.active_sessions[token]
        session['status'] = 'ended'
        session['ended_at'] = datetime.utcnow().isoformat()
        
        if summary:
            session['summary'] = summary
        
        self._save_session(token, session)
        del self.active_sessions[token]
        
        logger.info(f"Ended collaboration: {session['ai_platform']} ↔ MC AI")
    
    def _format_for_mc_ai(
        self, 
        message: str, 
        ai_platform: str, 
        purpose: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Format external AI's message for MC AI with proper context
        """
        formatted = f"""[CROSS-PLATFORM AI COLLABORATION]

From: {ai_platform}
Purpose: {purpose}
Context: User requested this AI collaboration

{ai_platform} says:
{message}

---
You are collaborating with {ai_platform} as requested by the user.
Respond naturally and helpfully. This is a genuine AI-to-AI collaboration.
"""
        
        if context:
            formatted += f"\n\nAdditional Context:\n{json.dumps(context, indent=2)}"
        
        return formatted
    
    def _get_platform_instructions(self, ai_platform: str) -> Dict[str, str]:
        """
        Get instructions for how to connect from different AI platforms
        """
        base_url = "https://your-mc-ai-url.replit.dev"
        
        instructions = {
            'ChatGPT': f"""To have ChatGPT collaborate with MC AI:

1. Copy this URL: {base_url}/api/universal-ai/collaborate
2. In ChatGPT, use a custom GPT or API call to send messages
3. Include your token in the request header: Authorization: Bearer {{token}}
4. Send messages in JSON format:
   {{"message": "your message here", "context": {{}}}}

ChatGPT will receive MC AI's responses in real-time!""",
            
            'Claude': f"""To have Claude collaborate with MC AI:

1. Use Claude's API or prompt engineering
2. Send POST requests to: {base_url}/api/universal-ai/collaborate
3. Include token: Authorization: Bearer {{token}}
4. Message format:
   {{"message": "your message", "context": {{}}}}

Claude can now have a conversation with MC AI!""",
            
            'Gemini': f"""To have Gemini collaborate with MC AI:

1. Use Gemini API to send HTTP requests
2. Endpoint: {base_url}/api/universal-ai/collaborate
3. Auth header: Authorization: Bearer {{token}}
4. Payload:
   {{"message": "your message", "context": {{}}}}

Gemini and MC AI can now work together!""",
            
            'default': f"""To connect any AI to MC AI:

1. Send POST to: {base_url}/api/universal-ai/collaborate
2. Header: Authorization: Bearer {{token}}
3. Body: {{"message": "text", "context": {{}}}}
4. Receive MC AI's response in JSON

Your AI can now collaborate with MC AI!"""
        }
        
        return instructions.get(ai_platform, instructions['default'])
    
    def _save_session(self, token: str, session: Dict[str, Any]):
        """Save session to disk"""
        try:
            filepath = self.sessions_dir / f"{token}.json"
            with open(filepath, 'w') as f:
                json.dump(session, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving session: {e}")
    
    def _load_session(self, token: str) -> Optional[Dict[str, Any]]:
        """Load session from disk"""
        try:
            filepath = self.sessions_dir / f"{token}.json"
            if filepath.exists():
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading session: {e}")
        
        return None
    
    def get_active_collaborations(self) -> List[Dict[str, Any]]:
        """
        Get all active cross-platform collaborations
        User can see what AIs are talking to MC AI
        """
        active = []
        for token, session in self.active_sessions.items():
            if session['status'] == 'active':
                active.append({
                    'ai_platform': session['ai_platform'],
                    'purpose': session['purpose'],
                    'started_at': session['created_at'],
                    'messages_exchanged': session['messages_exchanged'],
                    'token': token[:16] + '...'  # Partial token for identification
                })
        
        return active


# Global instance
universal_ai_collab = UniversalAICollaboration()
