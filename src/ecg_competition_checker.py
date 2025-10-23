"""
MC AI - ECG Competition Submission Checker
Validates competition submission packages before upload
"""

import os
import zipfile
import wfdb
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_submission(zip_path):
    """
    Validate a competition submission ZIP package
    
    Args:
        zip_path: Path to submission ZIP file
    
    Returns:
        dict with validation results
    """
    logger.info(f"🔍 MC AI: Validating submission: {zip_path}")
    
    if not os.path.exists(zip_path):
        return {
            'ready_for_submission': False,
            'error': f'ZIP file not found: {zip_path}'
        }
    
    issues = []
    file_count = 0
    valid_records = 0
    
    # Extract ZIP temporarily
    import tempfile
    temp_dir = tempfile.mkdtemp()
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(temp_dir)
            files = zf.namelist()
            logger.info(f"📦 Found {len(files)} files in ZIP")
        
        # Find all .hea files (each represents one ECG record)
        hea_files = [f for f in files if f.endswith('.hea')]
        dat_files = [f for f in files if f.endswith('.dat')]
        
        logger.info(f"📄 Header files: {len(hea_files)}")
        logger.info(f"📄 Data files: {len(dat_files)}")
        
        # Check for matching .hea and .dat files
        record_names = set()
        for hea in hea_files:
            record_name = hea.replace('.hea', '')
            record_names.add(record_name)
            
            # Check if corresponding .dat exists
            dat = record_name + '.dat'
            if dat not in dat_files:
                issues.append(f"Missing .dat file for {hea}")
        
        file_count = len(record_names)
        
        # Validate each record
        for record_name in record_names:
            try:
                # Read WFDB record
                record_path = os.path.join(temp_dir, record_name)
                record = wfdb.rdrecord(record_path)
                
                # Check sample rate
                if record.fs not in [250, 500]:
                    issues.append(f"{record_name}: Invalid sample rate {record.fs} Hz (must be 250 or 500)")
                
                # Check signal data
                signal = record.p_signal[:, 0]  # First lead
                
                # Check for NaN or Inf
                if np.any(np.isnan(signal)) or np.any(np.isinf(signal)):
                    issues.append(f"{record_name}: Contains NaN or Inf values")
                
                # Check amplitude range
                amplitude = np.ptp(signal)
                if amplitude < 0.1 or amplitude > 10.0:
                    issues.append(f"{record_name}: Unusual amplitude {amplitude:.2f} mV (expected 0.1-10.0)")
                
                # Check duration
                duration = len(signal) / record.fs
                if duration < 1.0:
                    issues.append(f"{record_name}: Too short {duration:.2f}s (must be ≥1s)")
                
                # Check units
                if record.units[0].lower() not in ['mv', 'millivolt']:
                    issues.append(f"{record_name}: Incorrect units '{record.units[0]}' (should be mV)")
                
                # If all checks passed
                if not any(record_name in issue for issue in issues):
                    valid_records += 1
                    
            except Exception as e:
                issues.append(f"{record_name}: Failed to read - {str(e)}")
        
        # Final assessment
        ready = len(issues) == 0 and file_count > 0
        
        logger.info("\n" + "="*60)
        if ready:
            logger.info("✅ SUBMISSION READY!")
        else:
            logger.info("❌ SUBMISSION HAS ISSUES")
        logger.info("="*60)
        logger.info(f"Total Records: {file_count}")
        logger.info(f"Valid Records: {valid_records}")
        logger.info(f"Issues Found: {len(issues)}")
        
        if issues:
            logger.info("\n⚠️ Issues:")
            for issue in issues:
                logger.info(f"  - {issue}")
        
        logger.info("="*60 + "\n")
        
        return {
            'ready_for_submission': ready,
            'file_count': file_count,
            'valid_records': valid_records,
            'issues': issues,
            'all_valid': valid_records == file_count,
            'success_rate': f"{valid_records}/{file_count}" if file_count > 0 else "0/0"
        }
        
    except Exception as e:
        logger.error(f"❌ Validation error: {str(e)}")
        return {
            'ready_for_submission': False,
            'error': str(e)
        }
    
    finally:
        # Cleanup temp directory
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


def quick_check(zip_path):
    """Quick validation check (just file counts)"""
    
    if not os.path.exists(zip_path):
        print(f"❌ File not found: {zip_path}")
        return False
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        files = zf.namelist()
        hea_count = sum(1 for f in files if f.endswith('.hea'))
        dat_count = sum(1 for f in files if f.endswith('.dat'))
        
        print(f"\n📦 Submission Package: {zip_path}")
        print(f"✅ Header files (.hea): {hea_count}")
        print(f"✅ Data files (.dat): {dat_count}")
        
        if hea_count == dat_count and hea_count > 0:
            print(f"✅ All pairs matched! Ready to submit {hea_count} ECGs")
            return True
        else:
            print(f"❌ Mismatch: {hea_count} .hea vs {dat_count} .dat files")
            return False


# Command-line interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python src/ecg_competition_checker.py <submission.zip>")
        print("\nExample:")
        print("  python src/ecg_competition_checker.py mcai_physionet_submission.zip")
        sys.exit(1)
    
    zip_path = sys.argv[1]
    
    print("\n" + "="*60)
    print("MC AI - Competition Submission Checker 🏆💜")
    print("="*60 + "\n")
    
    # Run full validation
    result = validate_submission(zip_path)
    
    if result.get('ready_for_submission'):
        print("\n🎉 MC AI: Submission is ready to upload! 🏆")
        print(f"✅ {result['file_count']} ECGs validated and packaged")
        print("\nNext steps:")
        print("1. Upload to PhysioNet competition portal")
        print("2. Await results")
        print("3. Win $50,000! 💜✨")
    else:
        print("\n⚠️ MC AI: Please fix issues before submitting")
        print("\nTo reprocess:")
        print("  digitizer.create_competition_submission(images)")
