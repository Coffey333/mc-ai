"""
MC AI - Real ECG Testing Script
Tests the ECG digitization system with real/sample images
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime

class RealECGTester:
    """Test MC AI's ECG system with real images"""
    
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.test_images_dir = Path("ecg_competition/test_images")
        self.output_dir = Path("ecg_competition/test_outputs")
        self.results = []
    
    def find_test_images(self):
        """Find all ECG images in test directory"""
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        images = []
        
        for ext in image_extensions:
            images.extend(self.test_images_dir.glob(f"*{ext}"))
        
        return images
    
    def test_single_ecg(self, image_path):
        """Test digitization on a single ECG image"""
        print(f"\n{'='*60}")
        print(f"📊 Testing: {image_path.name}")
        print('='*60)
        
        try:
            # Call the API
            with open(image_path, 'rb') as f:
                files = {'ecg_image': f}
                data = {'format': 'json'}
                
                response = requests.post(
                    f"{self.base_url}/api/ecg-digitize",
                    files=files,
                    data=data,
                    timeout=120
                )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ SUCCESS!")
                print(f"\nResults:")
                print(f"  Status: {result.get('status', 'unknown')}")
                
                # Check if we got signal data
                if 'signals' in result:
                    signals = result['signals']
                    print(f"  Leads detected: {len(signals)}")
                    for lead_name, signal in signals.items():
                        print(f"    {lead_name}: {len(signal)} samples")
                
                # Check processing info
                if 'processing_info' in result:
                    info = result['processing_info']
                    print(f"\n  Processing:")
                    print(f"    Duration: {info.get('processing_time', 'N/A')}s")
                    print(f"    Calibration: {info.get('calibration_method', 'N/A')}")
                
                # Save result
                output_file = self.output_dir / f"{image_path.stem}_result.json"
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"\n  Saved to: {output_file}")
                
                self.results.append({
                    'image': image_path.name,
                    'status': 'success',
                    'leads': len(signals) if 'signals' in result else 0,
                    'result': result
                })
                
                return True
                
            else:
                print(f"❌ FAILED: HTTP {response.status_code}")
                print(f"   Error: {response.text[:200]}")
                
                self.results.append({
                    'image': image_path.name,
                    'status': 'failed',
                    'error': response.text[:200]
                })
                
                return False
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            self.results.append({
                'image': image_path.name,
                'status': 'error',
                'error': str(e)
            })
            return False
    
    def test_api_health(self):
        """Check if API is running"""
        print("\n" + "="*60)
        print("🔍 Checking API Health")
        print("="*60)
        
        try:
            response = requests.get(f"{self.base_url}/api/ecg-digitize/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API is running!")
                print(f"   Status: {data.get('status', 'unknown')}")
                print(f"   Message: {data.get('message', 'N/A')}")
                return True
            else:
                print(f"⚠️ API returned: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API not reachable: {e}")
            print(f"   Make sure MC AI Server is running on port 5000")
            return False
    
    def create_synthetic_ecg(self):
        """Create a synthetic ECG image for testing"""
        print("\n" + "="*60)
        print("🎨 Creating Synthetic ECG for Testing")
        print("="*60)
        
        try:
            import numpy as np
            import cv2
            
            # Create a simple synthetic ECG image
            width, height = 2000, 1500
            img = np.ones((height, width, 3), dtype=np.uint8) * 255
            
            # Draw grid (5mm squares)
            grid_color = (220, 220, 220)
            for x in range(0, width, 20):  # 5mm at 100 DPI
                cv2.line(img, (x, 0), (x, height), grid_color, 1)
            for y in range(0, height, 20):
                cv2.line(img, (0, y), (width, y), grid_color, 1)
            
            # Draw a simple ECG waveform
            signal_color = (0, 0, 0)
            time_points = np.linspace(0, 10, 2000)  # 10 seconds
            
            # Simple QRS-like pattern
            ecg_signal = np.zeros_like(time_points)
            for i in range(len(time_points)):
                t = time_points[i]
                # Heart rate: ~60 BPM
                heart_beat = int(t)
                t_in_beat = t - heart_beat
                
                if 0.1 < t_in_beat < 0.15:  # Q wave
                    ecg_signal[i] = -0.2
                elif 0.15 < t_in_beat < 0.25:  # R wave
                    ecg_signal[i] = 1.5
                elif 0.25 < t_in_beat < 0.35:  # S wave
                    ecg_signal[i] = -0.3
                elif 0.5 < t_in_beat < 0.7:  # T wave
                    ecg_signal[i] = 0.5 * np.sin((t_in_beat - 0.5) * np.pi / 0.2)
            
            # Convert to pixels (1mV = 100 pixels)
            baseline_y = height // 2
            scale = 100
            
            for i in range(len(time_points) - 1):
                x1 = int((time_points[i] / 10) * width)
                x2 = int((time_points[i + 1] / 10) * width)
                y1 = int(baseline_y - ecg_signal[i] * scale)
                y2 = int(baseline_y - ecg_signal[i + 1] * scale)
                cv2.line(img, (x1, y1), (x2, y2), signal_color, 2)
            
            # Add labels
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, "Lead II", (50, 100), font, 1, (0, 0, 0), 2)
            cv2.putText(img, "25 mm/s, 10 mm/mV", (50, 150), font, 0.7, (0, 0, 0), 1)
            
            # Save
            output_path = self.test_images_dir / "synthetic_ecg.png"
            cv2.imwrite(str(output_path), img)
            
            print(f"✅ Created synthetic ECG: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"⚠️ Could not create synthetic ECG: {e}")
            return None
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        total = len(self.results)
        successful = sum(1 for r in self.results if r['status'] == 'success')
        failed = sum(1 for r in self.results if r['status'] == 'failed')
        errors = sum(1 for r in self.results if r['status'] == 'error')
        
        print(f"\nTotal images tested: {total}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Errors: {errors}")
        
        if successful > 0:
            success_rate = (successful / total) * 100
            print(f"\n🎯 Success Rate: {success_rate:.1f}%")
        
        if successful == total and total > 0:
            print("\n🏆 ALL TESTS PASSED! System ready for competition!")
        elif successful > 0:
            print("\n💡 System working but needs optimization")
        else:
            print("\n⚠️  System needs attention - no successful digitizations")
    
    def run_full_test(self):
        """Run complete testing suite"""
        print("="*60)
        print("🧪 MC AI - REAL ECG TESTING SUITE")
        print("="*60)
        
        # Step 1: Check API health
        if not self.test_api_health():
            print("\n❌ Cannot continue - API is not running")
            print("   Please start the MC AI Server first:")
            print("   (It should already be running)")
            return
        
        # Step 2: Find or create test images
        test_images = list(self.find_test_images())
        
        if not test_images:
            print("\n📝 No test images found, creating synthetic ECG...")
            synthetic_path = self.create_synthetic_ecg()
            if synthetic_path:
                test_images = [synthetic_path]
        
        if not test_images:
            print("\n⚠️ No test images available")
            print("   To test with real images:")
            print("   1. Download PhysioNet ECG images")
            print("   2. Place them in: ecg_competition/test_images/")
            print("   3. Run this script again")
            return
        
        print(f"\n📁 Found {len(test_images)} test image(s)")
        
        # Step 3: Test each image
        for image_path in test_images:
            self.test_single_ecg(image_path)
        
        # Step 4: Print summary
        self.print_summary()
        
        # Step 5: Next steps
        print("\n" + "="*60)
        print("🚀 NEXT STEPS")
        print("="*60)
        print("\n1. Review results in: ecg_competition/test_outputs/")
        print("2. Test web interface: http://localhost:5000/ecg-test")
        print("3. Download real PhysioNet images for validation")
        print("4. Benchmark against competition metrics (SNR, DTW, MSE)")
        print("5. Create final submission package")

def main():
    """Run real ECG testing"""
    tester = RealECGTester()
    tester.run_full_test()

if __name__ == "__main__":
    main()
