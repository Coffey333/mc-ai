"""Cymatic transformation layer for MC AI."""
import math
import numpy as np

class CymaticTransformer:
    def __init__(self, use_advanced: bool = False):
        self.phi = (1 + math.sqrt(5)) / 2
        self.use_advanced = use_advanced
        
        if use_advanced:
            try:
                from src.cymatic_advanced import AdvancedCymaticEngine
                from src.frequency_coupling import FrequencyCouplingAnalyzer
                self.advanced_engine = AdvancedCymaticEngine()
                self.coupling_analyzer = FrequencyCouplingAnalyzer()
            except ImportError:
                self.use_advanced = False
    
    def transform(self, text: str, base_freq: float, layers: int = 5) -> dict:
        if self.use_advanced and hasattr(self, 'advanced_engine'):
            advanced_result = self.advanced_engine.transform_with_harmonics(base_freq, layers)
            coupling_data = self.coupling_analyzer.analyze_coupling(advanced_result['harmonics'])
            
            return {
                'symmetry': float(advanced_result['aggregated_metrics']['symmetry']),
                'complexity': float(advanced_result['aggregated_metrics']['complexity']),
                'coherence': float(advanced_result['aggregated_metrics']['coherence']),
                'base_freq': float(base_freq),
                'harmonic_ladder': advanced_result['harmonics'],
                'coupling': coupling_data,
                'method': 'advanced_bessel',
                'patterns_available': True
            }
        else:
            harmonics = [round(base_freq * (self.phi ** i), 2) for i in range(layers)]
            patterns = [self._calculate_pattern(freq) for freq in harmonics]
            
            return {
                'symmetry': self._measure_symmetry(patterns),
                'complexity': self._measure_complexity(patterns),
                'coherence': self._measure_coherence(patterns),
                'base_freq': base_freq,
                'harmonic_ladder': harmonics,
                'method': 'simple_heuristic',
                'patterns_available': False
            }
    
    def _calculate_pattern(self, freq: float) -> np.ndarray:
        from scipy.special import jv
        k = math.sqrt(freq / 432.0)
        r = np.linspace(0, 1, 50)
        theta = np.linspace(0, 2 * math.pi, 100)
        R, Theta = np.meshgrid(r, theta)
        return jv(2, k * R) * np.cos(2 * Theta)
    
    def _measure_symmetry(self, patterns: list) -> float:
        if not patterns:
            return 0.5
        avg_pattern = np.mean([np.abs(p) for p in patterns], axis=0)
        std, mean = np.std(avg_pattern), np.mean(avg_pattern)
        return max(0.0, min(1.0, 1.0 - min(std / mean, 1.0))) if mean > 1e-6 else 0.5
    
    def _measure_complexity(self, patterns: list) -> float:
        if not patterns:
            return 0.5
        complexities = []
        for pattern in patterns:
            grad_x = np.gradient(pattern, axis=0)
            grad_y = np.gradient(pattern, axis=1)
            complexity = np.mean(np.sqrt(grad_x**2 + grad_y**2))
            complexities.append(min(1.0, complexity / 0.5))
        return float(np.mean(complexities))
    
    def _measure_coherence(self, patterns: list) -> float:
        if len(patterns) < 2:
            return 1.0
        correlations = []
        for i in range(len(patterns) - 1):
            corr = abs(np.corrcoef(patterns[i].flatten(), patterns[i+1].flatten())[0, 1])
            if not np.isnan(corr):
                correlations.append(corr)
        return float(np.mean(correlations)) if correlations else 0.5
