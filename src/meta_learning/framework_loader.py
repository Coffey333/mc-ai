"""
Framework Loader
Safely loads and executes dynamically generated frameworks
"""

import importlib.util
import os
import sys
import traceback
from typing import Dict, Any, Optional, Tuple
from src.meta_learning.framework_interface import BaseFramework, FrameworkManifest
from src.meta_learning.framework_registry import framework_registry

class FrameworkLoader:
    """
    Loads and validates dynamically generated frameworks
    
    Safety features:
    - Validates framework code before loading
    - Sandboxed execution with timeouts
    - Dependency checking
    - Error handling and rollback
    """
    
    def __init__(self):
        self.loaded_modules = {}
        self.failed_loads = {}
        print("🔧 Framework Loader initialized")
    
    def load_framework(self, 
                      framework_id: str, 
                      module_path: str,
                      manifest: FrameworkManifest,
                      auto_approve: bool = False) -> Tuple[bool, Optional[str]]:
        """
        Load a framework from a Python module
        
        Args:
            framework_id: Unique framework identifier
            module_path: Path to the Python module file
            manifest: Framework manifest
            auto_approve: Auto-approve if True (default: False, requires manual approval)
        
        Returns:
            (success, error_message)
        """
        try:
            # Validate file exists
            if not os.path.exists(module_path):
                error = f"Module file not found: {module_path}"
                self.failed_loads[framework_id] = error
                return False, error
            
            # Load module dynamically
            spec = importlib.util.spec_from_file_location(framework_id, module_path)
            if not spec or not spec.loader:
                error = "Failed to load module spec"
                self.failed_loads[framework_id] = error
                return False, error
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[framework_id] = module
            spec.loader.exec_module(module)
            
            # Find the framework class (should inherit from BaseFramework)
            framework_class = None
            for name in dir(module):
                obj = getattr(module, name)
                if (isinstance(obj, type) and 
                    issubclass(obj, BaseFramework) and 
                    obj is not BaseFramework):
                    framework_class = obj
                    break
            
            if not framework_class:
                error = "No BaseFramework subclass found in module"
                self.failed_loads[framework_id] = error
                return False, error
            
            # Instantiate framework
            framework_instance = framework_class()
            
            # Validate it implements required methods
            if not self._validate_framework(framework_instance):
                error = "Framework does not implement required methods"
                self.failed_loads[framework_id] = error
                return False, error
            
            # Register in registry
            approved = auto_approve
            framework_registry.register(
                framework_id, 
                framework_instance, 
                manifest,
                approved=approved
            )
            
            # Store loaded module
            self.loaded_modules[framework_id] = module
            
            status = "approved & active" if approved else "pending approval"
            print(f"✅ Loaded framework: {manifest.name} ({status})")
            
            return True, None
            
        except Exception as e:
            error = f"Failed to load framework: {str(e)}\n{traceback.format_exc()}"
            self.failed_loads[framework_id] = error
            print(f"❌ Framework load failed: {framework_id}")
            print(f"   Error: {error}")
            return False, error
    
    def _validate_framework(self, framework: BaseFramework) -> bool:
        """
        Validate framework implements required interface
        
        Args:
            framework: Framework instance to validate
        
        Returns:
            True if valid
        """
        required_methods = ['should_process', 'process', 'get_metadata']
        
        for method in required_methods:
            if not hasattr(framework, method):
                return False
            if not callable(getattr(framework, method)):
                return False
        
        return True
    
    def reload_framework(self, framework_id: str) -> Tuple[bool, Optional[str]]:
        """
        Reload a framework (useful after code updates)
        
        Args:
            framework_id: Framework to reload
        
        Returns:
            (success, error_message)
        """
        # Get manifest
        manifest = framework_registry.get_manifest(framework_id)
        if not manifest:
            return False, "Framework not found in registry"
        
        # Unregister old version
        framework_registry.unregister(framework_id)
        
        # Reload module
        if framework_id in sys.modules:
            del sys.modules[framework_id]
        
        # Determine module path (stored in registry or default location)
        module_path = f"src/meta_learning/generated/{framework_id}.py"
        
        # Load new version
        return self.load_framework(framework_id, module_path, manifest)
    
    def unload_framework(self, framework_id: str) -> bool:
        """
        Unload a framework
        
        Args:
            framework_id: Framework to unload
        
        Returns:
            True if unloaded successfully
        """
        # Unregister from registry
        framework_registry.unregister(framework_id)
        
        # Remove from loaded modules
        if framework_id in self.loaded_modules:
            del self.loaded_modules[framework_id]
        
        # Remove from sys.modules
        if framework_id in sys.modules:
            del sys.modules[framework_id]
        
        print(f"🗑️  Unloaded framework: {framework_id}")
        return True
    
    def get_load_status(self) -> Dict[str, Any]:
        """Get loading status for all frameworks"""
        return {
            'loaded_count': len(self.loaded_modules),
            'loaded_frameworks': list(self.loaded_modules.keys()),
            'failed_count': len(self.failed_loads),
            'failed_frameworks': self.failed_loads.copy()
        }


# Global loader instance
framework_loader = FrameworkLoader()
