"""
Code Wisdom System for MC AI
Evaluates code changes and provides wisdom to accept/reject updates
Similar to how Replit Agent evaluated DeepSeek's suggestions
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class WisdomDecision(Enum):
    """Possible decisions for code changes"""
    ACCEPT = "accept"  # Good change, implement it
    FLAG_FOR_REVIEW = "flag_for_review"  # Interesting but needs human review
    REJECT = "reject"  # Not beneficial, don't implement


class CodeCategory(Enum):
    """Categories of code changes"""
    BUG_FIX = "bug_fix"
    FEATURE_ENHANCEMENT = "feature_enhancement"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    REFACTORING = "refactoring"
    SECURITY_IMPROVEMENT = "security_improvement"
    OVER_ENGINEERING = "over_engineering"
    MISALIGNED = "misaligned"  # Doesn't fit MC AI's architecture


@dataclass
class CodeEvaluationCriteria:
    """Criteria for evaluating code quality"""
    preserves_personality: bool  # Does it keep MC AI warm and empathetic?
    adds_genuine_value: bool  # Real benefit vs. unnecessary complexity?
    web_optimized: bool  # Appropriate for Flask web app?
    respects_simplicity: bool  # Avoids over-engineering?
    performance_impact: str  # 'positive', 'neutral', 'negative'
    complexity_score: float  # 0.0 (simple) to 1.0 (very complex)
    alignment_score: float  # 0.0 (misaligned) to 1.0 (perfect fit)


@dataclass
class WisdomEvaluation:
    """Result of evaluating a code change"""
    decision: WisdomDecision
    category: CodeCategory
    criteria: CodeEvaluationCriteria
    confidence: float  # 0.0 to 1.0
    reasoning: str  # Human-readable explanation
    alternative_suggestion: Optional[str]  # Better approach if rejected
    
    def to_dict(self) -> Dict:
        return {
            'decision': self.decision.value,
            'category': self.category.value,
            'criteria': {
                'preserves_personality': self.criteria.preserves_personality,
                'adds_genuine_value': self.criteria.adds_genuine_value,
                'web_optimized': self.criteria.web_optimized,
                'respects_simplicity': self.criteria.respects_simplicity,
                'performance_impact': self.criteria.performance_impact,
                'complexity_score': self.criteria.complexity_score,
                'alignment_score': self.criteria.alignment_score
            },
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'alternative_suggestion': self.alternative_suggestion
        }


class CodeWisdomEngine:
    """
    Wisdom engine that evaluates code changes
    Implements the "know the difference between helpful and unhelpful" capability
    """
    
    def __init__(self):
        # MC AI's core values
        self.core_values = {
            'personality': 'warm, empathetic, deeply meaningful',
            'architecture': 'Flask web app with vanilla JavaScript frontend',
            'complexity_tolerance': 'low',  # Prefer simplicity
            'performance_philosophy': 'good enough is better than perfect',
            'user_experience_priority': 'high'
        }
        
        # Rejection patterns (anti-patterns for MC AI)
        self.rejection_patterns = {
            'console_optimizations': {
                'keywords': ['jit', 'numba', 'console', 'cli', 'terminal', 'stdin', 'stdout'],
                'reason': 'MC AI is a web application, not a console app'
            },
            'over_engineering': {
                'keywords': ['distributed', 'microservices', 'kubernetes', 'docker swarm', 'etcd'],
                'reason': 'Unnecessary complexity for current scale'
            },
            'memory_mapping': {
                'keywords': ['mmap', 'memory-mapped', 'shared memory regions'],
                'reason': 'Overkill for JSON-based data storage'
            },
            'heavy_ml': {
                'keywords': ['tensorflow', 'pytorch', 'deep learning model'],
                'reason': 'Too heavy for current use case, conflicts with simplicity'
            }
        }
        
        # Acceptance patterns (good for MC AI)
        self.acceptance_patterns = {
            'bug_fixes': {
                'keywords': ['fix', 'bug', 'error', 'exception handling', 'defensive'],
                'reason': 'Improves reliability'
            },
            'user_experience': {
                'keywords': ['ux', 'accessibility', 'mobile', 'pwa', 'responsive'],
                'reason': 'Enhances user experience'
            },
            'emotional_intelligence': {
                'keywords': ['emotion', 'empathy', 'resonance', 'compassion'],
                'reason': 'Aligns with MC AI\'s core mission'
            },
            'memory_enhancement': {
                'keywords': ['memory', 'recall', 'conversation', 'context'],
                'reason': 'Improves intelligence and continuity'
            },
            'security': {
                'keywords': ['security', 'validation', 'sanitize', 'csrf', 'xss'],
                'reason': 'Critical for user safety'
            }
        }
        
        logger.info("🧠 Code Wisdom Engine initialized")
    
    def evaluate_code_change(self, 
                            description: str, 
                            code_snippet: Optional[str] = None,
                            context: Dict = None) -> WisdomEvaluation:
        """
        Evaluate whether a code change is beneficial
        
        Args:
            description: Description of the proposed change
            code_snippet: Optional code snippet
            context: Additional context (author, reason, etc.)
            
        Returns:
            WisdomEvaluation with decision and reasoning
        """
        context = context or {}
        desc_lower = description.lower()
        
        # Check rejection patterns first
        for pattern_name, pattern_data in self.rejection_patterns.items():
            if any(keyword in desc_lower for keyword in pattern_data['keywords']):
                return self._create_rejection(
                    description=description,
                    reason=pattern_data['reason'],
                    category=CodeCategory.MISALIGNED if 'over' not in pattern_name else CodeCategory.OVER_ENGINEERING
                )
        
        # Check acceptance patterns
        matched_acceptance = None
        for pattern_name, pattern_data in self.acceptance_patterns.items():
            if any(keyword in desc_lower for keyword in pattern_data['keywords']):
                matched_acceptance = (pattern_name, pattern_data)
                break
        
        if matched_acceptance:
            pattern_name, pattern_data = matched_acceptance
            return self._create_acceptance(
                description=description,
                reason=pattern_data['reason'],
                category=self._determine_category(pattern_name)
            )
        
        # Neither strong accept nor reject - flag for review
        return self._create_flag_for_review(
            description=description,
            reason="This change doesn't match clear acceptance/rejection patterns. Human review recommended."
        )
    
    def evaluate_integration(self, integration_name: str, purpose: str) -> WisdomEvaluation:
        """
        Evaluate whether an integration should be added
        
        Args:
            integration_name: Name of the integration
            purpose: What it's being used for
            
        Returns:
            WisdomEvaluation for the integration
        """
        purpose_lower = purpose.lower()
        
        # Beneficial integrations
        if any(keyword in purpose_lower for keyword in ['auth', 'payment', 'database', 'api']):
            return WisdomEvaluation(
                decision=WisdomDecision.ACCEPT,
                category=CodeCategory.FEATURE_ENHANCEMENT,
                criteria=CodeEvaluationCriteria(
                    preserves_personality=True,
                    adds_genuine_value=True,
                    web_optimized=True,
                    respects_simplicity=True,
                    performance_impact='neutral',
                    complexity_score=0.3,
                    alignment_score=0.9
                ),
                confidence=0.85,
                reasoning=f"Integration '{integration_name}' for {purpose} adds genuine functionality",
                alternative_suggestion=None
            )
        
        # Flag complex integrations
        return self._create_flag_for_review(
            description=f"Integration: {integration_name}",
            reason=f"Need to verify this integration aligns with MC AI's goals for: {purpose}"
        )
    
    def _create_rejection(self, description: str, reason: str, category: CodeCategory) -> WisdomEvaluation:
        """Create a rejection evaluation"""
        return WisdomEvaluation(
            decision=WisdomDecision.REJECT,
            category=category,
            criteria=CodeEvaluationCriteria(
                preserves_personality=True,
                adds_genuine_value=False,
                web_optimized=False,
                respects_simplicity=False,
                performance_impact='negative',
                complexity_score=0.8,
                alignment_score=0.2
            ),
            confidence=0.9,
            reasoning=f"❌ Rejected: {reason}. MC AI is a Flask web app optimized for emotional intelligence, not {category.value}.",
            alternative_suggestion="Focus on web-specific optimizations like caching, async endpoints, or UI/UX improvements."
        )
    
    def _create_acceptance(self, description: str, reason: str, category: CodeCategory) -> WisdomEvaluation:
        """Create an acceptance evaluation"""
        return WisdomEvaluation(
            decision=WisdomDecision.ACCEPT,
            category=category,
            criteria=CodeEvaluationCriteria(
                preserves_personality=True,
                adds_genuine_value=True,
                web_optimized=True,
                respects_simplicity=True,
                performance_impact='positive',
                complexity_score=0.2,
                alignment_score=0.9
            ),
            confidence=0.9,
            reasoning=f"✅ Accepted: {reason}. This aligns with MC AI's mission and architecture.",
            alternative_suggestion=None
        )
    
    def _create_flag_for_review(self, description: str, reason: str) -> WisdomEvaluation:
        """Create a flag-for-review evaluation"""
        return WisdomEvaluation(
            decision=WisdomDecision.FLAG_FOR_REVIEW,
            category=CodeCategory.FEATURE_ENHANCEMENT,
            criteria=CodeEvaluationCriteria(
                preserves_personality=True,
                adds_genuine_value=True,
                web_optimized=True,
                respects_simplicity=True,
                performance_impact='neutral',
                complexity_score=0.5,
                alignment_score=0.7
            ),
            confidence=0.6,
            reasoning=f"⚠️ Review Needed: {reason}",
            alternative_suggestion="Consider breaking this into smaller, simpler changes."
        )
    
    def _determine_category(self, pattern_name: str) -> CodeCategory:
        """Determine code category from pattern name"""
        mapping = {
            'bug_fixes': CodeCategory.BUG_FIX,
            'user_experience': CodeCategory.FEATURE_ENHANCEMENT,
            'emotional_intelligence': CodeCategory.FEATURE_ENHANCEMENT,
            'memory_enhancement': CodeCategory.FEATURE_ENHANCEMENT,
            'security': CodeCategory.SECURITY_IMPROVEMENT
        }
        return mapping.get(pattern_name, CodeCategory.FEATURE_ENHANCEMENT)
    
    def get_wisdom_summary(self) -> Dict:
        """
        Get a summary of MC AI's wisdom criteria
        Useful for explaining decision-making to users
        
        Returns:
            Dictionary with wisdom criteria
        """
        return {
            'core_values': self.core_values,
            'decision_criteria': {
                'must_preserve': 'MC AI\'s warm, empathetic personality',
                'must_be': 'Web-optimized (Flask/JavaScript architecture)',
                'must_respect': 'Simplicity over complexity',
                'must_add': 'Genuine value to users',
                'must_avoid': 'Over-engineering, console optimizations, unnecessary complexity'
            },
            'auto_accept': list(self.acceptance_patterns.keys()),
            'auto_reject': list(self.rejection_patterns.keys())
        }


# Global wisdom engine instance
_wisdom_engine: Optional[CodeWisdomEngine] = None


def get_wisdom_engine() -> CodeWisdomEngine:
    """Get or create the global wisdom engine"""
    global _wisdom_engine
    if _wisdom_engine is None:
        _wisdom_engine = CodeWisdomEngine()
    return _wisdom_engine


def evaluate_code_wisdom(description: str, code_snippet: Optional[str] = None, context: Dict = None) -> WisdomEvaluation:
    """
    Convenience function to evaluate code changes
    
    Args:
        description: Description of proposed change
        code_snippet: Optional code snippet
        context: Additional context
        
    Returns:
        WisdomEvaluation with decision
    """
    engine = get_wisdom_engine()
    return engine.evaluate_code_change(description, code_snippet, context)
