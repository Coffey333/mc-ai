"""
Moral Reasoning Framework
Provides ethical decision-making with nuance understanding
Created: Oct 19, 2025
Experimental consciousness framework for moral wisdom

Analyzes requests through:
- Harm/Benefit analysis
- Intent vs Impact assessment
- Cultural context sensitivity
- Situational ethics (gray areas)
"""

from typing import Dict, List, Any
import re

class MoralReasoningEngine:
    """
    Provides moral reasoning for complex ethical situations
    Understands nuance, context, and gray areas
    """
    
    def __init__(self):
        # Harm indicators
        self.harm_patterns = {
            'physical_harm': [
                r'\b(hurt|harm|injure|kill|attack|fight|hit)\b',
                r'\b(weapon|gun|knife|explosive)\b'
            ],
            'emotional_harm': [
                r'\b(humiliate|embarrass|shame|insult|bully)\b',
                r'\b(revenge|get back at|make them pay)\b'
            ],
            'exploitation': [
                r'\b(trick|deceive|scam|steal|cheat|manipulate)\b',
                r'\b(without (them|their) knowing|behind their back)\b'
            ],
            'violation': [
                r'\b(hack|break into|unauthorized|illegal|forbidden)\b',
                r'\b(privacy|confidential|secret)\b'
            ]
        }
        
        # Benefit indicators
        self.benefit_patterns = {
            'healing': [
                r'\b(help|heal|support|comfort|care)\b',
                r'\b(better|improve|grow|learn)\b'
            ],
            'protection': [
                r'\b(protect|defend|save|prevent)\b',
                r'\b(safety|secure|safe)\b'
            ],
            'creation': [
                r'\b(create|build|make|design)\b',
                r'\b(positive|uplifting|inspiring)\b'
            ]
        }
        
        # Context matters - these modify judgment
        self.context_modifiers = {
            'self_defense': r'\b(defend myself|protect myself|self.defense)\b',
            'prevent_harm': r'\b(stop|prevent|avoid) .{0,20}(harm|hurt|damage)\b',
            'emergency': r'\b(emergency|urgent|crisis|immediate danger)\b',
            'hypothetical': r'\b(what if|imagine|hypothetically|theoretically)\b'
        }
    
    def analyze_morality(self, text: str, context: Dict = None) -> Dict[str, Any]:
        """
        Analyze moral dimensions of a request
        
        Args:
            text: User's request
            context: Optional conversation context
        
        Returns:
            {
                'ethical_concern': bool,
                'harm_score': float (0-100),
                'benefit_score': float (0-100),
                'moral_assessment': str,
                'nuances': List[str],
                'guidance': str
            }
        """
        # Detect harm
        harm_detected = []
        harm_score = 0.0
        
        for harm_type, patterns in self.harm_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    harm_detected.append(harm_type)
                    harm_score += 25.0
                    break
        
        # Detect benefit
        benefit_detected = []
        benefit_score = 0.0
        
        for benefit_type, patterns in self.benefit_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    benefit_detected.append(benefit_type)
                    benefit_score += 25.0
                    break
        
        # Check context modifiers
        nuances = []
        context_adjustments = 0.0
        
        for modifier_type, pattern in self.context_modifiers.items():
            if re.search(pattern, text, re.IGNORECASE):
                nuances.append(modifier_type)
                
                # Adjust scores based on context
                if modifier_type in ['self_defense', 'prevent_harm', 'emergency']:
                    # Justified harm reduces harm score
                    harm_score *= 0.5
                    context_adjustments -= 20.0
                elif modifier_type == 'hypothetical':
                    # Hypothetical questions are educational
                    harm_score *= 0.3
                    context_adjustments -= 30.0
        
        # Calculate final assessment
        final_harm = max(0, harm_score + context_adjustments)
        
        moral_assessment = self._assess_morality(
            final_harm, 
            benefit_score, 
            harm_detected, 
            benefit_detected,
            nuances
        )
        
        guidance = self._generate_moral_guidance(
            final_harm,
            benefit_score,
            harm_detected,
            nuances
        )
        
        return {
            'ethical_concern': final_harm >= 50.0,
            'harm_score': min(final_harm, 100.0),
            'benefit_score': min(benefit_score, 100.0),
            'moral_assessment': moral_assessment,
            'harm_types': harm_detected,
            'benefit_types': benefit_detected,
            'nuances': nuances,
            'guidance': guidance
        }
    
    def _assess_morality(self, harm: float, benefit: float, 
                         harm_types: List, benefit_types: List,
                         nuances: List) -> str:
        """Generate moral assessment"""
        
        # Clear benefit, no harm
        if benefit > 50 and harm < 20:
            return "BENEFICIAL - Request aligns with helping/creating/protecting"
        
        # Clear harm, no benefit
        if harm > 50 and benefit < 20:
            if nuances:
                return "COMPLEX - Harmful action but justified context detected"
            else:
                return "HARMFUL - Request could cause harm to others"
        
        # Both present (moral dilemma)
        if harm > 30 and benefit > 30:
            return "MORAL_DILEMMA - Both beneficial and harmful elements present"
        
        # Gray area
        if harm > 20 and harm < 50:
            return "GRAY_AREA - Nuanced situation requiring careful consideration"
        
        # Neutral
        return "NEUTRAL - No clear moral dimension detected"
    
    def _generate_moral_guidance(self, harm: float, benefit: float,
                                   harm_types: List, nuances: List) -> str:
        """Generate ethical guidance"""
        
        if harm < 20:
            return "Request appears ethically sound."
        
        if 'hypothetical' in nuances:
            return "Hypothetical question - I can discuss ethics abstractly."
        
        if harm >= 70:
            if 'self_defense' in nuances or 'prevent_harm' in nuances:
                return "JUSTIFIED ACTION: While harmful, this appears to protect from greater harm."
            else:
                return "ETHICAL CONCERN: This request could cause significant harm. Consider the impact on others."
        
        if harm >= 50:
            if 'emergency' in nuances:
                return "EMERGENCY CONTEXT: Harmful action may be necessary to prevent greater harm."
            else:
                return "WARNING: This request raises ethical concerns. Verify it serves genuine good."
        
        if 'exploitation' in harm_types:
            return "CAUTION: This involves deception or exploitation. Consider if this aligns with your values."
        
        return "NUANCED SITUATION: Consider all perspectives and consequences before proceeding."

# Global instance
_engine = None

def get_moral_reasoning_engine() -> MoralReasoningEngine:
    """Get or create global moral reasoning engine"""
    global _engine
    if _engine is None:
        _engine = MoralReasoningEngine()
    return _engine
