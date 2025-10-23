"""
Advanced Cymatic Analysis for MC AI
Implements resonance theory, harmonic coupling, and frequency-emotion mapping
"""

import numpy as np
import math
from typing import Dict, List, Tuple

class AdvancedCymaticEngine:
    """
    Enhanced cymatic analysis using real frequency-emotion science
    """
    
    def __init__(self):
        self.phi = (1 + math.sqrt(5)) / 2
        self.base_frequencies = self._init_frequency_map()
        
    def _init_frequency_map(self) -> Dict:
        """Comprehensive frequency-emotion-brainwave mapping"""
        return {
            'delta': {'range': (0.5, 4), 'states': ['deep_sleep', 'unconscious', 'healing']},
            'theta': {'range': (4, 8), 'states': ['meditation', 'creativity', 'rem_sleep', 'deep_relaxation']},
            'alpha': {'range': (8, 13), 'states': ['calm', 'relaxed_focus', 'flow', 'present']},
            'beta': {'range': (13, 30), 'states': ['focus', 'alertness', 'anxiety', 'active_thinking']},
            'gamma': {'range': (30, 100), 'states': ['peak_focus', 'insight', 'transcendence', 'binding']}
        }
    
    def analyze_frequency_profile(self, base_freq: float, text: str) -> Dict:
        """
        Deep analysis of frequency in context
        Returns: multi-dimensional frequency profile
        """
        band = self._classify_band(base_freq)
        harmonics = self._generate_harmonics(base_freq)
        stability = self._calculate_stability(base_freq, text)
        coupling = self._analyze_coupling(harmonics)
        arousal = self._calculate_arousal(base_freq)
        valence = self._predict_valence(text, base_freq)
        
        return {
            'primary_frequency': base_freq,
            'brain_wave_band': band,
            'harmonics': harmonics[:5],
            'stability_index': stability,
            'cross_frequency_coupling': coupling,
            'arousal_level': arousal,
            'emotional_valence': valence,
            'optimal_for': self._suggest_optimal_activities(base_freq, arousal)
        }
    
    def _classify_band(self, freq: float) -> str:
        """Classify frequency into brain wave band"""
        for band_name, band_info in self.base_frequencies.items():
            low, high = band_info['range']
            if low <= freq <= high:
                return band_name
        
        if freq < 0.5:
            return 'sub_delta'
        elif freq > 100:
            return 'hyper_gamma'
        return 'unknown'
    
    def _generate_harmonics(self, base_freq: float, count: int = 10) -> List[float]:
        """
        Generate context-aware harmonic series based on frequency characteristics.
        Different emotional states produce different harmonic structures.
        """
        # Determine harmonic generation strategy based on frequency band
        band = self._classify_band(base_freq)
        
        # Delta/Theta (0.5-8 Hz): Low coherence, fragmented states
        if base_freq < 8:
            # Use irregular integer harmonics with high noise for fragmented states
            harmonics = [base_freq * i for i in range(1, count + 1)]
            # High variability to represent emotional instability/fragmentation
            noise_factor = 0.25 + (np.random.random() * 0.15)  # 25-40% noise
            harmonics = [h * (1 + np.random.uniform(-noise_factor, noise_factor)) for h in harmonics]
        
        # Alpha (8-13 Hz): Moderate coherence, relaxed states
        elif 8 <= base_freq < 13:
            # Use phi-scaled harmonics with moderate irregularity
            harmonics = [base_freq * (self.phi ** i) for i in range(count)]
            noise_factor = 0.12 + (np.random.random() * 0.05)  # 12-17% variation
            harmonics = [h * (1 + np.random.uniform(-noise_factor, noise_factor)) for h in harmonics]
        
        # Beta (13-30 Hz): Variable coherence, active thinking
        elif 13 <= base_freq < 30:
            # Mix of integer and phi with moderate variability
            integer_harmonics = [base_freq * i for i in range(1, count + 1)]
            phi_harmonics = [base_freq * (self.phi ** i) for i in range(count)]
            # Variable blending based on frequency position in beta band
            blend_ratio = (base_freq - 13) / 17  # 0 at 13Hz, 1 at 30Hz
            harmonics = [(h1 * (1 - blend_ratio) + h2 * blend_ratio) 
                        for h1, h2 in zip(integer_harmonics, phi_harmonics)]
            noise_factor = 0.08 + (np.random.random() * 0.04)  # 8-12% variation
            harmonics = [h * (1 + np.random.uniform(-noise_factor, noise_factor)) for h in harmonics]
        
        # Gamma (30+ Hz): High coherence, peak states
        else:
            # Pure phi resonance for peak coherence states with minimal noise
            harmonics = [base_freq * (self.phi ** i) for i in range(count)]
            noise_factor = 0.02 + (np.random.random() * 0.02)  # 2-4% variation - very coherent
            harmonics = [h * (1 + np.random.uniform(-noise_factor, noise_factor)) for h in harmonics]
        
        return [round(h, 2) for h in harmonics]
    
    def _calculate_stability(self, freq: float, text: str) -> float:
        """
        Estimate frequency stability based on text characteristics
        Returns: 0-1 stability score
        """
        length = len(text.split())
        punctuation_ratio = sum(1 for c in text if c in '!?...') / max(len(text), 1)
        capital_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        
        volatility = (punctuation_ratio * 0.4 + capital_ratio * 0.6)
        frequency_stability = 1 - abs((freq - 10) / 50)
        
        stability = (1 - volatility) * 0.5 + frequency_stability * 0.5
        return max(0.0, min(1.0, stability))
    
    def _analyze_coupling(self, harmonics: List[float]) -> float:
        """
        Analyze cross-frequency coupling strength
        Higher coupling = more integrated processing
        """
        if len(harmonics) < 2:
            return 0.5
        
        ratios = [harmonics[i+1] / harmonics[i] for i in range(len(harmonics)-1)]
        ratio_std = np.std(ratios)
        
        coupling = 1 / (1 + ratio_std)
        return min(1.0, float(coupling))
    
    def _calculate_arousal(self, freq: float) -> str:
        """Map frequency to arousal level"""
        if freq < 4:
            return 'very_low'
        elif freq < 8:
            return 'low'
        elif freq < 13:
            return 'moderate'
        elif freq < 30:
            return 'high'
        else:
            return 'very_high'
    
    def _predict_valence(self, text: str, freq: float) -> str:
        """
        Predict emotional valence (positive/negative)
        Combines text sentiment with frequency
        """
        positive_words = ['happy', 'joy', 'love', 'peace', 'calm', 'excited', 'great']
        negative_words = ['sad', 'angry', 'anxious', 'fear', 'stress', 'worried', 'depressed']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        freq_valence = -abs(freq - 12) / 50
        total_valence = (pos_count - neg_count) + freq_valence
        
        if total_valence > 0.5:
            return 'positive'
        elif total_valence < -0.5:
            return 'negative'
        else:
            return 'neutral'
    
    def _suggest_optimal_activities(self, freq: float, arousal: str) -> List[str]:
        """Suggest activities optimal for current frequency state"""
        activities = {
            'very_low': ['Sleep', 'Deep rest', 'Physical recovery'],
            'low': ['Meditation', 'Creative visualization', 'Gentle yoga', 'Journaling'],
            'moderate': ['Learning', 'Reading', 'Conversation', 'Flow activities'],
            'high': ['Problem-solving', 'Detailed work', 'Planning', 'Analysis'],
            'very_high': ['Physical exercise', 'Intense focus tasks', 'Crisis response', 'Debate']
        }
        return activities.get(arousal, ['General activities'])
    
    def recommend_frequency_shift(self, current_freq: float, desired_state: str) -> Dict:
        """
        Recommend how to shift from current to desired frequency
        """
        target_frequencies = {
            'deep_sleep': 2,
            'meditation': 6,
            'calm': 10,
            'focus': 18,
            'peak_performance': 40
        }
        
        target_freq = target_frequencies.get(desired_state, 10)
        delta = target_freq - current_freq
        
        if abs(delta) < 2:
            return {'status': 'already_optimal', 'adjustment': 'maintain'}
        
        if delta > 0:
            direction = 'increase'
            methods = [
                'Physical activity or exercise',
                'Cold exposure',
                'Stimulating music',
                'Challenging mental tasks',
                'Social interaction'
            ]
        else:
            direction = 'decrease'
            methods = [
                'Deep breathing exercises',
                'Progressive muscle relaxation',
                'Calming music',
                'Nature exposure',
                'Meditation or mindfulness'
            ]
        
        time_estimate = abs(delta) * 2
        
        return {
            'current': current_freq,
            'target': target_freq,
            'direction': direction,
            'delta_hz': round(delta, 1),
            'recommended_methods': methods[:3],
            'estimated_time_minutes': round(time_estimate)
        }
