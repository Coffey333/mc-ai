"""
Approved Operations for Autonomous Updates

Defines the whitelist of operations MC AI can perform autonomously.
"""

import json
import os
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class UpdateOperations:
    """
    Whitelisted operations that MC AI can execute autonomously.
    """
    
    def __init__(self):
        # Whitelist of approved operations
        self.whitelist = [
            'add_emotion_to_catalog',
            'add_dataset_entry',
            'create_framework_extension',
            'update_emotion_template'
        ]
    
    def is_whitelisted(self, operation: str) -> bool:
        """Check if operation is in whitelist."""
        return operation in self.whitelist
    
    def execute(self, operation: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a whitelisted operation.
        
        Returns: {'success': bool, 'details': dict, 'error': str}
        """
        result = {'success': False, 'details': {}, 'error': None}
        
        try:
            if operation == 'add_emotion_to_catalog':
                return self._add_emotion_to_catalog(params)
            
            elif operation == 'add_dataset_entry':
                return self._add_dataset_entry(params)
            
            elif operation == 'create_framework_extension':
                return self._create_framework_extension(params)
            
            elif operation == 'update_emotion_template':
                return self._update_emotion_template(params)
            
            else:
                result['error'] = f"Operation not implemented: {operation}"
                return result
        
        except Exception as e:
            result['error'] = f"Execution error: {str(e)}"
            logger.error(f"Operation execution failed: {e}")
            return result
    
    def _add_emotion_to_catalog(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new emotion to the frequency catalog."""
        result = {'success': False, 'details': {}, 'error': None}
        
        try:
            emotion = params['emotion']
            frequency = params['frequency']
            catalog_type = params['catalog_type']
            
            # Determine catalog file
            if catalog_type == 'neuroscience':
                catalog_file = 'data/emotion_catalog/neuroscience_catalog.json'
            else:
                catalog_file = 'data/emotion_catalog/metaphysical_catalog.json'
            
            # Create directory if needed
            os.makedirs('data/emotion_catalog', exist_ok=True)
            
            # Load existing catalog
            if os.path.exists(catalog_file):
                with open(catalog_file, 'r') as f:
                    catalog = json.load(f)
            else:
                catalog = {}
            
            # Add new emotion
            catalog[emotion] = {
                'frequency': frequency,
                'added_by': 'MC_AI_Autonomous',
                'timestamp': params.get('timestamp', 'unknown'),
                'justification': params.get('justification', 'Pattern discovered')
            }
            
            # Save updated catalog
            with open(catalog_file, 'w') as f:
                json.dump(catalog, f, indent=2)
            
            result['success'] = True
            result['details'] = {
                'emotion': emotion,
                'frequency': frequency,
                'catalog': catalog_type,
                'file': catalog_file
            }
            
            logger.info(f"✅ Added emotion '{emotion}' ({frequency} Hz) to {catalog_type} catalog")
        
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Failed to add emotion: {e}")
        
        return result
    
    def _add_dataset_entry(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new entry to a dataset."""
        result = {'success': False, 'details': {}, 'error': None}
        
        try:
            domain = params['domain']
            question = params['question']
            answer = params['answer']
            
            # SECURITY: Sanitize domain to prevent path traversal
            # Only allow alphanumeric, underscore, hyphen
            safe_domain = ''.join(c for c in domain if c.isalnum() or c in ('_', '-'))
            if safe_domain != domain:
                result['error'] = "Domain contains invalid characters (security check failed)"
                return result
            
            # Determine dataset file based on domain
            dataset_file = f'datasets/{safe_domain}_autonomous.json'
            
            # SECURITY: Verify path is within datasets directory
            import os
            abs_path = os.path.abspath(dataset_file)
            datasets_dir = os.path.abspath('datasets/')
            if not abs_path.startswith(datasets_dir):
                result['error'] = "Path traversal detected (security)"
                logger.error(f"Path traversal attempt: {dataset_file}")
                return result
            
            # Load existing dataset
            if os.path.exists(dataset_file):
                with open(dataset_file, 'r') as f:
                    dataset = json.load(f)
            else:
                dataset = []
            
            # Create new entry
            entry = {
                'domain': domain,
                'question': question,
                'answer': answer,
                'examples': params.get('examples', []),
                'added_by': 'MC_AI_Autonomous',
                'timestamp': params.get('timestamp', 'unknown')
            }
            
            # Add to dataset
            dataset.append(entry)
            
            # Save updated dataset
            with open(dataset_file, 'w') as f:
                json.dump(dataset, f, indent=2)
            
            result['success'] = True
            result['details'] = {
                'domain': domain,
                'file': dataset_file,
                'total_entries': len(dataset)
            }
            
            logger.info(f"✅ Added dataset entry to {domain}")
        
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Failed to add dataset entry: {e}")
        
        return result
    
    def _create_framework_extension(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create an extension module for an existing framework."""
        result = {'success': False, 'details': {}, 'error': None}
        
        try:
            framework_name = params['framework_name']
            extension_name = params['extension_name']
            code = params['code']
            
            # SECURITY: Sanitize names to prevent path traversal
            safe_framework = ''.join(c for c in framework_name if c.isalnum() or c == '_')
            safe_extension = ''.join(c for c in extension_name if c.isalnum() or c == '_')
            
            if safe_framework != framework_name or safe_extension != extension_name:
                result['error'] = "Name contains invalid characters (security check failed)"
                return result
            
            # Create extension file
            extension_file = f'src/frameworks/{safe_framework}_{safe_extension}.py'
            
            # SECURITY: Verify path is within frameworks directory
            import os
            abs_path = os.path.abspath(extension_file)
            frameworks_dir = os.path.abspath('src/frameworks/')
            if not abs_path.startswith(frameworks_dir):
                result['error'] = "Path traversal detected (security)"
                logger.error(f"Path traversal attempt: {extension_file}")
                return result
            
            # Add header comment
            header = f'''"""
{framework_name.replace('_', ' ').title()} - {extension_name.replace('_', ' ').title()} Extension

Autonomous extension created by MC AI.
Justification: {params.get('justification', 'Functionality enhancement')}
"""

'''
            
            # Write extension
            with open(extension_file, 'w') as f:
                f.write(header + code)
            
            result['success'] = True
            result['details'] = {
                'framework': framework_name,
                'extension': extension_name,
                'file': extension_file
            }
            
            logger.info(f"✅ Created framework extension: {extension_file}")
        
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Failed to create framework extension: {e}")
        
        return result
    
    def _update_emotion_template(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update or create an emotion response template."""
        result = {'success': False, 'details': {}, 'error': None}
        
        try:
            emotion = params['emotion']
            template = params['template']
            
            # Create templates directory if needed
            os.makedirs('src/emotion_templates', exist_ok=True)
            
            # Template file
            template_file = 'src/emotion_templates/autonomous_templates.json'
            
            # Load existing templates
            if os.path.exists(template_file):
                with open(template_file, 'r') as f:
                    templates = json.load(f)
            else:
                templates = {}
            
            # Add/update template
            templates[emotion] = {
                'template': template,
                'updated_by': 'MC_AI_Autonomous',
                'timestamp': params.get('timestamp', 'unknown'),
                'justification': params.get('justification', 'Template refinement')
            }
            
            # Save updated templates
            with open(template_file, 'w') as f:
                json.dump(templates, f, indent=2)
            
            result['success'] = True
            result['details'] = {
                'emotion': emotion,
                'file': template_file,
                'total_templates': len(templates)
            }
            
            logger.info(f"✅ Updated emotion template for '{emotion}'")
        
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Failed to update template: {e}")
        
        return result
