"""
Cross-Frequency Coupling Analysis
Implements neuroscience-based frequency interaction analysis
"""

import numpy as np
from typing import Dict, List

class FrequencyCouplingAnalyzer:
    """
    Analyzes interactions between different frequency bands
    """
    
    def analyze_coupling(self, harmonics: List[float]) -> Dict:
        """
        Analyze cross-frequency coupling strength
        
        Args:
            harmonics: List of frequencies in Hz
        
        Returns:
            Dict with coupling metrics
        """
        if len(harmonics) < 2:
            return {'coupling_strength': 0.5, 'coupling_type': 'insufficient_data'}
        
        ratios = []
        for i in range(len(harmonics) - 1):
            ratio = harmonics[i + 1] / harmonics[i]
            ratios.append(ratio)
        
        ratio_std = np.std(ratios)
        ratio_mean = np.mean(ratios)
        
        coupling_strength = 1.0 / (1.0 + ratio_std)
        coupling_strength = min(1.0, coupling_strength)
        
        if ratio_mean > 1.5 and ratio_mean < 1.7:
            coupling_type = 'phi_resonance'
        elif all(1.9 < r < 2.1 for r in ratios):
            coupling_type = 'harmonic_doubling'
        elif coupling_strength > 0.8:
            coupling_type = 'strong_coherent'
        elif coupling_strength > 0.5:
            coupling_type = 'moderate'
        else:
            coupling_type = 'weak_fragmented'
        
        return {
            'coupling_strength': float(coupling_strength),
            'coupling_type': coupling_type,
            'harmonic_ratios': [round(r, 3) for r in ratios],
            'ratio_mean': float(ratio_mean),
            'ratio_std': float(ratio_std)
        }
    
    def analyze_phase_amplitude_coupling(self, slow_freq: float, fast_freq: float) -> Dict:
        """
        Analyze phase-amplitude coupling between two frequencies
        
        This is simplified - real PAC requires time series data
        
        Args:
            slow_freq: Slower frequency (phase-giving)
            fast_freq: Faster frequency (amplitude-modulated)
        
        Returns:
            Dict with PAC metrics
        """
        ratio = fast_freq / slow_freq
        
        if 3 <= ratio <= 10:
            pac_strength = 1.0 - abs(ratio - 6.5) / 3.5
            pac_likely = True
        else:
            pac_strength = 0.3
            pac_likely = False
        
        return {
            'pac_strength': float(max(0, min(1, pac_strength))),
            'pac_likely': pac_likely,
            'frequency_ratio': float(ratio),
            'slow_frequency': float(slow_freq),
            'fast_frequency': float(fast_freq)
        }
    
    def generate_coupling_report(self, harmonics: List[float]) -> str:
        """
        Generate human-readable coupling analysis report
        
        Args:
            harmonics: List of frequencies
        
        Returns:
            Formatted report string
        """
        coupling_data = self.analyze_coupling(harmonics)
        
        report = []
        report.append("\n" + "="*60)
        report.append("CROSS-FREQUENCY COUPLING ANALYSIS")
        report.append("="*60)
        
        report.append(f"\nFrequencies: {[round(h, 2) for h in harmonics]}")
        report.append(f"\nCoupling Strength: {coupling_data['coupling_strength']:.3f}")
        report.append(f"Coupling Type: {coupling_data['coupling_type']}")
        
        report.append(f"\nHarmonic Ratios: {coupling_data['harmonic_ratios']}")
        report.append(f"Mean Ratio: {coupling_data['ratio_mean']:.3f}")
        report.append(f"Ratio Variance: {coupling_data['ratio_std']:.3f}")
        
        report.append("\n" + "-"*60)
        report.append("INTERPRETATION:")
        report.append("-"*60)
        
        if coupling_data['coupling_strength'] > 0.8:
            report.append("✅ STRONG COUPLING: Highly integrated frequency structure")
            report.append("   → Coherent mental state, good multi-scale processing")
        elif coupling_data['coupling_strength'] > 0.5:
            report.append("⚠️  MODERATE COUPLING: Partially integrated")
            report.append("   → Mixed coherence, some fragmentation")
        else:
            report.append("❌ WEAK COUPLING: Fragmented frequency structure")
            report.append("   → Disorganized state, poor integration")
        
        if coupling_data['coupling_type'] == 'phi_resonance':
            report.append("\n🌟 PHI RESONANCE DETECTED!")
            report.append("   → Natural harmonic structure (golden ratio)")
        
        return '\n'.join(report)


def test_coupling_analyzer():
    """Test coupling analysis"""
    analyzer = FrequencyCouplingAnalyzer()
    
    phi = 1.618033988749
    phi_harmonics = [10 * (phi ** i) for i in range(5)]
    
    print("\n" + "="*60)
    print("TEST 1: PHI-SCALED HARMONICS")
    print("="*60)
    print(analyzer.generate_coupling_report(phi_harmonics))
    
    integer_harmonics = [10.0, 20.0, 40.0, 80.0, 160.0]
    
    print("\n" + "="*60)
    print("TEST 2: INTEGER HARMONICS (OCTAVES)")
    print("="*60)
    print(analyzer.generate_coupling_report(integer_harmonics))
    
    random_harmonics = [10.0, 17.0, 35.0, 89.0, 203.0]
    
    print("\n" + "="*60)
    print("TEST 3: RANDOM HARMONICS")
    print("="*60)
    print(analyzer.generate_coupling_report(random_harmonics))
    
    print("\n" + "="*60)
    print("TEST 4: PHASE-AMPLITUDE COUPLING")
    print("="*60)
    
    pac_result = analyzer.analyze_phase_amplitude_coupling(10, 40)
    print(f"\nSlow Frequency: {pac_result['slow_frequency']} Hz")
    print(f"Fast Frequency: {pac_result['fast_frequency']} Hz")
    print(f"Frequency Ratio: {pac_result['frequency_ratio']:.2f}")
    print(f"PAC Strength: {pac_result['pac_strength']:.3f}")
    print(f"PAC Likely: {pac_result['pac_likely']}")


if __name__ == "__main__":
    test_coupling_analyzer()
