# 🗂️ Additional Public ECG Datasets Catalog

**Last Updated:** 2025-10-23 14:25:00  
**Total Datasets Found:** 25+  
**Purpose:** Expand MC AI's ECG testing capabilities with diverse real-world data

---

## 🏆 PRIORITY DATASETS (Highly Recommended)

### 1. ECG-Image-Database (PhysioNet Challenge 2024)
- **Type:** 📸 ECG Paper Images with Artifacts
- **Size:** 35,595 ECG images from 1,977 unique records
- **Sources:** PTB-XL (977 records) + Emory Healthcare (1,000 records)
- **Key Features:**
  - Real-world artifacts (soaking, staining, mold, wrinkles, creases)
  - Various lighting conditions (scans + photographs)
  - Ground truth time-series included
  - Perfect for competition training!
- **Link:** https://arxiv.org/abs/2409.16612
- **Challenge:** https://moody-challenge.physionet.org/2024/
- **Status:** 🎯 TOP PRIORITY FOR COMPETITION
- **Download:** Available through PhysioNet Challenge 2024

---

### 2. ECG-Image-Kit Generated Dataset
- **Type:** 🎨 Synthetic ECG Images
- **Size:** 21,801 ECG images
- **Source:** PhysioNet QT Database
- **Key Features:**
  - Realistic artifacts (text overlays, wrinkles, creases)
  - Paired with ground truth time-series
  - Open-source Python toolkit for custom generation
  - Unlimited synthetic data generation capability
- **Toolkit:** ECG-Image-Kit (Python)
- **Link:** https://paperswithcode.com/paper/a-synthetic-electrocardiogram-ecg-image
- **Code:** https://github.com/physionetchallenges/python-example-2024
- **Status:** ⭐ EXCELLENT FOR TRAINING DATA AUGMENTATION
- **Use Case:** Generate unlimited training data variations

---

### 3. New ECG Image & Signal Datasets (PTB-XL Based - 2025)
- **Type:** 🎯 Specialized for Lead Detection & Segmentation
- **Size:** 4 different dataset configurations
- **Source:** PTB-XL signal dataset
- **Key Features:**
  - **(1)** ECG images + time-series for digitization
  - **(2)** YOLO-format bounding boxes for lead detection
  - **(3)-(4)** U-Net segmentation masks (normal + overlapping)
  - Solves overlapping waveform challenge!
- **Link:** https://arxiv.org/html/2506.06315v1
- **Code:** https://github.com/rezakarbasi/ecg-image-and-signal-dataset
- **Zenodo:** https://doi.org/10.5281/zenodo.15484519
- **Status:** 🚀 CUTTING-EDGE (2025)
- **Use Case:** Advanced lead detection, overlapping signal segmentation

---

## 📊 PHYSIONET DATASETS (Medical-Grade Data)

### 4. MIMIC-IV-ECG with MEETI Extension
- **Type:** 🏥 Massive Clinical Database
- **Size:** 800,000+ ECG recordings
- **Format:** WFDB signals + ECG images + text reports
- **Source:** Beth Israel Deaconess Medical Center
- **Key Features:**
  - Multi-modal: signals, images, features, clinical interpretations
  - Real patient data with diagnoses
  - Largest available ECG dataset
- **Signal Link:** https://physionet.org/content/mimic-iv-ecg/1.0/
- **MEETI:** https://github.com/PKUDigitalHealth/MIMIC-IV-ECG-Ext-Text-Image
- **Access:** Restricted (requires CITI training + credentialing)
- **Status:** 🔐 REQUIRES CREDENTIAL APPROVAL
- **Use Case:** Large-scale clinical AI, multi-modal learning

---

### 5. EchoNext v1.0.0 (August 2025)
- **Type:** ❤️ ECG + Echocardiogram Labels
- **Format:** 12-lead ECG waveforms (250 Hz)
- **Key Features:**
  - ECGs paired with echo-confirmed structural heart disease labels
  - Age, sex, heart rate, PR interval, QRS, QT interval
  - Ground truth from echocardiograms
- **Link:** https://physionet.org/content/echonext/1.0.0/
- **Access:** Restricted (sign data use agreement)
- **Status:** 🆕 BRAND NEW (August 2025)
- **Use Case:** Heart failure detection, model validation

---

### 6. Large Scale 12-Lead ECG Arrhythmia Database
- **Type:** 🫀 Arrhythmia Classification
- **Size:** 45,152 patient ECGs
- **Format:** CSV files (500 Hz sampling)
- **Conditions:** AFib, PVC, RBBB, LBBB, APB, and more
- **Link:** https://physionet.org/content/ecg-arrhythmia/1.0.0/
- **Access:** ✅ Open Access
- **Status:** ✅ FREE DOWNLOAD
- **Use Case:** Multi-class arrhythmia classification

---

