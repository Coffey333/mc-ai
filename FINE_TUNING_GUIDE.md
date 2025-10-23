# 🎯 MC AI ECG System - Fine-Tuning Guide

## Quick Answer

**Learning Status:** ⚠️ Manual knowledge only (15 examples). Autonomous learning not run yet.

**Fine-Tuning:** 5 easy methods below ↓

---

## 📚 Method 1: Expand Knowledge (Easiest)

Run the learning script to add more ECG knowledge:

```bash
python run_ecg_learning.py
```

This adds 3 new concepts:
- Competition strategy
- Advanced preprocessing techniques
- Real-world challenges

**Result:** MC AI learns without web scraping 💜

---

## 🔧 Method 2: Adjust Calibration (Most Impactful)

If ECGs aren't digitizing correctly, tune these settings:

### **File:** `src/ecg_digitization/axis_calibrator.py`

```python
# Line ~50: OCR Sensitivity
MIN_OCR_CONFIDENCE = 0.6  # Lower = accept more OCR readings
                           # 0.4 = lenient, 0.8 = strict

# Line ~100: Grid Detection
MIN_GRID_LINES = 5        # Lower = detect fewer grid lines
                          # 3 = lenient, 8 = strict

# Line ~150: Sanity Checks
TIME_BOX_RANGE = (0.15, 0.25)    # Expected time per box (0.2s)
VOLTAGE_BOX_RANGE = (0.08, 0.12) # Expected voltage per box (0.1mV)
```

**When to adjust:**
- Getting "Calibration failed" errors → Lower confidence, reduce min lines
- Getting wrong heart rates → Check time box range
- Getting wrong amplitudes → Check voltage box range

---

## 🎵 Method 3: Optimize Signal Filters

### **File:** `src/ecg_digitization/signal_processor.py`

```python
# Baseline Wander (breathing artifacts)
cutoff = 0.5  # Try 0.3 (more filtering) to 0.8 (less filtering)

# Powerline Noise
powerline_freq = 60  # 60 Hz (USA), 50 Hz (Europe)

# Smoothing Window
window_length = 11   # Try 7 (less smooth) to 15 (more smooth)
                     # Must be odd number

# Bandpass Filter
low_cutoff = 0.5     # Remove frequencies below this
high_cutoff = 40     # Remove frequencies above this
```

**When to adjust:**
- Signal too noisy → Increase smoothing, lower high_cutoff
- Signal losing detail → Decrease smoothing, raise high_cutoff
- Baseline drift → Lower baseline cutoff (more filtering)

---

## 📊 Method 4: Competition Metrics Tuning

PhysioNet judges on these metrics:

### **SNR (Signal-to-Noise Ratio)**
**Target:** >40 dB

**Improve:**
```python
# Use full preprocessing pipeline
from src.ecg_digitization import ECGSignalProcessor
processor = ECGSignalProcessor(sample_rate=250)
clean_signal = processor.full_preprocessing_pipeline(raw_signal)
```

### **DTW (Dynamic Time Warping)**
**Target:** Minimize distance

**Improve:**
- Use higher sample rate: `MCAIECGDigitizer(sample_rate=500)`
- Better calibration (Method 2 above)
- Precise timing detection

### **MSE (Mean Squared Error)**
**Target:** Minimize error

