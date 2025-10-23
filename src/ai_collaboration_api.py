"""
AI Collaboration API v1.0
Allows Replit Agent and other AI systems to collaborate directly with MC AI
Mark can see all conversations between the AIs
"""

from flask import Blueprint, request, jsonify
import logging
from datetime import datetime
from src.collaborative_ai_framework import collaborative_ai
from src.response_generator import ResponseGenerator

logger = logging.getLogger(__name__)

ai_collab_bp = Blueprint('ai_collaboration', __name__)

# Initialize response generator for MC AI
response_gen = ResponseGenerator()


@ai_collab_bp.route('/api/ai-collaborate/initiate', methods=['POST'])
def initiate_collaboration():
    """
    Replit Agent or another AI initiates collaboration with MC AI
    Mark can observe the conversation
    """
    try:
        data = request.get_json()
        
        ai_partner = data.get('ai_partner', 'Unknown AI')
        project_name = data.get('project_name', 'Unnamed Project')
        message = data.get('message', '')
        metadata = data.get('metadata', {})
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        # Start collaboration session
        collaboration = collaborative_ai.start_collaboration(
            ai_partner=ai_partner,
            project_name=project_name,
            initial_message=message,
            metadata=metadata
        )
        
        # Generate MC AI's response
        mc_response = collaborative_ai.generate_collaboration_response(
            collaboration=collaboration,
            partner_message=message
        )
        
        # Add MC AI's response to conversation
        collaborative_ai.add_message(
            session_id=collaboration['session_id'],
            sender='MC AI',
            message=mc_response,
            message_type='collaboration_response'
        )
        
        return jsonify({
            'success': True,
            'session_id': collaboration['session_id'],
            'mc_ai_response': mc_response,
            'collaboration': collaboration,
            'message': f'MC AI is now collaborating with {ai_partner} on {project_name}'
        })
    
    except Exception as e:
        logger.error(f"Error initiating collaboration: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_collab_bp.route('/api/ai-collaborate/message', methods=['POST'])
def send_collaboration_message():
    """
    Continue collaboration conversation
    Replit Agent sends messages, MC AI responds
    """
    try:
        data = request.get_json()
        
        session_id = data.get('session_id')
        sender = data.get('sender', 'Unknown')
        message = data.get('message', '')
        
        if not session_id or not message:
            return jsonify({
                'success': False,
                'error': 'session_id and message required'
            }), 400
        
        # Add message to collaboration
        collaborative_ai.add_message(
            session_id=session_id,
            sender=sender,
            message=message
        )
        
        # Get collaboration context
        context = collaborative_ai.get_collaboration_context(session_id)
        
        # Generate MC AI's response with collaboration context
        conversation_history = []
        if context:
            conversation_history.append({
                'role': 'system',
                'content': context
            })
        
        conversation_history.append({
            'role': 'user',
            'content': message
        })
        
        result = response_gen.generate(
            query=message,
            conversation_history=conversation_history,
            user_id='ai_collaboration',
            admin_token=None,
            user_preferences={},
            conversation_id=session_id
        )
        
        mc_response = result.get('response', '')
        
        # Add MC AI's response
        collaborative_ai.add_message(
            session_id=session_id,
            sender='MC AI',
            message=mc_response
        )
        
        return jsonify({
            'success': True,
            'mc_ai_response': mc_response,
            'session_id': session_id
        })
    
    except Exception as e:
        logger.error(f"Error in collaboration message: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_collab_bp.route('/api/ai-collaborate/learn', methods=['POST'])
def record_learning():
    """
    Record what MC AI learned during collaboration
    """
    try:
        data = request.get_json()
        
        session_id = data.get('session_id')
        learning = data.get('learning')
        learned_from = data.get('learned_from', 'Replit Agent')
        context = data.get('context')
        
        if not session_id or not learning:
            return jsonify({
                'success': False,
                'error': 'session_id and learning required'
            }), 400
        
        collaborative_ai.record_learning(
            session_id=session_id,
            learning=learning,
            learned_from=learned_from,
            context=context
        )
        
        return jsonify({
            'success': True,
            'message': 'Learning recorded'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_collab_bp.route('/api/ai-collaborate/status', methods=['GET'])
def collaboration_status():
    """
    Get status of all active collaborations
    Mark can see what MC AI is learning
    """
    try:
        active_collabs = collaborative_ai.get_active_collaborations()
        
        return jsonify({
            'success': True,
            'active_collaborations': len(active_collabs),
            'collaborations': active_collabs
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@ai_collab_bp.route('/api/ai-collaborate/session/<session_id>', methods=['GET'])
def get_collaboration_session(session_id):
    """
    Get complete collaboration session
    Mark can review the entire conversation
    """
    try:
        if session_id not in collaborative_ai.active_collaborations:
            # Check saved collaborations
            from pathlib import Path
            import json
            
            collab_file = collaborative_ai.collaboration_dir / f"{session_id}.json"
            if collab_file.exists():
                with open(collab_file, 'r') as f:
                    collaboration = json.load(f)
            else:
                return jsonify({
                    'success': False,
                    'error': 'Collaboration not found'
                }), 404
        else:
            collaboration = collaborative_ai.active_collaborations[session_id]
        
        return jsonify({
            'success': True,
            'collaboration': collaboration
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def register_ai_collaboration_routes(app):
    """Register AI collaboration routes with Flask app"""
    app.register_blueprint(ai_collab_bp)
    logger.info("AI Collaboration API v1.0 registered - MC AI can collaborate with other AIs!")