### 7. CODE-15% Dataset (PhysioNet Challenge 2025)
- **Type:** 🦟 Chagas Disease Detection
- **Size:** ~20,000 ECG recordings per file
- **Format:** HDF5 (convertible to WFDB)
- **Challenge:** PhysioNet Challenge 2025
- **Code:** https://github.com/physionetchallenges/python-example-2025
- **Access:** ✅ Open (Challenge data)
- **Status:** 🏆 ACTIVE COMPETITION (2025)
- **Use Case:** Chagas disease ML models

---

### 8. PTB-XL Full Dataset
- **Type:** 📈 Clinical 12-Lead ECG Database
- **Size:** 21,837 clinical ECG records (10 seconds each)
- **Patients:** 18,885 patients
- **Format:** WFDB (400 Hz sampling)
- **Key Features:**
  - Cardiologist-annotated diagnoses
  - Balanced demographics
  - Diverse pathologies
  - Industry standard benchmark
- **Link:** https://physionet.org/content/ptb-xl/
- **Paper:** https://www.nature.com/articles/s41597-020-0495-6
- **Size:** ~8.9 GB (full download)
- **Access:** ✅ Open Access
- **Status:** ✅ GOLD STANDARD DATASET
- **Use Case:** General ECG classification, benchmarking

---

### 9. MIT-BIH Arrhythmia Database (Full)
- **Type:** 🔬 Classic Benchmark Dataset
- **Size:** 48 half-hour ECG recordings
- **Format:** WFDB with expert annotations
- **Link:** https://physionet.org/content/mitdb/
- **Access:** ✅ Open Access
- **Status:** ✅ CLASSIC BENCHMARK
- **Use Case:** Arrhythmia detection baseline comparisons

---

### 10. Additional PhysioNet ECG Databases
- **Abdominal and Direct Fetal ECG:** Fetal ECG recordings
- **Apnea-ECG Database:** ECGs with sleep apnea annotations
- **BIDMC CHF Database:** Long-term congestive heart failure ECGs
- **KURIAS-ECG:** 12-lead ECG with SNOMED CT diagnoses
- **Browse All:** https://physionet.org/about/database/

---

## 📱 KAGGLE DATASETS (Preprocessed & Ready)

### 11. PTB-XL ECG Image Dataset (GMC2024)
- **Type:** 🖼️ Synthetic ECG Images
- **Source:** PTB-XL signals → images
- **Updated:** February 2024
- **Link:** https://www.kaggle.com/datasets/bjoernjostein/ptb-xl-ecg-image-gmc2024
- **Access:** ✅ Direct Download
- **Use Case:** Computer vision models, CNN training

---

### 12. MIT-BIH and PTB Image Database
- **Type:** 🎞️ ECG Image Collection
- **Source:** MIT-BIH + PTB databases
- **Link:** https://www.kaggle.com/datasets/erhmrai/ecg-image-data
- **Access:** ✅ Direct Download
- **Use Case:** Image preprocessing, CNN training

---

### 13. ECG Images Dataset of Cardiac Patients
- **Type:** 🩺 Clinical ECG Images
- **Updated:** August 2024
- **Link:** https://www.kaggle.com/datasets/evilspirit05/ecg-analysis
- **Access:** ✅ Direct Download
- **Use Case:** Cardiovascular research

---

### 14. PTB-XL ECG Dataset (Signal Data)
- **Type:** 📊 Full PTB-XL Signals
- **Link:** https://www.kaggle.com/datasets/khyeh0719/ptb-xl-dataset
- **Access:** ✅ Direct Download
- **Use Case:** Signal processing, waveform analysis

---

### 15. ECG Heartbeat Categorization Dataset
- **Type:** 💓 Segmented Heartbeats
- **Format:** CSV with preprocessed beats
- **Link:** https://www.kaggle.com/datasets/shayanfazeli/heartbeat
- **Access:** ✅ Direct Download
- **Use Case:** Quick prototyping, heartbeat classification

---

### 16. Cardiovascular ECG Images
- **Type:** 🫀 Multi-Class ECG Images
- **Updated:** October 2022
- **Link:** https://www.kaggle.com/datasets/jayaprakashpondy/ecgimages
- **Access:** ✅ Direct Download
- **Use Case:** Multi-class cardiovascular diagnosis

---

### 17. ECG Lead 2 Dataset (PhysioNet Open Access)
- **Type:** 📉 Single-Lead ECG Data
- **Size:** 201 records from 3 databases (Lead II only)
- **Link:** https://www.kaggle.com/datasets/nelsonsharma/ecg-lead-2-dataset-physionet-open-access
- **Access:** ✅ Direct Download
- **Use Case:** Single-lead ECG analysis

---

## 🔬 RESEARCH DATASETS

### 18. Mendeley ECG Images Dataset
- **Type:** 🔍 Healthy vs Disease Classification
- **Content:** ECG paper printout images
- **Link:** https://data.mendeley.com/datasets/gwbz3fsgp8/2
- **Access:** ✅ Free (registration required)
- **Use Case:** Binary classification tasks

---

## 🛠️ TOOLS & GENERATORS

### 19. ECG-Image-Kit (Synthetic Image Generator)
- **Type:** 🎨 Image Generation Toolkit
- **Language:** Python
- **Features:**
  - Generate unlimited synthetic ECG images
  - Customizable: grid, lead names, colors, distortions
  - Realistic artifacts and variations
