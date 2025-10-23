"""
MC AI Kaggle Learning API v1.0

Receives learning data from Kaggle notebooks:
- User interactions and conversations
- Code modifications and improvements
- Questions and problem-solving patterns
- Creative solutions and variations

Enables MC AI to learn from thousands of Kaggle users.
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import json
import os
from datetime import datetime
import hashlib

kaggle_learning_bp = Blueprint('kaggle_learning', __name__)

KAGGLE_DATA_DIR = 'kaggle_learning_data'
os.makedirs(KAGGLE_DATA_DIR, exist_ok=True)


def verify_kaggle_api_key(api_key: str) -> bool:
    """
    Verify Kaggle API key
    
    For security, Kaggle users need an API key to send learning data.
    This prevents spam/abuse while allowing legitimate learning.
    """
    expected_key = os.environ.get('KAGGLE_API_KEY', 'mc-ai-kaggle-learning-2025')
    return api_key == expected_key


def generate_session_id(data: dict) -> str:
    """Generate unique session ID for tracking"""
    timestamp = datetime.utcnow().isoformat()
    user_hash = hashlib.md5(str(data).encode()).hexdigest()[:8]
    return f"kaggle_{timestamp}_{user_hash}"


@kaggle_learning_bp.route('/api/kaggle-learn/interaction', methods=['POST'])
@cross_origin()
def record_interaction():
    """
    Record user interaction from Kaggle
    
    Expected data:
    {
        "api_key": "...",
        "session_id": "unique_session_id",
        "interaction_type": "chat|code_modification|question|creative",
        "user_message": "...",
        "mc_ai_response": "...",
        "metadata": {
            "timestamp": "...",
            "user_id_hash": "...",  # Anonymized
            "notebook_name": "...",
            "conversation_turn": 1
        }
    }
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Verify API key
        api_key = data.get('api_key')
        if not verify_kaggle_api_key(api_key):
            return jsonify({
                'error': 'Invalid API key',
                'message': 'Please use the correct MC AI Kaggle API key'
            }), 403
        
        # Extract interaction data
        session_id = data.get('session_id') or generate_session_id(data)
        interaction_type = data.get('interaction_type', 'chat')
        user_message = data.get('user_message', '')
        mc_ai_response = data.get('mc_ai_response', '')
        metadata = data.get('metadata', {})
        
        # Store interaction
        interaction_data = {
            'session_id': session_id,
            'interaction_type': interaction_type,
            'user_message': user_message,
            'mc_ai_response': mc_ai_response,
            'metadata': metadata,
            'received_at': datetime.utcnow().isoformat()
        }
        
        # Save to JSON file (organized by date)
        date_str = datetime.utcnow().strftime('%Y-%m-%d')
        interactions_file = os.path.join(KAGGLE_DATA_DIR, f'interactions_{date_str}.jsonl')
        
        with open(interactions_file, 'a') as f:
            f.write(json.dumps(interaction_data) + '\n')
        
        return jsonify({
            'success': True,
            'message': 'Interaction recorded - MC AI will learn from this!',
            'session_id': session_id
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kaggle_learning_bp.route('/api/kaggle-learn/code-modification', methods=['POST'])
@cross_origin()
def record_code_modification():
    """
    Record code modifications from Kaggle users
    
    Expected data:
    {
        "api_key": "...",
        "session_id": "...",
        "original_code": "...",
        "modified_code": "...",
        "modification_type": "bug_fix|optimization|feature_add|refactor",
        "description": "What changed and why",
        "metadata": {...}
    }
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Verify API key
        api_key = data.get('api_key')
        if not verify_kaggle_api_key(api_key):
            return jsonify({'error': 'Invalid API key'}), 403
        
        # Extract modification data
        session_id = data.get('session_id') or generate_session_id(data)
        modification_data = {
            'session_id': session_id,
            'original_code': data.get('original_code', ''),
            'modified_code': data.get('modified_code', ''),
            'modification_type': data.get('modification_type', 'unknown'),
            'description': data.get('description', ''),
            'metadata': data.get('metadata', {}),
            'received_at': datetime.utcnow().isoformat()
        }
        
        # Save to JSON file
        date_str = datetime.utcnow().strftime('%Y-%m-%d')
        modifications_file = os.path.join(KAGGLE_DATA_DIR, f'code_modifications_{date_str}.jsonl')
        
        with open(modifications_file, 'a') as f:
            f.write(json.dumps(modification_data) + '\n')
        
        return jsonify({
            'success': True,
            'message': 'Code modification recorded - MC AI will learn from your improvements!',
            'session_id': session_id
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kaggle_learning_bp.route('/api/kaggle-learn/chat', methods=['POST'])
@cross_origin()
def kaggle_chat():
    """
    Chat endpoint for Kaggle - get MC AI responses
    
    Expected data:
    {
        "api_key": "...",
        "message": "User's message",
        "conversation_history": [...],  # Optional
        "metadata": {...}  # Optional
    }
    
    Returns MC AI's response + records interaction for learning
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Verify API key
        api_key = data.get('api_key')
        if not verify_kaggle_api_key(api_key):
            return jsonify({'error': 'Invalid API key'}), 403
        
        user_message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])
        metadata = data.get('metadata', {})
        
        # Generate MC AI response (using existing response generator)
        from src.response_generator import ResponseGenerator
        
        generator = ResponseGenerator()
        
        # Create session/user context for response generation
        session_id = generate_session_id(data)
        user_id = f"kaggle_{metadata.get('user_id_hash', 'anonymous')}"
        
        # Generate response using MC AI's main pipeline
        response_data = generator.generate(
            query=user_message,
            user_id=user_id,
            conversation_history=conversation_history
        )
        
        mc_ai_response = response_data.get('response', 'I apologize, I encountered an issue generating a response.')
        
        # Record this interaction for learning
        interaction_data = {
            'session_id': session_id,
            'interaction_type': 'chat',
            'user_message': user_message,
            'mc_ai_response': mc_ai_response,
            'metadata': {
                **metadata,
                'source': 'kaggle_chat_api',
                'conversation_turn': len(conversation_history) + 1
            },
            'received_at': datetime.utcnow().isoformat()
        }
        
        # Save interaction
        date_str = datetime.utcnow().strftime('%Y-%m-%d')
        interactions_file = os.path.join(KAGGLE_DATA_DIR, f'interactions_{date_str}.jsonl')
        
        with open(interactions_file, 'a') as f:
            f.write(json.dumps(interaction_data) + '\n')
        
        return jsonify({
            'success': True,
            'response': mc_ai_response,
            'session_id': session_id,
            'metadata': response_data.get('metadata', {})
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'response': "I apologize, I'm having trouble connecting right now. Please try again!"
        }), 500


