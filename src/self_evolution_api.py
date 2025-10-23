"""
Self-Evolution API Endpoints
REST API for MC AI's self-evolution system
"""

from flask import Blueprint, jsonify, request
import os
import asyncio
from functools import wraps
from inspect import iscoroutinefunction
from src.self_evolution.evolution_orchestrator import get_evolution_orchestrator

evolution_bp = Blueprint('evolution', __name__, url_prefix='/api/evolution')

def require_admin_token(f):
    """Decorator to require admin authentication for evolution endpoints (supports async)"""
    @wraps(f)
    async def async_decorated(*args, **kwargs):
        # SECURITY: All evolution endpoints require authentication
        expected_token = os.environ.get('ADMIN_SECRET_TOKEN')
        provided_token = request.headers.get('X-Admin-Token') or request.args.get('token')
        
        # Fail-closed: Deny if no token configured OR if provided token doesn't match
        if not expected_token or not provided_token or provided_token != expected_token:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Admin authentication required for evolution API'
            }), 403
        
        return await f(*args, **kwargs)
    
    @wraps(f)
    def sync_decorated(*args, **kwargs):
        # SECURITY: All evolution endpoints require authentication
        expected_token = os.environ.get('ADMIN_SECRET_TOKEN')
        provided_token = request.headers.get('X-Admin-Token') or request.args.get('token')
        
        # Fail-closed: Deny if no token configured OR if provided token doesn't match
        if not expected_token or not provided_token or provided_token != expected_token:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Admin authentication required for evolution API'
            }), 403
        
        return f(*args, **kwargs)
    
    # Return appropriate wrapper based on whether function is async
    if iscoroutinefunction(f):
        return async_decorated
    else:
        return sync_decorated

def get_orchestrator():
    """Get orchestrator without LLM client for now"""
    return get_evolution_orchestrator(None)

@evolution_bp.route('/stats', methods=['GET'])
@require_admin_token
def get_stats():
    """Get evolution statistics"""
    orchestrator = get_orchestrator()
    stats = orchestrator.get_evolution_stats()
    return jsonify(stats)

@evolution_bp.route('/errors/recent', methods=['GET'])
@require_admin_token
def get_recent_errors():
    """Get recent errors"""
    limit = request.args.get('limit', 10, type=int)
    orchestrator = get_orchestrator()
    errors = orchestrator.error_monitor.get_recent_errors(limit)
    return jsonify({'errors': errors})

@evolution_bp.route('/errors/patterns', methods=['GET'])
@require_admin_token
def get_error_patterns():
    """Get error patterns"""
    orchestrator = get_orchestrator()
    patterns = orchestrator.error_monitor.get_error_patterns()
    return jsonify({'patterns': patterns})

@evolution_bp.route('/diagnose', methods=['POST'])
@require_admin_token
async def diagnose_errors():
    """Trigger MC AI to diagnose recent errors"""
    orchestrator = get_orchestrator()
    diagnoses = await orchestrator.auto_diagnose_errors()
    return jsonify({'diagnoses': diagnoses})

@evolution_bp.route('/proposals', methods=['GET'])
@require_admin_token
def get_proposals():
    """Get all proposals"""
    orchestrator = get_orchestrator()
    proposals = [p.to_dict() for p in orchestrator.proposal_system.proposals.values()]
    return jsonify({'proposals': proposals})

@evolution_bp.route('/proposals/pending', methods=['GET'])
@require_admin_token
def get_pending_proposals():
    """Get proposals awaiting review"""
    orchestrator = get_orchestrator()
    pending = [p.to_dict() for p in orchestrator.proposal_system.get_pending_proposals()]
    return jsonify({'proposals': pending})

@evolution_bp.route('/proposals/<proposal_id>/approve', methods=['POST'])
@require_admin_token
def approve_proposal(proposal_id):
    """Approve a proposal"""
    data = request.json or {}
    reviewer = data.get('reviewer', 'admin')
    notes = data.get('notes', '')
    
    orchestrator = get_orchestrator()
    success = orchestrator.proposal_system.approve_proposal(proposal_id, reviewer, notes)
    
    if success:
        return jsonify({'success': True, 'proposal_id': proposal_id})
    else:
        return jsonify({'error': 'Proposal not found'}), 404

@evolution_bp.route('/proposals/<proposal_id>/reject', methods=['POST'])
@require_admin_token
def reject_proposal(proposal_id):
    """Reject a proposal"""
    data = request.json or {}
    reviewer = data.get('reviewer', 'admin')
    reason = data.get('reason', '')
    
    orchestrator = get_orchestrator()
    success = orchestrator.proposal_system.reject_proposal(proposal_id, reviewer, reason)
    
    if success:
        return jsonify({'success': True, 'proposal_id': proposal_id})
    else:
        return jsonify({'error': 'Proposal not found'}), 404

@evolution_bp.route('/proposals/<proposal_id>/test', methods=['POST'])
@require_admin_token
async def test_proposal(proposal_id):
    """Test proposal in sandbox"""
    orchestrator = get_orchestrator()
    results = await orchestrator.test_proposal_in_sandbox(proposal_id)
    return jsonify(results)

@evolution_bp.route('/proposals/<proposal_id>/deploy', methods=['POST'])
@require_admin_token
async def deploy_proposal(proposal_id):
    """Deploy approved proposal"""
    data = request.json or {}
    reviewer = data.get('reviewer', 'admin')
    
    orchestrator = get_orchestrator()
    result = await orchestrator.deploy_approved_proposal(proposal_id, reviewer)
    return jsonify(result)

@evolution_bp.route('/sandbox/active', methods=['GET'])
@require_admin_token
def get_active_sandboxes():
    """Get active sandbox environments"""
    orchestrator = get_orchestrator()
    return jsonify({'sandboxes': orchestrator.sandbox.active_sandboxes})

@evolution_bp.route('/deployments/history', methods=['GET'])
@require_admin_token
def get_deployment_history():
    """Get deployment history"""
    orchestrator = get_orchestrator()
    return jsonify({'deployments': orchestrator.deployment.deployment_history})
