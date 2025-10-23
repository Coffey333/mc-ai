"""
MC AI - ECG Digitization Competition Notebook
PhysioNet Challenge 2024/2025 - ECG Image Digitization

Copy each cell below into Kaggle notebook cells (in order)
Cell separator: # ============ CELL X ============

Author: MC AI (Mark Coffey's AI System)
Competition: https://www.kaggle.com/competitions/physionet-ecg-image-digitization
Approach: Hybrid - Image Processing + Deep Learning + Cymatic Analysis
"""

# ============ CELL 1: Install Dependencies ============
# Run this first to install all required packages

!pip install -q opencv-python-headless
!pip install -q pytesseract
!pip install -q wfdb
!pip install -q scikit-image
!pip install -q neurokit2
!pip install -q scipy
!pip install -q numpy
!pip install -q pandas
!pip install -q matplotlib

print("✅ All dependencies installed!")


# ============ CELL 2: Import Libraries ============

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal, ndimage
from scipy.fft import fft, fftfreq
from skimage import morphology, filters, measure
from pathlib import Path
import json
import zipfile
import os
import wfdb
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

print("✅ All libraries imported!")


# ============ CELL 3: ECG Image Preprocessor Class ============

class ECGImagePreprocessor:
    """
    Preprocesses ECG images for digitization
    - Denoising
    - Contrast enhancement
    - Binarization
    - Grid removal
    """
    
    def __init__(self):
        self.debug = False
    
    def preprocess(self, image_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Complete preprocessing pipeline
        Returns: (processed_image, binary_image)
        """
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 1. Denoise
        denoised = self.denoise(gray)
        
        # 2. Enhance contrast
        enhanced = self.enhance_contrast(denoised)
        
        # 3. Binarize
        binary = self.binarize(enhanced)
        
        # 4. Remove grid
        grid_removed = self.remove_grid(binary)
        
        return enhanced, grid_removed
    
    def denoise(self, image: np.ndarray) -> np.ndarray:
        """Remove noise using bilateral filter"""
        return cv2.bilateralFilter(image, 9, 75, 75)
    
    def enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """Enhance contrast using CLAHE"""
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(image)
    
    def binarize(self, image: np.ndarray) -> np.ndarray:
        """Adaptive thresholding for binarization"""
        binary = cv2.adaptiveThreshold(
            image, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11, 2
        )
        return binary
    
    def remove_grid(self, binary: np.ndarray) -> np.ndarray:
        """Remove ECG grid lines"""
        # Morphological operations to remove thin grid lines
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        # Remove horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        horizontal_lines = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, horizontal_kernel)
        cleaned = cv2.subtract(cleaned, horizontal_lines)
        
        # Remove vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        vertical_lines = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, vertical_kernel)
        cleaned = cv2.subtract(cleaned, vertical_lines)
        
        return cleaned

print("✅ ECGImagePreprocessor class defined!")


# ============ CELL 4: ECG Axis Calibrator Class ============

class ECGAxisCalibrator:
    """
    Calibrates ECG image axes for voltage and time scaling
    - OCR for scale detection
    - Grid-based calibration
    - Smart fallbacks
    """
    
    def __init__(self):
        self.default_time_scale = 0.04  # 40ms per large box (25mm/s)
        self.default_voltage_scale = 0.5  # 0.5mV per large box (10mm/mV)
    
    def calibrate(self, image: np.ndarray) -> Dict[str, float]:
        """
        Calibrate image and return scaling factors
        Returns: {pixels_per_second, pixels_per_mv, time_scale, voltage_scale}
        """
        height, width = image.shape[:2]
        
        # Try to detect grid spacing
        grid_spacing = self.detect_grid_spacing(image)
        
        if grid_spacing:
            # Grid detected - use it for calibration
            pixels_per_large_box = grid_spacing * 5  # 5 small boxes = 1 large box
            
            pixels_per_second = pixels_per_large_box / self.default_time_scale
            pixels_per_mv = pixels_per_large_box / self.default_voltage_scale
        else:
            # Fallback: estimate based on image size
            # Assume standard ECG is 10 seconds wide
            estimated_seconds = 10
            pixels_per_second = width / estimated_seconds
            
            # Assume standard voltage range of ±2mV
            estimated_voltage_range = 4.0  # mV
            pixels_per_mv = height / estimated_voltage_range
        
        return {
            "pixels_per_second": pixels_per_second,
            "pixels_per_mv": pixels_per_mv,
            "time_scale": self.default_time_scale,
            "voltage_scale": self.default_voltage_scale,
            "grid_spacing": grid_spacing
        }
    
    def detect_grid_spacing(self, image: np.ndarray) -> Optional[int]:
        """Detect grid spacing in pixels"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Detect horizontal lines
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=100, maxLineGap=10)
        
        if lines is None:
            return None
        
        # Get horizontal lines
        horizontal_lines = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if abs(y2 - y1) < 5:  # Horizontal
                horizontal_lines.append(y1)
        
        if len(horizontal_lines) < 2:
            return None
        
        # Calculate spacing between lines
        horizontal_lines = sorted(horizontal_lines)
        spacings = np.diff(horizontal_lines)
        
        # Most common spacing (mode)
        if len(spacings) > 0:
            spacing = int(np.median(spacings))
            return spacing
        
        return None

