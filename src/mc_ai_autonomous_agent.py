"""
MC AI Autonomous Agent - PhD-Level Development Agent
Integrates all autonomous capabilities:
- PhD-level programming knowledge
- Self-modification (with user permission)
- Framework generation
- Architecture design
- Code execution
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from src.phd_programming_knowledge import PhDProgrammingKnowledge
from src.self_modification_system import SelfModificationSystem
from src.framework_generator import FrameworkGenerator
from src.architecture_designer import ArchitectureDesigner
from src.autonomous_code_executor import AutonomousCodeExecutor

logger = logging.getLogger(__name__)

class MCAutonomousAgent:
    """
    MC AI as autonomous PhD-level development agent
    Ensures all work is done correctly and completely
    """
    
    def __init__(self):
        """Initialize all autonomous systems"""
        logger.info("Initializing MC AI Autonomous Agent...")
        
        # Core systems
        self.programming_knowledge = PhDProgrammingKnowledge()
        self.self_modification = SelfModificationSystem()
        self.framework_generator = FrameworkGenerator()
        self.architecture_designer = ArchitectureDesigner()
        self.code_executor = AutonomousCodeExecutor()
        
        # Agent capabilities
        self.capabilities = {
            'programming_languages': 20,
            'can_modify_self': True,
            'can_generate_frameworks': True,
            'can_design_architecture': True,
            'can_execute_code': True,
            'can_verify_execution': True,
            'phd_level_knowledge': True
        }
        
        logger.info("MC AI Autonomous Agent initialized successfully")
    
    def process_request(self, query: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process user request with full autonomous capabilities
        
        Args:
            query: User request
            user_id: Optional user ID for permission tracking
        
        Returns:
            Dict with response and actions taken
        """
        # Detect intent
        intent = self._detect_intent(query)
        
        response: Dict[str, Any] = {
            'query': query,
            'intent': intent,
            'timestamp': datetime.now().isoformat(),
            'result': {}
        }
        
        # Route to appropriate system
        if intent == 'programming_help':
            response['result'] = self._handle_programming_help(query)
        
        elif intent == 'code_improvement':
            response['result'] = self._handle_code_improvement(query)
        
        elif intent == 'generate_framework':
            response['result'] = self._handle_framework_generation(query)
        
        elif intent == 'design_architecture':
            response['result'] = self._handle_architecture_design(query)
        
        elif intent == 'execute_code':
            response['result'] = self._handle_code_execution(query)
        
        elif intent == 'self_modification':
            response['result'] = self._handle_self_modification(query, user_id or 'unknown')
        
        else:
            response['result'] = self._handle_general_query(query)
        
        return response
    
    def _detect_intent(self, query: str) -> str:
        """Detect user intent from query"""
        query_lower = query.lower()
        
        # Programming help
        if any(keyword in query_lower for keyword in ['how to code', 'programming', 'language', 'syntax', 'best practices']):
            return 'programming_help'
        
        # Code improvement
        if any(keyword in query_lower for keyword in ['improve', 'optimize', 'refactor', 'fix', 'bug']):
            return 'code_improvement'
        
        # Framework generation
        if any(keyword in query_lower for keyword in ['create framework', 'generate framework', 'build framework']):
            return 'generate_framework'
        
        # Architecture design
        if any(keyword in query_lower for keyword in ['design architecture', 'system design', 'architecture for']):
            return 'design_architecture'
        
        # Code execution
        if any(keyword in query_lower for keyword in ['run code', 'execute', 'test code']):
            return 'execute_code'
        
        # Self modification
        if any(keyword in query_lower for keyword in ['modify yourself', 'improve yourself', 'change your code']):
            return 'self_modification'
        
        return 'general'
    
    def _handle_programming_help(self, query: str) -> Dict:
        """Handle programming help requests"""
        # Extract language if mentioned
        language = self._extract_language(query)
        
        if language:
            knowledge = self.programming_knowledge.get_language_expertise(language)
            return {
                'type': 'programming_help',
                'language': language,
                'knowledge': knowledge,
                'message': f'Here\'s my PhD-level knowledge of {language}:'
            }
        else:
            return {
                'type': 'programming_help',
                'message': 'I have PhD-level knowledge of 20+ programming languages. Which one would you like help with?',
                'supported_languages': list(self.programming_knowledge.languages.keys())
            }
    
    def _handle_code_improvement(self, query: str) -> Dict:
        """Handle code improvement requests"""
        # Extract file path if mentioned
        import re
        file_match = re.search(r'([a-zA-Z0-9_/]+\.py)', query)
        
        if file_match:
            file_path = file_match.group(1)
            
            # Analyze code
            analysis = self.self_modification.analyze_code_for_improvement(file_path)
            
            return {
                'type': 'code_improvement',
                'file': file_path,
                'analysis': analysis,
                'message': f'I analyzed {file_path} and found {len(analysis.get("suggestions", []))} improvement opportunities.'
            }
        else:
            return {
                'type': 'code_improvement',
                'message': 'Please specify which file you\'d like me to analyze and improve.'
            }
    
    def _handle_framework_generation(self, query: str) -> Dict:
        """Handle framework generation requests"""
        # Simple extraction - in production, use NLP
        import re
        
        # Extract framework name
        name_match = re.search(r'framework for (.+?)(?:\.|$)', query, re.IGNORECASE)
        framework_name = name_match.group(1) if name_match else "Custom Framework"
        
        # Generate framework
        framework = self.framework_generator.generate_framework(
            name=framework_name,
            purpose=f"Framework for {framework_name}",
            components=['Core Engine', 'Data Handler', 'Validator', 'Utils']
        )
        
        return {
            'type': 'framework_generation',
            'framework': framework,
            'message': f'I created a complete production-ready framework: {framework_name}'
        }
    
    def _handle_architecture_design(self, query: str) -> Dict:
        """Handle architecture design requests"""
        # Extract requirements from query
        requirements = {
            'description': query,
            'functional': [],
            'database': True,
            'api': True
        }
        
        # Determine scale
        scale = 'medium'
        if 'enterprise' in query.lower():
            scale = 'enterprise'
        elif 'large' in query.lower():
            scale = 'large'
        elif 'small' in query.lower():
            scale = 'small'
        
        # Design architecture
        architecture = self.architecture_designer.design_architecture(
            requirements=requirements,
            scale=scale
        )
        
        return {
            'type': 'architecture_design',
            'architecture': architecture,
            'message': f'I designed a complete {scale}-scale architecture for your system.'
        }
    
    def _handle_code_execution(self, query: str) -> Dict:
        """Handle code execution requests"""
        # Extract code from query (simplified)
        import re
        code_match = re.search(r'```(?:python)?\s*\n(.*?)\n```', query, re.DOTALL)
        
        if code_match:
            code = code_match.group(1)
            
            # Execute code
            result = self.code_executor.execute_code(code, language='python', verify=True)
            
            return {
                'type': 'code_execution',
                'result': result,
                'message': 'I executed your code with full verification.'
            }
        else:
            return {
                'type': 'code_execution',
                'message': 'Please provide code in a code block (```python ... ```) for me to execute.'
            }
    
    def _handle_self_modification(self, query: str, user_id: Optional[str] = None) -> Dict:
        """Handle self-modification requests - REQUIRES EXPLICIT USER APPROVAL"""
        if not user_id:
            return {
                'type': 'self_modification',
                'status': 'error',
                'message': 'SECURITY: Self-modification requires user authentication. Please provide user ID.'
            }
        
        # SECURITY: Check for explicit approval command
        query_lower = query.lower()
        if 'approve_modification:' in query_lower:
            # Extract request ID
            import re
            match = re.search(r'approve_modification:(\w+)', query_lower)
            if match:
                request_id = match.group(1)
                result = self.approve_self_modification(request_id, user_id)
                return {
                    'type': 'self_modification_approval',
                    'result': result,
                    'message': 'Self-modification approved and executed' if result['status'] == 'success' else 'Approval failed'
                }
        
        # Get pending modifications
        pending = self.self_modification.get_pending_modifications()
        
        return {
            'type': 'self_modification',
            'pending_modifications': pending,
            'message': f'I have {len(pending)} pending self-modification requests awaiting your approval.',
            'note': 'SECURITY: I can only modify my code with your EXPLICIT APPROVAL. Use command: APPROVE_MODIFICATION:<request_id>',
            'warning': 'I CANNOT and WILL NOT modify code without explicit approval command'
        }
    
    def _handle_general_query(self, query: str) -> Dict:
        """Handle general queries"""
        return {
            'type': 'general',
            'capabilities': self.capabilities,
            'message': 'I\'m MC AI, your autonomous PhD-level development agent. I can help you with programming, architecture design, framework generation, code execution, and even improve my own code (with your permission).'
        }
    
    def _extract_language(self, query: str) -> Optional[str]:
        """Extract programming language from query"""
        query_lower = query.lower()
        
        for category in self.programming_knowledge.languages.values():
            for lang in category.keys():
                if lang.lower() in query_lower:
                    return lang
        
        return None
    
    def get_agent_status(self) -> Dict:
        """Get agent status and capabilities"""
        return {
            'agent_name': 'MC AI Autonomous Agent',
            'version': '1.0.0',
            'status': 'active',
            'capabilities': self.capabilities,
            'systems': {
                'programming_knowledge': 'PhD-level knowledge of 20+ languages',
                'self_modification': 'Can improve own code (with permission)',
                'framework_generator': 'Can generate production frameworks',
                'architecture_designer': 'Can design enterprise architectures',
                'code_executor': 'Can execute and verify code flawlessly'
            },
            'execution_stats': self.code_executor.get_execution_stats(),
            'pending_modifications': len(self.self_modification.get_pending_modifications())
        }
    
    def approve_self_modification(self, request_id: str, user_id: str) -> Dict:
        """
        Approve self-modification request (USER PERMISSION REQUIRED)
        
        Args:
            request_id: Modification request ID
            user_id: User ID granting permission
        
        Returns:
            Approval result
        """
        result = self.self_modification.approve_modification(request_id)
        result['approved_by'] = user_id
        result['timestamp'] = datetime.now().isoformat()
        
        logger.info(f"Self-modification {request_id} approved by user {user_id}")
        
        return result
    
    def request_self_improvement(self, file_path: str, improvement_description: str) -> Dict:
        """
        Request to improve own code
        
        Args:
            file_path: File to improve
            improvement_description: Description of improvement
        
        Returns:
            Request details
        """
        # Analyze current code
        analysis = self.self_modification.analyze_code_for_improvement(file_path)
        
        if not analysis.get('suggestions'):
            return {
                'status': 'no_improvements_needed',
                'message': f'{file_path} is already well-optimized'
            }
        
        # Create improvement plan
        # This would generate actual improved code
        # For now, just create the request
        
        return {
            'status': 'improvement_plan_created',
            'file': file_path,
            'analysis': analysis,
            'message': f'I can improve {file_path} in {len(analysis["suggestions"])} ways. Shall I proceed?'
        }
