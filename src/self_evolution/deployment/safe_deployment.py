"""
Safe Deployment System
Deploys MC AI's changes with rollback capability
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

class SafeDeployment:
    """
    Safely deploys code changes with automatic rollback
    """
    
    def __init__(self, backup_dir: str = "backups/deployments"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.deployment_history = []
        
    def deploy_changes(self, proposal_id: str, file_changes: Dict[str, str]) -> Dict:
        """
        Deploy approved changes to production
        
        Args:
            proposal_id: ID of approved proposal
            file_changes: Dict of {file_path: new_content}
        
        Returns deployment result
        """
        deployment_id = f"deploy_{proposal_id}_{int(datetime.now().timestamp())}"
        backup_path = self.backup_dir / deployment_id
        
        try:
            # Step 1: Create backup of current state
            print(f"📦 Creating backup: {deployment_id}")
            backup_created = self._create_backup(backup_path, file_changes.keys())
            
            if not backup_created:
                return {
                    'success': False,
                    'error': 'Failed to create backup',
                    'deployment_id': deployment_id
                }
            
            # Step 2: Apply changes
            print(f"🚀 Deploying changes...")
            applied_files = []
            
            for file_path, new_content in file_changes.items():
                try:
                    target = Path(file_path)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(new_content)
                    applied_files.append(file_path)
                    print(f"   ✅ Updated: {file_path}")
                except Exception as e:
                    print(f"   ❌ Failed: {file_path} - {e}")
                    # Rollback on any failure
                    self._rollback(backup_path, applied_files)
                    return {
                        'success': False,
                        'error': f'Failed to apply changes to {file_path}: {e}',
                        'deployment_id': deployment_id,
                        'rolled_back': True
                    }
            
            # Step 3: Validate deployment
            print(f"✓ Validating deployment...")
            validation = self._validate_deployment(applied_files)
            
            if not validation['valid']:
                print(f"❌ Validation failed - rolling back")
                self._rollback(backup_path, applied_files)
                return {
                    'success': False,
                    'error': f"Validation failed: {validation['error']}",
                    'deployment_id': deployment_id,
                    'rolled_back': True
                }
            
            # Success!
            deployment_record = {
                'deployment_id': deployment_id,
                'proposal_id': proposal_id,
                'files_changed': list(file_changes.keys()),
                'deployed_at': datetime.now().isoformat(),
                'backup_path': str(backup_path),
                'success': True
            }
            
            self.deployment_history.append(deployment_record)
            
            print(f"✅ Deployment successful: {deployment_id}")
            
            return deployment_record
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Deployment failed: {e}',
                'deployment_id': deployment_id
            }
    
    def _create_backup(self, backup_path: Path, files: list) -> bool:
        """Create backup of files before deployment"""
        try:
            backup_path.mkdir(parents=True, exist_ok=True)
            
            for file_path in files:
                source = Path(file_path)
                if source.exists():
                    dest = backup_path / file_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, dest)
            
            return True
        except Exception as e:
            print(f"Backup failed: {e}")
            return False
    
    def _validate_deployment(self, files: list) -> Dict:
        """Validate deployed files"""
        # Check syntax
        for file_path in files:
            if file_path.endswith('.py'):
                try:
                    with open(file_path) as f:
                        compile(f.read(), file_path, 'exec')
                except SyntaxError as e:
                    return {
                        'valid': False,
                        'error': f'Syntax error in {file_path}: {e}'
                    }
        
        return {'valid': True}
    
    def _rollback(self, backup_path: Path, files: list):
        """Rollback changes from backup"""
        print(f"🔄 Rolling back changes...")
        
        try:
            for file_path in files:
                backup_file = backup_path / file_path
                if backup_file.exists():
                    shutil.copy2(backup_file, file_path)
                    print(f"   ↩️  Restored: {file_path}")
            
            print(f"✅ Rollback complete")
        except Exception as e:
            print(f"❌ Rollback failed: {e}")
    
    def rollback_deployment(self, deployment_id: str) -> bool:
        """Manually rollback a deployment"""
        # Find deployment record
        deployment = next((d for d in self.deployment_history if d['deployment_id'] == deployment_id), None)
        
        if not deployment:
            return False
        
        backup_path = Path(deployment['backup_path'])
        self._rollback(backup_path, deployment['files_changed'])
        
        return True

# Global instance
_deployment = None

def get_safe_deployment() -> SafeDeployment:
    """Get or create global deployment system"""
    global _deployment
    if _deployment is None:
        _deployment = SafeDeployment()
    return _deployment
