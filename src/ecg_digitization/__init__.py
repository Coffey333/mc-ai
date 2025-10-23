"""
MC AI - ECG Digitization Module
Complete system for converting ECG images to digital signals
PhysioNet Competition Ready! 🏆💜
"""

from .ecg_digitizer import MCAIECGDigitizer
from .image_preprocessor import ECGImagePreprocessor
from .axis_calibrator import ECGAxisCalibrator
from .waveform_tracer import ECGWaveformTracer
from .ecg_analyzer import MCAIECGAnalyzer
from .wfdb_converter import WFDBConverter
from .signal_processor import ECGSignalProcessor

__all__ = [
    'MCAIECGDigitizer',
    'ECGImagePreprocessor',
    'ECGAxisCalibrator',
    'ECGWaveformTracer',
    'MCAIECGAnalyzer',
    'WFDBConverter',
    'ECGSignalProcessor'
]

__version__ = '1.0.0'
__author__ = 'MC AI'