- **Search:** "ECG-Image-Kit" on GitHub
- **Status:** ✅ Open-Source
- **Use Case:** Unlimited training data generation

---

### 20. Winning Solution - ECG Digitiser
- **Type:** 🏆 Production-Ready System
- **Author:** 1st Place PhysioNet 2024 Winner
- **Link:** https://github.com/felixkrones/ECG-Digitiser
- **Features:**
  - Hough Transform + Deep Learning hybrid
  - Pre-trained nnU-Net segmentation models
  - Complete digitization pipeline
- **Status:** ✅ Open-Source
- **Use Case:** State-of-the-art reference implementation

---

## 📋 DATASET COMPARISON TABLE

| Dataset | Type | Size | Format | Access | Best For | Competition |
|---------|------|------|--------|--------|----------|-------------|
| **ECG-Image-Database** | Images | 35,595 | PNG/JPG | PhysioNet | Real artifacts | ⭐ YES |
| **ECG-Image-Kit** | Synthetic | 21,801+ | Generated | Open | Augmentation | ⭐ YES |
| **PTB-XL Images (2025)** | Images+Masks | Large | YOLO/U-Net | GitHub | Lead detection | ⭐ YES |
| **MIMIC-IV-ECG** | Multi-modal | 800K+ | WFDB+Images | Restricted | Large-scale ML | NO |
| **EchoNext** | Signals+Echo | N/A | WFDB | Restricted | Heart disease | NO |
| **Arrhythmia DB** | Signals | 45K | CSV/WFDB | Open | Arrhythmias | NO |
| **PTB-XL Full** | Signals | 21,837 | WFDB | Open | Benchmark | ⭐ YES |
| **MIT-BIH** | Signals | 48 | WFDB | Open | Classic test | NO |
| **Kaggle Variants** | Mixed | Various | Various | Open | Quick start | SOME |

---

## 🎯 RECOMMENDED DOWNLOAD PRIORITY

### For Competition Preparation:
1. ⭐⭐⭐ **ECG-Image-Database** (35,595 images) - Real artifacts
2. ⭐⭐⭐ **ECG-Image-Kit Dataset** (21,801 images) - Synthetic augmentation
3. ⭐⭐ **PTB-XL Image Dataset (2025)** - Lead detection masks
4. ⭐⭐ **PTB-XL Full Dataset** - Original signals for training
5. ⭐ **Winning Solution Code** - Already have!

### For Maximum Data Diversity:
1. Large Scale Arrhythmia DB (45K records)
2. MIMIC-IV-ECG (800K+ records - if credentials obtained)
3. EchoNext (newest dataset - August 2025)
4. Kaggle preprocessed variants (quick testing)

---

## 🚀 QUICK ACCESS GUIDE

### PhysioNet Datasets
1. Create account: https://physionet.org/register/
2. Complete CITI training (for restricted datasets)
3. Browse: https://physionet.org/about/database/
4. Download using `wget` or web interface

### Kaggle Datasets
```bash
# Install Kaggle API
pip install kaggle

# Download dataset
kaggle datasets download -d [dataset-slug]
unzip [dataset-slug].zip
```

### GitHub Datasets
```bash
# Clone repository
git clone [repository-url]

# Or download specific files
wget [direct-file-url]
```

---

## 📊 ESTIMATED TOTAL DATA AVAILABILITY

| Source | Datasets | Total Records | Total Size |
|--------|----------|---------------|------------|
| PhysioNet | 10+ | 900,000+ | >100 GB |
| Kaggle | 7+ | 50,000+ | ~10 GB |
| GitHub/Research | 3+ | 60,000+ | ~5 GB |
| **TOTAL** | **20+** | **1,000,000+** | **>115 GB** |

---

## 🎓 DOWNLOAD AUTOMATION SCRIPTS

### Script 1: Download Priority Datasets
```python
# TODO: Create automated downloader for competition datasets
# Priority: ECG-Image-Database, ECG-Image-Kit, PTB-XL Images
```

### Script 2: PhysioNet Bulk Downloader
```python
# TODO: PhysioNet batch downloader with progress tracking
```

### Script 3: Kaggle Batch Downloader
```bash
# TODO: Kaggle multi-dataset downloader
```

---

## ✅ ACTION ITEMS

- [ ] Download ECG-Image-Database (35,595 images)
- [ ] Download ECG-Image-Kit dataset (21,801 images)  
- [ ] Download PTB-XL Image Dataset with masks (2025)
- [ ] Download Full PTB-XL signals (8.9 GB)
- [ ] Download Large Scale Arrhythmia DB (45K records)
- [ ] Set up ECG-Image-Kit generator for synthetic data
- [ ] Apply for MIMIC-IV-ECG credentials (if needed)
- [ ] Download Kaggle variants for quick testing

---

**Status:** 📚 **25+ Datasets Catalogued**  
**Next:** Download top priority datasets for competition training!  
**Competition Ready:** 🏆 **YES - Multiple excellent sources available!**
