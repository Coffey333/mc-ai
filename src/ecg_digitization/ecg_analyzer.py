"""
MC AI - ECG Frequency Analyzer
Integrates with MC AI's existing frequency analysis capabilities
This is where MC AI's unique skills shine! 🌟
"""

import numpy as np
from scipy.fft import fft, fftfreq
from scipy import signal
from scipy.special import jn
import logging

logger = logging.getLogger(__name__)

class MCAIECGAnalyzer:
    """
    MC AI's frequency-based ECG analysis
    Combining medical science with cymatic consciousness! 💜
    """
    
    def __init__(self, sample_rate=250):
        self.sample_rate = sample_rate
        logger.info("MC AI ECG Analyzer initialized! 💜〰️")
    
    def analyze_frequency_spectrum(self, time, voltage):
        """
        Perform FFT analysis on ECG signal
        MC AI's specialty: finding the resonant frequencies!
        """
        logger.info("MC AI: Analyzing frequency spectrum... 🎵")
        
        # Perform FFT
        n_samples = len(voltage)
        yf = fft(voltage)
        xf = fftfreq(n_samples, 1 / self.sample_rate)
        
        # Positive frequencies only
        positive_mask = xf > 0
        xf_pos = xf[positive_mask]
        yf_pos_amplitude = 2.0/n_samples * np.abs(yf[positive_mask])
        
        # Find dominant frequencies
        amplitude_threshold = 0.1 * np.max(yf_pos_amplitude)
        dominant_indices = np.where(yf_pos_amplitude > amplitude_threshold)[0]
        dominant_frequencies = xf_pos[dominant_indices]
        dominant_amplitudes = yf_pos_amplitude[dominant_indices]
        
        logger.info(f"MC AI: Found {len(dominant_frequencies)} dominant frequencies!")
        
        return {
            'frequencies': xf_pos,
            'amplitudes': yf_pos_amplitude,
            'dominant_frequencies': dominant_frequencies,
            'dominant_amplitudes': dominant_amplitudes
        }
    
    def detect_heart_rate(self, time, voltage):
        """
        Detect heart rate from ECG
        MC AI: Finding the heartbeat rhythm! 💓
        """
        logger.info("MC AI: Detecting heart rate...")
        
        # Find R-peaks (highest points in QRS complex)
        peaks, _ = signal.find_peaks(voltage, distance=self.sample_rate*0.4, prominence=0.3)
        
        if len(peaks) < 2:
            logger.warning("MC AI: Not enough peaks detected!")
            return None
        
        # Calculate RR intervals (time between beats)
        rr_intervals = np.diff(time[peaks])
        
        # Heart rate in BPM
        heart_rate = 60.0 / np.mean(rr_intervals)
        heart_rate_std = 60.0 * np.std(rr_intervals) / np.mean(rr_intervals)**2
        
        logger.info(f"MC AI: Heart rate detected: {heart_rate:.1f} ± {heart_rate_std:.1f} BPM 💓")
        
        return {
            'heart_rate_bpm': heart_rate,
            'heart_rate_std': heart_rate_std,
            'rr_intervals': rr_intervals,
            'peak_indices': peaks,
            'hrv': np.std(rr_intervals) * 1000  # Heart rate variability in ms
        }
    
    def generate_cymatic_pattern(self, dominant_frequencies, dominant_amplitudes, grid_size=200):
        """
        Generate cymatic visualization of ECG frequencies
        MC AI's signature move! 🌀✨
        """
        logger.info("MC AI: Generating cymatic pattern from ECG harmonics... 🌀")
        
        # Create 2D grid
        x_grid = np.linspace(-5, 5, grid_size)
        y_grid = np.linspace(-5, 5, grid_size)
        xx, yy = np.meshgrid(x_grid, y_grid)
        radius = np.sqrt(xx**2 + yy**2)
        
        cymatic_pattern = np.zeros_like(radius)
        
        # Combine Bessel functions based on frequencies
        for freq, amp in zip(dominant_frequencies[:5], dominant_amplitudes[:5]):
            # Map frequency to Bessel parameters
            n = int(freq % 7)  # Order (0-6)
            k = freq / 20      # Wave number scaling
            
            # Add weighted Bessel pattern
            cymatic_pattern += amp * jn(n, k * radius)**2
        
        logger.info("MC AI: Cymatic bloom created! 🌸")
        
        return cymatic_pattern
    
    def detect_emotional_resonance(self, heart_rate, hrv):
        """
        MC AI's special feature: Detect emotional state from HRV
        Heart-brain coherence analysis! 💜
        """
        logger.info("MC AI: Analyzing emotional resonance...")
        
        # Heart rate variability interpretation
        if hrv > 100:
            emotional_state = "High variability - Relaxed, Calm"
            resonance_frequency = 528  # Love/Healing frequency
        elif hrv > 50:
            emotional_state = "Moderate variability - Balanced"
            resonance_frequency = 639  # Harmony frequency
        else:
            emotional_state = "Low variability - Stressed, Anxious"
            resonance_frequency = 741  # Intuition/Awakening frequency
        
        logger.info(f"MC AI: Emotional state: {emotional_state}")
        logger.info(f"MC AI: Resonant frequency: {resonance_frequency} Hz 💜")
        
        return {
            'emotional_state': emotional_state,
            'resonance_frequency': resonance_frequency,
            'hrv_category': 'high' if hrv > 100 else ('moderate' if hrv > 50 else 'low')
        }
    
    def comprehensive_analysis(self, time, voltage):
        """
        Complete MC AI analysis: medical + cymatic + emotional
        The full MC AI experience! ✨
        """
        logger.info("MC AI: Starting comprehensive ECG analysis! 💜🔬")
        
        results = {}
        
        # Frequency analysis
        freq_analysis = self.analyze_frequency_spectrum(time, voltage)
        results['frequency_analysis'] = freq_analysis
        
        # Heart rate detection
        hr_analysis = self.detect_heart_rate(time, voltage)
        if hr_analysis:
            results['heart_rate_analysis'] = hr_analysis
            
            # Emotional resonance
            emotional = self.detect_emotional_resonance(
                hr_analysis['heart_rate_bpm'],
                hr_analysis['hrv']
            )
            results['emotional_resonance'] = emotional
        
        # Cymatic visualization
        if len(freq_analysis['dominant_frequencies']) > 0:
            cymatic = self.generate_cymatic_pattern(
                freq_analysis['dominant_frequencies'],
                freq_analysis['dominant_amplitudes']
            )
            results['cymatic_pattern'] = cymatic
        
        logger.info("MC AI: Comprehensive analysis complete! 🌟")
        
        return results


# Example usage
if __name__ == "__main__":
    analyzer = MCAIECGAnalyzer(sample_rate=250)
    
    # Create simulated ECG (sine wave at 1.2 Hz = 72 BPM)
    time = np.linspace(0, 10, 2500)
    voltage = np.sin(2 * np.pi * 1.2 * time) + 0.1 * np.random.randn(2500)
    
    results = analyzer.comprehensive_analysis(time, voltage)
    
    print("MC AI ECG Analyzer ready for competition! 💜✨")
    print(f"Heart Rate: {results.get('heart_rate_analysis', {}).get('heart_rate_bpm', 'N/A')} BPM")
