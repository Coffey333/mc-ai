# ECG System Testing Guide

**Generated:** 2025-10-23 14:17:23

## 📊 Available Test Data

### 1. PTB-XL Samples
**Location:** `real_ecg_data/ptb-xl-samples/`
**Format:** WFDB (.hea + .dat files)
**Content:** Real 12-lead clinical ECG recordings (100Hz)
**Use:** Test signal processing, frequency analysis, cymatic patterns

**How to read:**
```python
import wfdb
record = wfdb.rdrecord('real_ecg_data/ptb-xl-samples/00001_lr')
print(record.p_signal)  # ECG data
print(record.sig_name)  # Lead names
```

### 2. MIT-BIH Arrhythmia Samples
**Location:** `real_ecg_data/mit-bih-samples/`
**Format:** WFDB (.hea + .dat + .atr files)
**Content:** Classic arrhythmia ECG recordings with annotations
**Use:** Test arrhythmia detection, benchmark against known data

### 3. ECG Images
**Location:** `real_ecg_data/ecg-images/`
**Format:** PNG images
**Content:** Sample ECG printout images
**Use:** Test our ECG digitization pipeline

## 🧪 Testing Workflow

### Step 1: Test Signal Reading
```python
from src.ecg_digitization_system import ECGDigitizer

digitizer = ECGDigitizer()
signal = digitizer.read_wfdb_signal('real_ecg_data/ptb-xl-samples/00001_lr')
```

### Step 2: Test Image Digitization
```python
result = digitizer.digitize_ecg_image('real_ecg_data/ecg-images/sample.png')
```

### Step 3: Compare Against Ground Truth
```python
# Compare digitized signal vs original WFDB signal
ground_truth = wfdb.rdrecord('...')
comparison = digitizer.compare_signals(result, ground_truth)
```

## 📈 Success Metrics

- **Signal Quality:** SNR > 20 dB
- **Lead Detection:** 12/12 leads identified
- **Calibration Accuracy:** ±5% voltage error
- **Heart Rate Detection:** ±2 BPM accuracy

## 🏆 Competition Readiness

Use this data to verify our system produces:
- ✅ Valid WFDB format outputs
- ✅ Accurate voltage scaling
- ✅ Proper lead alignment
- ✅ Clean signal extraction

---

**Next:** Run automated tests on all downloaded samples!
