"""
MC AI - ECG Digitizer Demo
Test the complete digitization pipeline with synthetic ECG
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from PIL import Image
import cv2

from src.ecg_digitization import MCAIECGDigitizer

def create_synthetic_ecg_image(output_path='test_ecg.png', duration=10, sample_rate=250):
    """
    Create a synthetic ECG image for testing
    MC AI creates his own test data! 🎨
    """
    print("MC AI: Creating synthetic ECG image... 🎨")
    
    # Generate synthetic ECG signal
    time = np.linspace(0, duration, duration * sample_rate)
    
    # Simple ECG simulation: P wave + QRS complex + T wave
    heart_rate = 72  # BPM
    beat_interval = 60.0 / heart_rate
    
    ecg_signal = np.zeros_like(time)
    
    for beat_time in np.arange(0, duration, beat_interval):
        # P wave (small)
        p_wave = 0.2 * np.exp(-((time - beat_time - 0.1)**2) / 0.001)
        
        # QRS complex (sharp, tall)
        qrs_wave = 2.0 * np.exp(-((time - beat_time - 0.2)**2) / 0.0005)
        
        # T wave (medium)
        t_wave = 0.5 * np.exp(-((time - beat_time - 0.35)**2) / 0.003)
        
        ecg_signal += p_wave + qrs_wave + t_wave
    
    # Create image with grid
    fig, ax = plt.subplots(figsize=(12, 4), dpi=100)
    
    # Plot ECG
    ax.plot(time, ecg_signal, 'k-', linewidth=1.5)
    
    # Add grid (like ECG paper)
    ax.grid(True, which='both', linestyle='-', linewidth=0.5, alpha=0.3)
    ax.set_xlim(0, duration)
    ax.set_ylim(-0.5, 3)
    
    # Labels
    ax.set_xlabel('Time (seconds)', fontsize=10)
    ax.set_ylabel('Voltage (mV)', fontsize=10)
    ax.set_title('Synthetic ECG - MC AI Test', fontsize=12)
    
    # Add scale annotation
    ax.text(0.5, 2.7, '25 mm/s, 10 mm/mV', fontsize=9, 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"MC AI: Synthetic ECG saved to {output_path} ✨")
    return output_path

def demo_complete_pipeline():
    """
    Demonstrate the complete ECG digitization pipeline
    """
    print("\n" + "="*70)
    print("MC AI - ECG Digitization System Demo")
    print("PhysioNet Competition Test Run 🏆💜")
    print("="*70 + "\n")
    
    # Step 1: Create synthetic ECG image
    print("Step 1: Creating test ECG image...")
    ecg_image_path = create_synthetic_ecg_image()
    
    # Step 2: Initialize digitizer
    print("\nStep 2: Initializing MC AI ECG Digitizer...")
    digitizer = MCAIECGDigitizer(sample_rate=250)
    
    # Step 3: Digitize the ECG
    print("\nStep 3: Running complete digitization pipeline...\n")
    
    try:
        result = digitizer.digitize_ecg_image(
            ecg_image_path,
            output_name='demo_ecg',
            output_dir='ecg_competition/demo_output'
        )
        
        if result and result['success']:
            print("\n" + "="*70)
            print("✨ DEMO SUCCESSFUL! ✨")
            print("="*70)
            print("\n📊 Results Summary:")
            print(f"   ✅ WFDB Valid: {result['wfdb_valid']}")
            print(f"   📏 Duration: {result['signal']['duration_s']:.2f} seconds")
            print(f"   📈 Samples: {result['signal']['num_samples']}")
            print(f"   📊 Amplitude: {result['signal']['amplitude_mV']:.2f} mV")
            
            if result['analysis']['heart_rate_bpm']:
                print(f"   💓 Heart Rate: {result['analysis']['heart_rate_bpm']:.1f} BPM")
                print(f"   💜 Emotional State: {result['analysis']['emotional_state']}")
            
            print(f"\n📝 Output Files:")
            print(f"   {result['wfdb_path']}.hea")
            print(f"   {result['wfdb_path']}.dat")
            
            if result['wfdb_valid']:
                print("\n🏆 MC AI is COMPETITION READY! 🏆")
            else:
                print(f"\n⚠️ Validation Issues: {result['validation_issues']}")
            
            print("="*70 + "\n")
            
        else:
            print("\n❌ Digitization failed!")
            if result:
                print(f"Issues: {result.get('validation_issues', 'Unknown error')}")
    
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_complete_pipeline()
