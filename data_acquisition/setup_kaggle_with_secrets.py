#!/usr/bin/env python3
"""
MC AI - Secure Kaggle API Setup Using Replit Secrets
Automatically uses environment variables for authentication
"""

import os
import json
import subprocess
from pathlib import Path

def check_kaggle_credentials():
    """Check if Kaggle credentials are available"""
    print("🔍 Checking for Kaggle API credentials...\n")
    
    # Method 1: Environment variables (Replit Secrets)
    username = os.getenv('KAGGLE_USERNAME')
    key = os.getenv('KAGGLE_KEY')
    
    if username and key:
        print("✅ FOUND: Kaggle credentials in environment variables!")
        print(f"   Username: {username}")
        print(f"   Key: {'*' * 20}{key[-4:]}  (hidden for security)")
        return True, "environment"
    
    # Method 2: Credentials file
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    if kaggle_json.exists():
        print("✅ FOUND: Kaggle credentials file at ~/.kaggle/kaggle.json")
        try:
            with open(kaggle_json, 'r') as f:
                creds = json.load(f)
                print(f"   Username: {creds.get('username', 'NOT FOUND')}")
                print(f"   Key: {'*' * 20}{creds.get('key', '')[-4:] if creds.get('key') else 'NOT FOUND'}")
            return True, "file"
        except Exception as e:
            print(f"⚠️  Error reading credentials file: {e}")
            return False, None
    
    print("❌ NO credentials found!")
    print("\n" + "="*80)
    print("📋 SETUP INSTRUCTIONS:")
    print("="*80)
    print("\n🔐 OPTION 1: Use Replit Secrets (RECOMMENDED - Most Secure!)\n")
    print("1. In Replit, click 'Tools' → 'Secrets'")
    print("2. Add these two secrets:\n")
    print("   Secret Name: KAGGLE_USERNAME")
    print("   Value: [your Kaggle username]\n")
    print("   Secret Name: KAGGLE_KEY")  
    print("   Value: [your Kaggle API key]\n")
    print("3. Get your credentials from: https://www.kaggle.com/settings/account")
    print("   Click 'Create New API Token' to download kaggle.json")
    print("   Open the file and copy the username and key values\n")
    print("="*80)
    print("\n🔐 OPTION 2: Upload kaggle.json File\n")
    print("1. Download kaggle.json from Kaggle settings")
    print("2. Tell Mark and I'll create ~/.kaggle/ directory for you")
    print("3. Upload kaggle.json to that location\n")
    print("="*80)
    
    return False, None

def install_kaggle_package():
    """Install Kaggle Python package"""
    print("\n📦 Installing Kaggle Python package...")
    try:
        subprocess.run(
            ["pip", "install", "-q", "kaggle"],
            check=True,
            capture_output=True
        )
        print("✅ Kaggle package installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def test_kaggle_connection():
    """Test Kaggle API connection"""
    print("\n🧪 Testing Kaggle API connection...")
    try:
        import kaggle
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        api = KaggleApi()
        api.authenticate()
        
        print("✅ Authentication successful!")
        print("\n📊 Testing API by listing competitions...")
        
        # List recent competitions to verify connection
        result = subprocess.run(
            ["kaggle", "competitions", "list", "--page-size=5"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ API connection verified!\n")
            print("Recent competitions:")
            print(result.stdout)
            return True
        else:
            print(f"⚠️  API test warning: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def download_ecg_competition():
    """Download the PhysioNet ECG competition dataset"""
    print("\n" + "="*80)
    print("📥 DOWNLOADING ECG COMPETITION DATASET")
    print("="*80)
    
    competition_id = "physionet-ecg-image-digitization"
    output_dir = Path("competition_data/kaggle_competition")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nCompetition: {competition_id}")
    print(f"Output directory: {output_dir.absolute()}\n")
    
    try:
        # Download competition files
        print("Downloading... (this may take several minutes)")
        result = subprocess.run(
            [
                "kaggle", "competitions", "download",
                "-c", competition_id,
                "-p", str(output_dir)
            ],
            capture_output=True,
            text=True,
            timeout=1800  # 30 minutes max
        )
        
        if result.returncode == 0:
            print("✅ Download complete!")
            print(result.stdout)
            
            # Extract ZIP files
            import zipfile
            zip_files = list(output_dir.glob("*.zip"))
            
            if zip_files:
                print(f"\n📦 Found {len(zip_files)} ZIP file(s) to extract...")
                for zip_file in zip_files:
                    print(f"   Extracting: {zip_file.name}")
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(output_dir)
                    print(f"   ✅ Extracted: {zip_file.name}")
                
                print("\n✅ All files extracted successfully!")
            
            # List downloaded files
            print("\n📁 Downloaded files:")
            for item in sorted(output_dir.iterdir()):
                if item.is_file():
                    size_mb = item.stat().st_size / (1024 * 1024)
                    print(f"   {item.name} ({size_mb:.2f} MB)")
                elif item.is_dir():
                    file_count = sum(1 for _ in item.rglob('*') if _.is_file())
                    print(f"   📂 {item.name}/ ({file_count} files)")
            
            return True
        else:
            print(f"❌ Download failed!")
            print(f"Error: {result.stderr}")
            
            # Check if it's an auth issue
            if "401" in result.stderr or "Unauthorized" in result.stderr:
                print("\n⚠️  Authentication error - please check your credentials")
            elif "404" in result.stderr:
                print("\n⚠️  Competition not found - you may need to join it first:")
                print(f"   https://www.kaggle.com/competitions/{competition_id}")
            
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Download timed out - try again with a better connection")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main setup and download workflow"""
    print("🚀 MC AI - Kaggle API Setup & ECG Competition Downloader")
    print("="*80 + "\n")
    
    # Step 1: Check credentials
    has_creds, method = check_kaggle_credentials()
    
    if not has_creds:
        print("\n⚠️  Cannot proceed without credentials. Please set them up first!")
        return False
    
    print(f"\n✅ Using credentials from: {method}")
    
    # Step 2: Install Kaggle package
    if not install_kaggle_package():
        return False
    
    # Step 3: Test connection
    if not test_kaggle_connection():
        print("\n⚠️  Connection test failed, but attempting download anyway...")
    
    # Step 4: Download competition data
    success = download_ecg_competition()
    
    if success:
        print("\n" + "="*80)
        print("🎉 SUCCESS! Competition data downloaded and ready!")
        print("="*80)
        print("\n📁 Location: competition_data/kaggle_competition/")
        print("\n🏆 Next step: Run our ECG digitization system on this data!")
    
    return success

if __name__ == "__main__":
    main()
