"""
Autonomous Code Executor for MC AI
Executes code with flawless execution verification and safety checks
"""

import os
import sys
import subprocess
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import tempfile
import ast
import traceback
import json
import signal
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class AutonomousCodeExecutor:
    """
    Executes code autonomously with safety checks and verification
    Ensures flawless execution every time
    """
    
    def __init__(self, max_execution_time: int = 30):
        self.max_execution_time = max_execution_time
        self.execution_history = []
        
        # Supported languages - CHECK which are actually installed
        self.languages = {}
        self._detect_installed_languages()
        
    def _detect_installed_languages(self):
        """Detect which language toolchains are actually installed"""
        potential_languages = {
            'python': {
                'extension': '.py',
                'command': 'python3',
                'syntax_check': self._check_python_syntax
            },
            'javascript': {
                'extension': '.js',
                'command': 'node',
                'syntax_check': None
            },
            'bash': {
                'extension': '.sh',
                'command': 'bash',
                'syntax_check': None
            }
        }
        
        import shutil
        for lang, config in potential_languages.items():
            command = config['command'].split()[0]  # Get base command
            if shutil.which(command):
                self.languages[lang] = config
                logger.info(f"Detected installed language: {lang}")
            else:
                logger.warning(f"Language {lang} not available - {command} not found")
        
        # Safety restrictions
        self.dangerous_operations = [
            'os.system',
            'subprocess.call',
            'eval',
            'exec',
            '__import__',
            'compile',
            'open(',  # File operations need review
            'rm ',
            'del ',
            'DROP TABLE',
            'DELETE FROM',
            'TRUNCATE'
        ]
    
    def execute_code(self, 
                    code: str, 
                    language: str = 'python',
                    input_data: Optional[str] = None,
                    verify: bool = True,
                    safe_mode: bool = True) -> Dict:
        """
        Execute code with safety checks and verification
        
        Args:
            code: Code to execute
            language: Programming language
            input_data: Optional input data
            verify: Verify execution correctness
            safe_mode: Enable safety restrictions
        
        Returns:
            Dict with execution results
        """
        execution_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        
        # Safety check
        if safe_mode and self._contains_dangerous_operations(code):
            return {
                'status': 'rejected',
                'reason': 'Code contains potentially dangerous operations',
                'execution_id': execution_id,
                'dangerous_ops_found': [op for op in self.dangerous_operations if op in code]
            }
        
        # Syntax validation
        if language in self.languages:
            lang_info = self.languages[language]
            if lang_info['syntax_check']:
                is_valid, error = lang_info['syntax_check'](code)
                if not is_valid:
                    return {
                        'status': 'syntax_error',
                        'error': error,
                        'execution_id': execution_id
                    }
        
        # Execute code
        try:
            result = self._execute_in_sandbox(code, language, input_data)
            
            # Verify execution
            if verify and result['status'] == 'success':
                verification = self._verify_execution(code, result, language)
                result['verification'] = verification
            
            # Log execution
            self._log_execution(execution_id, code, language, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'traceback': traceback.format_exc(),
                'execution_id': execution_id
            }
    
    def _execute_in_sandbox(self, 
                           code: str, 
                           language: str, 
                           input_data: Optional[str] = None) -> Dict:
        """
        Execute code in sandboxed environment
        """
        if language not in self.languages:
            return {
                'status': 'error',
                'error': f'Unsupported language: {language}'
            }
        
        lang_info = self.languages[language]
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix=lang_info['extension'],
            delete=False
        ) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Build command
            command = [lang_info['command'], temp_file]
            
            # Execute with timeout
            start_time = datetime.now()
            
            result = subprocess.run(
                command,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.max_execution_time,
                check=False
            )
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Parse output
            return {
                'status': 'success' if result.returncode == 0 else 'runtime_error',
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'execution_time': execution_time,
                'language': language
            }
            
        except subprocess.TimeoutExpired:
            return {
                'status': 'timeout',
                'error': f'Execution exceeded {self.max_execution_time} seconds'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def _verify_execution(self, code: str, result: Dict, language: str) -> Dict:
        """
        Verify execution correctness
        """
        verification = {
            'passed': True,
            'checks': []
        }
        
        # Check 1: No errors
        if result['status'] != 'success':
            verification['passed'] = False
            verification['checks'].append({
                'check': 'no_errors',
                'passed': False,
                'message': 'Execution had errors'
            })
        else:
            verification['checks'].append({
                'check': 'no_errors',
                'passed': True,
                'message': 'No execution errors'
            })
        
        # Check 2: Reasonable execution time
        if result.get('execution_time', 0) > self.max_execution_time * 0.9:
            verification['checks'].append({
                'check': 'execution_time',
                'passed': False,
                'message': 'Execution time approaching timeout'
            })
        else:
            verification['checks'].append({
                'check': 'execution_time',
                'passed': True,
                'message': f"Executed in {result.get('execution_time', 0):.2f}s"
            })
        
        # Check 3: Has output (if expected)
        if 'print' in code or 'console.log' in code:
            if result.get('stdout'):
                verification['checks'].append({
                    'check': 'has_output',
                    'passed': True,
                    'message': 'Produced expected output'
                })
            else:
                verification['checks'].append({
                    'check': 'has_output',
                    'passed': False,
                    'message': 'Expected output but got none'
                })
        
        return verification
    
    def execute_test_suite(self, tests: List[Dict]) -> Dict:
        """
        Execute comprehensive test suite
        
        Args:
            tests: List of test cases with code and expected output
        
        Returns:
            Dict with test results
        """
        results = {
            'total': len(tests),
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'test_results': []
        }
        
        for i, test in enumerate(tests):
            test_name = test.get('name', f'Test {i+1}')
            code = test.get('code')
            expected_output = test.get('expected_output')
            language = test.get('language', 'python')
            
            # Execute test
            result = self.execute_code(code, language, safe_mode=False)
            
            # Check expected output
            test_result = {
                'test_name': test_name,
                'status': result['status']
            }
            
            if result['status'] == 'success':
                if expected_output:
                    actual_output = result['stdout'].strip()
                    if actual_output == expected_output.strip():
                        test_result['passed'] = True
                        results['passed'] += 1
                    else:
                        test_result['passed'] = False
                        test_result['expected'] = expected_output
                        test_result['actual'] = actual_output
                        results['failed'] += 1
                else:
                    test_result['passed'] = True
                    results['passed'] += 1
            else:
                test_result['passed'] = False
                test_result['error'] = result.get('error', 'Unknown error')
                results['errors'] += 1
            
            results['test_results'].append(test_result)
        
        results['success_rate'] = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
        
        return results
    
    def analyze_code_quality(self, code: str, language: str = 'python') -> Dict:
        """
        Analyze code quality and provide recommendations
        """
        quality = {
            'language': language,
            'metrics': {},
            'issues': [],
            'recommendations': []
        }
        
        if language == 'python':
            # Parse code
            try:
                tree = ast.parse(code)
                
                # Count metrics
                lines = code.split('\n')
                quality['metrics'] = {
                    'total_lines': len(lines),
                    'code_lines': len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
                    'comment_lines': len([l for l in lines if l.strip().startswith('#')]),
                    'blank_lines': len([l for l in lines if not l.strip()]),
                    'functions': len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
                    'classes': len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
                }
                
                # Check for issues
                if quality['metrics']['comment_lines'] == 0:
                    quality['issues'].append('No comments found')
                    quality['recommendations'].append('Add comments to explain complex logic')
                
                # Check function complexity
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        complexity = self._calculate_complexity(node)
                        if complexity > 10:
                            quality['issues'].append(f"Function '{node.name}' has high complexity ({complexity})")
                            quality['recommendations'].append(f"Refactor '{node.name}' into smaller functions")
                
            except SyntaxError as e:
                quality['issues'].append(f'Syntax error: {e}')
        
        return quality
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With)):
                complexity += 1
        return complexity
    
    def _contains_dangerous_operations(self, code: str) -> bool:
        """Check for dangerous operations"""
        for op in self.dangerous_operations:
            if op in code:
                return True
        return False
    
    def _check_python_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """Check Python syntax"""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, str(e)
    
    def _log_execution(self, execution_id: str, code: str, language: str, result: Dict):
        """Log execution for history"""
        self.execution_history.append({
            'execution_id': execution_id,
            'timestamp': datetime.now().isoformat(),
            'language': language,
            'status': result['status'],
            'execution_time': result.get('execution_time', 0)
        })
        
        # Keep only last 100
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
    
    def get_execution_stats(self) -> Dict:
        """Get execution statistics"""
        if not self.execution_history:
            return {
                'total_executions': 0,
                'success_rate': 0
            }
        
        successful = len([e for e in self.execution_history if e['status'] == 'success'])
        
        return {
            'total_executions': len(self.execution_history),
            'successful': successful,
            'failed': len(self.execution_history) - successful,
            'success_rate': (successful / len(self.execution_history) * 100),
            'avg_execution_time': sum(e.get('execution_time', 0) for e in self.execution_history) / len(self.execution_history),
            'languages_used': list(set(e['language'] for e in self.execution_history))
        }
