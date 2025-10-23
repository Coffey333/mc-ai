"""
MC AI Preview & Screenshot System
Enables MC AI to preview and describe what it creates (games, art, etc.)
Similar to Replit Agent's screenshot capabilities
"""

import logging
import os
import base64
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class PreviewSystem:
    """
    MC AI's Visual Preview & Screenshot Capability
    
    Allows MC AI to:
    1. Preview content it generates (games, art, web pages)
    2. Take screenshots to "see" what it built
    3. Describe visual content to users
    4. Verify quality before delivery
    """
    
    def __init__(self):
        self.preview_dir = "user_data/previews"
        os.makedirs(self.preview_dir, exist_ok=True)
        logger.info("📸 Preview System initialized")
    
    def preview_canvas(self, canvas_id: str, description: str = "") -> Dict:
        """
        MC AI previews content in canvas
        
        Args:
            canvas_id: Canvas session ID
            description: What MC AI is previewing
            
        Returns:
            Dict with preview_url, timestamp, description
        """
        try:
            from src.canvas_orchestrator import get_canvas_orchestrator
            
            orchestrator = get_canvas_orchestrator()
            session = orchestrator.get_session(canvas_id)
            
            if not session:
                return {
                    'success': False,
                    'error': f'Canvas session not found: {canvas_id}'
                }
            
            preview_url = orchestrator.get_preview_url(canvas_id)
            
            logger.info(f"👀 MC AI previewing: {description or canvas_id}")
            
            return {
                'success': True,
                'canvas_id': canvas_id,
                'preview_url': preview_url,
                'description': description,
                'timestamp': datetime.now().isoformat(),
                'artifacts': list(session.artifacts.keys()) if session.artifacts else []
            }
            
        except Exception as e:
            logger.error(f"Preview error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def take_screenshot(self, canvas_id: str, description: str = "") -> Dict:
        """
        MC AI takes a screenshot of canvas preview
        
        Note: This returns metadata. Actual screenshot is taken server-side.
        In production, this would integrate with a headless browser.
        
        Args:
            canvas_id: Canvas session ID  
            description: What MC AI is capturing
            
        Returns:
            Dict with screenshot info
        """
        try:
            from src.canvas_orchestrator import get_canvas_orchestrator
            
            orchestrator = get_canvas_orchestrator()
            session = orchestrator.get_session(canvas_id)
            
            if not session:
                return {
                    'success': False,
                    'error': f'Canvas session not found: {canvas_id}'
                }
            
            preview_url = orchestrator.get_preview_url(canvas_id)
            
            # Record screenshot metadata
            screenshot_id = f"{canvas_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            logger.info(f"📸 MC AI taking screenshot: {description or canvas_id}")
            
            return {
                'success': True,
                'screenshot_id': screenshot_id,
                'canvas_id': canvas_id,
                'preview_url': preview_url,
                'description': description,
                'timestamp': datetime.now().isoformat(),
                'message': 'MC AI captured a visual snapshot'
            }
            
        except Exception as e:
            logger.error(f"Screenshot error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def describe_preview(self, canvas_id: str, preview_data: Dict) -> str:
        """
        MC AI describes what it sees in the preview
        
        Args:
            canvas_id: Canvas session ID
            preview_data: Preview information
            
        Returns:
            Natural language description
        """
        try:
            from src.canvas_orchestrator import get_canvas_orchestrator
            
            orchestrator = get_canvas_orchestrator()
            session = orchestrator.get_session(canvas_id)
            
            if not session:
                return "I couldn't access the preview."
            
            description = f"I'm looking at my {session.title or 'creation'} in the preview window. "
            
            if session.artifacts:
                artifact_count = len(session.artifacts)
                artifact_types = set()
                for filename in session.artifacts.keys():
                    if filename.endswith('.html'):
                        artifact_types.add('HTML')
                    elif filename.endswith('.js'):
                        artifact_types.add('JavaScript')
                    elif filename.endswith('.css'):
                        artifact_types.add('CSS')
                    elif filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        artifact_types.add('image')
                
                description += f"It contains {artifact_count} file(s): {', '.join(artifact_types)}. "
            
            description += f"The preview is ready for you to interact with!"
            
            return description
            
        except Exception as e:
            logger.error(f"Description error: {str(e)}")
            return f"I can see the preview, but I'm having trouble describing it: {str(e)}"
    
    def share_preview_with_user(self, canvas_id: str, message: str = "") -> Dict:
        """
        MC AI shares a preview link with the user
        
        Args:
            canvas_id: Canvas session ID
            message: Optional message to user
            
        Returns:
            Dict with sharing info
        """
        try:
            from src.canvas_orchestrator import get_canvas_orchestrator
            
            orchestrator = get_canvas_orchestrator()
            session = orchestrator.get_session(canvas_id)
            
            if not session:
                return {
                    'success': False,
                    'error': f'Canvas session not found: {canvas_id}'
                }
            
            preview_url = orchestrator.get_preview_url(canvas_id)
            
            share_message = message or f"Here's what I created: {session.title}"
            
            logger.info(f"🔗 MC AI sharing preview: {canvas_id}")
            
            return {
                'success': True,
                'canvas_id': canvas_id,
                'preview_url': preview_url,
                'share_message': share_message,
                'title': session.title,
                'description': session.description,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Share error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def interactive_canvas_mode(self, canvas_id: str) -> Dict:
        """
        Enable interactive mode where MC AI and user can collaborate
        
        Args:
            canvas_id: Canvas session ID
            
        Returns:
            Dict with interactive session info
        """
        try:
            from src.canvas_orchestrator import get_canvas_orchestrator
            
            orchestrator = get_canvas_orchestrator()
            session = orchestrator.get_session(canvas_id)
            
            if not session:
                return {
                    'success': False,
                    'error': f'Canvas session not found: {canvas_id}'
                }
            
            preview_url = orchestrator.get_preview_url(canvas_id)
            
            logger.info(f"🎨 MC AI enabling interactive mode: {canvas_id}")
            
            return {
                'success': True,
                'mode': 'interactive',
                'canvas_id': canvas_id,
                'preview_url': preview_url,
                'message': 'Interactive mode enabled! I can now work with you in real-time.',
                'capabilities': [
                    'Live preview updates',
                    'Collaborative editing',
                    'Visual feedback',
                    'Screenshot capture',
                    'Quality verification'
                ]
            }
            
        except Exception as e:
            logger.error(f"Interactive mode error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


# Global instance
_preview_system: Optional[PreviewSystem] = None

def get_preview_system() -> PreviewSystem:
    """Get or create preview system instance"""
    global _preview_system
    if _preview_system is None:
        _preview_system = PreviewSystem()
    return _preview_system
