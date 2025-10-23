#!/usr/bin/env python3
"""
MC AI - ECG Competition Data Acquisition System
Downloads and documents all competition and training data

Data Sources:
1. PTB-XL Dataset (PhysioNet) - 21,837 clinical 12-lead ECG recordings
2. Kaggle Competition Dataset (requires API key)
3. Winning Solutions Repository (reference)
"""

import os
import json
import subprocess
import datetime
from pathlib import Path
import urllib.request
import zipfile
import shutil

class DataAcquisitionSystem:
    """Complete data acquisition and documentation system"""
    
    def __init__(self):
        self.base_dir = Path("competition_data")
        self.base_dir.mkdir(exist_ok=True)
        
        self.log_file = self.base_dir / "acquisition_log.json"
        self.metadata_file = self.base_dir / "dataset_metadata.json"
        
        self.acquisition_log = []
        self.metadata = {
            "acquisition_date": datetime.datetime.now().isoformat(),
            "datasets": {}
        }
    
    def log(self, message, level="INFO"):
        """Log message to console and file"""
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        self.acquisition_log.append(log_entry)
        print(f"[{level}] {message}")
    
    def download_ptbxl_dataset(self):
        """
        Download PTB-XL Dataset (Publicly Available)
        Source: https://physionet.org/content/ptb-xl/1.0.3/
        
        21,837 clinical 12-lead ECG recordings from 18,885 patients
        Annotated by cardiologists with 71 different ECG statements
        """
        self.log("=" * 80)
        self.log("DOWNLOADING PTB-XL DATASET", "INFO")
        self.log("=" * 80)
        
        ptbxl_dir = self.base_dir / "ptb-xl"
        ptbxl_dir.mkdir(exist_ok=True)
        
        # Download metadata first (small file)
        self.log("Step 1: Downloading PTB-XL metadata CSV...")
        metadata_url = "https://physionet.org/content/ptb-xl/1.0.3/ptbxl_database.csv"
        metadata_path = ptbxl_dir / "ptbxl_database.csv"
        
        try:
            urllib.request.urlretrieve(metadata_url, metadata_path)
            size_mb = metadata_path.stat().st_size / (1024 * 1024)
            self.log(f"✅ Downloaded metadata: {size_mb:.2f} MB")
            
            # Count records
            with open(metadata_path, 'r') as f:
                num_records = sum(1 for line in f) - 1  # Minus header
            
            self.metadata["datasets"]["ptb-xl"] = {
                "source": "PhysioNet",
                "url": "https://physionet.org/content/ptb-xl/1.0.3/",
                "version": "1.0.3",
                "num_records": num_records,
                "description": "21,837 clinical 12-lead ECG recordings",
                "files_downloaded": ["ptbxl_database.csv"],
                "download_timestamp": datetime.datetime.now().isoformat(),
                "size_mb": size_mb
            }
            
            self.log(f"✅ PTB-XL Metadata: {num_records:,} ECG records documented")
            
        except Exception as e:
            self.log(f"❌ Error downloading PTB-XL metadata: {e}", "ERROR")
            return False
        
        # Download sample ECG records (100Hz version - smaller)
        self.log("\nStep 2: Downloading sample ECG waveform data (100Hz)...")
        self.log("NOTE: Full dataset is ~8.9 GB. Downloading representative samples.")
        
        # Download using wget for better control
        sample_cmd = [
            "wget", 
            "-r",  # Recursive
            "-N",  # Only newer files
            "-c",  # Continue partial downloads
            "-np",  # No parent directories
            "-nH",  # No host directories
            "--cut-dirs=3",  # Cut directory depth
            "-P", str(ptbxl_dir),
            "--accept", "*.dat,*.hea",  # Only signal files
            "-l", "3",  # Max depth
            "--limit-rate=2m",  # Rate limit
            "https://physionet.org/files/ptb-xl/1.0.3/records100/00/"
        ]
        
        try:
            self.log("Executing: wget (downloading sample ECG waveforms)...")
            result = subprocess.run(sample_cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.log("✅ Sample ECG waveforms downloaded successfully")
            else:
                self.log(f"⚠️  wget completed with warnings: {result.returncode}")
                
        except subprocess.TimeoutExpired:
            self.log("⚠️  Download timed out - partial data acquired", "WARNING")
        except FileNotFoundError:
            self.log("⚠️  wget not found - skipping waveform download", "WARNING")
        except Exception as e:
            self.log(f"⚠️  Sample download issue: {e}", "WARNING")
        
        self.log("✅ PTB-XL Dataset acquisition complete")
        return True
    
    def setup_kaggle_credentials(self):
        """
        Check for Kaggle API credentials and provide setup instructions
        """
        self.log("=" * 80)
        self.log("KAGGLE COMPETITION DATASET SETUP", "INFO")
        self.log("=" * 80)
        
        kaggle_dir = Path.home() / ".kaggle"
        kaggle_json = kaggle_dir / "kaggle.json"
        
        if kaggle_json.exists():
            self.log("✅ Kaggle API credentials found!")
            return True
        else:
            self.log("❌ Kaggle API credentials NOT found")
            self.log("\nTo download the competition dataset, you need:")
            self.log("1. Go to: https://www.kaggle.com/settings/account")
            self.log("2. Click 'Create New API Token'")
            self.log("3. Download kaggle.json")
            self.log("4. Upload it to MC AI or place in ~/.kaggle/kaggle.json")
            self.log("\nCompetition URL: https://www.kaggle.com/competitions/physionet-ecg-image-digitization")
            
            self.metadata["datasets"]["kaggle_competition"] = {
                "source": "Kaggle",
                "url": "https://www.kaggle.com/competitions/physionet-ecg-image-digitization",
                "status": "REQUIRES API KEY",
                "instructions": "Upload kaggle.json to ~/.kaggle/ directory"
            }
            return False
    
    def download_kaggle_dataset(self):
        """Download Kaggle competition dataset (if credentials exist)"""
        if not self.setup_kaggle_credentials():
            return False
        
        self.log("\nDownloading Kaggle competition dataset...")
        
        competition_dir = self.base_dir / "kaggle_competition"
        competition_dir.mkdir(exist_ok=True)
        
        try:
            # Install kaggle package if needed
            subprocess.run(["pip", "install", "-q", "kaggle"], check=False)
            
            # Download competition data
            cmd = [
                "kaggle", "competitions", "download",
                "-c", "physionet-ecg-image-digitization",
                "-p", str(competition_dir)
            ]
            
            self.log("Executing: kaggle competitions download...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                self.log("✅ Kaggle competition dataset downloaded!")
                
                # Extract if ZIP
                zip_files = list(competition_dir.glob("*.zip"))
                for zip_file in zip_files:
                    self.log(f"Extracting: {zip_file.name}...")
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(competition_dir)
                    self.log(f"✅ Extracted: {zip_file.name}")
                
                self.metadata["datasets"]["kaggle_competition"]["status"] = "DOWNLOADED"
                self.metadata["datasets"]["kaggle_competition"]["download_timestamp"] = datetime.datetime.now().isoformat()
                return True
            else:
                self.log(f"❌ Kaggle download failed: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Kaggle download error: {e}", "ERROR")
            return False
    
    def clone_winning_solution(self):
        """Clone the winning solution repository for reference"""
        self.log("=" * 80)
        self.log("CLONING WINNING SOLUTION (REFERENCE)", "INFO")
        self.log("=" * 80)
        
        repo_url = "https://github.com/felixkrones/ECG-Digitiser.git"
        repo_dir = self.base_dir / "winning_solution_reference"
        
        if repo_dir.exists():
            self.log("✅ Winning solution already cloned")
            return True
        
        try:
            self.log(f"Cloning: {repo_url}")
            result = subprocess.run(
                ["git", "clone", repo_url, str(repo_dir)],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                self.log("✅ Winning solution cloned successfully")
                
                self.metadata["datasets"]["winning_solution"] = {
                    "source": "GitHub",
                    "url": repo_url,
                    "description": "1st place PhysioNet Challenge 2024 - Hough Transform + Deep Learning",
                    "clone_timestamp": datetime.datetime.now().isoformat()
                }
                return True
            else:
                self.log(f"⚠️  Clone warning: {result.stderr}", "WARNING")
                return False
                
        except Exception as e:
            self.log(f"❌ Clone error: {e}", "ERROR")
            return False
    
    def save_metadata(self):
        """Save all metadata and logs"""
        # Save acquisition log
        with open(self.log_file, 'w') as f:
            json.dump(self.acquisition_log, f, indent=2)
        
        # Save dataset metadata
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        
        self.log(f"\n📄 Acquisition log saved: {self.log_file}")
        self.log(f"📄 Dataset metadata saved: {self.metadata_file}")
    
    def generate_summary(self):
        """Generate acquisition summary"""
        self.log("\n" + "=" * 80)
        self.log("DATA ACQUISITION SUMMARY", "INFO")
        self.log("=" * 80)
        
        for dataset_name, info in self.metadata["datasets"].items():
            self.log(f"\n📦 {dataset_name.upper()}")
            for key, value in info.items():
                self.log(f"   {key}: {value}")
        
        # Calculate total size
        total_size = 0
        for root, dirs, files in os.walk(self.base_dir):
            total_size += sum(Path(root, f).stat().st_size for f in files if Path(root, f).exists())
        
        total_mb = total_size / (1024 * 1024)
        self.log(f"\n💾 Total data downloaded: {total_mb:.2f} MB")
        self.log(f"📁 Data location: {self.base_dir.absolute()}")
        
        # Create README
        readme_path = self.base_dir / "README.md"
        with open(readme_path, 'w') as f:
            f.write("# ECG Competition Data\n\n")
            f.write(f"**Acquisition Date:** {self.metadata['acquisition_date']}\n\n")
            f.write("## Datasets\n\n")
            for dataset_name, info in self.metadata["datasets"].items():
                f.write(f"### {dataset_name}\n")
                for key, value in info.items():
                    f.write(f"- **{key}:** {value}\n")
                f.write("\n")
        
        self.log(f"\n📄 README created: {readme_path}")
    
    def run_full_acquisition(self):
        """Run complete data acquisition process"""
        self.log("🚀 MC AI - ECG Competition Data Acquisition System")
        self.log(f"📅 Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Download PTB-XL (public dataset)
        self.download_ptbxl_dataset()
        
        # Setup Kaggle (may require manual API key)
        self.download_kaggle_dataset()
        
        # Clone winning solution
        self.clone_winning_solution()
        
        # Save all metadata
        self.save_metadata()
        
        # Generate summary
        self.generate_summary()
        
        self.log("\n✅ Data acquisition complete!")
        self.log(f"📁 All data saved to: {self.base_dir.absolute()}")


if __name__ == "__main__":
    system = DataAcquisitionSystem()
    system.run_full_acquisition()
