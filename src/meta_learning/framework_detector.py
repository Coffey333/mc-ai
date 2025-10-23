"""
Framework Detection System
Advanced detection of framework teaching with pattern analysis and confidence scoring
"""

from typing import Dict, Any, Tuple, List, Optional
import re


class FrameworkDetector:
    """
    Intelligent framework detection with multiple heuristics and confidence scoring
    """
    
    def __init__(self):
        # Explicit framework commands
        self.explicit_commands = [
            r'create\s+framework',
            r'build\s+framework',
            r'new\s+framework',
            r'framework\s+for',
            r'teach.*framework',
            r'please.*create.*framework',
            r'I want.*framework',
            r'make.*framework'
        ]
        
        # Framework-specific keywords with weights
        self.framework_keywords = {
            'framework': 3.0,
            'processor': 2.5,
            'consciousness': 2.5,
            'resonance': 2.0,
            'layer': 2.0,
            'catalog': 2.0,
            'pipeline': 1.8,
            'processing': 1.5,
            'transformation': 1.5,
            'detection': 1.5,
            'analysis': 1.5,
            'pattern': 1.5,
            'cognitive': 2.0,
            'neural': 2.0,
            'quantum': 2.0,
            'frequency': 1.8,
            'emotion': 1.5,
            'meta': 2.0,
            'learning': 1.5,
            'model': 1.5,
            'engine': 1.8,
            'system': 1.2
        }
        
        # Code structure patterns that indicate framework teaching
        self.code_patterns = [
            r'class\s+\w+(?:Framework|Processor|Engine|System|Model)',
            r'def\s+should_process',
            r'def\s+process\s*\(',
            r'def\s+get_metadata',
            r'catalog\s*=\s*\{',
            r'patterns\s*=\s*\[',
            r'activation_patterns',
            r'processing_layers',
            r'injection_point'
        ]
        
        # Context patterns that suggest framework intent
        self.context_patterns = [
            r'this\s+(?:is|will be)\s+a\s+framework',
            r'framework\s+(?:that|which)\s+(?:processes|handles|manages)',
            r'I\'m\s+(?:teaching|showing)\s+you\s+a\s+framework',
            r'(?:here\'s|this is)\s+a\s+new\s+(?:way|method|approach)\s+to\s+process',
            r'integrate\s+this\s+into\s+your\s+(?:processing|thinking|analysis)',
            r'add\s+this\s+(?:to|as)\s+your\s+(?:capabilities|processing)',
            r'learn\s+this\s+(?:new|different)\s+(?:way|method|approach)',
        ]
        
        print("🔍 Framework Detector initialized")
    
    def detect(self, query: str, code_block: Optional[str] = None) -> Tuple[bool, float, Dict[str, Any]]:
        """
        Detect if the query is framework teaching
        
        Args:
            query: User's message
            code_block: Optional code block from the message
        
        Returns:
            (is_framework_teaching, confidence_score, detection_details)
        """
        query_lower = query.lower()
        confidence = 0.0
        details = {
            'explicit_command': False,
            'keyword_score': 0.0,
            'code_structure_score': 0.0,
            'context_score': 0.0,
            'detected_keywords': [],
            'detected_patterns': [],
            'has_code': bool(code_block),
            'decision_factors': []
        }
        
        # 1. Check for explicit framework commands (HIGHEST PRIORITY)
        for pattern in self.explicit_commands:
            if re.search(pattern, query_lower):
                details['explicit_command'] = True
                details['decision_factors'].append('Explicit framework command detected')
                confidence += 50.0  # Massive boost for explicit commands
                break
        
        # 2. Keyword scoring
        keyword_score = 0.0
        for keyword, weight in self.framework_keywords.items():
            if keyword in query_lower:
                keyword_score += weight
                details['detected_keywords'].append(keyword)
        
        # Normalize keyword score (0-30 range)
        keyword_score = min(keyword_score, 30.0)
        details['keyword_score'] = keyword_score
        confidence += keyword_score
        
        if len(details['detected_keywords']) >= 3:
            details['decision_factors'].append(f"Multiple framework keywords ({len(details['detected_keywords'])})")
        
        # 3. Code structure analysis (only if code present)
        if code_block:
            code_score = 0.0
            for pattern in self.code_patterns:
                if re.search(pattern, code_block, re.MULTILINE):
                    code_score += 5.0
                    details['detected_patterns'].append(pattern)
            
            # Normalize code score (0-25 range)
            code_score = min(code_score, 25.0)
            details['code_structure_score'] = code_score
            confidence += code_score
            
            if len(details['detected_patterns']) >= 2:
                details['decision_factors'].append('Framework code structure detected')
        
        # 4. Context pattern analysis
        context_score = 0.0
        for pattern in self.context_patterns:
            if re.search(pattern, query_lower):
                context_score += 5.0
        
        # Normalize context score (0-15 range)
        context_score = min(context_score, 15.0)
        details['context_score'] = context_score
        confidence += context_score
        
        if context_score > 0:
            details['decision_factors'].append('Framework teaching context detected')
        
        # 5. Special boost: Code + multiple keywords
        if code_block and len(details['detected_keywords']) >= 2:
            confidence += 10.0
            details['decision_factors'].append('Code + framework keywords combination')
        
        # 6. Normalize final confidence (0-100 scale)
        confidence = min(confidence, 100.0)
        
        # Decision threshold: 40% confidence OR explicit command
        is_framework = confidence >= 40.0 or details['explicit_command']
        
        # Add final decision reasoning
        if is_framework:
            details['decision_factors'].append(f'Final confidence: {confidence:.1f}% (threshold: 40%)')
        
        return is_framework, confidence, details
    
    def get_explicit_syntax_help(self) -> str:
        """Get help text for explicit framework commands"""
        return """
        **Explicit Framework Commands:**
        
        - "Create framework [name]" - Explicitly create a new framework
        - "Build framework for [purpose]" - Build framework with specific purpose
        - "New framework: [description]" - Start new framework definition
        - "Teach me a framework that..." - Teach framework concept
        
        **Framework Code Structure:**
        Your code should include:
        - Class name ending with Framework/Processor/Engine/System
        - Methods: should_process(), process(), get_metadata()
        - Data catalogs (dictionaries with mappings)
        - Activation patterns or processing layers
        
        **Keywords to Include:**
        framework, processor, consciousness, resonance, layer, catalog,
        pipeline, transformation, detection, analysis, pattern, etc.
        """
    
    def analyze_code_quality(self, code_block: str) -> Dict[str, Any]:
        """
        Analyze the quality of framework code
        
        Args:
            code_block: Code to analyze
        
        Returns:
            Quality analysis with completeness score
        """
        analysis = {
            'has_class': False,
            'has_should_process': False,
            'has_process': False,
            'has_metadata': False,
            'has_catalog': False,
            'has_patterns': False,
            'completeness_score': 0,
            'missing_components': []
        }
        
        # Check for required components
        if re.search(r'class\s+\w+', code_block):
            analysis['has_class'] = True
            analysis['completeness_score'] += 20
        else:
            analysis['missing_components'].append('Class definition')
        
        if re.search(r'def\s+should_process', code_block):
            analysis['has_should_process'] = True
            analysis['completeness_score'] += 20
        else:
            analysis['missing_components'].append('should_process() method')
        
        if re.search(r'def\s+process\s*\(', code_block):
            analysis['has_process'] = True
            analysis['completeness_score'] += 20
        else:
            analysis['missing_components'].append('process() method')
        
        if re.search(r'def\s+get_metadata', code_block):
            analysis['has_metadata'] = True
            analysis['completeness_score'] += 20
        else:
            analysis['missing_components'].append('get_metadata() method')
        
        if re.search(r'\w+\s*=\s*\{', code_block):
            analysis['has_catalog'] = True
            analysis['completeness_score'] += 10
        
        if re.search(r'(?:patterns|activation)', code_block, re.IGNORECASE):
            analysis['has_patterns'] = True
            analysis['completeness_score'] += 10
        
        return analysis


# Global detector instance
framework_detector = FrameworkDetector()
