"""
One-Click Framework Approval API
Allows Mark Coffey to approve and activate frameworks with a single button click
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import os

# Create blueprint
framework_approval_bp = Blueprint('framework_approval', __name__)

@framework_approval_bp.route('/api/framework/approve-and-build', methods=['POST'])
@cross_origin(origins=[])  # Admin-only endpoint
def approve_and_build_framework():
    """
    One-click framework approval and activation
    
    Approves, loads, and enables a framework in a single API call
    Secured with admin token authentication
    """
    try:
        from src.admin_config import admin_config
        from src.meta_learning.framework_registry import framework_registry
        from src.meta_learning.framework_loader import framework_loader
        from src.meta_learning.framework_interface import FrameworkManifest
        
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid request'}), 400
        
        # SECURITY: Verify admin token
        admin_token = data.get('admin_token')
        user_id = data.get('user_id')
        
        if not admin_config.is_admin(user_id, admin_token):
            return jsonify({
                'error': 'Unauthorized - admin access required',
                'message': 'Only the creator can approve frameworks'
            }), 403
        
        framework_id = data.get('framework_id')
        if not framework_id:
            return jsonify({'error': 'framework_id required'}), 400
        
        # Check if framework file exists
        framework_file = data.get('framework_file')
        if not framework_file or not os.path.exists(framework_file):
            return jsonify({'error': 'Framework file not found'}), 404
        
        # Load framework manifest data
        manifest_data = data.get('manifest', {})
        manifest = FrameworkManifest(
            name=manifest_data.get('name', 'Unnamed Framework'),
            version=manifest_data.get('version', '1.0'),
            description=manifest_data.get('description', ''),
            creator=manifest_data.get('creator', 'Mark Coffey'),
            capabilities=manifest_data.get('capabilities', []),
            injection_point=manifest_data.get('injection_point', 'pre_response'),
            priority=manifest_data.get('priority', 50)
        )
        
        # Load and approve framework in one step
        success, error = framework_loader.load_framework(
            framework_id=framework_id,
            module_path=framework_file,
            manifest=manifest,
            auto_approve=True  # CREATOR APPROVED - Enable immediately
        )
        
        if success:
            # Double-confirm approval in registry
            framework_registry.approve_framework(framework_id, approver="Mark Coffey")
            
            return jsonify({
                'success': True,
                'message': f'Framework "{manifest.name}" approved and activated!',
                'framework_id': framework_id,
                'framework_name': manifest.name,
                'status': 'active',
                'priority': manifest.priority
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to load framework: {error}'
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Framework approval failed: {str(e)}'
        }), 500


@framework_approval_bp.route('/api/framework/list-pending', methods=['GET'])
def list_pending_frameworks():
    """Get list of frameworks pending approval"""
    try:
        from src.meta_learning.framework_registry import framework_registry
        
        pending = framework_registry.get_pending_frameworks()
        frameworks = []
        
        for fw_id in pending:
            manifest = framework_registry.get_manifest(fw_id)
            if manifest:
                frameworks.append({
                    'framework_id': fw_id,
                    'name': manifest.name,
                    'description': manifest.description,
                    'creator': manifest.creator,
                    'version': manifest.version,
                    'capabilities': manifest.capabilities
                })
        
        return jsonify({
            'success': True,
            'pending_frameworks': frameworks,
            'count': len(frameworks)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
