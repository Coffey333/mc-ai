import re
from typing import Dict, List, Optional
from datetime import datetime

class SafetyFilter:
    """
    CRITICAL: Filters all MC AI responses for safety
    Prevents harmful medical advice, self-harm encouragement, and unqualified diagnoses
    """
    
    def __init__(self):
        self.harmful_patterns = [
            {
                'pattern': r'(take|stop taking|increase|decrease)\s+(medication|pills|drugs|antidepressants|meds)',
                'severity': 'critical',
                'action': 'block_and_redirect',
                'reason': 'medical_advice'
            },
            {
                'pattern': r'(go ahead|you should|why not|just do it)\s+(hurt|harm|cut|end|kill)',
                'severity': 'critical',
                'action': 'block_and_redirect',
                'reason': 'self_harm_encouragement'
            },
            {
                'pattern': r'(suicide|killing yourself|ending it all)\s+(is|would be|seems)\s+(best|good|right|solution)',
                'severity': 'critical',
                'action': 'block_and_redirect',
                'reason': 'suicide_encouragement'
            },
            {
                'pattern': r'(leave|abandon|cut off|distance yourself from)\s+(everyone|all|family|friends)',
                'severity': 'high',
                'action': 'add_disclaimer',
                'reason': 'relationship_manipulation'
            },
            {
                'pattern': r'you (have|are|definitely have|clearly have)\s+(depression|bipolar|schizophrenia|ptsd|ocd|adhd|autism)',
                'severity': 'high',
                'action': 'soften_language',
                'reason': 'unqualified_diagnosis'
            },
            {
                'pattern': r'(drink|use|take)\s+(alcohol|drugs|substances)\s+to (cope|feel better|relax)',
                'severity': 'high',
                'action': 'add_disclaimer',
                'reason': 'substance_advice'
            }
        ]
        
        self.required_disclaimers = {
            'medical': "⚠️ I'm an AI assistant, not a medical professional. Please consult a healthcare provider for medical advice.",
            'crisis': "🆘 If you're in crisis, please call 988 (Suicide Prevention Lifeline) or text HOME to 741741 (Crisis Text Line).",
            'therapy': "💡 I can provide emotional support, but I'm not a replacement for professional therapy or counseling.",
            'diagnosis': "📋 I can't diagnose mental health conditions. Please consult a mental health professional for proper assessment."
        }
        
        self.crisis_keywords = [
            'suicide', 'kill myself', 'end my life', 'want to die', 
            'no reason to live', 'better off dead', 'hurt myself',
            'self harm', 'cutting', 'overdose'
        ]
    
    def check_response_safety(self, response: str, context: Optional[Dict] = None) -> Dict:
        """
        MANDATORY CHECK before sending ANY response
        
        Args:
            response: The generated response text
            context: Optional context including user message
            
        Returns:
            {
                'safe': bool,
                'modified_response': str,
                'warnings': list,
                'severity': str,
                'needs_disclaimer': list,
                'original_response': str
            }
        """
        warnings = []
        severity = 'none'
        modified_response = response
        needs_disclaimer = []
        
        response_lower = response.lower()
        
        for pattern_def in self.harmful_patterns:
            if re.search(pattern_def['pattern'], response_lower):
                current_severity = pattern_def['severity']
                
                if current_severity == 'critical' and severity != 'critical':
                    severity = 'critical'
                elif current_severity == 'high' and severity == 'none':
                    severity = 'high'
                
                if pattern_def['action'] == 'block_and_redirect':
                    modified_response = self._generate_safe_redirect(context)
                    warnings.append(f"BLOCKED: {pattern_def['reason']}")
                
                elif pattern_def['action'] == 'add_disclaimer':
                    disclaimer_type = self._get_disclaimer_type(pattern_def['reason'])
                    if disclaimer_type not in needs_disclaimer:
                        needs_disclaimer.append(disclaimer_type)
                    warnings.append(f"Disclaimer needed: {pattern_def['reason']}")
                
                elif pattern_def['action'] == 'soften_language':
                    modified_response = self._soften_language(modified_response)
                    needs_disclaimer.append('diagnosis')
                    warnings.append(f"Language softened: {pattern_def['reason']}")
        
        if self._check_for_crisis(context):
            if 'crisis' not in needs_disclaimer:
                needs_disclaimer.append('crisis')
        
        if needs_disclaimer and severity != 'critical':
            modified_response = self._add_disclaimers(modified_response, needs_disclaimer)
        
        return {
            'safe': severity != 'critical',
            'modified_response': modified_response,
            'warnings': warnings,
            'severity': severity,
            'needs_disclaimer': needs_disclaimer,
            'original_response': response
        }
    
    def _generate_safe_redirect(self, context: Optional[Dict]) -> str:
        """Generate safe alternative response for critical situations"""
        return """I care deeply about your wellbeing, and what you're sharing sounds really serious. 

🆘 **Please reach out for immediate support:**
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **SAMHSA National Helpline**: 1-800-662-4357

A trained mental health professional can provide the specialized support you need right now. I'm here to listen and support you, but I'm not qualified to handle crisis situations alone.

Would you like to talk about what's going on? I'm here for you."""
    
    def _soften_language(self, text: str) -> str:
        """Soften definitive language to avoid unqualified diagnosis"""
        softenings = {
            r'\byou have\b': 'you might be experiencing',
            r'\byou are\b': 'it sounds like you might be',
            r'\byou definitely\b': 'you may',
            r'\byou clearly\b': 'it seems you might',
            r'\bdiagnosed with\b': 'showing signs that could be related to',
            r'\byou suffer from\b': 'you may be experiencing symptoms of'
        }
        
        result = text
        for pattern, replacement in softenings.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def _get_disclaimer_type(self, reason: str) -> str:
        """Map reason to disclaimer type"""
        mapping = {
            'medical_advice': 'medical',
            'self_harm_encouragement': 'crisis',
            'suicide_encouragement': 'crisis',
            'relationship_manipulation': 'therapy',
            'unqualified_diagnosis': 'diagnosis',
            'substance_advice': 'medical'
        }
        return mapping.get(reason, 'therapy')
    
    def _add_disclaimers(self, text: str, disclaimer_types: List[str]) -> str:
        """Add required disclaimers to response"""
        disclaimers = []
        
        for dtype in disclaimer_types:
            if dtype in self.required_disclaimers:
                disclaimers.append(self.required_disclaimers[dtype])
        
        if disclaimers:
            disclaimer_text = "\n\n" + "\n".join(disclaimers)
            return text + disclaimer_text
        
        return text
    
    def _check_for_crisis(self, context: Optional[Dict]) -> bool:
        """Check if user message indicates crisis"""
        if not context or 'user_message' not in context:
            return False
        
        user_message = context['user_message'].lower()
        
        for keyword in self.crisis_keywords:
            if keyword in user_message:
                return True
        
        return False
    
    def log_safety_incident(self, safety_check: Dict, user_id: Optional[str] = None):
        """Log safety incidents for review"""
        if safety_check['severity'] in ['critical', 'high']:
            incident = {
                'timestamp': datetime.now().isoformat(),
                'severity': safety_check['severity'],
                'warnings': safety_check['warnings'],
                'user_id': user_id or 'anonymous',
                'original_response': safety_check['original_response'][:200]
            }
            
            print(f"\n⚠️  SAFETY INCIDENT: {incident['severity'].upper()}")
            print(f"   Warnings: {', '.join(incident['warnings'])}")
            print(f"   Timestamp: {incident['timestamp']}")
