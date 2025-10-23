"""
Framework Blueprint
Specification layer for converting teaching into framework blueprints
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class FrameworkBlueprint:
    """
    Formal specification for a framework to be generated
    Converts Mark's teaching into structured blueprint
    """
    
    def __init__(self,
                 name: str,
                 description: str,
                 creator: str = "Mark Coffey"):
        self.name = name
        self.description = description
        self.creator = creator
        self.created_at = datetime.now().isoformat()
        
        # Core components
        self.catalogs: Dict[str, Any] = {}
        self.processing_layers: List[Dict[str, Any]] = []
        self.activation_patterns: List[str] = []
        self.capabilities: List[str] = []
        
        # Integration points
        self.injection_point = "pre_response"
        self.priority = 50
        
        # Dependencies
        self.dependencies: List[str] = []
    
    def add_catalog(self, catalog_name: str, catalog_data: Dict[str, Any]):
        """
        Add a data catalog (e.g., frequency mappings, theme weights)
        
        Args:
            catalog_name: Name of catalog
            catalog_data: Catalog contents
        """
        self.catalogs[catalog_name] = catalog_data
    
    def add_processing_layer(self, 
                            layer_name: str,
                            layer_type: str,
                            logic: str,
                            inputs: List[str],
                            outputs: List[str]):
        """
        Add a processing layer
        
        Args:
            layer_name: Layer identifier
            layer_type: Type (detection, transformation, analysis, etc.)
            logic: Processing logic description
            inputs: Required inputs
            outputs: Produced outputs
        """
        self.processing_layers.append({
            'name': layer_name,
            'type': layer_type,
            'logic': logic,
            'inputs': inputs,
            'outputs': outputs
        })
    
    def add_activation_pattern(self, pattern: str):
        """
        Add a pattern that triggers this framework
        
        Args:
            pattern: Detection pattern (keyword, regex, etc.)
        """
        self.activation_patterns.append(pattern)
    
    def add_capability(self, capability: str):
        """Add a capability this framework provides"""
        self.capabilities.append(capability)
    
    def set_injection_point(self, point: str, priority: int = 50):
        """
        Set where in pipeline this framework runs
        
        Args:
            point: Injection point (pre_response, post_emotion, etc.)
            priority: Execution priority (0-100)
        """
        self.injection_point = point
        self.priority = priority
    
    def add_dependency(self, package: str):
        """Add required Python package"""
        self.dependencies.append(package)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert blueprint to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'creator': self.creator,
            'created_at': self.created_at,
            'catalogs': self.catalogs,
            'processing_layers': self.processing_layers,
            'activation_patterns': self.activation_patterns,
            'capabilities': self.capabilities,
            'injection_point': self.injection_point,
            'priority': self.priority,
            'dependencies': self.dependencies
        }
    
    def to_json(self, filepath: str):
        """Save blueprint to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FrameworkBlueprint':
        """Create blueprint from dictionary"""
        blueprint = cls(
            name=data['name'],
            description=data['description'],
            creator=data.get('creator', 'Mark Coffey')
        )
        
        blueprint.catalogs = data.get('catalogs', {})
        blueprint.processing_layers = data.get('processing_layers', [])
        blueprint.activation_patterns = data.get('activation_patterns', [])
        blueprint.capabilities = data.get('capabilities', [])
        blueprint.injection_point = data.get('injection_point', 'pre_response')
        blueprint.priority = data.get('priority', 50)
        blueprint.dependencies = data.get('dependencies', [])
        
        return blueprint
    
    @classmethod
    def from_json(cls, filepath: str) -> 'FrameworkBlueprint':
        """Load blueprint from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)


class BlueprintExtractor:
    """
    Extracts framework blueprints from teaching code/conversations
    Uses LLM to analyze and create structured blueprints
    """
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def extract_from_code(self, code: str, teaching_context: str) -> Optional[FrameworkBlueprint]:
        """
        Extract framework blueprint from code example
        
        Args:
            code: Python code showing framework
            teaching_context: Mark's explanation/context
        
        Returns:
            FrameworkBlueprint or None
        """
        # Use LLM to analyze code and extract blueprint
        analysis_prompt = f"""Analyze this code that Mark Coffey shared to teach MC AI a new processing framework:

```python
{code}
```

Context: {teaching_context}

Extract a structured blueprint with:
1. Framework name and description
2. Any data catalogs (frequency mappings, weights, etc.)
3. Processing layers (what transformations it does)
4. Activation patterns (when should it run)
5. Capabilities it provides

Return as JSON with these keys: name, description, catalogs, processing_layers, activation_patterns, capabilities"""
        
        try:
            response = self.llm_client.complete(
                "You are analyzing code to extract framework blueprints for MC AI.",
                [{'role': 'user', 'content': analysis_prompt}],
                max_tokens=2000
            )
            
            # Parse JSON response
            blueprint_data = json.loads(response['text'])
            
            # Create blueprint
            blueprint = FrameworkBlueprint(
                name=blueprint_data['name'],
                description=blueprint_data['description']
            )
            
            # Add catalogs
            for cat_name, cat_data in blueprint_data.get('catalogs', {}).items():
                blueprint.add_catalog(cat_name, cat_data)
            
            # Add layers
            for layer in blueprint_data.get('processing_layers', []):
                blueprint.add_processing_layer(
                    layer_name=layer['name'],
                    layer_type=layer.get('type', 'processing'),
                    logic=layer.get('logic', ''),
                    inputs=layer.get('inputs', []),
                    outputs=layer.get('outputs', [])
                )
            
            # Add patterns and capabilities
            for pattern in blueprint_data.get('activation_patterns', []):
                blueprint.add_activation_pattern(pattern)
            
            for capability in blueprint_data.get('capabilities', []):
                blueprint.add_capability(capability)
            
            return blueprint
            
        except Exception as e:
            print(f"Failed to extract blueprint: {e}")
            return None