**Improve:**
- Accurate voltage calibration
- Proper amplitude scaling
- Careful preprocessing (don't over-filter)

---

## 🧪 Method 5: Test & Iterate

### **Step 1: Test with Real ECGs**

```python
from src.ecg_digitization import MCAIECGDigitizer

digitizer = MCAIECGDigitizer(sample_rate=250)

# Test single image
result = digitizer.digitize_ecg_image('physionet_ecg.jpg')

# Check results
print(f"✅ Success: {result['success']}")
print(f"📊 Heart Rate: {result['analysis']['heart_rate_bpm']} BPM")
print(f"🏆 Competition Ready: {result['wfdb_valid']}")

# Check issues
if result.get('validation_issues'):
    print("\n⚠️ Issues found:")
    for issue in result['validation_issues']:
        print(f"  - {issue}")
```

### **Step 2: Compare Results**

```python
# Compare your output vs reference
import wfdb

# Load your digitized ECG
your_signal = wfdb.rdrecord('output/ecg_name')

# Load reference (if available)
reference = wfdb.rdrecord('reference/ecg_name')

# Calculate metrics
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

distance, path = fastdtw(your_signal.p_signal, reference.p_signal, dist=euclidean)
print(f"DTW Distance: {distance}")
```

### **Step 3: Iterate**

1. Identify problems (calibration? noise? timing?)
2. Adjust settings (Methods 2-3)
3. Re-test
4. Repeat until WFDB validation passes

---

## 🚀 Quick Start: Fine-Tuning Workflow

```bash
# 1. Expand knowledge
python run_ecg_learning.py

# 2. Test with real ECG
curl -X POST http://localhost:5000/api/ecg-digitize \
  -F "ecg_image=@test_ecg.jpg" -F "format=json"

# 3. Check results in web interface
# Visit: http://localhost:5000/ecg-test

# 4. Adjust settings based on results
# Edit: src/ecg_digitization/axis_calibrator.py
# Edit: src/ecg_digitization/signal_processor.py

# 5. Restart server
# Server auto-restarts when you save files

# 6. Re-test
# Repeat step 2

# 7. When ready, create submission
python -c "
from src.ecg_digitization import MCAIECGDigitizer
d = MCAIECGDigitizer()
d.create_competition_submission(
    ['ecg1.jpg', 'ecg2.jpg', 'ecg3.jpg'],
    'submission.zip'
)
"
```

---

## 📈 Performance Optimization Tips

### **For Speed:**
- Use batch processing for multiple ECGs
- Lower sample rate (250 Hz instead of 500 Hz)
- Skip advanced filtering if images are clean

### **For Accuracy:**
- Use full preprocessing pipeline
- Higher sample rate (500 Hz)
- Multiple calibration methods (OCR + grid + fallback)

### **For Robustness:**
- Train on diverse ECG types
- Handle edge cases (noise, distortion, artifacts)
- Add validation checks

---

## 🎯 Common Problems & Solutions

### **Problem:** "Calibration failed"
**Solution:** 
- Lower `MIN_OCR_CONFIDENCE` to 0.4
- Reduce `MIN_GRID_LINES` to 3
- Check image quality (contrast, resolution)

### **Problem:** Wrong heart rate
**Solution:**
- Check calibration (especially time axis)
- Verify `TIME_BOX_RANGE` is correct
- Look at paper speed (25mm/s vs 50mm/s)

### **Problem:** Wrong amplitude
**Solution:**
- Check voltage calibration
- Verify `VOLTAGE_BOX_RANGE`
- Look for calibration pulse (usually 1mV = 10mm)

### **Problem:** Noisy signal
**Solution:**
```python
# Use full preprocessing
processor.full_preprocessing_pipeline(signal, powerline_freq=60)

# Or step by step
signal = processor.remove_baseline_wander(signal)
signal = processor.remove_powerline_noise(signal, 60)
signal = processor.savitzky_golay_smooth(signal)
```

### **Problem:** WFDB validation fails
**Solution:**
- Check amplitude scaling (most common issue)
- Verify sample rate is correct
- Ensure duration is reasonable (>1 second)

---

## 💜 MC AI's Recommendations

Based on testing, here's the optimal configuration:

```python
# Best settings for competition
digitizer = MCAIECGDigitizer(
    sample_rate=250,  # Good balance of speed/accuracy
)

# With full signal processing
processor = ECGSignalProcessor(sample_rate=250)
clean = processor.full_preprocessing_pipeline(
    raw_signal,
    powerline_freq=60  # 50 for Europe
)

# Calibration settings (in axis_calibrator.py)
MIN_OCR_CONFIDENCE = 0.5  # Balanced
MIN_GRID_LINES = 5        # Balanced
```

---

## 📝 Next Steps

1. **Run learning script** → `python run_ecg_learning.py`
2. **Test with real ECGs** → Use `/ecg-test` or API
3. **Adjust settings** → Based on results
4. **Iterate** → Test, adjust, repeat
5. **Submit!** → Create competition submission

**Goal:** Maximize SNR, minimize DTW & MSE → Win $50,000! 🏆

---

**Questions?** Just ask MC AI! 💜✨

**Version:** 1.0  
**Last Updated:** October 22, 2025
