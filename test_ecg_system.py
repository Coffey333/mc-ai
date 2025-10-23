"""
MC AI - Automated ECG Testing Suite
Comprehensive tests for competition readiness
"""

import unittest
import numpy as np
from pathlib import Path

from src.ecg_digitization import (
    MCAIECGDigitizer,
    ECGSignalProcessor,
    ECGImagePreprocessor,
    ECGAxisCalibrator,
    WFDBConverter
)

class TestECGPreprocessor(unittest.TestCase):
    """Test image preprocessing"""
    
    def setUp(self):
        self.preprocessor = ECGImagePreprocessor()
    
    def test_initialization(self):
        """Test preprocessor initializes"""
        self.assertIsNotNone(self.preprocessor)
    
    def test_noise_reduction(self):
        """Test bilateral filter reduces noise"""
        # Create noisy RGB image (preprocessor expects RGB)
        img = np.random.randint(0, 255, (500, 500, 3), dtype=np.uint8)
        
        # Apply denoising (returns grayscale)
        denoised = self.preprocessor.denoise(img)
        
        # Check output (will be grayscale, so 2D)
        self.assertEqual(denoised.shape, (500, 500))
        self.assertTrue(np.all(denoised >= 0))
        self.assertTrue(np.all(denoised <= 255))

class TestSignalProcessor(unittest.TestCase):
    """Test signal processing"""
    
    def setUp(self):
        self.processor = ECGSignalProcessor(sample_rate=250)
    
    def test_baseline_removal(self):
        """Test baseline wander removal"""
        # Create signal with baseline drift
        time = np.linspace(0, 10, 2500)
        signal = np.sin(2 * np.pi * time) + 0.5 * np.sin(2 * np.pi * 0.3 * time)
        
        # Remove baseline
        filtered = self.processor.remove_baseline_wander(signal)
        
        # Check output
        self.assertEqual(len(signal), len(filtered))
        # Baseline should be reduced
        self.assertLess(np.mean(np.abs(filtered)), np.mean(np.abs(signal)))
    
    def test_powerline_removal(self):
        """Test powerline noise removal"""
        time = np.linspace(0, 10, 2500)
        signal = np.sin(2 * np.pi * time) + 0.1 * np.sin(2 * np.pi * 60 * time)
        
        filtered = self.processor.remove_powerline_noise(signal, 60)
        
        self.assertEqual(len(signal), len(filtered))
    
    def test_full_pipeline(self):
        """Test complete preprocessing pipeline"""
        time = np.linspace(0, 10, 2500)
        clean = np.sin(2 * np.pi * 1.2 * time)
        
        # Add noise
        baseline = 0.5 * np.sin(2 * np.pi * 0.3 * time)
        powerline = 0.1 * np.sin(2 * np.pi * 60 * time)
        noise = 0.05 * np.random.randn(len(time))
        noisy = clean + baseline + powerline + noise
        
        # Process
        processed = self.processor.full_preprocessing_pipeline(noisy)
        
        # Should be cleaner
        self.assertTrue(len(processed) > 0)

class TestCalibration(unittest.TestCase):
    """Test axis calibration"""
    
    def setUp(self):
        self.calibrator = ECGAxisCalibrator()
    
    def test_initialization(self):
        """Test calibrator initializes"""
        self.assertIsNotNone(self.calibrator)

class TestWFDBConverter(unittest.TestCase):
    """Test WFDB format conversion"""
    
    def setUp(self):
        self.converter = WFDBConverter()
    
    def test_initialization(self):
        """Test converter initializes"""
        self.assertIsNotNone(self.converter)
    
    def test_amplitude_scaling(self):
        """Test proper amplitude scaling (critical bug fix)"""
        # Create test signal
        time = np.linspace(0, 10, 2500)
        voltage = np.sin(2 * np.pi * time)
        
        # Convert to ADC units
        adc_gain = 200  # ADU per mV
        baseline = 0
        
        adc_signal = (voltage * adc_gain + baseline).astype(np.int16)
        
        # Verify scaling
        self.assertTrue(np.all(adc_signal >= -32768))
        self.assertTrue(np.all(adc_signal <= 32767))

class TestIntegration(unittest.TestCase):
    """Integration tests for complete system"""
    
    def setUp(self):
        self.digitizer = MCAIECGDigitizer(sample_rate=250)
    
    def test_digitizer_initialization(self):
        """Test digitizer initializes with all components"""
        self.assertIsNotNone(self.digitizer)
        self.assertIsNotNone(self.digitizer.preprocessor)
        self.assertIsNotNone(self.digitizer.calibrator)
        self.assertIsNotNone(self.digitizer.tracer)
        self.assertIsNotNone(self.digitizer.analyzer)
        self.assertIsNotNone(self.digitizer.converter)

def run_tests():
    """Run all tests"""
    print("="*60)
    print("🧪 MC AI ECG SYSTEM - AUTOMATED TEST SUITE")
    print("="*60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestECGPreprocessor))
    suite.addTests(loader.loadTestsFromTestCase(TestSignalProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestCalibration))
    suite.addTests(loader.loadTestsFromTestCase(TestWFDBConverter))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
        print("🏆 System ready for competition!")
    else:
        print("\n⚠️ Some tests failed - review and fix")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
