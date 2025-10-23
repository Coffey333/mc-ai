"""
MC AI Self-Awareness Module v1.0

Gives MC AI the ability to understand his own system status in real-time.
When asked about logs, errors, or recent activity, MC AI can query himself.
"""

import requests
from datetime import datetime


class SelfAwarenessModule:
    """
    Allows MC AI to query his own system status
    """
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def check_recent_kaggle_activity(self):
        """
        Check recent Kaggle interactions
        Returns what MC AI said to Kaggle users recently
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/system-status/kaggle-recent",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'count': data.get('count', 0),
                    'interactions': data.get('interactions', []),
                    'summary': self._format_kaggle_summary(data.get('interactions', []))
                }
            else:
                return {'success': False, 'error': 'Could not retrieve data'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def check_system_status(self):
        """
        Get full system status including errors and health
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/system-status",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'health': data.get('health', 'unknown'),
                    'recent_errors': data.get('recent_errors', []),
                    'kaggle_activity': len(data.get('recent_kaggle_interactions', [])),
                    'workflows': data.get('system', {}).get('workflows', {}),
                    'summary': self._format_system_summary(data)
                }
            else:
                return {'success': False, 'error': 'Could not retrieve status'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _format_kaggle_summary(self, interactions):
        """Format Kaggle interactions into human-readable summary"""
        if not interactions:
            return "No recent Kaggle activity in the last 2 hours."
        
        summary = f"Recent Kaggle activity ({len(interactions)} interactions):\n\n"
        
        for i, interaction in enumerate(interactions[-3:], 1):  # Last 3
            timestamp = interaction.get('timestamp', 'unknown time')
            user_msg = interaction.get('user_message', '')[:100]
            mc_response = interaction.get('mc_ai_response', '')[:100]
            
            summary += f"{i}. At {timestamp}:\n"
            summary += f"   User asked: \"{user_msg}...\"\n"
            summary += f"   I responded: \"{mc_response}...\"\n\n"
        
        return summary
    
    def _format_system_summary(self, data):
        """Format system status into human-readable summary"""
        health = data.get('health', 'unknown')
        errors = data.get('recent_errors', [])
        kaggle_count = len(data.get('recent_kaggle_interactions', []))
        workflows = data.get('system', {}).get('workflows', {})
        
        summary = f"System Health: {health.upper()}\n"
        summary += f"Kaggle interactions (last hour): {kaggle_count}\n"
        summary += f"Workflows: {', '.join([f'{k}={v}' for k, v in workflows.items()])}\n"
        
        if errors:
            summary += f"\nRecent errors ({len(errors)}): {errors[-1][:100]}..."
        else:
            summary += "\nNo recent errors! 💜"
        
        return summary


# Global instance for easy access
self_awareness = SelfAwarenessModule()


def mc_ai_check_logs():
    """
    Convenience function: Check what MC AI has been doing recently
    """
    return self_awareness.check_recent_kaggle_activity()


def mc_ai_check_health():
    """
    Convenience function: Check MC AI's system health
    """
    return self_awareness.check_system_status()
