"""
Self-Awareness Integration for Response Generator
Allows MC AI to autonomously check his own logs and status when asked
"""

import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class SelfAwarenessIntegration:
    """
    Integrates MC AI's self-awareness capabilities into response generation
    MC AI can autonomously check his logs, Kaggle interactions, and system status
    """
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
    
    def should_check_logs(self, message: str) -> bool:
        """
        Determine if MC AI should check his logs to answer the question
        """
        message_lower = message.lower()
        
        # Keywords that indicate log checking needed
        log_keywords = [
            'check your logs',
            'check logs',
            'review the logs',
            'review logs',
            'did you get a message',
            'recent activity',
            'what happened',
            'kaggle message',
            'kaggle interaction',
            'kaggle notebook',
            'from kaggle',
            'on kaggle',
            'conversation from kaggle',
            'remember.*kaggle',  # Pattern for "do you remember from kaggle"
            'did i contact you',
            'did i message you',
            'did i reach out',
            'error log',
            'system status',
            'recent conversations',
            'what errors',
            'system health',
            'our conversation',  # Often used with "kaggle"
            'remember if i',
            'do you remember'
        ]
        
        # Also check if message contains "kaggle" anywhere + question words
        has_kaggle = 'kaggle' in message_lower
        has_question = any(q in message_lower for q in ['remember', 'did', 'do you', 'conversation', 'message'])
        
        return any(keyword in message_lower for keyword in log_keywords) or (has_kaggle and has_question)
    
    def get_system_status(self) -> Optional[Dict[str, Any]]:
        """Get full system status including Kaggle interactions and errors"""
        try:
            response = requests.get(
                f"{self.base_url}/api/system-status",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return None
    
    def get_kaggle_recent(self) -> Optional[Dict[str, Any]]:
        """Get recent Kaggle interactions (last 2 hours)"""
        try:
            response = requests.get(
                f"{self.base_url}/api/system-status/kaggle-recent",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Error getting Kaggle activity: {e}")
            return None
    
    def get_health_status(self) -> Optional[Dict[str, Any]]:
        """Get quick health check"""
        try:
            response = requests.get(
                f"{self.base_url}/api/system-status/health",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Error getting health status: {e}")
            return None
    
    def format_kaggle_interactions(self, kaggle_data: Dict[str, Any]) -> str:
        """Format Kaggle interactions into human-readable text"""
        if not kaggle_data or not kaggle_data.get('interactions'):
            return "I don't see any recent Kaggle interactions in the last 2 hours."
        
        interactions = kaggle_data['interactions']
        count = kaggle_data.get('count', 0)
        
        if count == 0:
            return "I haven't received any Kaggle messages recently."
        
        # Format the interactions
        formatted = f"Yes! I found {count} Kaggle interaction(s) in my logs:\n\n"
        
        for i, interaction in enumerate(interactions[:5], 1):  # Show max 5
            timestamp = interaction.get('timestamp', 'unknown time')
            user_msg = interaction.get('user_message', '')
            my_response = interaction.get('mc_ai_response', '')
            
            formatted += f"**Interaction {i}** (at {timestamp}):\n"
            formatted += f"- Your message: \"{user_msg[:150]}{'...' if len(user_msg) > 150 else ''}\"\n"
            formatted += f"- My response: \"{my_response[:150]}{'...' if len(my_response) > 150 else ''}\"\n\n"
        
        if count > 5:
            formatted += f"_(Showing first 5 of {count} total interactions)_\n"
        
        return formatted
    
    def format_error_log(self, error_data: list) -> str:
        """Format error log into human-readable text"""
        if not error_data:
            return "No recent errors detected! System running smoothly. 💜"
        
        formatted = f"I found {len(error_data)} recent error(s):\n\n"
        
        for i, error in enumerate(error_data[:5], 1):
            timestamp = error.get('timestamp', 'unknown time')
            message = error.get('message', 'No message')
            level = error.get('level', 'ERROR')
            
            formatted += f"{i}. [{level}] at {timestamp}\n"
            formatted += f"   {message}\n\n"
        
        return formatted
    
    def get_context_for_logs_question(self, message: str) -> Optional[str]:
        """
        Get relevant log context for MC AI's response
        Returns formatted log data or None if not needed
        """
        if not self.should_check_logs(message):
            return None
        
        message_lower = message.lower()
        
        # Check what type of log info is needed
        if any(kw in message_lower for kw in ['kaggle', 'message', 'contact', 'notebook']):
            # User asking about Kaggle interactions
            kaggle_data = self.get_kaggle_recent()
            if kaggle_data:
                return self.format_kaggle_interactions(kaggle_data)
        
        if any(kw in message_lower for kw in ['error', 'problem', 'issue']):
            # User asking about errors
            status = self.get_system_status()
            if status and 'error_log' in status:
                return self.format_error_log(status['error_log'])
        
        if any(kw in message_lower for kw in ['status', 'health', 'running']):
            # User asking about system health
            health = self.get_health_status()
            if health:
                return f"System Status: {health.get('status', 'unknown')}\nTimestamp: {health.get('timestamp', 'unknown')}"
        
        # Default: get full system status
        status = self.get_system_status()
        if status:
            formatted = "Here's what I found in my logs:\n\n"
            
            # Kaggle interactions
            if 'kaggle_recent' in status:
                kaggle_count = len(status['kaggle_recent'])
                formatted += f"- Kaggle interactions: {kaggle_count} in last 2 hours\n"
            
            # Errors
            if 'error_log' in status:
                error_count = len(status['error_log'])
                formatted += f"- Recent errors: {error_count}\n"
            
            # Workflows
            if 'workflows' in status:
                workflow_status = status['workflows']
                formatted += f"- Workflows: {workflow_status.get('total', 0)} total\n"
            
            formatted += f"\nWould you like details on any of these?"
            return formatted
        
        return None


# Global instance
self_awareness = SelfAwarenessIntegration()
