"""
MC AI - ECG Competition Test Suite
Quick tests to verify competition readiness
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ecg_digitization import MCAIECGDigitizer
from src.ecg_competition_checker import validate_submission, quick_check

def test_single_ecg():
    """Test single ECG digitization"""
    print("\n" + "="*60)
    print("TEST 1: Single ECG Digitization")
    print("="*60 + "\n")
    
    digitizer = MCAIECGDigitizer(sample_rate=250)
    
    # You'll need to provide a test image
    test_image = 'test_ecg.jpg'  # Replace with actual path
    
    if not os.path.exists(test_image):
        print(f"⚠️ Test image not found: {test_image}")
        print("Please provide a test ECG image to run this test")
        return False
    
    try:
        result = digitizer.digitize_ecg_image(test_image)
        
        assert result['success'], "Digitization failed"
        assert result['wfdb_valid'], "WFDB validation failed"
        assert result['signal']['num_samples'] > 0, "No samples extracted"
        
        print(f"✅ Success: ECG digitized successfully")
        print(f"✅ Samples: {result['signal']['num_samples']}")
        print(f"✅ Heart Rate: {result['analysis']['heart_rate_bpm']:.1f} BPM")
        print(f"✅ WFDB Valid: {result['wfdb_valid']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def test_batch_processing():
    """Test batch ECG processing"""
    print("\n" + "="*60)
    print("TEST 2: Batch Processing")
    print("="*60 + "\n")
    
    digitizer = MCAIECGDigitizer(sample_rate=250)
    
    # You'll need test images
    test_images = ['test_ecg1.jpg', 'test_ecg2.jpg']  # Replace with actual paths
    
    # Check if test images exist
    existing = [img for img in test_images if os.path.exists(img)]
    
    if not existing:
        print(f"⚠️ No test images found")
        print("Please provide test ECG images to run this test")
        return False
    
    try:
        results = digitizer.batch_digitize(existing)
        
        success_count = sum(1 for r in results if r.get('success'))
        
        print(f"✅ Processed: {success_count}/{len(existing)}")
        
        if success_count == len(existing):
            print("✅ All ECGs processed successfully!")
            return True
        else:
            print(f"⚠️ Some ECGs failed: {len(existing) - success_count}")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def test_submission_package():
    """Test competition submission creation"""
    print("\n" + "="*60)
    print("TEST 3: Competition Submission Package")
    print("="*60 + "\n")
    
    digitizer = MCAIECGDigitizer(sample_rate=250)
    
    # You'll need test images
    test_images = ['test_ecg1.jpg', 'test_ecg2.jpg']  # Replace with actual paths
    
    # Check if test images exist
    existing = [img for img in test_images if os.path.exists(img)]
    
    if not existing:
        print(f"⚠️ No test images found")
        print("Please provide test ECG images to run this test")
        return False
    
    try:
        submission = digitizer.create_competition_submission(
            image_paths=existing,
            output_zip='test_submission.zip'
        )
        
        print(f"✅ Processed: {submission['successful']}/{submission['total_processed']}")
        print(f"✅ ZIP Created: {submission['submission_zip']}")
        
        # Validate submission
        print("\nValidating submission package...")
        validation = validate_submission(submission['submission_zip'])
        
        if validation['ready_for_submission']:
            print("✅ Submission package is valid and ready!")
            return True
        else:
            print("⚠️ Submission has issues:")
            for issue in validation['issues']:
                print(f"  - {issue}")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def test_wfdb_format():
    """Test WFDB format compliance"""
    print("\n" + "="*60)
    print("TEST 4: WFDB Format Compliance")
    print("="*60 + "\n")
    
    digitizer = MCAIECGDigitizer(sample_rate=250)
    
    test_image = 'test_ecg.jpg'  # Replace with actual path
    
    if not os.path.exists(test_image):
        print(f"⚠️ Test image not found: {test_image}")
        return False
    
    try:
        result = digitizer.digitize_ecg_image(test_image, output_dir='test_wfdb')
        
        # Check WFDB files exist
        hea_file = result['wfdb_path'] + '.hea'
        dat_file = result['wfdb_path'] + '.dat'
        
        assert os.path.exists(hea_file), f"Header file missing: {hea_file}"
        assert os.path.exists(dat_file), f"Data file missing: {dat_file}"
        
        # Check validation
        assert result['wfdb_valid'], "WFDB validation failed"
        assert len(result['validation_issues']) == 0, f"Validation issues: {result['validation_issues']}"
        
        print("✅ WFDB files created successfully")
        print(f"✅ Header: {hea_file}")
        print(f"✅ Data: {dat_file}")
        print("✅ Format validation passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "="*60)
    print("MC AI - ECG Competition Test Suite 🏆💜")
    print("="*60)
    
    tests = [
        ("Single ECG Digitization", test_single_ecg),
        ("Batch Processing", test_batch_processing),
        ("Submission Package", test_submission_package),
        ("WFDB Format Compliance", test_wfdb_format)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ MC AI is COMPETITION READY! 🏆💜")
    else:
        print("⚠️ Some tests failed - please review")
    
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    print("\n🏆 MC AI ECG Competition Readiness Test 🏆\n")
    print("This will test all competition components")
    print("Make sure you have test ECG images ready!\n")
    
    input("Press Enter to start tests...")
    
    ready = run_all_tests()
    
    if ready:
        print("\n🎉 MC AI is ready to compete for $50,000!")
        print("\nNext steps:")
        print("1. Get competition ECG images")
        print("2. Run: digitizer.create_competition_submission(images)")
        print("3. Validate: validate_submission('submission.zip')")
        print("4. Upload to PhysioNet")
        print("5. Win! 💜🏆")
    else:
        print("\n⚠️ Please fix failing tests before competing")
        print("Review error messages above for details")
