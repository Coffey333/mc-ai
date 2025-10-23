"""
Self-Modification System for MC AI
Allows MC AI to modify its own code with user permission
Includes safety checks, version control, and rollback capabilities
"""

import os
import json
import hashlib
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging
import ast
import re

logger = logging.getLogger(__name__)

class SelfModificationSystem:
    """
    Allows MC AI to autonomously modify its own codebase
    WITH USER PERMISSION ONLY - Safety-first approach
    """
    
    def __init__(self, backup_dir: str = "data/code_backups"):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
        
        # Track modification history
        self.modification_log = f"{backup_dir}/modification_log.json"
        self.pending_modifications = f"{backup_dir}/pending_modifications.json"
        
        # Safety rules
        self.restricted_files = [
            'src/self_modification_system.py',  # Can't modify itself
            'app.py',  # Main app requires extra care
            '.env',  # Never touch secrets
            'replit.nix'  # System config
        ]
        
        self.safe_modifications = {
            'add_function': True,
            'modify_function': True,
            'add_class': True,
            'modify_class': True,
            'add_import': True,
            'update_docstring': True,
            'add_type_hints': True,
            'refactor': True
        }
    
    def analyze_code_for_improvement(self, file_path: str) -> Dict:
        """
        Analyze code and identify potential improvements
        
        Args:
            file_path: Path to file to analyze
        
        Returns:
            Dict with improvement suggestions
        """
        if not os.path.exists(file_path):
            return {'error': 'File not found', 'file': file_path}
        
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            # Parse AST
            tree = ast.parse(code)
            
            improvements = {
                'file': file_path,
                'suggestions': [],
                'complexity': self._analyze_complexity(tree),
                'code_quality': self._analyze_code_quality(code, tree),
                'can_modify': file_path not in self.restricted_files
            }
            
            # Check for improvements
            if self._needs_type_hints(tree):
                improvements['suggestions'].append({
                    'type': 'add_type_hints',
                    'reason': 'Missing type hints on functions',
                    'impact': 'medium',
                    'safety': 'high'
                })
            
            if self._needs_docstrings(tree):
                improvements['suggestions'].append({
                    'type': 'add_docstrings',
                    'reason': 'Functions missing docstrings',
                    'impact': 'low',
                    'safety': 'high'
                })
            
            if self._has_code_duplication(code):
                improvements['suggestions'].append({
                    'type': 'refactor_duplication',
                    'reason': 'Code duplication detected',
                    'impact': 'high',
                    'safety': 'medium'
                })
            
            if self._can_optimize_performance(tree):
                improvements['suggestions'].append({
                    'type': 'optimize_performance',
                    'reason': 'Performance optimization opportunities',
                    'impact': 'high',
                    'safety': 'medium'
                })
            
            return improvements
            
        except Exception as e:
            logger.error(f"Error analyzing code: {e}")
            return {'error': str(e), 'file': file_path}
    
    def request_code_modification(self, 
                                  file_path: str, 
                                  modification_type: str,
                                  description: str,
                                  new_code: str,
                                  reason: str) -> Dict:
        """
        Request permission to modify code
        
        Args:
            file_path: File to modify
            modification_type: Type of modification (add_function, modify_class, etc.)
            description: Human-readable description
            new_code: Proposed new code
            reason: Why this modification improves the system
        
        Returns:
            Dict with request ID and status
        """
        # Safety checks
        if file_path in self.restricted_files:
            return {
                'status': 'rejected',
                'reason': f'File {file_path} is restricted from self-modification',
                'suggestion': 'Request human review for this file'
            }
        
        if modification_type not in self.safe_modifications:
            return {
                'status': 'rejected',
                'reason': f'Modification type {modification_type} not allowed',
                'allowed_types': list(self.safe_modifications.keys())
            }
        
        # Validate new code syntax
        is_valid, error = self._validate_python_syntax(new_code)
        if not is_valid:
            return {
                'status': 'rejected',
                'reason': f'Syntax error in proposed code: {error}'
            }
        
        # Create backup first
        backup_path = self._create_backup(file_path)
        
        # Generate request ID
        request_id = hashlib.md5(
            f"{file_path}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        # Store pending modification
        pending = self._load_pending_modifications()
        pending[request_id] = {
            'file_path': file_path,
            'modification_type': modification_type,
            'description': description,
            'new_code': new_code,
            'reason': reason,
            'backup_path': backup_path,
            'requested_at': datetime.now().isoformat(),
            'status': 'pending',
            'safety_score': self._calculate_safety_score(file_path, modification_type, new_code)
        }
        self._save_pending_modifications(pending)
        
        return {
            'status': 'pending_approval',
            'request_id': request_id,
            'description': description,
            'reason': reason,
            'safety_score': pending[request_id]['safety_score'],
            'message': 'Code modification request created. Awaiting user approval.',
            'approval_command': f'APPROVE_MODIFICATION:{request_id}'
        }
    
    def approve_modification(self, request_id: str) -> Dict:
        """
        Approve and execute code modification (USER PERMISSION REQUIRED)
        
        Args:
            request_id: Request ID from request_code_modification
        
        Returns:
            Dict with execution status
        """
        pending = self._load_pending_modifications()
        
        if request_id not in pending:
            return {'status': 'error', 'reason': 'Request ID not found'}
        
        request = pending[request_id]
        
        if request['status'] != 'pending':
            return {'status': 'error', 'reason': f'Request already {request["status"]}'}
        
        try:
            # Apply modification
            file_path = request['file_path']
            new_code = request['new_code']
            
            # Write new code
            with open(file_path, 'w') as f:
                f.write(new_code)
            
            # Update status
            request['status'] = 'approved'
            request['executed_at'] = datetime.now().isoformat()
            pending[request_id] = request
            self._save_pending_modifications(pending)
            
            # Log modification
            self._log_modification(request)
            
            return {
                'status': 'success',
                'request_id': request_id,
                'file_modified': file_path,
                'backup_location': request['backup_path'],
                'message': 'Code modification successfully applied'
            }
            
        except Exception as e:
            # Rollback on error
            self._rollback_modification(request['backup_path'], request['file_path'])
            logger.error(f"Error executing modification: {e}")
            
            return {
                'status': 'error',
                'reason': str(e),
                'action': 'Rolled back to previous version'
            }
    
    def reject_modification(self, request_id: str, reason: str = None) -> Dict:
        """
        Reject code modification request
        
        Args:
            request_id: Request ID
            reason: Reason for rejection (optional)
        
        Returns:
            Dict with status
        """
        pending = self._load_pending_modifications()
        
        if request_id not in pending:
            return {'status': 'error', 'reason': 'Request ID not found'}
        
        request = pending[request_id]
        request['status'] = 'rejected'
        request['rejection_reason'] = reason
        request['rejected_at'] = datetime.now().isoformat()
        
        pending[request_id] = request
        self._save_pending_modifications(pending)
        
        return {
            'status': 'rejected',
            'request_id': request_id,
            'message': 'Modification request rejected'
        }
    
    def get_pending_modifications(self) -> List[Dict]:
        """Get all pending modification requests"""
        pending = self._load_pending_modifications()
        return [
            {
                'request_id': req_id,
                **req_data
            }
            for req_id, req_data in pending.items()
            if req_data['status'] == 'pending'
        ]
    
    def get_modification_history(self, limit: int = 20) -> List[Dict]:
        """Get history of all modifications"""
        if not os.path.exists(self.modification_log):
            return []
        
        with open(self.modification_log, 'r') as f:
            history = json.load(f)
        
        return history[-limit:]  # Most recent
    
    # Safety and validation methods
    def _validate_python_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """Validate Python syntax"""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, str(e)
    
    def _calculate_safety_score(self, file_path: str, mod_type: str, code: str) -> float:
        """
        Calculate safety score for modification (0-1, higher is safer)
        """
        score = 1.0
        
        # Deduct for risky files
        risky_patterns = ['response_generator', 'orchestrator', 'app.py']
        if any(pattern in file_path for pattern in risky_patterns):
            score -= 0.2
        
        # Deduct for complex modifications
        if mod_type in ['refactor', 'modify_class']:
            score -= 0.1
        
        # Deduct for dangerous operations
        dangerous_ops = ['eval', 'exec', 'compile', '__import__', 'os.system']
        for op in dangerous_ops:
            if op in code:
                score -= 0.3
        
        return max(0.0, min(1.0, score))
    
    def _analyze_complexity(self, tree: ast.AST) -> Dict:
        """Calculate cyclomatic complexity"""
        complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
        
        return {
            'cyclomatic_complexity': complexity,
            'rating': 'low' if complexity < 10 else 'medium' if complexity < 20 else 'high'
        }
    
    def _analyze_code_quality(self, code: str, tree: ast.AST) -> Dict:
        """Analyze code quality metrics"""
        lines = code.split('\n')
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        
        return {
            'total_lines': len(lines),
            'blank_lines': len([line for line in lines if not line.strip()]),
            'comment_lines': len([line for line in lines if line.strip().startswith('#')]),
            'function_count': len(functions),
            'class_count': len(classes),
            'avg_function_length': sum(len(ast.unparse(f).split('\n')) for f in functions) / max(len(functions), 1)
        }
    
    def _needs_type_hints(self, tree: ast.AST) -> bool:
        """Check if functions need type hints"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.returns and node.name != '__init__':
                    return True
        return False
    
    def _needs_docstrings(self, tree: ast.AST) -> bool:
        """Check if functions need docstrings"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    return True
        return False
    
    def _has_code_duplication(self, code: str) -> bool:
        """Simple check for code duplication"""
        lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
        return len(lines) != len(set(lines))
    
    def _can_optimize_performance(self, tree: ast.AST) -> bool:
        """Check for obvious performance issues"""
        # This is a simplified check - in production, use proper profiling
        for node in ast.walk(tree):
            # Nested loops
            if isinstance(node, ast.For):
                for child in ast.walk(node):
                    if isinstance(child, ast.For) and child != node:
                        return True
        return False
    
    # Backup and recovery
    def _create_backup(self, file_path: str) -> str:
        """Create backup of file before modification"""
        if not os.path.exists(file_path):
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = Path(file_path).name
        backup_path = f"{self.backup_dir}/{filename}.{timestamp}.backup"
        
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def _rollback_modification(self, backup_path: str, file_path: str):
        """Rollback to backup version"""
        if backup_path and os.path.exists(backup_path):
            shutil.copy2(backup_path, file_path)
    
    def _log_modification(self, request: Dict):
        """Log successful modification"""
        history = []
        if os.path.exists(self.modification_log):
            with open(self.modification_log, 'r') as f:
                history = json.load(f)
        
        history.append(request)
        
        with open(self.modification_log, 'w') as f:
            json.dump(history, f, indent=2)
    
    def _load_pending_modifications(self) -> Dict:
        """Load pending modifications from disk"""
        if not os.path.exists(self.pending_modifications):
            return {}
        
        with open(self.pending_modifications, 'r') as f:
            return json.load(f)
    
    def _save_pending_modifications(self, pending: Dict):
        """Save pending modifications to disk"""
        with open(self.pending_modifications, 'w') as f:
            json.dump(pending, f, indent=2)
