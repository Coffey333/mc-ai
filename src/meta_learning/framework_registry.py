"""
Framework Registry
Manages all loaded and available frameworks
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from src.meta_learning.framework_interface import BaseFramework, FrameworkManifest

class FrameworkRegistry:
    """
    Registry for managing dynamically loaded frameworks
    
    Responsibilities:
    - Track all available frameworks
    - Manage framework versions
    - Handle framework approval status
    - Provide framework discovery
    """
    
    def __init__(self):
        self.frameworks: Dict[str, BaseFramework] = {}
        self.manifests: Dict[str, FrameworkManifest] = {}
        self.approval_db = "user_data/framework_approvals/approvals.json"
        self.registry_file = "user_data/framework_approvals/registry.json"
        
        os.makedirs(os.path.dirname(self.approval_db), exist_ok=True)
        
        self._load_registry()
        print("🧠 Framework Registry initialized")
    
    def register(self, 
                 framework_id: str, 
                 framework: BaseFramework, 
                 manifest: FrameworkManifest,
                 approved: bool = False) -> bool:
        """
        Register a new framework
        
        Args:
            framework_id: Unique identifier
            framework: Framework instance
            manifest: Framework manifest
            approved: Whether framework is approved by creator
        
        Returns:
            True if registered successfully
        """
        if framework_id in self.frameworks:
            print(f"⚠️  Framework {framework_id} already registered")
            return False
        
        # Store framework and manifest
        self.frameworks[framework_id] = framework
        self.manifests[framework_id] = manifest
        
        # CRITICAL: Disable framework until approved
        if not approved:
            framework.disable()
            print(f"🔒 Framework registered but DISABLED pending approval: {manifest.name}")
        else:
            framework.enable()
        
        # Save to registry
        self._save_to_registry(framework_id, manifest, approved)
        
        status = "approved & active" if approved else "pending approval (disabled)"
        print(f"✅ Registered framework: {manifest.name} ({status})")
        return True
    
    def unregister(self, framework_id: str) -> bool:
        """Unregister a framework"""
        if framework_id not in self.frameworks:
            return False
        
        del self.frameworks[framework_id]
        del self.manifests[framework_id]
        self._remove_from_registry(framework_id)
        
        print(f"❌ Unregistered framework: {framework_id}")
        return True
    
    def get_framework(self, framework_id: str) -> Optional[BaseFramework]:
        """Get a framework by ID"""
        return self.frameworks.get(framework_id)
    
    def get_manifest(self, framework_id: str) -> Optional[FrameworkManifest]:
        """Get a framework's manifest"""
        return self.manifests.get(framework_id)
    
    def get_all_frameworks(self) -> Dict[str, BaseFramework]:
        """Get all registered frameworks"""
        return self.frameworks.copy()
    
    def get_approved_frameworks(self) -> List[str]:
        """Get list of approved framework IDs"""
        registry = self._load_registry()
        return [fid for fid, data in registry.items() if data.get('approved', False)]
    
    def get_pending_frameworks(self) -> List[str]:
        """Get list of pending approval framework IDs"""
        registry = self._load_registry()
        return [fid for fid, data in registry.items() if not data.get('approved', False)]
    
    def approve_framework(self, framework_id: str, approver: str = "Mark Coffey") -> bool:
        """
        Approve a framework for use
        
        Args:
            framework_id: Framework to approve
            approver: Who approved it (default: Mark Coffey)
        
        Returns:
            True if approved successfully
        """
        registry = self._load_registry()
        
        if framework_id not in registry:
            return False
        
        registry[framework_id]['approved'] = True
        registry[framework_id]['approved_by'] = approver
        registry[framework_id]['approved_at'] = datetime.now().isoformat()
        
        self._save_registry(registry)
        
        # Enable the framework
        if framework_id in self.frameworks:
            self.frameworks[framework_id].enable()
        
        print(f"✅ Framework approved: {framework_id} by {approver}")
        return True
    
    def revoke_approval(self, framework_id: str) -> bool:
        """Revoke approval for a framework"""
        registry = self._load_registry()
        
        if framework_id not in registry:
            return False
        
        registry[framework_id]['approved'] = False
        registry[framework_id]['revoked_at'] = datetime.now().isoformat()
        
        self._save_registry(registry)
        
        # Disable the framework
        if framework_id in self.frameworks:
            self.frameworks[framework_id].disable()
        
        print(f"⚠️  Framework approval revoked: {framework_id}")
        return True
    
    def is_approved(self, framework_id: str) -> bool:
        """Check if framework is approved"""
        registry = self._load_registry()
        return registry.get(framework_id, {}).get('approved', False)
    
    def get_frameworks_by_injection_point(self, injection_point: str) -> List[BaseFramework]:
        """
        Get all approved AND enabled frameworks for a specific injection point
        
        Args:
            injection_point: Where in pipeline (e.g., 'pre_response', 'post_emotion')
        
        Returns:
            List of frameworks sorted by priority (highest first)
        """
        frameworks = []
        
        for fid, manifest in self.manifests.items():
            # CRITICAL: Double-check approval status before returning
            if manifest.injection_point == injection_point and self.is_approved(fid):
                framework = self.frameworks.get(fid)
                # Framework must be both approved AND enabled
                if framework and framework.enabled:
                    frameworks.append((manifest.priority, framework))
                elif framework and not framework.enabled:
                    print(f"⚠️  Skipping disabled framework: {manifest.name}")
        
        # Sort by priority (highest first)
        frameworks.sort(key=lambda x: x[0], reverse=True)
        
        return [f for _, f in frameworks]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        registry = self._load_registry()
        
        approved = [fid for fid, data in registry.items() if data.get('approved', False)]
        pending = [fid for fid, data in registry.items() if not data.get('approved', False)]
        
        framework_stats = {}
        for fid, framework in self.frameworks.items():
            framework_stats[fid] = framework.get_stats()
        
        return {
            'total_frameworks': len(registry),
            'approved_count': len(approved),
            'pending_count': len(pending),
            'loaded_count': len(self.frameworks),
            'approved_frameworks': approved,
            'pending_frameworks': pending,
            'framework_stats': framework_stats
        }
    
    def _save_to_registry(self, framework_id: str, manifest: FrameworkManifest, approved: bool):
        """Save framework to registry"""
        registry = self._load_registry()
        
        registry[framework_id] = {
            'manifest': manifest.to_dict(),
            'approved': approved,
            'registered_at': datetime.now().isoformat()
        }
        
        self._save_registry(registry)
    
    def _remove_from_registry(self, framework_id: str):
        """Remove framework from registry"""
        registry = self._load_registry()
        
        if framework_id in registry:
            del registry[framework_id]
            self._save_registry(registry)
    
    def _load_registry(self) -> Dict[str, Any]:
        """Load registry from file"""
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_registry(self, registry: Dict[str, Any]):
        """Save registry to file"""
        with open(self.registry_file, 'w') as f:
            json.dump(registry, f, indent=2)


# Global registry instance
framework_registry = FrameworkRegistry()