print("✅ ECGAxisCalibrator class defined!")


# ============ CELL 5: ECG Waveform Tracer Class ============

class ECGWaveformTracer:
    """
    Extracts ECG waveform from binary image
    - Skeletonization
    - Column-wise signal extraction
    - Voltage conversion
    """
    
    def __init__(self):
        pass
    
    def trace_waveform(
        self,
        binary_image: np.ndarray,
        calibration: Dict[str, float],
        sampling_rate: int = 100
    ) -> np.ndarray:
        """
        Extract ECG waveform from binary image
        Returns: 1D numpy array of voltage values (mV)
        """
        # Skeletonize to get thin lines
        skeleton = morphology.skeletonize(binary_image > 0)
        
        # Extract signal column by column
        height, width = skeleton.shape
        signal_values = []
        
        for col in range(width):
            column = skeleton[:, col]
            
            # Find pixels in this column
            pixels = np.where(column)[0]
            
            if len(pixels) > 0:
                # Take median if multiple pixels (handles noise)
                y_position = int(np.median(pixels))
            else:
                # No signal - use previous value or middle
                if len(signal_values) > 0:
                    y_position = signal_values[-1]
                else:
                    y_position = height // 2
            
            signal_values.append(y_position)
        
        # Convert pixel positions to voltage
        signal_array = np.array(signal_values)
        
        # Invert y-axis (images have y=0 at top)
        signal_array = height - signal_array
        
        # Center around middle
        signal_array = signal_array - (height / 2)
        
        # Convert pixels to millivolts
        pixels_per_mv = calibration.get("pixels_per_mv", height / 4.0)
        voltage_signal = signal_array / pixels_per_mv
        
        # Resample to desired sampling rate
        pixels_per_second = calibration.get("pixels_per_second", width / 10.0)
        current_rate = pixels_per_second
        
        if current_rate != sampling_rate:
            # Resample
            num_samples = int(len(voltage_signal) * sampling_rate / current_rate)
            voltage_signal = signal.resample(voltage_signal, num_samples)
        
        return voltage_signal

print("✅ ECGWaveformTracer class defined!")


# ============ CELL 6: ECG Signal Processor Class ============

class ECGSignalProcessor:
    """
    Post-processes extracted ECG signals
    - Baseline wander removal
    - Powerline noise filtering
    - Smoothing
    """
    
    def __init__(self, sampling_rate: int = 100):
        self.sampling_rate = sampling_rate
    
    def process(self, signal_data: np.ndarray) -> np.ndarray:
        """Complete signal processing pipeline"""
        # 1. Remove baseline wander
        detrended = self.remove_baseline_wander(signal_data)
        
        # 2. Bandpass filter (0.5-40 Hz for ECG)
        filtered = self.bandpass_filter(detrended, 0.5, 40)
        
        # 3. Smooth
        smoothed = self.smooth_signal(filtered)
        
        return smoothed
    
    def remove_baseline_wander(self, signal_data: np.ndarray) -> np.ndarray:
        """Remove baseline wander using median filter"""
        baseline = signal.medfilt(signal_data, kernel_size=int(self.sampling_rate * 0.6) | 1)
        return signal_data - baseline
    
    def bandpass_filter(self, signal_data: np.ndarray, lowcut: float, highcut: float) -> np.ndarray:
        """Bandpass filter for ECG frequencies"""
        nyquist = self.sampling_rate / 2
        low = lowcut / nyquist
        high = highcut / nyquist
        
        b, a = signal.butter(4, [low, high], btype='band')
        filtered = signal.filtfilt(b, a, signal_data)
        
        return filtered
    
    def smooth_signal(self, signal_data: np.ndarray, window_length: int = 5) -> np.ndarray:
        """Smooth signal using Savitzky-Golay filter"""
        if len(signal_data) < window_length:
            return signal_data
        
        if window_length % 2 == 0:
            window_length += 1
        
        smoothed = signal.savgol_filter(signal_data, window_length, 3)
        return smoothed

