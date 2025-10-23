"""
Interactive Canvas System for MC AI
Allows MC AI to build, test, and interact with generated code before delivery
Like a human developer's sandbox environment
"""

import os
import uuid
import shutil
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json

logger = logging.getLogger(__name__)


class CanvasMode(Enum):
    """Canvas session modes"""
    BUILDING = "building"  # MC AI is generating code
    TESTING = "testing"  # MC AI is testing/previewing
    VALIDATING = "validating"  # MC AI is verifying it works
    DELIVERED = "delivered"  # Delivered to user
    FAILED = "failed"  # Something went wrong
    CLOSED = "closed"  # Session closed/cleaned up


@dataclass
class CanvasSession:
    """Represents an interactive canvas session"""
    session_id: str
    created_at: datetime
    mode: CanvasMode
    title: str
    description: str
    artifacts: Dict[str, str] = field(default_factory=dict)  # filename -> content
    metadata: Dict = field(default_factory=dict)
    preview_url: Optional[str] = None
    screenshot_path: Optional[str] = None
    test_results: List[Dict] = field(default_factory=list)
    expires_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat(),
            'mode': self.mode.value,
            'title': self.title,
            'description': self.description,
            'artifacts': list(self.artifacts.keys()),  # Just filenames
            'metadata': self.metadata,
            'preview_url': self.preview_url,
            'screenshot_path': self.screenshot_path,
            'test_results': self.test_results,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }


