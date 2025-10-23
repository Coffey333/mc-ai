#!/usr/bin/env python3
"""
MC AI - Real ECG Data Downloader
Downloads actual medical ECG data from verified public sources for testing

Data Sources:
1. PTB-XL (PhysioNet) - 21,837 clinical 12-lead ECG recordings
2. MIT-BIH Arrhythmia Database - Classic ECG benchmark dataset
3. ECG-Image-Database - Real ECG images for digitization testing
"""

import os
import subprocess
import json
import datetime
from pathlib import Path
import urllib.request
import tarfile
import zipfile

class RealECGDataDownloader:
    """Download real ECG datasets for testing"""
    
    def __init__(self):
        self.base_dir = Path("real_ecg_data")
        self.base_dir.mkdir(exist_ok=True)
        self.log = []
        
    def log_message(self, msg, level="INFO"):
        """Log with timestamp"""
        timestamp = datetime.datetime.now().isoformat()
        entry = {"timestamp": timestamp, "level": level, "message": msg}
        self.log.append(entry)
        print(f"[{level}] {msg}")
    
    def download_ptbxl_samples(self):
        """Download PTB-XL sample ECG waveforms"""
        self.log_message("=" * 80)
        self.log_message("DOWNLOADING PTB-XL REAL ECG WAVEFORMS")
        self.log_message("=" * 80)
        
        ptbxl_dir = self.base_dir / "ptb-xl-samples"
        ptbxl_dir.mkdir(exist_ok=True)
        
        # Download sample records (folder 00 - about 100 records)
        self.log_message("Downloading PTB-XL sample records (100Hz)...")
        
        base_url = "https://physionet.org/files/ptb-xl/1.0.3/records100/00000/"
        
        # Download a few sample records
        sample_records = [
            "00001_lr",  # Record 1
            "00002_lr",  # Record 2
            "00003_lr",  # Record 3
            "00004_lr",  # Record 4
            "00005_lr",  # Record 5
        ]
        
        downloaded = 0
        for record in sample_records:
            try:
                # Download .hea (header) file
                hea_url = f"{base_url}{record}.hea"
                hea_path = ptbxl_dir / f"{record}.hea"
                
                # Download .dat (data) file
                dat_url = f"{base_url}{record}.dat"
                dat_path = ptbxl_dir / f"{record}.dat"
                
                self.log_message(f"  Downloading {record}...")
                urllib.request.urlretrieve(hea_url, hea_path)
                urllib.request.urlretrieve(dat_url, dat_path)
                
                downloaded += 1
                self.log_message(f"  ✅ {record} downloaded")
                
            except Exception as e:
                self.log_message(f"  ⚠️  {record} failed: {e}", "WARNING")
        
        self.log_message(f"\n✅ Downloaded {downloaded} real ECG records from PTB-XL")
        return downloaded > 0
    
    def download_mitbih_samples(self):
        """Download MIT-BIH Arrhythmia Database samples"""
        self.log_message("\n" + "=" * 80)
        self.log_message("DOWNLOADING MIT-BIH ARRHYTHMIA DATABASE")
        self.log_message("=" * 80)
        
        mitbih_dir = self.base_dir / "mit-bih-samples"
        mitbih_dir.mkdir(exist_ok=True)
        
        # MIT-BIH Arrhythmia Database URL
        base_url = "https://physionet.org/files/mitdb/1.0.0/"
        
        # Download a few classic records
        sample_records = [
            "100",  # Normal sinus rhythm
            "101",  # Normal
            "102",  # Normal
            "103",  # Normal
            "104",  # Normal
        ]
        
        downloaded = 0
        for record in sample_records:
            try:
                # Download .hea, .dat, and .atr files
                for ext in ['.hea', '.dat', '.atr']:
                    url = f"{base_url}{record}{ext}"
                    path = mitbih_dir / f"{record}{ext}"
                    
                    self.log_message(f"  Downloading {record}{ext}...")
                    urllib.request.urlretrieve(url, path)
                
                downloaded += 1
                self.log_message(f"  ✅ Record {record} complete")
                
            except Exception as e:
                self.log_message(f"  ⚠️  Record {record} failed: {e}", "WARNING")
        
        self.log_message(f"\n✅ Downloaded {downloaded} MIT-BIH ECG records")
        return downloaded > 0
    
    def download_ecg_image_samples(self):
        """Download sample ECG images for digitization testing"""
        self.log_message("\n" + "=" * 80)
        self.log_message("DOWNLOADING ECG IMAGE SAMPLES FOR TESTING")
        self.log_message("=" * 80)
        
        images_dir = self.base_dir / "ecg-images"
        images_dir.mkdir(exist_ok=True)
        
        # PhysioNet Challenge sample images (if available)
        self.log_message("Looking for publicly available ECG image samples...")
        
        # Try downloading from the winning solution's test images
        test_image_url = "https://raw.githubusercontent.com/felixkrones/ECG-Digitiser/main/figures/segmentation.png"
        
        try:
            image_path = images_dir / "sample_ecg_segmentation.png"
            urllib.request.urlretrieve(test_image_url, image_path)
            self.log_message(f"✅ Downloaded sample ECG image: {image_path.name}")
            return True
        except Exception as e:
            self.log_message(f"⚠️  Could not download sample image: {e}", "WARNING")
            return False
    
    def scan_existing_data(self):
        """Scan and document what data we have"""
        self.log_message("\n" + "=" * 80)
        self.log_message("SCANNING EXISTING DATA")
        self.log_message("=" * 80)
        
        inventory = {
            "scan_date": datetime.datetime.now().isoformat(),
            "datasets": {}
        }
        
        # Check competition_data directory
        comp_data = Path("competition_data")
        if comp_data.exists():
            ptbxl_csv = comp_data / "ptb-xl" / "ptbxl_database.csv"
            if ptbxl_csv.exists():
                size_mb = ptbxl_csv.stat().st_size / (1024 * 1024)
                with open(ptbxl_csv, 'r') as f:
                    num_lines = sum(1 for _ in f) - 1
                
                inventory["datasets"]["ptb-xl-metadata"] = {
                    "file": str(ptbxl_csv),
                    "records": num_lines,
                    "size_mb": round(size_mb, 2)
                }
                self.log_message(f"✅ Found PTB-XL metadata: {num_lines:,} records")
        
        # Check real_ecg_data directory
        if self.base_dir.exists():
            for dataset_dir in self.base_dir.iterdir():
                if dataset_dir.is_dir():
                    file_count = sum(1 for _ in dataset_dir.rglob('*') if _.is_file())
                    total_size = sum(f.stat().st_size for f in dataset_dir.rglob('*') if f.is_file())
                    size_mb = total_size / (1024 * 1024)
                    
                    inventory["datasets"][dataset_dir.name] = {
                        "directory": str(dataset_dir),
                        "files": file_count,
                        "size_mb": round(size_mb, 2)
                    }
                    self.log_message(f"✅ Found {dataset_dir.name}: {file_count} files ({size_mb:.2f} MB)")
        
        # Save inventory
        inventory_path = self.base_dir / "data_inventory.json"
        with open(inventory_path, 'w') as f:
            json.dump(inventory, f, indent=2)
        
        self.log_message(f"\n📄 Data inventory saved: {inventory_path}")
        return inventory
    
    def create_testing_guide(self):
        """Create guide for testing ECG system with downloaded data"""
        guide_path = self.base_dir / "TESTING_GUIDE.md"
        
        content = f"""# ECG System Testing Guide

**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

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
"""
        
        with open(guide_path, 'w') as f:
            f.write(content)
        
        self.log_message(f"\n📘 Testing guide created: {guide_path}")
    
    def run_full_download(self):
        """Execute complete download workflow"""
        self.log_message("🚀 MC AI - Real ECG Data Download System")
        self.log_message(f"📅 Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Download datasets
        ptbxl_ok = self.download_ptbxl_samples()
        mitbih_ok = self.download_mitbih_samples()
        images_ok = self.download_ecg_image_samples()
        
        # Scan existing data
        inventory = self.scan_existing_data()
        
        # Create testing guide
        self.create_testing_guide()
        
        # Save log
        log_path = self.base_dir / "download_log.json"
        with open(log_path, 'w') as f:
            json.dump(self.log, f, indent=2)
        
        # Summary
        self.log_message("\n" + "=" * 80)
        self.log_message("✅ DOWNLOAD COMPLETE!")
        self.log_message("=" * 80)
        self.log_message(f"\n📁 Data location: {self.base_dir.absolute()}")
        self.log_message(f"📄 Download log: {log_path}")
        self.log_message(f"📊 Data inventory: {self.base_dir / 'data_inventory.json'}")
        self.log_message(f"📘 Testing guide: {self.base_dir / 'TESTING_GUIDE.md'}")
        
        total_datasets = sum([ptbxl_ok, mitbih_ok, images_ok])
        self.log_message(f"\n🎯 Successfully downloaded {total_datasets}/3 datasets")
        self.log_message("\n🧪 Ready to test ECG digitization system with REAL data!")


if __name__ == "__main__":
    downloader = RealECGDataDownloader()
    downloader.run_full_download()
