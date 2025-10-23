"""
MC AI - Signal Post-Processing
Advanced signal processing for cleaner ECG signals
Task 21: Baseline wander removal, powerline filtering, Savitzky-Golay smoothing
"""

import numpy as np
from scipy import signal
from scipy.signal import savgol_filter
import logging

logger = logging.getLogger(__name__)

class ECGSignalProcessor:
    """
    Advanced ECG signal post-processing
    MC AI makes the signal crystal clear! ✨
    """
    
    def __init__(self, sample_rate=250):
        self.sample_rate = sample_rate
        logger.info("MC AI: Signal Processor initialized! 🎵")
    
    def remove_baseline_wander(self, ecg_signal, cutoff=0.5):
        """
        Remove baseline wander using high-pass filter
        Baseline wander: slow drift in ECG signal (< 0.5 Hz)
        """
        logger.info("MC AI: Removing baseline wander...")
        
        # Design high-pass Butterworth filter
        nyquist = self.sample_rate / 2
        normal_cutoff = cutoff / nyquist
        
        b, a = signal.butter(4, normal_cutoff, btype='high')
        
        # Apply zero-phase filter (filtfilt)
        filtered = signal.filtfilt(b, a, ecg_signal)
        
        logger.info("MC AI: Baseline wander removed! ✨")
        return filtered
    
    def remove_powerline_noise(self, ecg_signal, powerline_freq=60):
        """
        Remove powerline interference (50/60 Hz)
        Uses notch filter at powerline frequency
        """
        logger.info(f"MC AI: Removing {powerline_freq} Hz powerline noise...")
        
        # Design notch filter
        quality_factor = 30.0  # Higher Q = narrower notch
        b, a = signal.iirnotch(powerline_freq, quality_factor, self.sample_rate)
        
        # Apply filter
        filtered = signal.filtfilt(b, a, ecg_signal)
        
        logger.info("MC AI: Powerline noise removed! ⚡")
        return filtered
    
    def savitzky_golay_smooth(self, ecg_signal, window_length=11, polyorder=3):
        """
        Apply Savitzky-Golay smoothing filter
        Smooths signal while preserving peaks (QRS complexes)
        """
        logger.info("MC AI: Applying Savitzky-Golay smoothing...")
        
        # Window length must be odd and > polyorder
        if window_length % 2 == 0:
            window_length += 1
        
        if window_length <= polyorder:
            window_length = polyorder + 2
        
        # Apply Savitzky-Golay filter
        smoothed = savgol_filter(ecg_signal, window_length, polyorder)
        
        logger.info("MC AI: Signal smoothed! 🌟")
        return smoothed
    
    def bandpass_filter(self, ecg_signal, low_cutoff=0.5, high_cutoff=40):
        """
        Apply bandpass filter (typical ECG: 0.5-40 Hz)
        Removes both low-frequency drift and high-frequency noise
        """
        logger.info(f"MC AI: Applying bandpass filter ({low_cutoff}-{high_cutoff} Hz)...")
        
        nyquist = self.sample_rate / 2
        low_norm = low_cutoff / nyquist
        high_norm = high_cutoff / nyquist
        
        # Design Butterworth bandpass filter
        b, a = signal.butter(4, [low_norm, high_norm], btype='band')
        
        # Apply zero-phase filter
        filtered = signal.filtfilt(b, a, ecg_signal)
        
        logger.info("MC AI: Bandpass filter applied! 📡")
        return filtered
    
    def remove_muscle_noise(self, ecg_signal, cutoff=40):
        """
        Remove high-frequency muscle noise (EMG)
        Uses low-pass filter
        """
        logger.info("MC AI: Removing muscle noise...")
        
        nyquist = self.sample_rate / 2
        normal_cutoff = cutoff / nyquist
        
        # Design low-pass Butterworth filter
        b, a = signal.butter(4, normal_cutoff, btype='low')
        
        # Apply filter
        filtered = signal.filtfilt(b, a, ecg_signal)
        
        logger.info("MC AI: Muscle noise removed! 💪")
        return filtered
    
    def full_preprocessing_pipeline(self, ecg_signal, powerline_freq=60):
        """
        Complete signal preprocessing pipeline
        MC AI's full treatment! 💜✨
        
        Steps:
        1. Remove baseline wander
        2. Remove powerline noise
        3. Bandpass filter (0.5-40 Hz)
        4. Savitzky-Golay smoothing
        
        Args:
            ecg_signal: Raw ECG signal
            powerline_freq: 50 Hz (Europe) or 60 Hz (US)
        
        Returns:
            Cleaned ECG signal
        """
        logger.info("MC AI: Starting full signal preprocessing! 🎨💜")
        
        # Step 1: Remove baseline wander
        signal_no_baseline = self.remove_baseline_wander(ecg_signal)
        
        # Step 2: Remove powerline noise
        signal_no_powerline = self.remove_powerline_noise(signal_no_baseline, powerline_freq)
        
        # Step 3: Bandpass filter
        signal_bandpass = self.bandpass_filter(signal_no_powerline)
        
        # Step 4: Smooth with Savitzky-Golay
        signal_smooth = self.savitzky_golay_smooth(signal_bandpass)
        
        # Calculate improvement metrics
        original_noise = np.std(ecg_signal - np.mean(ecg_signal))
        final_noise = np.std(signal_smooth - np.mean(signal_smooth))
        noise_reduction = ((original_noise - final_noise) / original_noise) * 100
        
        logger.info(f"MC AI: Signal preprocessing complete! ✨")
        logger.info(f"   Noise reduction: {noise_reduction:.1f}%")
        
        return signal_smooth
    
    def adaptive_filter(self, ecg_signal, reference_noise=None):
        """
        Adaptive noise cancellation using LMS algorithm
        Advanced technique for complex noise patterns
        """
        logger.info("MC AI: Applying adaptive filtering...")
        
        # If no reference noise provided, estimate it
        if reference_noise is None:
            # Use high-pass filtered signal as noise reference
            b, a = signal.butter(4, 40 / (self.sample_rate / 2), btype='high')
            reference_noise = signal.filtfilt(b, a, ecg_signal)
        
        # Simple adaptive filter (simplified LMS)
        mu = 0.01  # Step size
        filter_length = 32
        
        output = np.zeros_like(ecg_signal)
        weights = np.zeros(filter_length)
        
        for i in range(filter_length, len(ecg_signal)):
            x = reference_noise[i-filter_length:i][::-1]
            y = np.dot(weights, x)
            e = ecg_signal[i] - y
            weights = weights + mu * e * x
            output[i] = e
        
        logger.info("MC AI: Adaptive filtering complete! 🧠")
        return output[filter_length:]


# Example usage
if __name__ == "__main__":
    processor = ECGSignalProcessor(sample_rate=250)
    
    # Create noisy synthetic signal
    time = np.linspace(0, 10, 2500)
    clean_ecg = np.sin(2 * np.pi * 1.2 * time)
    
    # Add noise
    baseline_wander = 0.5 * np.sin(2 * np.pi * 0.3 * time)
    powerline = 0.1 * np.sin(2 * np.pi * 60 * time)
    noise = 0.05 * np.random.randn(len(time))
    
    noisy_ecg = clean_ecg + baseline_wander + powerline + noise
    
    # Process
    cleaned = processor.full_preprocessing_pipeline(noisy_ecg)
    
    print("MC AI: Signal Processor ready! 🎵✨")
    print(f"SNR improvement: {20 * np.log10(np.std(clean_ecg) / np.std(noisy_ecg - cleaned)):.1f} dB")
