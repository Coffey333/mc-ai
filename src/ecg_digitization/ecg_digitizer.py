"""
MC AI - Complete ECG Digitizer
End-to-end pipeline: Image → Digital Signal → WFDB Format
Ready for competition! 🏆💜
"""

import numpy as np
import logging
from pathlib import Path

from .image_preprocessor import ECGImagePreprocessor
from .axis_calibrator import ECGAxisCalibrator
from .waveform_tracer import ECGWaveformTracer
from .ecg_analyzer import MCAIECGAnalyzer
from .wfdb_converter import WFDBConverter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MCAIECGDigitizer:
    """
    MC AI's Complete ECG Digitization System
    Image → Clean → Calibrate → Trace → Analyze → WFDB
    Competition-ready! 💜🏆
    """
    
    def __init__(self, sample_rate=250):
        self.sample_rate = sample_rate
        
        # Initialize all components
        self.preprocessor = ECGImagePreprocessor()
        self.calibrator = ECGAxisCalibrator()
        self.tracer = ECGWaveformTracer()
        self.analyzer = MCAIECGAnalyzer(sample_rate=sample_rate)
        self.converter = WFDBConverter()
        
        logger.info("=" * 60)
        logger.info("MC AI ECG Digitization System Initialized! 💜")
        logger.info("Ready to compete for $50,000! 🏆")
        logger.info("=" * 60)
    
    def digitize_ecg_image(self, image_path, output_name=None, output_dir='ecg_competition/digitized'):
        """
        Complete end-to-end ECG digitization
        
        Args:
            image_path: Path to ECG image file
            output_name: Name for output files (default: use input filename)
            output_dir: Directory for outputs
        
        Returns:
            dict with all results and file paths
        """
        logger.info("🎬 MC AI: Starting ECG digitization pipeline!")
        logger.info(f"📄 Input: {image_path}")
        
        # Step 1: Preprocess Image
        logger.info("\n📸 Step 1/6: Preprocessing image...")
        clean, binary, enhanced, denoised = self.preprocessor.preprocess_pipeline(
            image_path, 
            remove_grid=True
        )
        
        # Step 2: Calibrate Axes
        logger.info("\n📏 Step 2/6: Calibrating axes...")
        original = self.preprocessor.load_image(image_path)
        calibration = self.calibrator.full_calibration(original, binary)
        
        # Step 3: Trace Waveform
        logger.info("\n🎨 Step 3/6: Tracing waveform...")
        time, voltage = self.tracer.trace_waveform(
            clean,
            calibration,
            sample_rate=self.sample_rate,
            method='columnwise'
        )
        
        if time is None or voltage is None:
            logger.error("❌ Waveform extraction failed!")
            return None
        
        # Step 4: Analyze Signal
        logger.info("\n🔬 Step 4/6: Analyzing signal...")
        analysis = self.analyzer.comprehensive_analysis(time, voltage)
        
        # Step 5: Convert to WFDB
        logger.info("\n📝 Step 5/6: Converting to WFDB format...")
        
        if output_name is None:
            output_name = Path(image_path).stem
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        wfdb_path = self.converter.create_wfdb_record(
            time=time,
            voltage=voltage,
            record_name=output_name,
            output_dir=output_dir,
            sample_rate=self.sample_rate
        )
        
        # Step 6: Validate WFDB
        logger.info("\n✅ Step 6/6: Validating WFDB format...")
        is_valid, issues = self.converter.validate_wfdb_format(wfdb_path)
        
        # Prepare results
        results = {
            'success': True,
            'input_image': str(image_path),
            'output_name': output_name,
            'wfdb_path': wfdb_path,
            'wfdb_valid': is_valid,
            'validation_issues': issues,
            'signal': {
                'time': time,
                'voltage': voltage,
                'duration_s': time[-1],
                'num_samples': len(time),
                'sample_rate': self.sample_rate,
                'amplitude_mV': float(np.ptp(voltage))
            },
            'analysis': {
                'heart_rate_bpm': analysis.get('heart_rate_analysis', {}).get('heart_rate_bpm'),
                'hrv_ms': analysis.get('heart_rate_analysis', {}).get('hrv'),
                'emotional_state': analysis.get('emotional_resonance', {}).get('emotional_state'),
                'resonance_frequency': analysis.get('emotional_resonance', {}).get('resonance_frequency')
            },
            'calibration': calibration['final']
        }
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("✨ MC AI: Digitization Complete! ✨")
        logger.info("=" * 60)
        logger.info(f"📊 Signal: {len(time)} samples, {time[-1]:.1f}s duration")
        logger.info(f"📈 Amplitude: {np.ptp(voltage):.2f} mV")
        
        if results['analysis']['heart_rate_bpm']:
            logger.info(f"💓 Heart Rate: {results['analysis']['heart_rate_bpm']:.1f} BPM")
            logger.info(f"🧘 HRV: {results['analysis']['hrv_ms']:.1f} ms")
            logger.info(f"💜 Emotional State: {results['analysis']['emotional_state']}")
        
        logger.info(f"📝 WFDB Files: {wfdb_path}.hea, {wfdb_path}.dat")
        logger.info(f"✅ Competition Ready: {is_valid}")
        logger.info("=" * 60)
        
        return results
    
    def batch_digitize(self, image_paths, output_dir='ecg_competition/batch_digitized'):
        """
        Digitize multiple ECG images
        Perfect for competition submission!
        """
        logger.info(f"\n🎬 MC AI: Batch digitizing {len(image_paths)} ECGs...")
        
        results = []
        success_count = 0
        
        for i, image_path in enumerate(image_paths):
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing {i+1}/{len(image_paths)}: {image_path}")
            logger.info(f"{'='*60}")
            
            try:
                result = self.digitize_ecg_image(image_path, output_dir=output_dir)
                if result and result['success']:
                    results.append(result)
                    success_count += 1
            except Exception as e:
                logger.error(f"❌ Failed to process {image_path}: {e}")
                results.append({
                    'success': False,
                    'input_image': str(image_path),
                    'error': str(e)
                })
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✨ Batch Processing Complete!")
        logger.info(f"✅ Success: {success_count}/{len(image_paths)}")
        logger.info(f"{'='*60}")
        
        return results
    
    def create_competition_submission(self, image_paths, output_zip='mcai_ecg_submission.zip'):
        """
        Complete competition workflow:
        1. Digitize all images
        2. Convert to WFDB
        3. Package as ZIP
        4. Ready to submit!
        """
        logger.info("\n🏆 MC AI: Creating competition submission package! 🏆\n")
        
        # Digitize all images
        output_dir = 'ecg_competition/submission_batch'
        results = self.batch_digitize(image_paths, output_dir=output_dir)
        
        # Package into ZIP
        zip_path = self.converter.create_submission_package(output_dir, output_zip)
        
        logger.info("\n🎉 MC AI ready to compete for $50,000! 💜🏆")
        
        return {
            'results': results,
            'submission_zip': zip_path,
            'total_processed': len(results),
            'successful': sum(1 for r in results if r.get('success', False))
        }


# Example usage
if __name__ == "__main__":
    digitizer = MCAIECGDigitizer(sample_rate=250)
    
    print("\n" + "="*60)
    print("MC AI ECG Digitization System")
    print("Ready for PhysioNet Competition! 🏆💜")
    print("="*60)
    print("\nUsage:")
    print("  result = digitizer.digitize_ecg_image('path/to/ecg.jpg')")
    print("  submission = digitizer.create_competition_submission(['img1.jpg', 'img2.jpg'])")
    print("="*60 + "\n")
