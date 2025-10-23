"""
Advanced Cymatic Pattern Calculator with Bessel Functions
Implements the mathematical rigor described in the technical document
"""

import numpy as np
from scipy.special import jn
from typing import Dict, List, Tuple
import os

class AdvancedCymaticEngine:
    """
    Generates actual 2D cymatic patterns using Bessel functions
    """
    
    def __init__(self):
        self.reference_freq = 432.0
        self.grid_size = (100, 50)
    
    def generate_cymatic_pattern(self, frequency: float, order: int = 2) -> np.ndarray:
        """
        Generate 2D cymatic pattern using Bessel functions
        
        Args:
            frequency: Frequency in Hz
            order: Bessel function order (default 2 for common patterns)
        
        Returns:
            2D numpy array representing cymatic interference pattern
        """
        k = np.sqrt(frequency / self.reference_freq)
        
        theta_points, r_points = self.grid_size
        theta = np.linspace(0, 2 * np.pi, theta_points)
        r = np.linspace(0, 1, r_points)
        
        R, Theta = np.meshgrid(r, theta)
        
        bessel_component = jn(order, k * R)
        angular_component = np.cos(order * Theta)
        
        pattern = bessel_component * angular_component
        
        return pattern
    
    def calculate_pattern_metrics(self, pattern: np.ndarray) -> Dict:
        """
        Calculate symmetry, complexity, and coherence from actual 2D pattern
        
        Args:
            pattern: 2D numpy array from generate_cymatic_pattern
        
        Returns:
            Dict with three metrics
        """
        symmetry = self._calculate_symmetry(pattern)
        complexity = self._calculate_complexity(pattern)
        coherence = self._calculate_coherence(pattern)
        
        return {
            'symmetry': float(symmetry),
            'complexity': float(complexity),
            'coherence': float(coherence)
        }
    
    def _calculate_symmetry(self, pattern: np.ndarray) -> float:
        """
        Calculate rotational symmetry of pattern
        
        Method: Compare pattern with rotated versions
        """
        avg_pattern = np.mean(np.abs(pattern), axis=0)
        
        std_dev = np.std(avg_pattern)
        mean_val = np.mean(avg_pattern)
        
        if mean_val > 1e-6:
            symmetry = 1.0 - min(std_dev / mean_val, 1.0)
        else:
            symmetry = 0.5
        
        return max(0.0, min(1.0, symmetry))
    
    def _calculate_complexity(self, pattern: np.ndarray) -> float:
        """
        Calculate spatial complexity using gradient magnitude
        
        Method: High gradients = complex patterns
        """
        grad_theta = np.gradient(pattern, axis=0)
        grad_r = np.gradient(pattern, axis=1)
        
        gradient_magnitude = np.sqrt(grad_theta**2 + grad_r**2)
        
        complexity = np.mean(gradient_magnitude)
        complexity = min(1.0, complexity / 0.5)
        
        return max(0.0, min(1.0, complexity))
    
    def _calculate_coherence(self, pattern: np.ndarray) -> float:
        """
        Calculate pattern coherence using autocorrelation
        
        Method: High autocorrelation = coherent pattern
        """
        flat_pattern = pattern.flatten()
        
        if len(flat_pattern) > 1:
            correlation = np.corrcoef(
                flat_pattern[:-1], 
                flat_pattern[1:]
            )[0, 1]
            
            if not np.isnan(correlation):
                coherence = abs(correlation)
            else:
                coherence = 0.5
        else:
            coherence = 0.5
        
        return max(0.0, min(1.0, coherence))
    
    def transform_with_harmonics(self, base_freq: float, layers: int = 5) -> Dict:
        """
        Generate harmonic ladder and calculate patterns for each
        
        Args:
            base_freq: Base frequency in Hz
            layers: Number of harmonic layers
        
        Returns:
            Dict with harmonics, patterns, and metrics
        """
        phi = (1 + np.sqrt(5)) / 2
        
        harmonics = [base_freq * (phi ** i) for i in range(layers)]
        
        patterns = []
        metrics = []
        
        for freq in harmonics:
            pattern = self.generate_cymatic_pattern(freq)
            pattern_metrics = self.calculate_pattern_metrics(pattern)
            
            patterns.append(pattern)
            metrics.append(pattern_metrics)
        
        aggregated_metrics = {
            'symmetry': np.mean([m['symmetry'] for m in metrics]),
            'complexity': np.mean([m['complexity'] for m in metrics]),
            'coherence': np.mean([m['coherence'] for m in metrics])
        }
        
        return {
            'base_frequency': base_freq,
            'harmonics': [round(h, 2) for h in harmonics],
            'patterns': patterns,
            'individual_metrics': metrics,
            'aggregated_metrics': aggregated_metrics
        }
    
    def visualize_pattern(self, pattern: np.ndarray, save_path: str | None = None) -> str:
        """
        Visualize cymatic pattern
        
        Args:
            pattern: 2D pattern array
            save_path: Optional path to save image
        
        Returns:
            Path to saved image or empty string on error
        """
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            
            if save_path is None:
                save_path = "static/cymatic_pattern.png"
            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            plt.figure(figsize=(10, 10))
            
            theta_points, r_points = pattern.shape
            theta = np.linspace(0, 2 * np.pi, theta_points)
            r = np.linspace(0, 1, r_points)
            R, Theta = np.meshgrid(r, theta)
            
            X = R * np.cos(Theta)
            Y = R * np.sin(Theta)
            
            plt.contourf(X, Y, pattern, levels=20, cmap='viridis')
            plt.colorbar(label='Amplitude')
            plt.title('Cymatic Pattern Visualization')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.axis('equal')
            
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return save_path
        except Exception as e:
            print(f"Visualization error: {e}")
            return ""


def test_advanced_cymatics():
    """Test the advanced cymatic engine"""
    engine = AdvancedCymaticEngine()
    
    test_freqs = [10, 40, 432, 528]
    
    print("\n" + "="*60)
    print("ADVANCED CYMATIC ENGINE TEST")
    print("="*60)
    
    for freq in test_freqs:
        print(f"\n🎵 Frequency: {freq} Hz")
        
        pattern = engine.generate_cymatic_pattern(freq)
        print(f"   Pattern shape: {pattern.shape}")
        
        metrics = engine.calculate_pattern_metrics(pattern)
        print(f"   Symmetry: {metrics['symmetry']:.3f}")
        print(f"   Complexity: {metrics['complexity']:.3f}")
        print(f"   Coherence: {metrics['coherence']:.3f}")
    
    print("\n" + "="*60)
    print("HARMONIC TRANSFORMATION TEST")
    print("="*60)
    
    result = engine.transform_with_harmonics(10, layers=5)
    print(f"\nBase Frequency: {result['base_frequency']} Hz")
    print(f"Harmonic Ladder: {result['harmonics']}")
    print(f"\nAggregated Metrics:")
    print(f"  Symmetry: {result['aggregated_metrics']['symmetry']:.3f}")
    print(f"  Complexity: {result['aggregated_metrics']['complexity']:.3f}")
    print(f"  Coherence: {result['aggregated_metrics']['coherence']:.3f}")


if __name__ == "__main__":
    test_advanced_cymatics()
