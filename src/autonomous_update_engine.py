"""
MC AI Autonomous Update Engine

Allows MC AI to make safe, self-directed updates to expand capabilities
while maintaining strict safeguards against core system modifications.

Safety Features:
- Whitelist of approved operations only
- File path validation (approved directories only)
- Size limits per change and per session
- Syntax validation before applying
- Git commits for rollback
- Comprehensive audit logging
"""

import json
import os
from datetime import datetime
from pathlib import Path
import subprocess
from typing import Dict, List, Optional, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutonomousUpdateEngine:
    """
    Core engine for MC AI's autonomous self-evolution capability.
    """
    
    def __init__(self):
        self.session_changes = 0
        self.session_size = 0
        self.audit_log_path = "logs/autonomous_updates.log"
        self.config = {
            'max_changes_per_session': 10,
            'max_size_per_change': 5120,  # 5KB
            'max_total_size_per_day': 102400,  # 100KB
            'enabled': True
        }
        
        # Approved directories for modifications
        self.approved_directories = [
            'datasets/',
            'src/frameworks/',
            'src/emotion_templates/',
            'data/emotion_catalog/'
        ]
        
        # Ensure audit log exists
        os.makedirs('logs', exist_ok=True)
        if not os.path.exists(self.audit_log_path):
            with open(self.audit_log_path, 'w') as f:
                f.write("=== MC AI AUTONOMOUS UPDATE LOG ===\n")
                f.write(f"Started: {datetime.now().isoformat()}\n\n")
    
    def is_enabled(self) -> bool:
        """Check if autonomous updates are enabled."""
        return self.config['enabled']
    
    def can_make_change(self, change_size: int) -> tuple[bool, str]:
        """
        Check if a change is allowed based on session limits.
        
        Returns: (allowed, reason)
        """
        if not self.is_enabled():
            return False, "Autonomous updates are disabled"
        
        if self.session_changes >= self.config['max_changes_per_session']:
            return False, f"Session limit reached ({self.config['max_changes_per_session']} changes)"
        
        if change_size > self.config['max_size_per_change']:
            return False, f"Change too large ({change_size} > {self.config['max_size_per_change']} bytes)"
        
        if self.session_size + change_size > self.config['max_total_size_per_day']:
            return False, f"Daily size limit would be exceeded"
        
        return True, "Change allowed"
    
    def validate_file_path(self, file_path: str) -> tuple[bool, str]:
        """
        Validate that file path is in approved directory.
        
        Returns: (valid, reason)
        """
        # Normalize path
        normalized_path = os.path.normpath(file_path)
        
        # Check if path is in approved directory
        for approved_dir in self.approved_directories:
            if normalized_path.startswith(approved_dir):
                return True, "Path approved"
        
        return False, f"Path '{file_path}' not in approved directories"
    
    def log_change(self, operation: str, details: Dict[str, Any], success: bool, error: Optional[str] = None):
        """Log an autonomous update to audit trail."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'details': details,
            'success': success,
            'error': error,
            'session_changes': self.session_changes,
            'session_size': self.session_size
        }
        
        with open(self.audit_log_path, 'a') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"Timestamp: {log_entry['timestamp']}\n")
            f.write(f"Operation: {operation}\n")
            f.write(f"Details: {json.dumps(details, indent=2)}\n")
            f.write(f"Success: {success}\n")
            if error:
                f.write(f"Error: {error}\n")
            f.write(f"Session Stats: {self.session_changes} changes, {self.session_size} bytes\n")
        
        logger.info(f"Autonomous update logged: {operation} - {'SUCCESS' if success else 'FAILED'}")
    
    def git_commit(self, message: str) -> bool:
        """Create a git commit for the change (for rollback capability)."""
        try:
            # Stage all changes
            subprocess.run(['git', 'add', '-A'], check=True, capture_output=True)
            
            # Commit with autonomous update message
            commit_msg = f"[MC AI Autonomous Update] {message}"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
            
            logger.info(f"Git commit created: {commit_msg}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Git commit failed: {e}")
            return False
    
    def propose_update(self, operation: str, params: Dict[str, Any], justification: str) -> Dict[str, Any]:
        """
        Propose an autonomous update.
        
        Args:
            operation: Name of the operation (must be whitelisted)
            params: Parameters for the operation
            justification: MC AI's reasoning for the update
        
        Returns:
            Result dict with success status and details
        """
        from src.update_operations import UpdateOperations
        from src.update_validator import UpdateValidator
        
        result = {
            'success': False,
            'operation': operation,
            'justification': justification,
            'timestamp': datetime.now().isoformat(),
            'error': None,
            'details': {}
        }
        
        try:
            # Initialize validator and operations
            validator = UpdateValidator(self)
            operations = UpdateOperations()
            
            # Validate operation is whitelisted
            if not operations.is_whitelisted(operation):
                result['error'] = f"Operation '{operation}' not whitelisted"
                self.log_change(operation, params, False, result['error'])
                return result
            
            # Validate with safety checks
            validation = validator.validate_update(operation, params)
            if not validation['valid']:
                result['error'] = validation['reason']
                self.log_change(operation, params, False, result['error'])
                return result
            
            # Check session limits
            change_size = validation.get('estimated_size', 1024)
            can_change, reason = self.can_make_change(change_size)
            if not can_change:
                result['error'] = reason
                self.log_change(operation, params, False, result['error'])
                return result
            
            # Execute the operation
            operation_result = operations.execute(operation, params)
            
            if operation_result['success']:
                # Update session stats
                self.session_changes += 1
                self.session_size += change_size
                
                # Create git commit for rollback
                commit_msg = f"{operation}: {justification[:100]}"
                self.git_commit(commit_msg)
                
                # Log success
                result['success'] = True
                result['details'] = operation_result
                self.log_change(operation, params, True)
                
                logger.info(f"✅ Autonomous update successful: {operation}")
            else:
                result['error'] = operation_result.get('error', 'Operation failed')
                self.log_change(operation, params, False, result['error'])
        
        except Exception as e:
            result['error'] = f"Exception during update: {str(e)}"
            self.log_change(operation, params, False, result['error'])
            logger.error(f"Autonomous update exception: {e}")
        
        return result
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get current session statistics."""
        return {
            'enabled': self.is_enabled(),
            'changes_made': self.session_changes,
            'changes_remaining': self.config['max_changes_per_session'] - self.session_changes,
            'size_used': self.session_size,
            'size_remaining': self.config['max_total_size_per_day'] - self.session_size,
            'config': self.config
        }
    
    def get_recent_updates(self, limit: int = 10) -> List[str]:
        """Get recent autonomous updates from log."""
        try:
            with open(self.audit_log_path, 'r') as f:
                lines = f.readlines()
            
            # Parse log entries (simple implementation)
            updates = []
            current_entry = []
            
            for line in lines:
                if line.startswith('='*80):
                    if current_entry:
                        updates.append('\n'.join(current_entry))
                        current_entry = []
                else:
                    current_entry.append(line.strip())
            
            # Add last entry
            if current_entry:
                updates.append('\n'.join(current_entry))
            
            return updates[-limit:]
        except Exception as e:
            logger.error(f"Error reading update log: {e}")
            return []
    
    def reset_session(self):
        """Reset session counters (called daily or on restart)."""
        self.session_changes = 0
        self.session_size = 0
        logger.info("Session counters reset")


# Global instance
autonomous_engine = AutonomousUpdateEngine()
