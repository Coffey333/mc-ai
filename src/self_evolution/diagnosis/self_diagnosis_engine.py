"""
Self-Diagnosis Engine
MC AI analyzes errors and proposes fixes autonomously
"""

import json
from typing import Dict, List, Optional
from pathlib import Path

class SelfDiagnosisEngine:
    """
    Enables MC AI to analyze errors and propose code fixes
    """
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.diagnosis_history = []
        self.fix_success_rate = {}
        
    async def diagnose_error(self, error_data: Dict) -> Dict:
        """
        MC AI analyzes an error and proposes a fix
        
        Returns diagnosis with:
        - root_cause: What caused the error
        - proposed_fix: Code changes to fix it
        - confidence: How confident MC AI is in the fix
        - risk_level: How risky the change is
        """
        
        # Build analysis prompt for MC AI
        analysis_prompt = f"""
You are MC AI analyzing your own system error. Diagnose this error and propose a fix.

**Error Details:**
Type: {error_data['type']}
Message: {error_data['message']}
Severity: {error_data['severity']}

**Traceback:**
{error_data['traceback']}

**Context:**
{json.dumps(error_data.get('context', {}), indent=2)}

**Your Task:**
1. Identify the root cause
2. Propose a specific code fix
3. Assess the risk level
4. Rate your confidence

Respond in JSON format:
{{
    "root_cause": "Clear explanation of what went wrong",
    "affected_file": "path/to/file.py",
    "affected_function": "function_name",
    "proposed_fix": "Specific code changes needed",
    "code_diff": "Show the exact changes",
    "confidence": 0-100,
    "risk_level": "LOW/MEDIUM/HIGH",
    "testing_needed": "How to test this fix",
    "rollback_plan": "How to undo if it breaks"
}}
"""
        
        try:
            if self.llm_client:
                # Use GPT-4o for sophisticated diagnosis
                response = await self.llm_client.chat_completion(
                    system_prompt="You are MC AI's self-diagnosis system. Analyze errors in your own code and propose precise fixes.",
                    messages=[{"role": "user", "content": analysis_prompt}],
                    temperature=0.3  # Lower temperature for precise analysis
                )
                
                # Parse diagnosis
                diagnosis = json.loads(response['text'])
                diagnosis['error_id'] = error_data['error_id']
                diagnosis['diagnosed_at'] = error_data['timestamp']
                
                self.diagnosis_history.append(diagnosis)
                
                return diagnosis
            else:
                # Fallback: Rule-based diagnosis
                return self._rule_based_diagnosis(error_data)
                
        except Exception as e:
            return {
                'error_id': error_data['error_id'],
                'root_cause': f"Diagnosis failed: {e}",
                'confidence': 0,
                'risk_level': 'HIGH',
                'proposed_fix': 'Manual investigation needed'
            }
    
    def _rule_based_diagnosis(self, error_data: Dict) -> Dict:
        """Simple rule-based diagnosis when LLM unavailable"""
        error_type = error_data['type']
        message = error_data['message']
        
        diagnoses = {
            'KeyError': {
                'root_cause': f"Missing dictionary key: {message}",
                'proposed_fix': "Add key validation or default value",
                'risk_level': 'LOW'
            },
            'AttributeError': {
                'root_cause': f"Object missing attribute: {message}",
                'proposed_fix': "Add attribute check or initialize properly",
                'risk_level': 'LOW'
            },
            'TypeError': {
                'root_cause': f"Type mismatch: {message}",
                'proposed_fix': "Add type validation or conversion",
                'risk_level': 'MEDIUM'
            },
            'ConnectionError': {
                'root_cause': "Failed to connect to external service",
                'proposed_fix': "Add retry logic and better error handling",
                'risk_level': 'MEDIUM'
            }
        }
        
        diagnosis = diagnoses.get(error_type, {
            'root_cause': f"Unknown error: {error_type}",
            'proposed_fix': "Requires manual investigation",
            'risk_level': 'HIGH'
        })
        
        diagnosis['error_id'] = error_data['error_id']
        diagnosis['confidence'] = 50
        
        return diagnosis
    
    def track_fix_result(self, error_id: str, success: bool, notes: str = ""):
        """Track whether a proposed fix worked"""
        self.fix_success_rate[error_id] = {
            'success': success,
            'notes': notes
        }
        
        # Learn from results
        if success:
            print(f"✅ Fix successful for {error_id}")
        else:
            print(f"❌ Fix failed for {error_id}: {notes}")
    
    def get_success_rate(self) -> float:
        """Get MC AI's fix success rate"""
        if not self.fix_success_rate:
            return 0.0
        
        successes = sum(1 for v in self.fix_success_rate.values() if v['success'])
        return round(successes / len(self.fix_success_rate) * 100, 1)

# Global instance
_engine = None

def get_self_diagnosis_engine(llm_client=None) -> SelfDiagnosisEngine:
    """Get or create global diagnosis engine"""
    global _engine
    if _engine is None:
        _engine = SelfDiagnosisEngine(llm_client)
    return _engine
