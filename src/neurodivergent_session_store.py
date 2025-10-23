"""
Neurodivergent Session Store
Persistent storage for protocol activation that survives history truncation
WITH FILE LOCKING for multi-worker safety

CRITICAL SAFETY REQUIREMENT:
- Once activated for a session, protocol NEVER deactivates
- No automatic cleanup/expiration
- Persists forever to protect vulnerable clients
"""

import json
import os
import fcntl  # File locking for Unix/Linux (Replit platform)
from datetime import datetime

class NeurodivergentSessionStore:
    """
    Stores neurodivergent protocol activation status per session
    Survives conversation history truncation and worker restarts
    """
    
    def __init__(self):
        self.store_dir = 'user_data/neurodivergent_sessions'
        os.makedirs(self.store_dir, exist_ok=True)
        self.store_file = os.path.join(self.store_dir, 'active_sessions.json')
        # DO NOT cache in memory - reload from disk every time for multi-worker safety
    
    def _with_file_lock(self, operation, mode='r'):
        """
        Execute operation with file locking to prevent race conditions
        CRITICAL: Prevents concurrent write conflicts across workers
        
        Args:
            operation: Function that takes file handle and returns result
            mode: File open mode ('r' for read, 'r+' or 'a+' for write)
        """
        lock_file = self.store_file + '.lock'
        
        try:
            # Create lock file if it doesn't exist
            with open(lock_file, 'a'):
                pass
            
            # Open lock file and acquire exclusive lock
            with open(lock_file, 'r+') as lock_fd:
                # CRITICAL: Acquire lock (blocks if another worker has it)
                fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
                
                try:
                    # Execute operation while holding lock
                    result = operation()
                    return result
                finally:
                    # Release lock
                    fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)
        except Exception as e:
            print(f"⚠️ File lock operation failed: {e}")
            return {} if mode == 'r' else None
    
    def _load_store(self):
        """
        Load session store from disk WITH FILE LOCKING
        CRITICAL: Locked read ensures consistency during concurrent writes
        """
        def load_operation():
            if os.path.exists(self.store_file):
                try:
                    with open(self.store_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception as e:
                    print(f"⚠️ Session store load failed: {e}")
                    return {}
            return {}
        
        return self._with_file_lock(load_operation, mode='r')
    
    def _save_store(self, data):
        """
        Save session store to disk WITH FILE LOCKING
        CRITICAL: Locked write prevents concurrent write conflicts
        """
        def save_operation():
            try:
                # Write to temp file first
                temp_file = self.store_file + '.tmp'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Atomic rename
                import shutil
                shutil.move(temp_file, self.store_file)
                return True
            except Exception as e:
                print(f"⚠️ Session store save failed: {e}")
                return False
        
        return self._with_file_lock(save_operation, mode='r+')
    
    def _cleanup_expired(self, data):
        """
        NO CLEANUP - Sessions stay active FOREVER once protocol is triggered
        CRITICAL: Neurodivergent protocol MUST persist indefinitely for client safety
        
        Returns data unchanged (cleanup disabled for safety)
        """
        # SAFETY REQUIREMENT: Once activated, NEVER deactivate automatically
        # Vulnerable clients need protection that persists across days/weeks/months
        # Storage cost is negligible compared to preventing self-harm
        return data  # Return all sessions unchanged - NO expiration
    
    def activate_protocol(self, session_id, reason='unknown', user_id=None):
        """
        Mark protocol as active for this session
        CRITICAL: Uses file locking to prevent concurrent write conflicts
        
        Args:
            session_id: Unique identifier for this conversation/session
            reason: Why the protocol was activated (message/history/profile)
            user_id: Optional user ID if available
        """
        if not session_id:
            return False
        
        def activate_operation():
            # RELOAD from disk to get latest state (while holding lock)
            store_data = {}
            if os.path.exists(self.store_file):
                try:
                    with open(self.store_file, 'r', encoding='utf-8') as f:
                        store_data = json.load(f)
                except:
                    store_data = {}
            
            # Update session
            store_data[session_id] = {
                'active': True,
                'activated_at': datetime.now().isoformat(),
                'reason': reason,
                'user_id': user_id
            }
            
            # Clean expired before saving
            store_data = self._cleanup_expired(store_data)
            
            # SAVE (while still holding lock)
            try:
                temp_file = self.store_file + '.tmp'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(store_data, f, indent=2, ensure_ascii=False)
                import shutil
                shutil.move(temp_file, self.store_file)
                return True
            except Exception as e:
                print(f"⚠️ Save failed: {e}")
                return False
        
        success = self._with_file_lock(activate_operation, mode='r+')
        
        if success:
            print(f"🛡️  PERSISTENT ACTIVATION: Session {session_id} marked as neurodivergent (LOCKED)")
        
        return success
    
    def is_protocol_active(self, session_id):
        """
        Check if protocol is active for this session
        CRITICAL: Reloads from disk EVERY TIME to ensure multi-worker consistency
        
        Returns True if protocol was activated at any point in this session,
        even if conversation history has been truncated or handled by different worker
        """
        if not session_id:
            return False
        
        # RELOAD from disk to get latest state (critical for multi-worker)
        store_data = self._load_store()
        
        session_data = store_data.get(session_id, {})
        return session_data.get('active', False)
    
    def get_session_info(self, session_id):
        """
        Get full session information
        CRITICAL: Reloads from disk for multi-worker consistency
        """
        store_data = self._load_store()
        return store_data.get(session_id, {})
    
    def deactivate_protocol(self, session_id):
        """
        Deactivate protocol for this session
        (Should rarely be used - once activated, should stay active)
        CRITICAL: Reloads from disk, updates, saves - works across workers
        """
        # RELOAD from disk
        store_data = self._load_store()
        
        if session_id in store_data:
            del store_data[session_id]
            # SAVE atomically
            self._save_store(store_data)


# Global singleton instance
_session_store = None

def get_session_store():
    """Get global session store instance"""
    global _session_store
    if _session_store is None:
        _session_store = NeurodivergentSessionStore()
    return _session_store
