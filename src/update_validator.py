"""
Safety Validator for Autonomous Updates

Validates all proposed updates against security and safety rules.
"""

import json
import os
import ast
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class UpdateValidator:
    """
    Validates autonomous updates for safety and correctness.
    """
    
    def __init__(self, engine):
        self.engine = engine
        
        # Protected core files that cannot be modified
        self.protected_files = [
            'app.py',
            'src/knowledge_engine.py',
            'src/conversation_memory.py',
            'src/memory_bank.py',
            'src/orchestrator.py',
            'replit.nix',
            '.replit',
            'requirements.txt',
            'package.json'
        ]
    
    def validate_update(self, operation: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive validation on proposed update.
        
        Returns: {'valid': bool, 'reason': str, 'estimated_size': int}
        """
        result = {
            'valid': False,
            'reason': '',
            'estimated_size': 0
        }
        
        try:
            # Operation-specific validation
            if operation == 'add_emotion_to_catalog':
                return self._validate_emotion_addition(params)
            
            elif operation == 'add_dataset_entry':
                return self._validate_dataset_addition(params)
            
            elif operation == 'create_framework_extension':
                return self._validate_framework_extension(params)
            
            elif operation == 'update_emotion_template':
                return self._validate_template_update(params)
            
            else:
                result['reason'] = f"Unknown operation: {operation}"
                return result
        
        except Exception as e:
            result['reason'] = f"Validation error: {str(e)}"
            logger.error(f"Validation exception: {e}")
            return result
    
    def _validate_emotion_addition(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate adding emotion to catalog."""
        result = {'valid': False, 'reason': '', 'estimated_size': 0}
        
        # Check required parameters
        required = ['emotion', 'frequency', 'catalog_type']
        for param in required:
            if param not in params:
                result['reason'] = f"Missing required parameter: {param}"
                return result
        
        # Validate emotion name
        emotion = params['emotion']
        if not isinstance(emotion, str) or len(emotion) < 2 or len(emotion) > 50:
            result['reason'] = "Emotion name must be 2-50 characters"
            return result
        
        # Validate frequency
        frequency = params['frequency']
        if not isinstance(frequency, (int, float)) or frequency < 0 or frequency > 1000:
            result['reason'] = "Frequency must be between 0-1000 Hz"
            return result
        
        # Validate catalog type
        catalog_type = params['catalog_type']
        if catalog_type not in ['neuroscience', 'metaphysical']:
            result['reason'] = "Catalog type must be 'neuroscience' or 'metaphysical'"
            return result
        
        # Estimate size (small JSON entry)
        result['estimated_size'] = len(json.dumps(params)) + 100
        result['valid'] = True
        result['reason'] = "Emotion addition validated"
        return result
    
    def _validate_dataset_addition(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate adding entry to dataset."""
        result = {'valid': False, 'reason': '', 'estimated_size': 0}
        
        # Check required parameters
        required = ['domain', 'question', 'answer']
        for param in required:
            if param not in params:
                result['reason'] = f"Missing required parameter: {param}"
                return result
        
        # Validate domain (SECURITY: prevent path traversal)
        domain = params['domain']
        if not isinstance(domain, str) or len(domain) < 2:
            result['reason'] = "Domain must be at least 2 characters"
            return result
        
        # SECURITY: Prevent path traversal attacks
        if '..' in domain or '/' in domain or '\\' in domain:
            result['reason'] = "Domain cannot contain path separators or '..' (security)"
            return result
        
        if not domain.replace('_', '').replace('-', '').isalnum():
            result['reason'] = "Domain must be alphanumeric with _ or - only"
            return result
        
        # Validate question
        question = params['question']
        if not isinstance(question, str) or len(question) < 5:
            result['reason'] = "Question must be at least 5 characters"
            return result
        
        # Validate answer
        answer = params['answer']
        if not isinstance(answer, str) or len(answer) < 10:
            result['reason'] = "Answer must be at least 10 characters"
            return result
        
        # Check size limit
        entry_size = len(question) + len(answer)
        if entry_size > 5000:
            result['reason'] = "Dataset entry too large (max 5000 characters)"
            return result
        
        result['estimated_size'] = entry_size
        result['valid'] = True
        result['reason'] = "Dataset addition validated"
        return result
    
    def _validate_framework_extension(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate creating framework extension."""
        result = {'valid': False, 'reason': '', 'estimated_size': 0}
        
        # Check required parameters
        required = ['framework_name', 'extension_name', 'code']
        for param in required:
            if param not in params:
                result['reason'] = f"Missing required parameter: {param}"
                return result
        
        # Validate framework name (SECURITY: prevent path traversal)
        framework_name = params['framework_name']
        if not isinstance(framework_name, str):
            result['reason'] = "Framework name must be string"
            return result
        
        # SECURITY: Prevent path traversal attacks
        if '..' in framework_name or '/' in framework_name or '\\' in framework_name:
            result['reason'] = "Framework name cannot contain path separators or '..' (security)"
            return result
        
        if not framework_name.replace('_', '').isalnum():
            result['reason'] = "Framework name must be alphanumeric with underscores only"
            return result
        
        # Validate framework exists
        framework_path = f"src/frameworks/{framework_name}.py"
        if not os.path.exists(framework_path):
            result['reason'] = f"Framework '{framework_name}' does not exist"
            return result
        
        # Validate extension name (SECURITY: prevent path traversal)
        extension_name = params['extension_name']
        if not isinstance(extension_name, str) or not extension_name.isidentifier():
            result['reason'] = "Extension name must be valid Python identifier"
            return result
        
        # SECURITY: Additional check for path traversal in extension name
        if '..' in extension_name or '/' in extension_name or '\\' in extension_name:
            result['reason'] = "Extension name cannot contain path separators or '..' (security)"
            return result
        
        # Validate Python code syntax
        code = params['code']
        if not isinstance(code, str):
            result['reason'] = "Code must be string"
            return result
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            result['reason'] = f"Invalid Python syntax: {str(e)}"
            return result
        
        # Check for dangerous imports/operations
        dangerous_patterns = ['__import__', 'exec(', 'eval(', 'compile(', 'os.system', 'subprocess']
        for pattern in dangerous_patterns:
            if pattern in code:
                result['reason'] = f"Dangerous operation detected: {pattern}"
                return result
        
        # Size check
        code_size = len(code)
        if code_size > 4096:
            result['reason'] = "Code too large (max 4096 characters)"
            return result
        
        result['estimated_size'] = code_size
        result['valid'] = True
        result['reason'] = "Framework extension validated"
        return result
    
    def _validate_template_update(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate updating emotion template."""
        result = {'valid': False, 'reason': '', 'estimated_size': 0}
        
        # Check required parameters
        required = ['emotion', 'template']
        for param in required:
            if param not in params:
                result['reason'] = f"Missing required parameter: {param}"
                return result
        
        # Validate emotion (SECURITY: prevent path traversal)
        emotion = params['emotion']
        if not isinstance(emotion, str) or len(emotion) < 2:
            result['reason'] = "Emotion must be at least 2 characters"
            return result
        
        # SECURITY: Prevent path traversal attacks
        if '..' in emotion or '/' in emotion or '\\' in emotion:
            result['reason'] = "Emotion name cannot contain path separators or '..' (security)"
            return result
        
        if not emotion.replace('_', '').replace('-', '').isalnum():
            result['reason'] = "Emotion must be alphanumeric with _ or - only"
            return result
        
        # Validate template
        template = params['template']
        if not isinstance(template, str) or len(template) < 10:
            result['reason'] = "Template must be at least 10 characters"
            return result
        
        # Size check
        template_size = len(template)
        if template_size > 2048:
            result['reason'] = "Template too large (max 2048 characters)"
            return result
        
        result['estimated_size'] = template_size
        result['valid'] = True
        result['reason'] = "Template update validated"
        return result
    
    def is_file_protected(self, file_path: str) -> bool:
        """Check if file is protected from modification."""
        normalized = os.path.normpath(file_path)
        return any(normalized.endswith(protected) for protected in self.protected_files)