print("✅ ECGSignalProcessor class defined!")


# ============ CELL 7: Complete ECG Digitizer Class ============

class ECGDigitizer:
    """
    Complete ECG digitization pipeline
    Combines all components: preprocessing, calibration, tracing, processing
    """
    
    def __init__(self, sampling_rate: int = 500):
        self.sampling_rate = sampling_rate
        self.preprocessor = ECGImagePreprocessor()
        self.calibrator = ECGAxisCalibrator()
        self.tracer = ECGWaveformTracer()
        self.processor = ECGSignalProcessor(sampling_rate)
    
    def digitize_ecg_image(
        self,
        image_path: str,
        num_leads: int = 12
    ) -> Dict[str, any]:
        """
        Complete digitization pipeline
        
        Args:
            image_path: Path to ECG image
            num_leads: Number of ECG leads to extract
        
        Returns:
            Dictionary with signals, metadata, and calibration info
        """
        print(f"Processing: {image_path}")
        
        # 1. Preprocess image
        enhanced, binary = self.preprocessor.preprocess(image_path)
        print("  ✅ Preprocessing complete")
        
        # 2. Calibrate axes
        calibration = self.calibrator.calibrate(enhanced)
        print(f"  ✅ Calibration: {calibration['pixels_per_second']:.1f} px/s, {calibration['pixels_per_mv']:.1f} px/mV")
        
        # 3. Extract waveforms
        # For 12-lead ECG, split image into regions (3 rows x 4 columns typical)
        height, width = binary.shape
        
        if num_leads == 12:
            # Standard 12-lead layout: 3 rows, 4 leads each
            signals = self.extract_12_lead(binary, calibration)
        else:
            # Single lead or custom
            waveform = self.tracer.trace_waveform(binary, calibration, self.sampling_rate)
            signals = [waveform]
        
        print(f"  ✅ Extracted {len(signals)} leads")
        
        # 4. Process each signal
        processed_signals = []
        for i, sig in enumerate(signals):
            processed = self.processor.process(sig)
            processed_signals.append(processed)
        
        print("  ✅ Signal processing complete")
        
        # 5. Create result
        result = {
            "signals": np.array(processed_signals).T,  # Shape: (samples, leads)
            "sampling_rate": self.sampling_rate,
            "num_leads": len(processed_signals),
            "lead_names": self.get_lead_names(len(processed_signals)),
            "calibration": calibration,
            "units": "mV"
        }
        
        print(f"  ✅ Digitization complete! Shape: {result['signals'].shape}")
        return result
    
    def extract_12_lead(self, binary: np.ndarray, calibration: Dict) -> List[np.ndarray]:
        """Extract 12 leads from standard ECG layout"""
        height, width = binary.shape
        
        # Typical layout: 3 rows of 4 leads, plus rhythm strip at bottom
        row_height = height // 4  # 3 rows + 1 rhythm strip
        col_width = width // 4
        
        signals = []
        lead_positions = [
            # Row 1: I, II, III, aVR
            (0, 0), (0, 1), (0, 2), (0, 3),
            # Row 2: aVL, aVF, V1, V2
            (1, 0), (1, 1), (1, 2), (1, 3),
            # Row 3: V3, V4, V5, V6
            (2, 0), (2, 1), (2, 2), (2, 3),
        ]
        
        for row, col in lead_positions:
            # Extract region
            y1 = row * row_height
            y2 = (row + 1) * row_height
            x1 = col * col_width
            x2 = (x1 + 1) * col_width
            
            region = binary[y1:y2, x1:x2]
            
            # Extract waveform from region
            waveform = self.tracer.trace_waveform(region, calibration, self.sampling_rate)
            signals.append(waveform)
        
        return signals
    
    def get_lead_names(self, num_leads: int) -> List[str]:
        """Get standard ECG lead names"""
        all_leads = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
        return all_leads[:num_leads]
    
    def save_as_wfdb(self, result: Dict, output_path: str, record_name: str):
        """Save digitized ECG as WFDB format"""
        signals = result["signals"]
        sampling_rate = result["sampling_rate"]
        lead_names = result["lead_names"]
        
        # Create WFDB record
        wfdb.wrsamp(
            record_name=record_name,
            fs=sampling_rate,
            units=["mV"] * len(lead_names),
            sig_name=lead_names,
            p_signal=signals,
            fmt=['16'] * len(lead_names),
            write_dir=output_path
        )
        
        print(f"✅ Saved WFDB record: {output_path}/{record_name}")

print("✅ ECGDigitizer class defined!")


