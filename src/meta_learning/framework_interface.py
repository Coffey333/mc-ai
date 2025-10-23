"""
Base Framework Interface
All dynamically generated frameworks must inherit from this
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime

class BaseFramework(ABC):
    """
    Base class for all dynamically loaded processing frameworks
    
    All frameworks created through teaching must inherit this and implement:
    - should_process(): Determine if this framework applies to the query
    - process(): Transform or enhance the query/response
    - get_metadata(): Return framework information
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize framework
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.created_at = datetime.now().isoformat()
        self.version = "1.0.0"
        self.enabled = True
        self.execution_count = 0
        self.error_count = 0
        self.last_execution = None
        self.last_error = None
        self.execution_times = []  # Track execution performance
    
    @abstractmethod
    def should_process(self, query: str, context: Dict[str, Any]) -> bool:
        """
        Determine if this framework should process the query
        
        Args:
            query: User's input
            context: Current conversation context
        
        Returns:
            True if framework should process, False otherwise
        """
        pass
    
    @abstractmethod
    def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the query with this framework
        
        Args:
            query: User's input
            context: Current conversation context
        
        Returns:
            Dict with:
                - enhanced_query: Modified/enhanced query (or original)
                - metadata: Framework execution metadata
                - insights: Any insights generated
        """
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get framework metadata
        
        Returns:
            Dict with framework information:
                - name: Framework name
                - description: What it does
                - creator: Who created it (usually 'Mark Coffey')
                - version: Version number
                - capabilities: List of capabilities
        """
        pass
    
    def validate_input(self, query: str, context: Dict[str, Any]) -> bool:
        """
        Validate input before processing
        Override this for custom validation
        
        Args:
            query: User's input
            context: Current conversation context
        
        Returns:
            True if valid, False otherwise
        """
        return bool(query and isinstance(context, dict))
    
    def on_success(self, result: Dict[str, Any], execution_time: float = 0.0):
        """
        Called after successful processing
        Override for custom success handling
        
        Args:
            result: Processing result
            execution_time: Time taken in seconds
        """
        self.execution_count += 1
        self.last_execution = datetime.now().isoformat()
        if execution_time > 0:
            self.execution_times.append(execution_time)
            # Keep only last 100 execution times
            if len(self.execution_times) > 100:
                self.execution_times.pop(0)
    
    def on_error(self, error: Exception):
        """
        Called when processing fails
        Override for custom error handling
        
        Args:
            error: Exception that occurred
        """
        self.error_count += 1
        self.last_error = {
            'error': str(error),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get framework execution statistics"""
        avg_time = sum(self.execution_times) / len(self.execution_times) if self.execution_times else 0
        
        # Calculate success rate, clamped to [0,1]
        if self.execution_count == 0:
            success_rate = 0.0
        else:
            success_rate = max(0.0, min(1.0, (self.execution_count - self.error_count) / self.execution_count))
        
        return {
            'execution_count': self.execution_count,
            'error_count': self.error_count,
            'success_rate': success_rate,
            'enabled': self.enabled,
            'version': self.version,
            'created_at': self.created_at,
            'last_execution': self.last_execution,
            'last_error': self.last_error,
            'avg_execution_time_ms': round(avg_time * 1000, 2) if avg_time > 0 else 0,
            'total_executions_tracked': len(self.execution_times)
        }
    
    def enable(self):
        """Enable this framework"""
        self.enabled = True
    
    def disable(self):
        """Disable this framework"""
        self.enabled = False


class FrameworkManifest:
    """
    Manifest describing a framework's capabilities and requirements
    """
    
    def __init__(self, 
                 name: str,
                 version: str,
                 description: str,
                 creator: str,
                 capabilities: List[str],
                 dependencies: Optional[List[str]] = None,
                 injection_point: str = "pre_response",
                 priority: int = 50):
        """
        Create framework manifest
        
        Args:
            name: Framework name
            version: Semantic version (e.g., "1.0.0")
            description: What the framework does
            creator: Who created it
            capabilities: List of capabilities
            dependencies: Required Python packages
            injection_point: Where in pipeline to inject (pre_response, post_emotion, etc.)
            priority: Execution priority (0-100, higher = earlier)
        """
        self.name = name
        self.version = version
        self.description = description
        self.creator = creator
        self.capabilities = capabilities
        self.dependencies = dependencies or []
        self.injection_point = injection_point
        self.priority = priority
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert manifest to dictionary"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'creator': self.creator,
            'capabilities': self.capabilities,
            'dependencies': self.dependencies,
            'injection_point': self.injection_point,
            'priority': self.priority,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FrameworkManifest':
        """Create manifest from dictionary"""
        return cls(
            name=data['name'],
            version=data['version'],
            description=data['description'],
            creator=data['creator'],
            capabilities=data['capabilities'],
            dependencies=data.get('dependencies', []),
            injection_point=data.get('injection_point', 'pre_response'),
            priority=data.get('priority', 50)
        )
