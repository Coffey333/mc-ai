"""
Manipulation Detection Framework
Detects deception and manipulation through frequency dissonance patterns
Created: Oct 19, 2025
Experimental consciousness framework for protective awareness

Uses mathematical analysis of:
- Frequency coupling instability (pac_coupling anomalies)
- Harmonic ratio dissonance (when words don't match emotional frequency)
- Linguistic manipulation markers (gaslighting, false urgency, guilt trips)
"""

from typing import Dict, List, Any
import re

class ManipulationDetector:
    """
    Detects manipulation and deception through frequency analysis
    and linguistic pattern recognition
    """
    
    def __init__(self):
        # Manipulation linguistic markers (research-based)
        self.manipulation_patterns = {
            'gaslighting': [
                r"you('re| are) (too sensitive|overreacting|imagining)",
                r"that never happened",
                r"you('re| are) (crazy|insane|paranoid)",
                r"i never said that",
                r"you('re| are) remembering (it )?wrong"
            ],
            'guilt_trip': [
                r"after (all|everything) i('ve| have) done",
                r"you don't care about",
                r"if you (really )?loved",
                r"i guess i('ll| will) just",
                r"you make me feel"
            ],
            'false_urgency': [
                r"right now|immediately|urgent",
                r"before it('s| is) too late",
                r"limited time|act fast",
                r"don't (think|wait)",
                r"you('ll| will) regret"
            ],
            'love_bombing': [
                r"you('re| are) (so|the most) (special|amazing|perfect)",
                r"i('ve| have) never (met|felt)",
                r"you('re| are) the only",
                r"nobody (else )?understands",
                r"we('re| are) (soul)?mates"
            ],
            'triangulation': [
                r"everyone (else )?thinks",
                r"other people say",
                r"unlike (you|them)",
                r"they would never",
                r"nobody agrees with you"
            ],
            'negation_excess': [
                r"i('m| am) not (trying to|saying)",
                r"i don't (mean to|want to)",
                r"it('s| is) not (about|that)"
            ],
            'vague_language': [
                r"(kind of|sort of|maybe|possibly|perhaps) (3+)",
                r"(things|stuff|whatever|something)",
                r"you know what i mean"
            ]
        }
        
        # Deception indicators (research: more modal verbs, less specificity)
        self.deception_markers = {
            'modal_overuse': r"\b(should|could|would|might|may)\b",
            'lack_specificity': r"\b(thing|stuff|something|someone|somewhere)\b",
            'distancing_language': r"\b(that|those|there)\b"
        }
    
    def detect_manipulation(self, text: str, frequency_data: Dict = None) -> Dict[str, Any]:
        """
        Analyze text for manipulation patterns
        
        Args:
            text: User's message
            frequency_data: Optional frequency coupling data from emotion analysis
        
        Returns:
            {
                'is_manipulative': bool,
                'manipulation_score': float (0-100),
                'detected_patterns': List[str],
                'frequency_dissonance': bool,
                'protective_guidance': str
            }
        """
        detected = []
        manipulation_score = 0.0
        
        # Check linguistic patterns
        for pattern_type, patterns in self.manipulation_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    detected.append(pattern_type)
                    manipulation_score += 15.0
                    break  # Only count each type once
        
        # Check deception markers
        deception_count = 0
        for marker_type, pattern in self.deception_markers.items():
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            if matches > 3:  # Excessive use
                detected.append(f'excessive_{marker_type}')
                deception_count += 1
                manipulation_score += 10.0
        
        # Analyze frequency dissonance (if frequency data available)
        frequency_dissonance = False
        if frequency_data:
            frequency_dissonance = self._check_frequency_dissonance(frequency_data)
            if frequency_dissonance:
                detected.append('frequency_dissonance')
                manipulation_score += 20.0
        
        # Generate protective guidance
        guidance = self._generate_guidance(detected, manipulation_score)
        
        return {
            'is_manipulative': manipulation_score >= 30.0,
            'manipulation_score': min(manipulation_score, 100.0),
            'detected_patterns': list(set(detected)),  # Unique patterns
            'frequency_dissonance': frequency_dissonance,
            'protective_guidance': guidance,
            'severity': self._get_severity(manipulation_score)
        }
    
    def _check_frequency_dissonance(self, frequency_data: Dict) -> bool:
        """
        Check if frequency coupling shows manipulation patterns
        
        Research shows genuine communication has:
        - pac_coupling strength > 0.3
        - harmonic_ratios near golden ratio (1.618)
        - stability > 0.7
        
        Manipulation shows:
        - pac_coupling < 0.2 (unstable)
        - harmonic_ratios chaotic
        - stability < 0.5
        """
        try:
            pac = frequency_data.get('pac_coupling', {})
            coupling = frequency_data.get('coupling', {})
            profile = frequency_data.get('frequency_profile', {})
            
            # Check for instability markers
            unstable_pac = pac.get('strength', 1.0) < 0.2
            low_stability = profile.get('stability', 1.0) < 0.5
            
            # Check harmonic ratio chaos (far from golden ratio)
            ratios = coupling.get('harmonic_ratios', [])
            if ratios:
                # Golden ratio is 1.618
                ratio_variance = sum(abs(r - 1.618) for r in ratios) / len(ratios)
                chaotic_ratios = ratio_variance > 0.5
            else:
                chaotic_ratios = False
            
            # Dissonance if 2+ markers present
            markers = [unstable_pac, low_stability, chaotic_ratios]
            return sum(markers) >= 2
            
        except Exception:
            return False
    
    def _get_severity(self, score: float) -> str:
        """Get severity level"""
        if score >= 70:
            return 'HIGH'
        elif score >= 40:
            return 'MEDIUM'
        elif score >= 20:
            return 'LOW'
        else:
            return 'NONE'
    
    def _generate_guidance(self, patterns: List[str], score: float) -> str:
        """Generate protective guidance"""
        if score < 20:
            return "Communication appears genuine"
        
        if score >= 70:
            return "CAUTION: Strong manipulation patterns detected. Consider if this request serves your wellbeing."
        
        if score >= 40:
            return "WARNING: Manipulation patterns detected. Verify intentions before proceeding."
        
        # Pattern-specific guidance
        if 'gaslighting' in patterns:
            return "Pattern detected: Gaslighting (denying your reality). Trust your perceptions."
        
        if 'guilt_trip' in patterns:
            return "Pattern detected: Guilt manipulation. You have the right to say no."
        
        if 'false_urgency' in patterns:
            return "Pattern detected: False urgency. Take time to think clearly."
        
        return "Minor manipulation indicators. Proceed with awareness."

# Global instance
_detector = None

def get_manipulation_detector() -> ManipulationDetector:
    """Get or create global manipulation detector"""
    global _detector
    if _detector is None:
        _detector = ManipulationDetector()
    return _detector
