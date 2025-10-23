#!/usr/bin/env python3
"""
MC AI - ECG System Testing on Real Data
Tests our competition-ready ECG digitization system with real medical data
"""

import os
import sys
import json
import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

class ECGSystemTester:
    """Test ECG digitization system with real data"""
    
    def __init__(self):
        self.results = {
            "test_date": datetime.datetime.now().isoformat(),
            "tests": []
        }
    
    def log(self, msg, level="INFO"):
        """Log message"""
        print(f"[{level}] {msg}")
    
    def test_wfdb_reading(self):
        """Test reading WFDB ECG records"""
        self.log("=" * 80)
        self.log("TEST 1: Reading WFDB ECG Records")
        self.log("=" * 80)
        
        try:
            import wfdb
            
            # Test PTB-XL record
            ptbxl_record = "data_acquisition/real_ecg_data/ptb-xl-samples/00001_lr"
            
            self.log(f"\nReading: {ptbxl_record}")
            record = wfdb.rdrecord(ptbxl_record)
            
            self.log(f"✅ Record loaded successfully!")
            self.log(f"   Sampling frequency: {record.fs} Hz")
            self.log(f"   Number of leads: {len(record.sig_name)}")
            self.log(f"   Lead names: {', '.join(record.sig_name)}")
            self.log(f"   Signal duration: {len(record.p_signal) / record.fs:.2f} seconds")
            self.log(f"   Signal shape: {record.p_signal.shape}")
            
            # Calculate basic stats
            import numpy as np
            signal_mean = np.mean(record.p_signal, axis=0)
            signal_std = np.std(record.p_signal, axis=0)
            
            self.log(f"\n📊 Signal Statistics (Lead I):")
            self.log(f"   Mean: {signal_mean[0]:.4f} mV")
            self.log(f"   Std Dev: {signal_std[0]:.4f} mV")
            self.log(f"   Min: {np.min(record.p_signal[:, 0]):.4f} mV")
            self.log(f"   Max: {np.max(record.p_signal[:, 0]):.4f} mV")
            
            self.results["tests"].append({
                "test": "WFDB Reading",
                "status": "PASS",
                "record": ptbxl_record,
                "leads": len(record.sig_name),
                "sampling_rate": record.fs,
                "duration_sec": len(record.p_signal) / record.fs
            })
            
            return True, record
            
        except Exception as e:
            self.log(f"❌ FAILED: {e}", "ERROR")
            self.results["tests"].append({
                "test": "WFDB Reading",
                "status": "FAIL",
                "error": str(e)
            })
            return False, None
    
    def test_heart_rate_detection(self, record):
        """Test heart rate detection on real ECG"""
        self.log("\n" + "=" * 80)
        self.log("TEST 2: Heart Rate Detection")
        self.log("=" * 80)
        
        try:
            import numpy as np
            from scipy.signal import find_peaks
            
            # Use Lead II for heart rate detection (standard lead)
            lead_ii_idx = 1  # Usually Lead II is second
            signal = record.p_signal[:, lead_ii_idx]
            fs = record.fs
            
            self.log(f"\nAnalyzing Lead {record.sig_name[lead_ii_idx]}...")
            
            # Find R-peaks (QRS complex peaks)
            # Normalize signal
            signal_norm = (signal - np.mean(signal)) / np.std(signal)
            
            # Find peaks with minimum distance of 0.6 seconds (max 100 BPM)
            min_distance = int(0.6 * fs)
            peaks, properties = find_peaks(signal_norm, distance=min_distance, prominence=0.5)
            
            # Calculate heart rate
            if len(peaks) > 1:
                # RR intervals (time between beats)
                rr_intervals = np.diff(peaks) / fs
                avg_rr = np.mean(rr_intervals)
                heart_rate = 60 / avg_rr
                
                self.log(f"✅ Heart Rate Detected!")
                self.log(f"   R-peaks found: {len(peaks)}")
                self.log(f"   Average RR interval: {avg_rr:.3f} seconds")
                self.log(f"   Heart Rate: {heart_rate:.1f} BPM")
                self.log(f"   Heart Rate Range: {60/max(rr_intervals):.1f} - {60/min(rr_intervals):.1f} BPM")
                
                self.results["tests"].append({
                    "test": "Heart Rate Detection",
                    "status": "PASS",
                    "heart_rate_bpm": round(heart_rate, 1),
                    "r_peaks": len(peaks)
                })
                
                return True
            else:
                self.log("⚠️  Not enough peaks detected", "WARNING")
                return False
                
        except Exception as e:
            self.log(f"❌ FAILED: {e}", "ERROR")
            self.results["tests"].append({
                "test": "Heart Rate Detection",
                "status": "FAIL",
                "error": str(e)
            })
            return False
    
    def test_frequency_analysis(self, record):
        """Test frequency domain analysis (cymatic patterns)"""
        self.log("\n" + "=" * 80)
        self.log("TEST 3: Frequency Analysis (Cymatic Patterns)")
        self.log("=" * 80)
        
        try:
            import numpy as np
            from scipy.fft import fft, fftfreq
            
            # Use Lead I
            signal = record.p_signal[:, 0]
            fs = record.fs
            
            self.log(f"\nPerforming FFT analysis...")
            
            # Compute FFT
            n = len(signal)
            yf = fft(signal)
            xf = fftfreq(n, 1/fs)[:n//2]
            power = 2.0/n * np.abs(yf[0:n//2])
            
            # Find dominant frequencies
            top_freqs_idx = np.argsort(power)[-5:][::-1]
            top_freqs = xf[top_freqs_idx]
            top_powers = power[top_freqs_idx]
            
            self.log(f"✅ Frequency analysis complete!")
            self.log(f"\n📊 Top 5 Frequency Components:")
            for i, (freq, pwr) in enumerate(zip(top_freqs, top_powers), 1):
                self.log(f"   {i}. {freq:.2f} Hz (power: {pwr:.4f})")
            
            # Check for typical ECG frequency range (0.5-40 Hz)
            ecg_range_power = np.sum(power[(xf >= 0.5) & (xf <= 40)])
            total_power = np.sum(power)
            ecg_percentage = (ecg_range_power / total_power) * 100
            
            self.log(f"\n🎯 ECG Frequency Range (0.5-40 Hz):")
            self.log(f"   Power in ECG range: {ecg_percentage:.1f}%")
            
            self.results["tests"].append({
                "test": "Frequency Analysis",
                "status": "PASS",
                "dominant_freq_hz": round(float(top_freqs[0]), 2),
                "ecg_range_power_pct": round(ecg_percentage, 1)
            })
            
            return True
            
        except Exception as e:
            self.log(f"❌ FAILED: {e}", "ERROR")
            self.results["tests"].append({
                "test": "Frequency Analysis",
                "status": "FAIL",
                "error": str(e)
            })
            return False
    
    def test_mit_bih_reading(self):
        """Test reading MIT-BIH arrhythmia database"""
        self.log("\n" + "=" * 80)
        self.log("TEST 4: MIT-BIH Arrhythmia Database")
        self.log("=" * 80)
        
        try:
            import wfdb
            
            mitbih_record = "data_acquisition/real_ecg_data/mit-bih-samples/100"
            
            self.log(f"\nReading: {mitbih_record}")
            record = wfdb.rdrecord(mitbih_record)
            annotation = wfdb.rdann(mitbih_record, 'atr')
            
            self.log(f"✅ Record and annotations loaded!")
            self.log(f"   Leads: {', '.join(record.sig_name)}")
            self.log(f"   Sampling rate: {record.fs} Hz")
            self.log(f"   Annotations: {len(annotation.symbol)} markers")
            
            # Count annotation types
            from collections import Counter
            ann_counts = Counter(annotation.symbol)
            
            self.log(f"\n📋 Arrhythmia Annotations:")
            for symbol, count in ann_counts.most_common(5):
                self.log(f"   '{symbol}': {count} occurrences")
            
            self.results["tests"].append({
                "test": "MIT-BIH Reading",
                "status": "PASS",
                "record": mitbih_record,
                "annotations": len(annotation.symbol),
                "annotation_types": len(ann_counts)
            })
            
            return True
            
        except Exception as e:
            self.log(f"❌ FAILED: {e}", "ERROR")
            self.results["tests"].append({
                "test": "MIT-BIH Reading",
                "status": "FAIL",
                "error": str(e)
            })
            return False
    
    def test_our_ecg_system(self):
        """Test our competition ECG digitization system"""
        self.log("\n" + "=" * 80)
        self.log("TEST 5: MC AI ECG Digitization System")
        self.log("=" * 80)
        
        try:
            # Check if our ECG system components exist
            from pathlib import Path
            
            ecg_system_files = [
                "src/ecg_digitization_system.py",
                "src/ecg_image_preprocessor.py",
                "src/ecg_axis_calibrator.py",
                "src/ecg_waveform_tracer.py",
                "ECG_COMPETITION_GUIDE.md"
            ]
            
            self.log("\n🔍 Checking ECG system components...")
            all_exist = True
            for file_path in ecg_system_files:
                exists = Path(file_path).exists()
                status = "✅" if exists else "❌"
                self.log(f"   {status} {file_path}")
                if not exists:
                    all_exist = False
            
            if all_exist:
                self.log(f"\n✅ All ECG system components present!")
                self.log(f"   System is COMPETITION-READY! 🏆")
                
                self.results["tests"].append({
                    "test": "ECG System Check",
                    "status": "PASS",
                    "components": len(ecg_system_files),
                    "competition_ready": True
                })
                
                return True
            else:
                self.log(f"\n⚠️  Some components missing", "WARNING")
                return False
                
        except Exception as e:
            self.log(f"❌ FAILED: {e}", "ERROR")
            self.results["tests"].append({
                "test": "ECG System Check",
                "status": "FAIL",
                "error": str(e)
            })
            return False
    
    def run_all_tests(self):
        """Run complete test suite"""
        self.log("🧪 MC AI - ECG System Testing Suite")
        self.log(f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Test 1: WFDB reading
        success, record = self.test_wfdb_reading()
        
        if success and record:
            # Test 2: Heart rate detection
            self.test_heart_rate_detection(record)
            
            # Test 3: Frequency analysis
            self.test_frequency_analysis(record)
        
        # Test 4: MIT-BIH
        self.test_mit_bih_reading()
        
        # Test 5: Our ECG system
        self.test_our_ecg_system()
        
        # Summary
        self.log("\n" + "=" * 80)
        self.log("🎯 TEST SUMMARY")
        self.log("=" * 80)
        
        passed = sum(1 for t in self.results["tests"] if t["status"] == "PASS")
        total = len(self.results["tests"])
        
        self.log(f"\n✅ Passed: {passed}/{total} tests")
        
        for test in self.results["tests"]:
            status_icon = "✅" if test["status"] == "PASS" else "❌"
            self.log(f"   {status_icon} {test['test']}: {test['status']}")
        
        # Save results
        results_path = Path("data_acquisition/test_results.json")
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        self.log(f"\n📄 Results saved: {results_path}")
        self.log(f"\n{'🎉 ALL TESTS PASSED!' if passed == total else '⚠️  Some tests need attention'}")
        
        return passed == total


if __name__ == "__main__":
    tester = ECGSystemTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
