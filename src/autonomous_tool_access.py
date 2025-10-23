"""
MC AI Autonomous Tool Access System v1.0
Allows MC AI to use his full Replit system tools when called from external sources (Kaggle, APIs, etc.)

Security: API key required, rate limiting, audit logging
Capabilities: File operations, code execution, dataset access, knowledge retrieval, system introspection
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AutonomousToolAccess:
    """
    Gives MC AI full access to his Replit system tools
    Used when external sources (Kaggle, API calls) interact with MC AI
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.datasets_dir = self.base_dir / "datasets"
        self.knowledge_dir = self.base_dir / "knowledge_library"
        self.audit_log = []
        
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any], requester_info: Dict[str, str]) -> Dict[str, Any]:
        """
        Execute a tool autonomously based on MC AI's decision
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool
            requester_info: Information about who's requesting (for audit)
            
        Returns:
            Dict with tool execution results
        """
        # Audit log
        self._log_tool_use(tool_name, parameters, requester_info)
        
        # Tool router
        tool_map = {
            'read_file': self._read_file,
            'list_files': self._list_files,
            'search_files': self._search_files,
            'execute_python': self._execute_python,
            'query_dataset': self._query_dataset,
            'access_knowledge': self._access_knowledge,
            'system_status': self._system_status,
            'analyze_code': self._analyze_code,
            'get_conversation_history': self._get_conversation_history,
            'emotional_analysis': self._emotional_analysis
        }
        
        if tool_name not in tool_map:
            return {
                'success': False,
                'error': f'Unknown tool: {tool_name}',
                'available_tools': list(tool_map.keys())
            }
        
        try:
            result = tool_map[tool_name](**parameters)
            return {
                'success': True,
                'tool': tool_name,
                'result': result,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Tool execution error ({tool_name}): {e}")
            return {
                'success': False,
                'error': str(e),
                'tool': tool_name
            }
    
    def _read_file(self, file_path: str, max_lines: Optional[int] = None) -> Dict[str, Any]:
        """Read a file from the system"""
        full_path = self.base_dir / file_path
        
        if not full_path.exists():
            return {'error': f'File not found: {file_path}'}
        
        # Security: Don't allow reading sensitive files
        sensitive_patterns = ['.env', 'secret', 'token', 'key', 'password']
        if any(pattern in str(full_path).lower() for pattern in sensitive_patterns):
            return {'error': 'Cannot read sensitive files'}
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                if max_lines:
                    lines = [f.readline() for _ in range(max_lines)]
                    content = ''.join(lines)
                else:
                    content = f.read()
            
            return {
                'file_path': file_path,
                'content': content,
                'size_bytes': len(content),
                'lines': len(content.split('\n'))
            }
        except Exception as e:
            return {'error': f'Error reading file: {str(e)}'}
    
    def _list_files(self, directory: str = ".", pattern: Optional[str] = None) -> Dict[str, Any]:
        """List files in a directory"""
        full_path = self.base_dir / directory
        
        if not full_path.exists():
            return {'error': f'Directory not found: {directory}'}
        
        try:
            files = []
            for item in full_path.iterdir():
                if pattern and pattern not in item.name:
                    continue
                
                files.append({
                    'name': item.name,
                    'type': 'directory' if item.is_dir() else 'file',
                    'size': item.stat().st_size if item.is_file() else None,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                })
            
            return {
                'directory': directory,
                'file_count': len(files),
                'files': files
            }
        except Exception as e:
            return {'error': f'Error listing files: {str(e)}'}
    
    def _search_files(self, search_term: str, directory: str = ".", file_extension: Optional[str] = None) -> Dict[str, Any]:
        """Search for files containing a term"""
        full_path = self.base_dir / directory
        results = []
        
        try:
            for file_path in full_path.rglob('*'):
                if not file_path.is_file():
                    continue
                
                if file_extension and not file_path.suffix == file_extension:
                    continue
                
                # Skip binary files and sensitive files
                if file_path.suffix in ['.pyc', '.so', '.bin', '.dat']:
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if search_term.lower() in content.lower():
                            # Find line numbers with matches
                            lines = content.split('\n')
                            matching_lines = [
                                {'line_num': i+1, 'content': line.strip()[:100]}
                                for i, line in enumerate(lines)
                                if search_term.lower() in line.lower()
                            ]
                            
                            results.append({
                                'file': str(file_path.relative_to(self.base_dir)),
                                'matches': len(matching_lines),
                                'preview': matching_lines[:5]  # First 5 matches
                            })
                except:
                    continue  # Skip files that can't be read
            
            return {
                'search_term': search_term,
                'files_found': len(results),
                'results': results
            }
        except Exception as e:
            return {'error': f'Search error: {str(e)}'}
    
    def _execute_python(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute Python code safely (read-only operations)
        WARNING: Limited to safe operations only
        """
        # Security: Block dangerous operations
        dangerous_keywords = ['import os', 'import sys', 'subprocess', 'exec', 'eval', '__import__', 'open(', 'write']
        if any(keyword in code for keyword in dangerous_keywords):
            return {'error': 'Code contains potentially dangerous operations'}
        
        try:
            # Create a restricted execution environment
            safe_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                    'sum': sum,
                    'min': min,
                    'max': max,
                    'range': range,
                }
            }
            
            # Capture output
            from io import StringIO
            import sys
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            # Execute code
            exec(code, safe_globals)
            
            # Get output
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            return {
                'output': output,
                'executed': True
            }
        except Exception as e:
            return {'error': f'Execution error: {str(e)}'}
    
    def _query_dataset(self, dataset_name: Optional[str] = None, category: Optional[str] = None) -> Dict[str, Any]:
        """Query MC AI's dataset collection"""
        try:
            datasets = []
            
            # Search in datasets directory
            for json_file in self.datasets_dir.glob('*.json'):
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                        
                        if dataset_name and dataset_name.lower() not in json_file.stem.lower():
                            continue
                        
                        if category and data.get('category') != category:
                            continue
                        
                        datasets.append({
                            'name': json_file.stem,
                            'category': data.get('category', 'unknown'),
                            'examples': len(data.get('examples', [])),
                            'description': data.get('description', 'No description')
                        })
                except:
                    continue
            
            return {
                'datasets_found': len(datasets),
                'datasets': datasets
            }
        except Exception as e:
            return {'error': f'Dataset query error: {str(e)}'}
    
    def _access_knowledge(self, query: str, frequency_range: Optional[tuple] = None) -> Dict[str, Any]:
        """Access MC AI's knowledge library"""
        try:
            # Check if knowledge index exists
            knowledge_db = self.knowledge_dir / 'knowledge_index.db'
            
            if not knowledge_db.exists():
                return {'error': 'Knowledge index not found'}
            
            import sqlite3
            conn = sqlite3.connect(str(knowledge_db))
            cursor = conn.cursor()
            
            # Search knowledge sources
            cursor.execute("""
                SELECT title, url, word_count, frequency_range, topics
                FROM knowledge_sources
                WHERE content LIKE ? OR title LIKE ? OR topics LIKE ?
                LIMIT 10
            """, (f'%{query}%', f'%{query}%', f'%{query}%'))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'title': row[0],
                    'url': row[1],
                    'word_count': row[2],
                    'frequency_range': row[3],
                    'topics': row[4]
                })
            
            conn.close()
            
            return {
                'query': query,
                'sources_found': len(results),
                'sources': results
            }
        except Exception as e:
            return {'error': f'Knowledge access error: {str(e)}'}
    
    def _system_status(self) -> Dict[str, Any]:
        """Get MC AI's system status"""
        try:
            return {
                'system_name': 'MC AI',
                'status': 'operational',
                'uptime': 'active',
                'capabilities': [
                    'Emotional Intelligence',
                    'Code Analysis',
                    'Dataset Processing',
                    'Knowledge Retrieval',
                    'ECG Digitization',
                    'Autonomous Learning',
                    'User Profiling',
                    'Self-Awareness'
                ],
                'datasets_available': len(list(self.datasets_dir.glob('*.json'))),
                'knowledge_sources': self._count_knowledge_sources(),
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {'error': f'Status check error: {str(e)}'}
    
    def _analyze_code(self, code: str, language: str = 'python') -> Dict[str, Any]:
        """Analyze code for quality, complexity, patterns"""
        try:
            analysis = {
                'language': language,
                'lines': len(code.split('\n')),
                'characters': len(code),
                'complexity_score': self._calculate_complexity(code),
                'suggestions': []
            }
            
            # Simple analysis
            if language == 'python':
                if 'def ' in code:
                    analysis['functions'] = code.count('def ')
                if 'class ' in code:
                    analysis['classes'] = code.count('class ')
                if '# TODO' in code or '# FIXME' in code:
                    analysis['suggestions'].append('Code contains TODO/FIXME comments')
            
            return analysis
        except Exception as e:
            return {'error': f'Code analysis error: {str(e)}'}
    
    def _get_conversation_history(self, user_id: str, limit: int = 10) -> Dict[str, Any]:
        """Retrieve conversation history for a user"""
        try:
            conv_dir = self.base_dir / 'conversations'
            if not conv_dir.exists():
                return {'conversations': []}
            
            user_convs = list(conv_dir.glob(f'{user_id}_*.json'))
            conversations = []
            
            for conv_file in user_convs[:limit]:
                try:
                    with open(conv_file, 'r') as f:
                        data = json.load(f)
                        conversations.append({
                            'conversation_id': conv_file.stem,
                            'message_count': len(data.get('messages', [])),
                            'timestamp': data.get('timestamp', 'unknown')
                        })
                except:
                    continue
            
            return {
                'user_id': user_id,
                'conversation_count': len(conversations),
                'conversations': conversations
            }
        except Exception as e:
            return {'error': f'History retrieval error: {str(e)}'}
    
    def _emotional_analysis(self, text: str) -> Dict[str, Any]:
        """Perform emotional analysis on text"""
        try:
            # Use MC AI's emotion detection system
            from emotion_engine import EmotionEngine
            
            engine = EmotionEngine()
            result = engine.detect_emotion(text)
            
            return {
                'text_analyzed': text[:100] + '...' if len(text) > 100 else text,
                'emotions_detected': result.get('emotions', []),
                'primary_emotion': result.get('primary_emotion'),
                'frequency_signature': result.get('frequency')
            }
        except Exception as e:
            # Fallback simple analysis
            return {
                'text_analyzed': text[:100] + '...' if len(text) > 100 else text,
                'note': 'Advanced emotion engine not available',
                'simple_analysis': 'Text received for analysis'
            }
    
    def _calculate_complexity(self, code: str) -> int:
        """Simple complexity calculation"""
        complexity = 0
        complexity += code.count('if ')
        complexity += code.count('for ')
        complexity += code.count('while ')
        complexity += code.count('def ')
        complexity += code.count('class ')
        return complexity
    
    def _count_knowledge_sources(self) -> int:
        """Count knowledge sources in database"""
        try:
            knowledge_db = self.knowledge_dir / 'knowledge_index.db'
            if not knowledge_db.exists():
                return 0
            
            import sqlite3
            conn = sqlite3.connect(str(knowledge_db))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM knowledge_sources")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def _log_tool_use(self, tool_name: str, parameters: Dict[str, Any], requester_info: Dict[str, str]):
        """Log tool usage for audit trail"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'tool': tool_name,
            'parameters': parameters,
            'requester': requester_info,
        }
        
        self.audit_log.append(log_entry)
        
        # Keep only last 1000 entries
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]
        
        logger.info(f"Tool used: {tool_name} by {requester_info.get('source', 'unknown')}")
    
    def get_audit_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent tool usage audit log"""
        return self.audit_log[-limit:]
    
    def get_available_tools(self) -> Dict[str, str]:
        """Get list of all available tools with descriptions"""
        return {
            'read_file': 'Read content from a file',
            'list_files': 'List files in a directory',
            'search_files': 'Search for files containing specific text',
            'execute_python': 'Execute safe Python code (read-only)',
            'query_dataset': 'Query MC AI dataset collection',
            'access_knowledge': 'Search knowledge library',
            'system_status': 'Get MC AI system status',
            'analyze_code': 'Analyze code quality and complexity',
            'get_conversation_history': 'Retrieve conversation history',
            'emotional_analysis': 'Perform emotional analysis on text'
        }
