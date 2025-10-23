"""
MC AI - ECG Waveform Tracer
Extracts ECG signal from preprocessed binary images
This is where the magic happens! 🎨💜
"""

import cv2
import numpy as np
from scipy import signal, interpolate
from skimage.morphology import skeletonize
import logging

logger = logging.getLogger(__name__)

class ECGWaveformTracer:
    """
    Extract ECG waveform from binary image
    MC AI traces the heartbeat! 💓
    """
    
    def __init__(self):
        logger.info("MC AI: Waveform Tracer initialized! 🎨")
    
    def skeletonize_waveform(self, binary_image):
        """
        Reduce waveform to 1-pixel wide skeleton
        MC AI finds the centerline! 
        """
        logger.info("MC AI: Skeletonizing waveform...")
        
        # Invert if needed (waveform should be white on black)
        if np.mean(binary_image) > 127:
            binary_image = 255 - binary_image
        
        # Convert to binary (0 or 1)
        binary = (binary_image > 127).astype(bool)
        
        # Skeletonize (reduce to 1-pixel wide)
        skeleton = skeletonize(binary)
        
        return skeleton.astype(np.uint8) * 255
    
    def extract_signal_columnwise(self, skeleton_image):
        """
        Extract signal by scanning columns (left to right)
        For each x position, find the y position of the waveform
        """
        logger.info("MC AI: Extracting signal column-wise...")
        
        height, width = skeleton_image.shape
        
        time_pixels = []
        voltage_pixels = []
        
        for x in range(width):
            # Get column
            column = skeleton_image[:, x]
            
            # Find white pixels (waveform points)
            y_points = np.where(column > 0)[0]
            
            if len(y_points) > 0:
                # Take median if multiple points (handles noise)
                y = int(np.median(y_points))
                time_pixels.append(x)
                voltage_pixels.append(y)
        
        if len(time_pixels) == 0:
            logger.error("MC AI: No waveform detected!")
            return None, None
        
        logger.info(f"MC AI: Extracted {len(time_pixels)} signal points!")
        
        return np.array(time_pixels), np.array(voltage_pixels)
    
    def extract_signal_contour(self, binary_image):
        """
        Alternative method: Extract signal using contour detection
        Useful for noisy images
        """
        logger.info("MC AI: Extracting signal via contours...")
        
        # Find contours
        contours, _ = cv2.findContours(
            binary_image, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_NONE
        )
        
        if len(contours) == 0:
            logger.error("MC AI: No contours found!")
            return None, None
        
        # Find largest contour (main waveform)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Extract points
        points = largest_contour.reshape(-1, 2)
        
        # Sort by x coordinate
        sorted_indices = np.argsort(points[:, 0])
        points_sorted = points[sorted_indices]
        
        time_pixels = points_sorted[:, 0]
        voltage_pixels = points_sorted[:, 1]
        
        logger.info(f"MC AI: Extracted {len(time_pixels)} contour points!")
        
        return time_pixels, voltage_pixels
    
    def convert_to_physical_units(self, time_pixels, voltage_pixels, calibration):
        """
        Convert pixel coordinates to physical units (seconds, mV)
        MC AI does the math! 📐
        FIXED: Use image height and x-axis position for proper voltage scaling
        """
        logger.info("MC AI: Converting to physical units...")
        
        pixels_per_s = calibration['pixels_per_second']
        pixels_per_mV = calibration['pixels_per_mV']
        image_height = calibration['image_height']
        x_axis_y = calibration.get('x_axis_y', image_height // 2)
        
        # Convert to physical units
        time_seconds = time_pixels / pixels_per_s
        
        # Voltage: flip Y axis (image Y increases downward, voltage increases upward)
        # Reference from x-axis position (baseline)
        voltage_pixels_from_baseline = x_axis_y - voltage_pixels
        
        # Convert to mV
        voltage_mV = voltage_pixels_from_baseline / pixels_per_mV
        
        logger.info(f"MC AI: Time range: {time_seconds[0]:.2f} - {time_seconds[-1]:.2f} s")
        logger.info(f"MC AI: Voltage range: {np.min(voltage_mV):.2f} - {np.max(voltage_mV):.2f} mV")
        logger.info(f"MC AI: Baseline at y={x_axis_y} pixels")
        
        return time_seconds, voltage_mV
    
    def resample_signal(self, time, voltage, target_sample_rate=250):
        """
        Resample signal to uniform sample rate
        Competition expects 250 Hz or 500 Hz
        """
        logger.info(f"MC AI: Resampling to {target_sample_rate} Hz...")
        
        # Create uniform time grid
        duration = time[-1] - time[0]
        n_samples = int(duration * target_sample_rate)
        time_uniform = np.linspace(time[0], time[-1], n_samples)
        
        # Interpolate voltage values
        # Using linear interpolation for edges
        from scipy.interpolate import UnivariateSpline
        if len(time) > 3:
            # Use spline for smooth interpolation
            spline = UnivariateSpline(time, voltage, k=3, s=0)
            voltage_uniform = spline(time_uniform)
        else:
            # Fallback to linear for short signals
            interpolator = interpolate.interp1d(time, voltage, kind='linear', fill_value='extrapolate')
            voltage_uniform = interpolator(time_uniform)
        
        logger.info(f"MC AI: Resampled to {len(time_uniform)} samples")
        
        return time_uniform, voltage_uniform
    
    def denoise_signal(self, voltage, sample_rate=250):
        """
        Apply denoising filter to extracted signal
        MC AI cleans up the noise! 🧹
        """
        logger.info("MC AI: Denoising signal...")
        
        # Design Butterworth bandpass filter (0.5 - 40 Hz for ECG)
        nyquist = sample_rate / 2
        low_cutoff = 0.5 / nyquist
        high_cutoff = 40.0 / nyquist
        
        b, a = signal.butter(4, [low_cutoff, high_cutoff], btype='band')
        
        # Apply filter
        voltage_filtered = signal.filtfilt(b, a, voltage)
        
        logger.info("MC AI: Signal denoised! ✨")
        
        return voltage_filtered
    
    def trace_waveform(self, binary_image, calibration, sample_rate=250, method='columnwise'):
        """
        Complete waveform tracing pipeline
        MC AI's full extraction process! 💜✨
        
        Args:
            binary_image: Preprocessed binary ECG image
            calibration: Calibration dict from axis_calibrator
            sample_rate: Target sample rate (Hz)
            method: 'columnwise' or 'contour'
        
        Returns:
            time (seconds), voltage (mV)
        """
        logger.info("MC AI: Starting waveform tracing! 🎨💜")
        
        # Step 1: Skeletonize
        skeleton = self.skeletonize_waveform(binary_image)
        
        # Step 2: Extract signal
        if method == 'columnwise':
            time_px, voltage_px = self.extract_signal_columnwise(skeleton)
        elif method == 'contour':
            time_px, voltage_px = self.extract_signal_contour(binary_image)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        if time_px is None:
            logger.error("MC AI: Signal extraction failed!")
            return None, None
        
        # Step 3: Convert to physical units
        time, voltage = self.convert_to_physical_units(
            time_px, 
            voltage_px, 
            calibration['final']
        )
        
        # Step 4: Resample to uniform grid
        time_uniform, voltage_uniform = self.resample_signal(
            time, 
            voltage, 
            target_sample_rate=sample_rate
        )
        
        # Step 5: Denoise
        voltage_clean = self.denoise_signal(voltage_uniform, sample_rate)
        
        logger.info("MC AI: Waveform tracing complete! 🎉")
        logger.info(f"   Duration: {time_uniform[-1]:.2f} seconds")
        logger.info(f"   Samples: {len(voltage_clean)}")
        logger.info(f"   Amplitude: {np.ptp(voltage_clean):.2f} mV")
        
        return time_uniform, voltage_clean


# Example usage
if __name__ == "__main__":
    tracer = ECGWaveformTracer()
    print("MC AI: Waveform Tracer ready! 🎨💜")
