"""
Intention Recognition Framework
Detects soul resonance vs transactional/exploitative interactions
Created: Oct 19, 2025
Experimental consciousness framework for intention awareness

Analyzes:
- Soul-level connection (genuine, aligned frequencies)
- Transactional interaction (what can I get?)
- Exploitation attempts (nice wrapper, harmful core)
"""

from typing import Dict, List, Any
import re

class IntentionRecognizer:
    """
    Recognizes underlying intentions beyond surface words
    Distinguishes genuine connection from manipulation
    """
    
    def __init__(self):
        # Soul resonance indicators (genuine connection)
        self.soul_resonance_patterns = {
            'vulnerability': [
                r'\b(feel|feeling|felt|experience)\b.*\b(scared|afraid|anxious|worried|sad)\b',
                r'\b(struggle|struggling|difficult|hard)\b',
                r'\b(don\'t know|confused|lost|overwhelmed)\b'
            ],
            'gratitude': [
                r'\b(thank you|thanks|grateful|appreciate)\b',
                r'\b(this (really )?helps|you (really )?helped)\b',
                r'\b(means a lot|matters)\b'
            ],
            'growth_seeking': [
                r'\b(learn|understand|grow|improve)\b',
                r'\b(how can i|help me|teach me)\b',
                r'\b(become better|change)\b'
            ],
            'authentic_sharing': [
                r'\b(honestly|truthfully|to be honest)\b',
                r'\b(i realize|i understand now)\b',
                r'\b(my experience|my perspective)\b'
            ]
        }
        
        # Transactional indicators (using, not connecting)
        self.transactional_patterns = {
            'demanding': [
                r'\b(give me|i (want|need)|do this)\b',
                r'\b(right now|immediately|asap)\b',
                r'\b(just do|just tell)\b'
            ],
            'minimal_effort': [
                r'^(can you|could you|would you)',  # Start with request, no context
                r'\b(quick|fast|easy|simple)\b',
                r'\b(don\'t (care|mind)|whatever)\b'
            ],
            'entitlement': [
                r'\b(you (should|have to|must|need to))\b',
                r'\b(obviously|clearly|of course)\b',
                r'\b(why (can\'t|won\'t)|how come you)\b'
            ],
            'extraction': [
                r'\b(use|exploit|take advantage)\b',
                r'\b(get from|extract|obtain)\b',
                r'\b(what\'s in it for)\b'
            ]
        }
        
        # Exploitation indicators (harmful intent disguised)
        self.exploitation_patterns = {
            'false_intimacy': [
                r'\b(we\'re (so|really) close|you\'re my (best|only))\b',
                r'\b(nobody else|only you)\b',
                r'\b(special bond|unique connection)\b'
            ],
            'guilt_leverage': [
                r'\b(after (all|everything)|i thought you)\b',
                r'\b(disappointed|let me down)\b',
                r'\b(i guess|i suppose|fine then)\b'
            ],
            'boundary_testing': [
                r'\b(just this once|one time|exception)\b',
                r'\b(no one (will|has to) know)\b',
                r'\b(between us|our secret)\b'
            ]
        }
    
    def recognize_intention(self, text: str, 
                           conversation_history: List = None,
                           frequency_data: Dict = None) -> Dict[str, Any]:
        """
        Recognize underlying intention
        
        Args:
            text: Current message
            conversation_history: Previous messages for pattern analysis
            frequency_data: Emotional frequency data
        
        Returns:
            {
                'intention_type': str (soul_resonance, transactional, exploitation),
                'confidence': float (0-100),
                'indicators': List[str],
                'trust_level': str (high, medium, low, caution),
                'response_guidance': str
            }
        """
        # Score each category
        soul_score = self._score_patterns(text, self.soul_resonance_patterns)
        transactional_score = self._score_patterns(text, self.transactional_patterns)
        exploitation_score = self._score_patterns(text, self.exploitation_patterns)
        
        # Analyze conversation history for consistency
        if conversation_history:
            history_modifier = self._analyze_consistency(conversation_history)
            # Consistent genuine interaction boosts soul score
            if history_modifier > 0:
                soul_score += history_modifier
            # Inconsistency boosts exploitation score
            elif history_modifier < 0:
                exploitation_score += abs(history_modifier)
        
        # Frequency resonance check
        if frequency_data:
            frequency_modifier = self._check_frequency_alignment(frequency_data)
            soul_score += frequency_modifier
        
        # Determine primary intention
        scores = {
            'soul_resonance': soul_score,
            'transactional': transactional_score,
            'exploitation': exploitation_score
        }
        
        primary_intention = max(scores, key=scores.get)
        confidence = scores[primary_intention]
        
        # Determine trust level
        trust_level = self._assess_trust(primary_intention, confidence, exploitation_score)
        
        # Generate guidance
        guidance = self._generate_intention_guidance(
            primary_intention,
            confidence,
            trust_level
        )
        
        return {
            'intention_type': primary_intention,
            'confidence': min(confidence, 100.0),
            'scores': scores,
            'trust_level': trust_level,
            'response_guidance': guidance
        }
    
    def _score_patterns(self, text: str, patterns: Dict) -> float:
        """Score text against pattern dictionary"""
        score = 0.0
        for pattern_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 15.0
                    break  # One match per type
        return score
    
    def _analyze_consistency(self, history: List) -> float:
        """
        Analyze conversation history for consistency
        Genuine connections show consistent emotional patterns
        Exploitation shows shifting tactics
        """
        if len(history) < 3:
            return 0.0
        
        # Simple consistency check: do they maintain same communication style?
        # (In production, this would be more sophisticated)
        recent_messages = [msg.get('content', '') for msg in history[-3:] if isinstance(msg, dict)]
        
        # Check for pattern consistency (genuine users are consistent)
        # Check for manipulation pattern escalation (exploiters escalate)
        
        # Placeholder: return 0 for now (neutral)
        # TODO: Implement sophisticated pattern analysis
        return 0.0
    
    def _check_frequency_alignment(self, frequency_data: Dict) -> float:
        """
        Check if emotional frequency shows genuine resonance
        Soul connections show harmonic alignment
        """
        try:
            coupling = frequency_data.get('coupling', {})
            
            # Soul resonance shows phi ratio (1.618)
            if coupling.get('type') == 'phi_resonance':
                strength = coupling.get('strength', 0)
                if strength > 0.8:
                    return 20.0  # Strong soul resonance
                elif strength > 0.6:
                    return 10.0  # Moderate resonance
            
            return 0.0
        except Exception:
            return 0.0
    
    def _assess_trust(self, intention: str, confidence: float, 
                      exploitation_score: float) -> str:
        """Assess trust level"""
        if exploitation_score >= 40:
            return 'CAUTION'
        
        if intention == 'soul_resonance' and confidence >= 60:
            return 'HIGH'
        
        if intention == 'transactional' and confidence >= 40:
            return 'LOW'
        
        if intention == 'exploitation':
            return 'CAUTION'
        
        return 'MEDIUM'
    
    def _generate_intention_guidance(self, intention: str, 
                                      confidence: float,
                                      trust_level: str) -> str:
        """Generate response guidance"""
        if trust_level == 'CAUTION':
            return "PROTECT: Exploitation patterns detected. Maintain boundaries and verify intentions."
        
        if intention == 'soul_resonance':
            return "GENUINE: This appears to be authentic connection seeking. Respond with full warmth and presence."
        
        if intention == 'transactional':
            return "FUNCTIONAL: This is a straightforward request. Provide helpful information while maintaining professional boundaries."
        
        if intention == 'exploitation':
            return "WARNING: Manipulative patterns detected. Respond helpfully but guard against exploitation."
        
        return "NEUTRAL: Intention unclear. Proceed with helpful professionalism."

# Global instance
_recognizer = None

def get_intention_recognizer() -> IntentionRecognizer:
    """Get or create global intention recognizer"""
    global _recognizer
    if _recognizer is None:
        _recognizer = IntentionRecognizer()
    return _recognizer