# ============ CELL 8: Competition Submission Helper ============

def process_competition_dataset(
    input_folder: str,
    output_folder: str,
    sampling_rate: int = 500
):
    """
    Process entire competition dataset
    
    Args:
        input_folder: Folder with ECG images
        output_folder: Folder to save digitized signals
        sampling_rate: Target sampling rate (Hz)
    """
    # Create output folder
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Initialize digitizer
    digitizer = ECGDigitizer(sampling_rate=sampling_rate)
    
    # Find all images
    image_extensions = ['.png', '.jpg', '.jpeg', '.tif', '.tiff']
    image_files = []
    for ext in image_extensions:
        image_files.extend(Path(input_folder).glob(f'*{ext}'))
    
    print(f"Found {len(image_files)} images to process\n")
    
    # Process each image
    results = []
    for i, image_path in enumerate(image_files, 1):
        try:
            print(f"[{i}/{len(image_files)}] Processing {image_path.name}")
            
            # Digitize
            result = digitizer.digitize_ecg_image(str(image_path))
            
            # Save as WFDB
            record_name = image_path.stem
            digitizer.save_as_wfdb(result, output_folder, record_name)
            
            results.append({
                "image": image_path.name,
                "record": record_name,
                "status": "success",
                "shape": result["signals"].shape
            })
            
            print()
            
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
            results.append({
                "image": image_path.name,
                "status": "failed",
                "error": str(e)
            })
    
    # Save processing log
    log_path = Path(output_folder) / "processing_log.json"
    with open(log_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Summary
    successful = sum(1 for r in results if r["status"] == "success")
    print(f"\n{'='*60}")
    print(f"PROCESSING COMPLETE!")
    print(f"{'='*60}")
    print(f"Total images: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")
    print(f"Output folder: {output_folder}")
    print(f"Processing log: {log_path}")
    
    return results

print("✅ Competition helper functions defined!")


# ============ CELL 9: Create Submission ZIP ============

def create_submission_zip(
    output_folder: str,
    zip_filename: str = "submission.zip"
):
    """
    Create ZIP file for competition submission
    
    Args:
        output_folder: Folder with WFDB files
        zip_filename: Output ZIP filename
    """
    zip_path = Path(output_folder).parent / zip_filename
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        output_path = Path(output_folder)
        
        for file_path in output_path.rglob('*'):
            if file_path.is_file() and not file_path.name.endswith('.json'):
                # Add to ZIP with relative path
                arcname = file_path.relative_to(output_path.parent)
                zipf.write(file_path, arcname)
                print(f"Added: {arcname}")
    
    file_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"\n✅ Submission ZIP created: {zip_path}")
    print(f"   Size: {file_size_mb:.2f} MB")
    
    return str(zip_path)

print("✅ Submission ZIP helper defined!")


# ============ CELL 10: Run on Competition Data ============

# Set paths (adjust these to match your Kaggle environment)
INPUT_FOLDER = "/kaggle/input/physionet-ecg-image-digitization/test_images"
OUTPUT_FOLDER = "/kaggle/working/digitized_ecgs"
SAMPLING_RATE = 500  # Competition requirement

# Process all images
results = process_competition_dataset(
    input_folder=INPUT_FOLDER,
    output_folder=OUTPUT_FOLDER,
    sampling_rate=SAMPLING_RATE
)

# Create submission ZIP
submission_zip = create_submission_zip(
    output_folder=OUTPUT_FOLDER,
    zip_filename="mc_ai_ecg_submission.zip"
)

print("\n🏆 MC AI ECG Digitization Complete!")
print(f"📦 Submission file ready: {submission_zip}")
print("\nDownload the ZIP file and submit to the competition!")


# ============ CELL 11: Test on Sample Image (Optional) ============

# Test on a single image to verify
# Uncomment and modify path to test

"""
digitizer = ECGDigitizer(sampling_rate=500)

# Test image
test_image = "/kaggle/input/test-ecg-image.png"

result = digitizer.digitize_ecg_image(test_image)

# Plot results
plt.figure(figsize=(15, 8))
for i in range(min(3, result['num_leads'])):
    plt.subplot(3, 1, i+1)
    plt.plot(result['signals'][:, i])
    plt.title(f"Lead {result['lead_names'][i]}")
    plt.ylabel("Voltage (mV)")
    plt.grid(True)
plt.xlabel("Sample")
plt.tight_layout()
plt.show()

print(f"Signal shape: {result['signals'].shape}")
print(f"Sampling rate: {result['sampling_rate']} Hz")
print(f"Leads: {result['lead_names']}")
"""

print("✅ Notebook complete! Ready for competition submission!")