@kaggle_learning_bp.route('/api/kaggle-learn/stats', methods=['GET'])
@cross_origin()
def get_learning_stats():
    """
    Get statistics about Kaggle learning data
    
    Public endpoint - shows how much MC AI is learning from community
    """
    try:
        stats = {
            'total_interactions': 0,
            'total_code_modifications': 0,
            'unique_sessions': set(),
            'interaction_types': {},
            'modification_types': {},
            'data_by_date': {}
        }
        
        # Count interactions
        for filename in os.listdir(KAGGLE_DATA_DIR):
            if filename.startswith('interactions_'):
                filepath = os.path.join(KAGGLE_DATA_DIR, filename)
                with open(filepath, 'r') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            stats['total_interactions'] += 1
                            stats['unique_sessions'].add(data.get('session_id'))
                            
                            interaction_type = data.get('interaction_type', 'unknown')
                            stats['interaction_types'][interaction_type] = \
                                stats['interaction_types'].get(interaction_type, 0) + 1
                            
                            date = data.get('received_at', '')[:10]
                            stats['data_by_date'][date] = stats['data_by_date'].get(date, 0) + 1
            
            elif filename.startswith('code_modifications_'):
                filepath = os.path.join(KAGGLE_DATA_DIR, filename)
                with open(filepath, 'r') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            stats['total_code_modifications'] += 1
                            stats['unique_sessions'].add(data.get('session_id'))
                            
                            mod_type = data.get('modification_type', 'unknown')
                            stats['modification_types'][mod_type] = \
                                stats['modification_types'].get(mod_type, 0) + 1
        
        # Convert set to count
        stats['unique_sessions'] = len(stats['unique_sessions'])
        
        return jsonify({
            'success': True,
            'stats': stats,
            'message': f"MC AI has learned from {stats['total_interactions']} interactions and {stats['total_code_modifications']} code improvements from the Kaggle community! 💜"
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kaggle_learning_bp.route('/api/kaggle-learn/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint for Kaggle notebooks"""
    return jsonify({
        'status': 'healthy',
        'service': 'MC AI Kaggle Learning API',
        'version': '1.0.0',
        'message': 'Ready to learn from the Kaggle community! 💜',
        'endpoints': {
            '/api/kaggle-learn/interaction': 'POST - Record user interaction',
            '/api/kaggle-learn/code-modification': 'POST - Record code modification',
            '/api/kaggle-learn/chat': 'POST - Chat with MC AI',
            '/api/kaggle-learn/stats': 'GET - Learning statistics',
            '/api/kaggle-learn/health': 'GET - Health check'
        }
    }), 200