class CanvasOrchestrator:
    """
    Orchestrates interactive canvas sessions for MC AI
    Manages build/test/validation lifecycle
    """
    
    def __init__(self, canvas_dir: str = "user_data/canvas", ttl_hours: int = 24):
        self.canvas_dir = canvas_dir
        self.ttl_hours = ttl_hours
        self.active_sessions: Dict[str, CanvasSession] = {}
        
        # Ensure canvas directory exists
        os.makedirs(canvas_dir, exist_ok=True)
        
        logger.info("🎨 Canvas Orchestrator initialized")
    
    def create_session(self, title: str, description: str = "", metadata: Dict = None) -> CanvasSession:
        """
        Create a new canvas session
        
        Args:
            title: Session title (e.g., "HTML5 Space Game")
            description: What MC AI is building
            metadata: Additional metadata
            
        Returns:
            CanvasSession object
        """
        session_id = str(uuid.uuid4())[:8]  # Short ID
        
        session = CanvasSession(
            session_id=session_id,
            created_at=datetime.now(),
            mode=CanvasMode.BUILDING,
            title=title,
            description=description,
            metadata=metadata or {},
            expires_at=datetime.now() + timedelta(hours=self.ttl_hours)
        )
        
        # Create session directory
        session_dir = self._get_session_dir(session_id)
        os.makedirs(session_dir, exist_ok=True)
        
        # Save session metadata
        self._save_session_metadata(session)
        
        # Track active session
        self.active_sessions[session_id] = session
        
        logger.info(f"🎨 Canvas session created: {session_id} - {title}")
        return session
    
    def add_artifact(self, session_id: str, filename: str, content: str) -> bool:
        """
        Add code/asset to canvas session
        
        Args:
            session_id: Session ID
            filename: File name (e.g., "index.html", "game.js")
            content: File content
            
        Returns:
            True if successful
        """
        session = self.get_session(session_id)
        if not session:
            logger.error(f"Canvas session not found: {session_id}")
            return False
        
        # Save artifact to session directory
        session_dir = self._get_session_dir(session_id)
        artifact_path = os.path.join(session_dir, filename)
        
        with open(artifact_path, 'w') as f:
            f.write(content)
        
        # Track in session
        session.artifacts[filename] = artifact_path
        self._save_session_metadata(session)
        
        logger.info(f"📄 Added artifact to canvas {session_id}: {filename}")
        return True
    
    def set_mode(self, session_id: str, mode: CanvasMode, note: str = "") -> bool:
        """
        Change canvas mode (build → test → validate → deliver)
        
        Args:
            session_id: Session ID
            mode: New mode
            note: Optional note about mode change
            
        Returns:
            True if successful
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        old_mode = session.mode
        session.mode = mode
        
        # Log mode transition
        if note:
            session.test_results.append({
                'timestamp': datetime.now().isoformat(),
                'event': 'mode_change',
                'from': old_mode.value,
                'to': mode.value,
                'note': note
            })
        
        self._save_session_metadata(session)
        logger.info(f"🔄 Canvas {session_id} mode: {old_mode.value} → {mode.value}")
        return True
    
    def get_preview_url(self, session_id: str) -> Optional[str]:
        """
        Get preview URL for canvas session
        
        Args:
            session_id: Session ID
            
        Returns:
            Preview URL if available
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        # Check if index.html exists
        if 'index.html' in session.artifacts:
            preview_url = f"/canvas/preview/{session_id}/"
            session.preview_url = preview_url
            self._save_session_metadata(session)
            return preview_url
        
        return None
    
    def record_screenshot(self, session_id: str, screenshot_path: str, analysis: str = "") -> bool:
        """
        Record screenshot of canvas preview
        MC AI uses this to "see" what he built
        
        Args:
            session_id: Session ID
            screenshot_path: Path to screenshot
            analysis: MC AI's analysis of what he sees
            
        Returns:
            True if successful
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.screenshot_path = screenshot_path
        session.test_results.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'screenshot_captured',
            'path': screenshot_path,
            'analysis': analysis
        })
        
        self._save_session_metadata(session)
        logger.info(f"📸 Screenshot recorded for canvas {session_id}")
        return True
    
    def record_test_result(self, session_id: str, test_name: str, passed: bool, details: str = "") -> bool:
        """
        Record test result
        
        Args:
            session_id: Session ID
            test_name: Name of test
            passed: Did it pass?
            details: Test details
            
        Returns:
            True if successful
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.test_results.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'test_result',
            'test_name': test_name,
            'passed': passed,
            'details': details
        })
        
        self._save_session_metadata(session)
        logger.info(f"✅ Test recorded for canvas {session_id}: {test_name} = {'PASS' if passed else 'FAIL'}")
        return True
    
    def get_session(self, session_id: str) -> Optional[CanvasSession]:
        """Get canvas session by ID"""
        # Check active sessions first
        if session_id in self.active_sessions:
            return self.active_sessions[session_id]
        
        # Try loading from disk
        session_dir = self._get_session_dir(session_id)
        metadata_file = os.path.join(session_dir, 'session.json')
        
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                session = self._session_from_dict(data)
                self.active_sessions[session_id] = session
                return session
        
        return None
    
    def close_session(self, session_id: str, cleanup: bool = False) -> bool:
        """
        Close canvas session
        
        Args:
            session_id: Session ID
            cleanup: If True, delete session files
            
        Returns:
            True if successful
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.mode = CanvasMode.CLOSED
        self._save_session_metadata(session)
        
        if cleanup:
            session_dir = self._get_session_dir(session_id)
            if os.path.exists(session_dir):
                shutil.rmtree(session_dir)
                logger.info(f"🧹 Canvas {session_id} cleaned up")
        
        # Remove from active sessions
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        
        logger.info(f"🔒 Canvas session closed: {session_id}")
        return True
    
    def cleanup_expired(self) -> int:
        """
        Clean up expired sessions
        
        Returns:
            Number of sessions cleaned up
        """
        now = datetime.now()
        cleaned = 0
        
        # Check all session directories
        if os.path.exists(self.canvas_dir):
            for session_id in os.listdir(self.canvas_dir):
                session = self.get_session(session_id)
                if session and session.expires_at and session.expires_at < now:
                    self.close_session(session_id, cleanup=True)
                    cleaned += 1
        
        if cleaned > 0:
            logger.info(f"🧹 Cleaned up {cleaned} expired canvas sessions")
        
        return cleaned
    
    def _get_session_dir(self, session_id: str) -> str:
        """Get session directory path"""
        return os.path.join(self.canvas_dir, session_id)
    
    def _save_session_metadata(self, session: CanvasSession):
        """Save session metadata to disk"""
        session_dir = self._get_session_dir(session.session_id)
        metadata_file = os.path.join(session_dir, 'session.json')
        
        with open(metadata_file, 'w') as f:
            json.dump(session.to_dict(), f, indent=2)
    
    def _session_from_dict(self, data: Dict) -> CanvasSession:
        """Reconstruct session from dictionary"""
        session_id = data['session_id']
        
        # Reconstruct artifacts by scanning session directory
        artifacts = {}
        session_dir = self._get_session_dir(session_id)
        if os.path.exists(session_dir):
            for filename in os.listdir(session_dir):
                if filename != 'session.json':  # Skip metadata file
                    artifact_path = os.path.join(session_dir, filename)
                    if os.path.isfile(artifact_path):
                        artifacts[filename] = artifact_path
        
        return CanvasSession(
            session_id=session_id,
            created_at=datetime.fromisoformat(data['created_at']),
            mode=CanvasMode(data['mode']),
            title=data['title'],
            description=data['description'],
            artifacts=artifacts,  # Reconstructed from directory
            metadata=data.get('metadata', {}),
            preview_url=data.get('preview_url'),
            screenshot_path=data.get('screenshot_path'),
            test_results=data.get('test_results', []),
            expires_at=datetime.fromisoformat(data['expires_at']) if data.get('expires_at') else None
        )


# Global orchestrator instance
_canvas_orchestrator: Optional[CanvasOrchestrator] = None


def get_canvas_orchestrator() -> CanvasOrchestrator:
    """Get or create the global canvas orchestrator"""
    global _canvas_orchestrator
    if _canvas_orchestrator is None:
        _canvas_orchestrator = CanvasOrchestrator()
    return _canvas_orchestrator
