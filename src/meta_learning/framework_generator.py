"""
Framework Code Generator
Generates Python framework code from blueprints
"""

import os
from typing import Dict, Any
from datetime import datetime
from src.meta_learning.framework_blueprint import FrameworkBlueprint

class FrameworkGenerator:
    """
    Generates Python code for frameworks from blueprints
    """
    
    def __init__(self):
        self.output_dir = "src/meta_learning/generated"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_from_blueprint(self, blueprint: FrameworkBlueprint) -> str:
        """
        Generate Python framework code from blueprint
        
        Args:
            blueprint: Framework blueprint
        
        Returns:
            Path to generated file
        """
        # Generate class name from framework name
        class_name = self._to_class_name(blueprint.name)
        module_name = self._to_module_name(blueprint.name)
        
        # Generate code
        code = self._generate_code(class_name, blueprint)
        
        # Save to file
        filepath = os.path.join(self.output_dir, f"{module_name}.py")
        with open(filepath, 'w') as f:
            f.write(code)
        
        print(f"✅ Generated framework: {filepath}")
        return filepath
    
    def _generate_code(self, class_name: str, blueprint: FrameworkBlueprint) -> str:
        """Generate the actual Python code"""
        
        # Header
        code = f'''"""
{blueprint.name}
{blueprint.description}

Auto-generated framework created by: {blueprint.creator}
Generated: {datetime.now().isoformat()}
"""

from src.meta_learning.framework_interface import BaseFramework
from typing import Dict, Any

class {class_name}(BaseFramework):
    """
    {blueprint.description}
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        
'''
        
        # Add catalogs as class attributes
        for catalog_name, catalog_data in blueprint.catalogs.items():
            code += f"        # {catalog_name} catalog\n"
            code += f"        self.{catalog_name} = {repr(catalog_data)}\n\n"
        
        # Add should_process method
        code += "    def should_process(self, query: str, context: Dict[str, Any]) -> bool:\n"
        code += '        """\n'
        code += "        Determine if this framework should process the query\n"
        code += '        """\n'
        code += "        query_lower = query.lower()\n\n"
        
        if blueprint.activation_patterns:
            code += "        # Check activation patterns\n"
            code += f"        patterns = {repr(blueprint.activation_patterns)}\n"
            code += "        for pattern in patterns:\n"
            code += "            if pattern.lower() in query_lower:\n"
            code += "                return True\n\n"
        
        code += "        return False\n\n"
        
        # Add process method
        code += "    def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:\n"
        code += '        """\n'
        code += "        Process the query with this framework\n"
        code += '        """\n'
        
        # Generate processing logic based on layers
        if blueprint.processing_layers:
            code += "        # Processing layers\n"
            code += "        results = {}\n\n"
            
            for layer in blueprint.processing_layers:
                code += f"        # Layer: {layer['name']}\n"
                code += f"        # {layer.get('logic', 'Processing...')}\n"
                code += f"        results['{layer['name']}'] = self._process_{self._to_method_name(layer['name'])}(query, context)\n\n"
        else:
            code += "        # Default processing\n"
            code += "        results = {'processed': True}\n\n"
        
        code += "        return {\n"
        code += "            'enhanced_query': query,\n"
        code += "            'metadata': {\n"
        code += f"                'framework': '{blueprint.name}',\n"
        code += "                'processing_results': results\n"
        code += "            },\n"
        code += "            'insights': {\n"
        code += f"                'message': 'Processed by {blueprint.name}',\n"
        code += "                'results': results\n"
        code += "            }\n"
        code += "        }\n\n"
        
        # Add helper methods for each processing layer
        if blueprint.processing_layers:
            for layer in blueprint.processing_layers:
                method_name = self._to_method_name(layer['name'])
                code += f"    def _process_{method_name}(self, query: str, context: Dict[str, Any]) -> Any:\n"
                code += f'        """{layer.get("logic", "Process layer")}"""\n'
                
                # Generate actual processing logic
                layer_type = layer.get('type', 'processing')
                if layer_type == 'detection':
                    code += "        # Detection logic\n"
                    code += "        detected = []\n"
                    code += "        query_lower = query.lower()\n"
                    code += "        # Add detection patterns here\n"
                    code += "        return {'detected': detected}\n\n"
                elif layer_type == 'transformation':
                    code += "        # Transformation logic\n"
                    code += "        transformed = query  # Apply transformations\n"
                    code += "        return {'transformed': transformed}\n\n"
                elif layer_type == 'analysis':
                    code += "        # Analysis logic\n"
                    code += "        score = 0.5  # Calculate score\n"
                    code += "        return {'analysis_score': score}\n\n"
                else:
                    code += "        # General processing logic\n"
                    code += f"        # {layer.get('logic', 'Processing...')}\n"
                    code += "        return {'status': 'processed', 'layer': '" + layer['name'] + "'}\n\n"
        
        # Add get_metadata method
        code += "    def get_metadata(self) -> Dict[str, Any]:\n"
        code += '        """Return framework metadata"""\n'
        code += "        return {\n"
        code += f"            'name': '{blueprint.name}',\n"
        code += f"            'description': '{blueprint.description}',\n"
        code += f"            'creator': '{blueprint.creator}',\n"
        code += "            'version': self.version,\n"
        code += f"            'capabilities': {repr(blueprint.capabilities)}\n"
        code += "        }\n"
        
        return code
    
    def _to_class_name(self, name: str) -> str:
        """Convert framework name to class name (PascalCase)"""
        return ''.join(word.capitalize() for word in name.replace('-', ' ').replace('_', ' ').split())
    
    def _to_module_name(self, name: str) -> str:
        """Convert framework name to module name (snake_case)"""
        return name.lower().replace(' ', '_').replace('-', '_')
    
    def _to_method_name(self, name: str) -> str:
        """Convert layer name to method name (snake_case)"""
        return name.lower().replace(' ', '_').replace('-', '_')


# Global generator instance
framework_generator = FrameworkGenerator()
