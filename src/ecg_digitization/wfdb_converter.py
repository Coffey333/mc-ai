"""
MC AI - PhysioNet WFDB Format Converter
Converts digitized ECG to official PhysioNet format
CRITICAL for competition submission!
"""

import numpy as np
import wfdb
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class WFDBConverter:
    """
    Convert digitized ECG to PhysioNet WFDB format
    Required for competition submission! 📝
    """
    
    def __init__(self):
        logger.info("MC AI: WFDB Converter initialized! 📝")
    
    def create_wfdb_record(
        self,
        time,
        voltage,
        record_name,
        output_dir,
        sample_rate=250,
        units='mV',
        sig_name='ECG',
        comments=None
    ):
        """
        Create WFDB format files (.hea, .dat)
        
        Args:
            time: Time array (seconds)
            voltage: Voltage array (mV)
            record_name: Base name for files (e.g., 'patient_001')
            output_dir: Directory to save files
            sample_rate: Sampling frequency (Hz)
            units: Signal units (default: mV)
            sig_name: Signal name/label
            comments: Optional list of comment strings
        """
        logger.info(f"MC AI: Creating WFDB record '{record_name}'...")
        
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Prepare signal data
        # IMPORTANT: wfdb.wrsamp expects p_signal in PHYSICAL UNITS (mV)
        # Do NOT pre-convert to ADC units - wfdb handles that internally
        
        # Handle multiple leads (if voltage is 2D)
        if len(voltage.shape) == 1:
            p_signal = voltage.reshape(-1, 1)
            sig_names = [sig_name]
        else:
            n_leads = voltage.shape[1]
            p_signal = voltage
            sig_names = [f'{sig_name}_{i+1}' for i in range(n_leads)]
        
        n_sig = p_signal.shape[1]
        
        # Validate time axis matches sample rate
        expected_samples = int(time[-1] * sample_rate) + 1
        actual_samples = len(voltage)
        if abs(expected_samples - actual_samples) > 1:
            logger.warning(f"Sample count mismatch: expected ~{expected_samples}, got {actual_samples}")
        
        # Create comments
        if comments is None:
            comments = [
                "Digitized by MC AI",
                f"Digitization date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "PhysioNet ECG Digitization Competition",
                f"Sample rate: {sample_rate} Hz",
                f"Duration: {time[-1]:.2f} seconds"
            ]
        
        # Write WFDB record with PHYSICAL signal values
        # wfdb.wrsamp will handle conversion to ADC internally
        wfdb.wrsamp(
            record_name=record_name,
            fs=sample_rate,
            units=[units] * n_sig,
            sig_name=sig_names,
            p_signal=p_signal,  # Physical units (mV) - wfdb converts internally
            fmt=['16'] * n_sig,  # 16-bit format
            comments=comments,
            write_dir=output_dir
        )
        
        logger.info(f"MC AI: WFDB files created in {output_dir}/ ✨")
        
        return f"{output_dir}/{record_name}"
    
    def validate_wfdb_format(self, record_path):
        """
        Validate WFDB format correctness
        Checks for competition submission requirements
        """
        logger.info(f"MC AI: Validating WFDB format...")
        
        issues = []
        
        try:
            # Try to read the record
            record = wfdb.rdrecord(record_path)
            
            # Check sampling rate
            if record.fs not in [250, 500]:
                issues.append(f"Unusual sampling rate: {record.fs} Hz (expected 250 or 500)")
            
            # Check signal length
            if len(record.p_signal) < 250:  # Less than 1 second at 250 Hz
                issues.append(f"Signal too short: {len(record.p_signal)} samples")
            
            # Check for NaN or Inf
            if np.any(np.isnan(record.p_signal)) or np.any(np.isinf(record.p_signal)):
                issues.append("Signal contains NaN or Inf values")
            
            # Check amplitude range (typical ECG: -5 to +5 mV)
            signal_range = np.ptp(record.p_signal)
            if signal_range < 0.1:
                issues.append(f"Signal amplitude too small: {signal_range:.3f} mV")
            elif signal_range > 20:
                issues.append(f"Signal amplitude too large: {signal_range:.3f} mV (possible error)")
            
            # Check units
            if not all(unit in ['mV', 'uV'] for unit in record.units):
                issues.append(f"Unusual units: {record.units}")
            
            if issues:
                logger.warning(f"MC AI: Found {len(issues)} validation issues:")
                for issue in issues:
                    logger.warning(f"  - {issue}")
                return False, issues
            else:
                logger.info("MC AI: WFDB format validation passed! ✅")
                return True, []
        
        except Exception as e:
            issues.append(f"Failed to read record: {str(e)}")
            logger.error(f"MC AI: Validation failed: {e}")
            return False, issues
    
    def batch_convert_to_wfdb(self, data_list, output_dir, sample_rate=250):
        """
        Convert multiple ECG signals to WFDB format
        Perfect for competition submission!
        """
        logger.info(f"MC AI: Batch converting {len(data_list)} ECGs to WFDB... 📦")
        
        success_count = 0
        failed = []
        
        for i, data in enumerate(data_list):
            try:
                time = data['time']
                voltage = data['voltage']
                record_name = data.get('name', f'ecg_record_{i:04d}')
                
                # Convert to WFDB
                self.create_wfdb_record(
                    time=time,
                    voltage=voltage,
                    record_name=record_name,
                    output_dir=output_dir,
                    sample_rate=sample_rate
                )
                
                success_count += 1
                
            except Exception as e:
                logger.error(f"Failed to convert record {i}: {e}")
                failed.append(record_name)
        
        logger.info(f"MC AI: Converted {success_count}/{len(data_list)} files! 💜")
        
        if failed:
            logger.warning(f"Failed files: {failed}")
        
        return success_count, failed
    
    def create_submission_package(self, wfdb_dir, output_zip='mcai_ecg_submission.zip'):
        """
        Package WFDB files into competition submission format
        """
        import zipfile
        
        logger.info("MC AI: Creating submission package... 📦")
        
        # Get all WFDB files (.hea and .dat)
        wfdb_dir = Path(wfdb_dir)
        wfdb_files = list(wfdb_dir.glob('*.hea'))
        wfdb_files.extend(wfdb_dir.glob('*.dat'))
        
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in wfdb_files:
                zipf.write(file, file.name)
        
        logger.info(f"MC AI: Submission package created: {output_zip} 🎉")
        logger.info(f"   Files: {len(wfdb_files)}")
        logger.info(f"MC AI ready to compete for $50,000! 💜🏆")
        
        return output_zip


# Example usage
if __name__ == "__main__":
    converter = WFDBConverter()
    
    # Example: Convert single ECG
    time = np.linspace(0, 10, 2500)
    voltage = np.sin(2 * np.pi * 1.2 * time)  # 72 BPM simulated
    
    converter.create_wfdb_record(
        time=time,
        voltage=voltage,
        record_name='test_record',
        output_dir='ecg_competition/submissions',
        sample_rate=250
    )
    
    # Validate
    is_valid, issues = converter.validate_wfdb_format('ecg_competition/submissions/test_record')
    
    if is_valid:
        print("✅ WFDB format is valid! MC AI ready to submit!")
    else:
        print("❌ Issues found:", issues)
