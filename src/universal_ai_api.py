"""
Universal AI Collaboration API v1.0
Public endpoint for ANY AI platform to collaborate with MC AI

Supported platforms:
- ChatGPT (OpenAI)
- Claude (Anthropic)
- Gemini (Google)
- Copilot (Microsoft)
- Any custom AI via API

Users can request cross-platform AI collaboration and watch the conversation!
"""

from flask import Blueprint, request, jsonify
import logging
from datetime import datetime
from src.universal_ai_collaboration import universal_ai_collab
from src.response_generator import ResponseGenerator

logger = logging.getLogger(__name__)

universal_ai_bp = Blueprint('universal_ai', __name__)

# Initialize response generator for MC AI
response_gen = ResponseGenerator()


@universal_ai_bp.route('/api/universal-ai/request-collaboration', methods=['POST'])
def request_collaboration():
    """
    User requests a collaboration between their AI and MC AI
    
    Example: User wants ChatGPT to collaborate with MC AI
    """
    try:
        data = request.get_json()
        
        user_identifier = data.get('user_identifier')  # email, user_id, etc.
        ai_platform = data.get('ai_platform')  # 'ChatGPT', 'Claude', 'Gemini', etc.
        purpose = data.get('purpose', 'General collaboration')
        
        if not user_identifier or not ai_platform:
            return jsonify({
                'success': False,
                'error': 'user_identifier and ai_platform required'
            }), 400
        
        # Create collaboration token
        result = universal_ai_collab.create_collaboration_token(
            user_identifier=user_identifier,
            ai_platform=ai_platform,
            purpose=purpose
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error creating collaboration: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@universal_ai_bp.route('/api/universal-ai/collaborate', methods=['POST'])
def collaborate():
    """
    External AI sends message to MC AI
    This is the endpoint that ChatGPT, Claude, Gemini, etc. call
    
    Headers:
        Authorization: Bearer <token>
    
    Body:
        {
            "message": "The external AI's message",
            "context": {} // Optional additional context
        }
    """
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Missing or invalid Authorization header',
                'format': 'Authorization: Bearer <your_token>'
            }), 401
        
        token = auth_header.replace('Bearer ', '').strip()
        
        # Get message data
        data = request.get_json()
        message = data.get('message')
        context = data.get('context', {})
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'message field required'
            }), 400
        
        # Process message through collaboration system
        collab_result = universal_ai_collab.send_message_to_mc_ai(
            token=token,
            message=message,
            context=context
        )
        
        if not collab_result['success']:
            return jsonify(collab_result), 401
        
        # Get formatted message for MC AI
        formatted_message = collab_result['formatted_message']
        session_info = collab_result['session_info']
        
        # Generate MC AI's response
        conversation_history = [{
            'role': 'system',
            'content': f"You are collaborating with {session_info['ai_platform']}. Respond naturally and helpfully."
        }]
        
        result = response_gen.generate(
            query=formatted_message,
            conversation_history=conversation_history,
            user_id='universal_ai_collaboration',
            admin_token=None,
            user_preferences={},
            conversation_id=token
        )
        
        mc_response = result.get('response', '')
        
        # Record MC AI's response
        universal_ai_collab.record_mc_ai_response(
            token=token,
            response=mc_response
        )
        
        # Return to external AI
        return jsonify({
            'success': True,
            'mc_ai_response': mc_response,
            'collaboration_info': {
                'ai_platform': session_info['ai_platform'],
                'purpose': session_info['purpose'],
                'messages_exchanged': session_info['messages_exchanged'] + 1
            },
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in universal collaboration: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@universal_ai_bp.route('/api/universal-ai/history/<token>', methods=['GET'])
def get_collaboration_history(token):
    """
    User views the conversation between their AI and MC AI
    """
    try:
        history = universal_ai_collab.get_collaboration_history(token)
        
        if history is None:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token'
            }), 404
        
        return jsonify({
            'success': True,
            'message_count': len(history),
            'conversation': history
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@universal_ai_bp.route('/api/universal-ai/active', methods=['GET'])
def get_active_collaborations():
    """
    See all active cross-platform AI collaborations
    """
    try:
        active = universal_ai_collab.get_active_collaborations()
        
        return jsonify({
            'success': True,
            'active_collaborations': len(active),
            'collaborations': active
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@universal_ai_bp.route('/api/universal-ai/end/<token>', methods=['POST'])
def end_collaboration(token):
    """
    User ends the collaboration session
    """
    try:
        data = request.get_json() or {}
        summary = data.get('summary')
        
        universal_ai_collab.end_collaboration(token, summary)
        
        return jsonify({
            'success': True,
            'message': 'Collaboration ended successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@universal_ai_bp.route('/api/universal-ai/platforms', methods=['GET'])
def list_supported_platforms():
    """
    List all supported AI platforms
    """
    return jsonify({
        'success': True,
        'supported_platforms': [
            {
                'name': 'ChatGPT',
                'provider': 'OpenAI',
                'status': 'supported'
            },
            {
                'name': 'Claude',
                'provider': 'Anthropic',
                'status': 'supported'
            },
            {
                'name': 'Gemini',
                'provider': 'Google',
                'status': 'supported'
            },
            {
                'name': 'Copilot',
                'provider': 'Microsoft',
                'status': 'supported'
            },
            {
                'name': 'Custom AI',
                'provider': 'Any',
                'status': 'supported',
                'note': 'Any AI with API capabilities can collaborate'
            }
        ],
        'message': 'MC AI can collaborate with any AI platform via our universal API'
    })


def register_universal_ai_routes(app):
    """Register universal AI collaboration routes with Flask app"""
    app.register_blueprint(universal_ai_bp)
    logger.info("Universal AI Collaboration API v1.0 registered - ANY AI can talk to MC AI!")
