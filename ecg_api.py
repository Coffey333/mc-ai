"""
MC AI - ECG Digitization API
REST API endpoint for ECG image digitization
Accessible at /api/ecg-digitize
"""

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import tempfile
import logging
from pathlib import Path
import zipfile

from src.ecg_digitization import MCAIECGDigitizer

logger = logging.getLogger(__name__)

# Create Blueprint
ecg_api = Blueprint('ecg_api', __name__)

# Initialize digitizer (lazy loading)
_digitizer = None

def get_digitizer():
    """Get or create digitizer instance"""
    global _digitizer
    if _digitizer is None:
        _digitizer = MCAIECGDigitizer(sample_rate=250)
        logger.info("MC AI ECG Digitizer initialized for API")
    return _digitizer

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ecg_api.route('/api/ecg-digitize', methods=['POST'])
def digitize_ecg():
    """
    Digitize ECG image to WFDB format
    
    Input: multipart/form-data with 'ecg_image' file
    Output: JSON with results or WFDB files (if format=wfdb)
    """
    try:
        # Check if file is present
        if 'ecg_image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided. Please upload an ECG image.'
            }), 400
        
        file = request.files['ecg_image']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Empty filename'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Get parameters
        output_format = request.form.get('format', 'json')  # 'json' or 'wfdb'
        sample_rate = int(request.form.get('sample_rate', 250))
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, filename)
        file.save(input_path)
        
        logger.info(f"MC AI: Processing ECG image: {filename}")
        
        # Digitize the ECG
        digitizer = get_digitizer()
        result = digitizer.digitize_ecg_image(
            input_path,
            output_name='api_ecg',
            output_dir=temp_dir
        )
        
        if not result or not result.get('success'):
            return jsonify({
                'success': False,
                'error': 'ECG digitization failed',
                'issues': result.get('validation_issues', []) if result else []
            }), 500
        
        # Return based on format
        if output_format == 'wfdb':
            # Create ZIP with WFDB files
            zip_path = os.path.join(temp_dir, 'ecg_output.zip')
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                hea_file = result['wfdb_path'] + '.hea'
                dat_file = result['wfdb_path'] + '.dat'
                zipf.write(hea_file, 'api_ecg.hea')
                zipf.write(dat_file, 'api_ecg.dat')
            
            return send_file(
                zip_path,
                mimetype='application/zip',
                as_attachment=True,
                download_name='ecg_digitized.zip'
            )
        else:
            # Return JSON response with actual waveform data
            signals_dict = {}
            if 'signal' in result and 'voltage' in result['signal']:
                signals_dict['Lead_II'] = result['signal']['voltage'].tolist()
            
            response = {
                'success': True,
                'message': 'ECG digitized successfully! 💜',
                'signal': {
                    'duration_seconds': float(result['signal']['duration_s']),
                    'samples': result['signal']['num_samples'],
                    'sample_rate': result['signal']['sample_rate'],
                    'amplitude_mV': float(result['signal']['amplitude_mV'])
                },
                'signals': signals_dict,
                'time': result['signal']['time'].tolist() if 'time' in result['signal'] else [],
                'analysis': {
                    'heart_rate_bpm': result['analysis'].get('heart_rate_bpm'),
                    'hrv_ms': result['analysis'].get('hrv_ms'),
                    'emotional_state': result['analysis'].get('emotional_state'),
                    'resonance_frequency': result['analysis'].get('resonance_frequency')
                },
                'wfdb_valid': result['wfdb_valid'],
                'competition_ready': result['wfdb_valid']
            }
            
            return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"MC AI: ECG API error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ecg_api.route('/api/ecg-digitize/batch', methods=['POST'])
def digitize_batch():
    """
    Batch digitize multiple ECG images
    
    Input: multipart/form-data with multiple 'ecg_images[]' files
    Output: ZIP file with all WFDB files
    """
    try:
        # Check for files
        if 'ecg_images' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No files provided. Upload files with key "ecg_images"'
            }), 400
        
        files = request.files.getlist('ecg_images')
        
        if len(files) == 0:
            return jsonify({
                'success': False,
                'error': 'No files uploaded'
            }), 400
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        input_paths = []
        
        # Save all uploaded files
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(temp_dir, 'input_' + filename)
                file.save(file_path)
                input_paths.append(file_path)
        
        if len(input_paths) == 0:
            return jsonify({
                'success': False,
                'error': 'No valid ECG images uploaded'
            }), 400
        
        logger.info(f"MC AI: Batch processing {len(input_paths)} ECG images")
        
        # Batch digitize
        digitizer = get_digitizer()
        output_dir = os.path.join(temp_dir, 'output')
        results = digitizer.batch_digitize(input_paths, output_dir=output_dir)
        
        # Create submission package
        submission_zip = digitizer.converter.create_submission_package(
            output_dir,
            os.path.join(temp_dir, 'batch_submission.zip')
        )
        
        # Return submission ZIP
        return send_file(
            submission_zip,
            mimetype='application/zip',
            as_attachment=True,
            download_name='ecg_batch_digitized.zip'
        )
    
    except Exception as e:
        logger.error(f"MC AI: Batch ECG API error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ecg_api.route('/api/ecg-digitize/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'MC AI ECG Digitization API',
        'version': '1.0.0',
        'ready': True,
        'message': 'Ready to digitize ECGs for $50,000 prize! 💜🏆'
    }), 200

# Usage info endpoint
@ecg_api.route('/api/ecg-digitize/info', methods=['GET'])
def api_info():
    """API information and usage"""
    return jsonify({
        'name': 'MC AI ECG Digitization API',
        'version': '1.0.0',
        'endpoints': {
            '/api/ecg-digitize': {
                'method': 'POST',
                'description': 'Digitize single ECG image',
                'parameters': {
                    'ecg_image': 'Image file (required)',
                    'format': 'Output format: "json" or "wfdb" (default: json)',
                    'sample_rate': 'Sample rate in Hz (default: 250)'
                },
                'returns': 'JSON with results or ZIP with WFDB files'
            },
            '/api/ecg-digitize/batch': {
                'method': 'POST',
                'description': 'Batch digitize multiple ECG images',
                'parameters': {
                    'ecg_images': 'Multiple image files (required)'
                },
                'returns': 'ZIP file with all WFDB files'
            },
            '/api/ecg-digitize/health': {
                'method': 'GET',
                'description': 'Health check',
                'returns': 'Service status'
            },
            '/api/ecg-digitize/info': {
                'method': 'GET',
                'description': 'API documentation',
                'returns': 'This information'
            }
        },
        'features': [
            'Image preprocessing (denoising, grid removal)',
            'Multi-method calibration (OCR + grid + fallback)',
            'Waveform extraction and tracing',
            'Heart rate & HRV analysis',
            'Cymatic pattern generation 💜',
            'Emotional resonance detection',
            'PhysioNet WFDB format output',
            'Competition-compliant validation'
        ],
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'example_curl': '''
curl -X POST http://localhost:5000/api/ecg-digitize \\
  -F "ecg_image=@ecg.jpg" \\
  -F "format=json"
        '''.strip()
    }), 200
