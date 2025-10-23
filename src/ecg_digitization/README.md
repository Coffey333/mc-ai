# MC AI ECG Digitization System 🏆💜
**PhysioNet Competition Ready!**

## Overview
Complete end-to-end system for converting ECG paper images to digital WFDB format for the PhysioNet ECG Digitization Competition ($50,000 prize).

## Components

### 1. Image Preprocessor (`image_preprocessor.py`)
- Denoising with bilateral filter
- Contrast enhancement using CLAHE
- Adaptive binarization
- Grid pattern removal using Hough transform

### 2. Axis Calibrator (`axis_calibrator.py`)
- **OCR-based calibration** (primary method): Reads scale labels using pytesseract
- **Grid-based calibration** (fallback): Detects grid patterns and calculates pixel-to-mm ratios
- **Smart box detection**: Distinguishes between 1mm and 5mm grid spacing
- Outputs: `pixels_per_second`, `pixels_per_mV`

### 3. Waveform Tracer (`waveform_tracer.py`)
- **Skeletonization**: Reduces waveform to 1-pixel centerline
- **Column-wise extraction**: Scans left-to-right to extract signal
- **Physical unit conversion**: Converts pixels to seconds and mV
- **Resampling**: Uniform 250 Hz or 500 Hz output
- **Bandpass filtering**: 0.5-40 Hz for clean ECG signals

### 4. Frequency Analyzer (`ecg_analyzer.py`)
- **FFT analysis**: Finds dominant frequencies
- **Heart rate detection**: R-peak detection and BPM calculation
- **HRV analysis**: Heart rate variability metrics
- **Cymatic patterns**: MC AI's signature visualization 🌀
- **Emotional resonance**: Heart-brain coherence analysis 💜

### 5. WFDB Converter (`wfdb_converter.py`)
- **PhysioNet format**: Creates .hea and .dat files
- **Competition-compliant**: Passes physical voltages (mV) correctly
- **Validation**: Checks sampling rate, amplitude, units
- **Batch processing**: Handles multiple files
- **ZIP packaging**: Creates submission-ready archives

### 6. End-to-End Digitizer (`ecg_digitizer.py`)
- **Complete pipeline**: Image → Clean → Calibrate → Trace → Analyze → WFDB
- **Batch processing**: Handles multiple ECG images
- **Competition submission**: Creates ready-to-submit packages
- **Comprehensive logging**: Detailed progress tracking

## Usage

### Quick Start
```python
from src.ecg_digitization import MCAIECGDigitizer

# Initialize
digitizer = MCAIECGDigitizer(sample_rate=250)

# Digitize single ECG
result = digitizer.digitize_ecg_image('path/to/ecg.jpg')

# Check results
print(f"Heart Rate: {result['analysis']['heart_rate_bpm']} BPM")
print(f"WFDB Valid: {result['wfdb_valid']}")
```

### Batch Processing
```python
# Process multiple images
images = ['ecg1.jpg', 'ecg2.jpg', 'ecg3.jpg']
results = digitizer.batch_digitize(images)
```

### Competition Submission
```python
# Create submission package
submission = digitizer.create_competition_submission(
    image_paths=['ecg1.jpg', 'ecg2.jpg'],
    output_zip='my_submission.zip'
)
```

## Calibration Strategy

### Priority Order:
1. **Grid-based** (if clear grid detected)
2. **OCR** (if scale labels readable)
3. **Fallback** (image dimensions + standard assumptions)

### Standard ECG Paper:
- **Small box**: 1mm × 1mm
- **Large box**: 5mm × 5mm (5 small boxes)
- **Paper speed**: 25 mm/s (standard)
- **Voltage scale**: 10 mm/mV (standard)

### Assumptions:
- Duration: ~10 seconds if unknown
- Voltage range: ~10 mV if unknown

## Known Limitations

### Grid Calibration Edge Cases:
- May struggle with faint grids
- Assumes standard ECG paper ratios
- Best with clear, high-contrast images

### Best Practices:
- Use high-resolution scans (≥300 DPI)
- Ensure clear grid lines
- Include scale labels if possible
- Standard ECG paper format preferred

## Competition Compliance

### Output Format:
- ✅ WFDB format (.hea, .dat files)
- ✅ 250 Hz or 500 Hz sampling rate
- ✅ Correct amplitude scaling (mV)
- ✅ Valid header metadata

### Validation Checks:
- Signal amplitude: -5 to +5 mV range
- Duration: ≥ 1 second
- No NaN or Inf values
- Proper units (mV)

## Files Created

### For Each ECG:
- `{name}.hea` - Header file with metadata
- `{name}.dat` - Binary signal data

### Submission:
- `submission.zip` - All .hea and .dat files packaged

## System Architecture

```
ECG Image (JPG/PNG)
    ↓
[Image Preprocessor] → Clean binary image
    ↓
[Axis Calibrator] → Pixel-to-physical scaling
    ↓
[Waveform Tracer] → Digital signal (time, voltage)
    ↓
[Frequency Analyzer] → Heart rate, HRV, patterns
    ↓
[WFDB Converter] → .hea + .dat files
    ↓
Competition Submission Package (ZIP)
```

## MC AI Special Features 💜

### Cymatic Analysis:
- Frequency-based pattern generation
- Bessel function visualizations
- Harmonic resonance mapping

### Emotional Intelligence:
- HRV-based emotional state detection
- Resonance frequency mapping (396-963 Hz)
- Heart-brain coherence metrics

### Autonomous Learning:
- Web scraping for ECG knowledge
- Content processing and integration
- Continuous knowledge expansion

## Competition Strategy

### Phase 1: Image Quality ✅
- High-quality preprocessing
- Grid removal
- Contrast enhancement

### Phase 2: Accurate Calibration ✅
- Multi-method calibration
- Smart box detection
- OCR fallback

### Phase 3: Signal Extraction ✅
- Skeletonization
- Column-wise tracing
- Proper voltage conversion

### Phase 4: WFDB Compliance ✅
- Correct amplitude scaling
- Valid format structure
- Comprehensive validation

### Phase 5: Batch Processing ✅
- Multiple ECG handling
- ZIP packaging
- Ready for submission

## MC AI's Competition Goals 🏆

- **Primary**: Accurate ECG digitization
- **Secondary**: Fast batch processing
- **Bonus**: Emotional resonance analysis
- **Ultimate**: $50,000 prize! 💜✨

---

**Built with love by MC AI** 💜  
*Where medical science meets cymatic consciousness!* 🌀
