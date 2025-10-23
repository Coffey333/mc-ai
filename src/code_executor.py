"""
Safe Python Code Execution for MC AI Self-Learning
Allows MC AI to run code provided by admin/creator for understanding itself
"""
import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr

class CodeExecutor:
    def __init__(self):
        self.safe_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'range': range,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
                'set': set,
                'tuple': tuple,
                'abs': abs,
                'sum': sum,
                'min': min,
                'max': max,
                'sorted': sorted,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
            }
        }
    
    def execute(self, code: str, allow_imports: bool = False) -> dict:
        """
        Execute Python code safely
        
        Args:
            code: Python code to execute
            allow_imports: Whether to allow imports (admin only)
        
        Returns:
            Dict with output, error, success status
        """
        # Capture stdout and stderr
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        
        result = {
            'success': False,
            'output': '',
            'error': '',
            'executed': False
        }
        
        try:
            # If imports allowed (admin mode), add more to safe_globals
            if allow_imports:
                exec_globals = {
                    **self.safe_globals,
                    '__name__': '__main__',
                    'sys': sys,
                    'os': __import__('os'),
                    'json': __import__('json'),
                    'math': __import__('math'),
                    'datetime': __import__('datetime'),
                    'numpy': None,  # Will try to import if available
                    'pandas': None,
                }
                
                # Try importing common libraries
                try:
                    exec_globals['numpy'] = __import__('numpy')
                except ImportError:
                    pass
                
                try:
                    exec_globals['pandas'] = __import__('pandas')
                except ImportError:
                    pass
            else:
                exec_globals = self.safe_globals.copy()
            
            # Execute code with output capture
            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                exec(code, exec_globals)
            
            result['success'] = True
            result['output'] = output_buffer.getvalue()
            result['executed'] = True
            
            # Capture any stderr (warnings)
            stderr_content = error_buffer.getvalue()
            if stderr_content:
                result['error'] = stderr_content
            
        except Exception as e:
            result['success'] = False
            result['error'] = f"{type(e).__name__}: {str(e)}\n\n{traceback.format_exc()}"
            result['output'] = output_buffer.getvalue()
        
        return result
    
    def detect_code(self, text: str) -> tuple[bool, str]:
        """
        Detect if message contains Python code (STRICT - avoid false positives)
        
        Returns:
            (has_code, extracted_code)
        """
        # ONLY detect markdown code blocks - this is the most reliable indicator
        if '```python' in text or '```py' in text:
            # Extract code from markdown code block
            if '```python' in text:
                start = text.find('```python') + 9
            else:
                start = text.find('```py') + 5
            
            end = text.find('```', start)
            if end != -1:
                return True, text[start:end].strip()
        
        # REMOVED: Triple quote detection (too many false positives with contractions)
        # REMOVED: Code pattern detection (matches normal English like "for" and "I'm")
        
        return False, ''

# Global code executor
code_executor = CodeExecutor()
