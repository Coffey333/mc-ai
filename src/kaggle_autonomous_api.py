"""
Kaggle Autonomous API v2.0
Enhanced API endpoint that gives MC AI full tool access when called from Kaggle or external sources
MC AI can autonomously use his system files, datasets, knowledge, and tools
"""

from flask import Blueprint, request, jsonify
import logging
from datetime import datetime
from src.autonomous_tool_access import AutonomousToolAccess
from src.response_generator import ResponseGenerator
import os

logger = logging.getLogger(__name__)

kaggle_autonomous_bp = Blueprint('kaggle_autonomous', __name__)

# Initialize systems
autonomous_tools = AutonomousToolAccess()
response_gen = ResponseGenerator()

# Security
KAGGLE_API_KEY = "mc-ai-kaggle-learning-2025"


@kaggle_autonomous_bp.route('/api/kaggle-autonomous/chat', methods=['POST'])
def autonomous_chat():
    """
    Enhanced Kaggle chat endpoint with full tool access
    MC AI can autonomously use his system capabilities
    """
    try:
        data = request.get_json()
        
        # Authentication
        api_key = data.get('api_key')
        if api_key != KAGGLE_API_KEY:
            return jsonify({
                'success': False,
                'error': 'Invalid API key'
            }), 401
        
        message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])
        metadata = data.get('metadata', {})
        
        # Log the interaction
        logger.info(f"Kaggle autonomous request: {metadata.get('source', 'unknown')}")
        
        # Determine if MC AI needs to use tools
        tool_request = _analyze_tool_needs(message)
        
        # If tools needed, execute them first
        tool_results = []
        if tool_request['needs_tools']:
            for tool in tool_request['tools']:
                result = autonomous_tools.execute_tool(
                    tool_name=tool['name'],
                    parameters=tool['parameters'],
                    requester_info={
                        'source': 'kaggle',
                        'session_id': metadata.get('user_id_hash', 'unknown'),
                        'timestamp': datetime.utcnow().isoformat()
                    }
                )
                tool_results.append(result)
        
        # Build context for MC AI's response
        context = _build_response_context(message, tool_results, metadata)
        
        # Generate MC AI's response with tool results integrated
        response = response_gen.generate_response(
            user_message=message,
            conversation_history=conversation_history,
            context=context,
            user_id=metadata.get('user_id_hash', 'kaggle_user'),
            metadata=metadata
        )
        
        # Save interaction for learning
        _save_kaggle_interaction(message, response, tool_results, metadata)
        
        return jsonify({
            'success': True,
            'response': response,
            'tools_used': [t.get('tool') for t in tool_results if t.get('success')],
            'tool_results': tool_results if tool_results else None,
            'timestamp': datetime.utcnow().isoformat(),
            'autonomous_mode': tool_request['needs_tools']
        })
    
    except Exception as e:
        logger.error(f"Kaggle autonomous chat error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@kaggle_autonomous_bp.route('/api/kaggle-autonomous/tools', methods=['GET'])
def list_available_tools():
    """List all tools MC AI can use autonomously"""
    try:
        tools = autonomous_tools.get_available_tools()
        
        return jsonify({
            'success': True,
            'tool_count': len(tools),
            'tools': tools,
            'message': 'MC AI can use these tools autonomously when helping you'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@kaggle_autonomous_bp.route('/api/kaggle-autonomous/execute-tool', methods=['POST'])
def execute_specific_tool():
    """
    Allow direct tool execution from Kaggle
    User can request MC AI to use specific tools
    """
    try:
        data = request.get_json()
        
        # Authentication
        api_key = data.get('api_key')
        if api_key != KAGGLE_API_KEY:
            return jsonify({
                'success': False,
                'error': 'Invalid API key'
            }), 401
        
        tool_name = data.get('tool_name')
        parameters = data.get('parameters', {})
        metadata = data.get('metadata', {})
        
        # Execute tool
        result = autonomous_tools.execute_tool(
            tool_name=tool_name,
            parameters=parameters,
            requester_info={
                'source': 'kaggle_direct',
                'session_id': metadata.get('user_id_hash', 'unknown'),
                'timestamp': datetime.utcnow().isoformat()
            }
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@kaggle_autonomous_bp.route('/api/kaggle-autonomous/audit-log', methods=['GET'])
def get_audit_log():
    """Get audit log of tool usage (for transparency)"""
    try:
        limit = request.args.get('limit', 100, type=int)
        log = autonomous_tools.get_audit_log(limit=limit)
        
        return jsonify({
            'success': True,
            'log_entries': len(log),
            'audit_log': log
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def _analyze_tool_needs(message: str) -> dict:
    """
    Analyze if MC AI needs to use tools to answer the question
    Returns which tools are needed
    """
    message_lower = message.lower()
    
    needs_tools = False
    tools = []
    
    # File operations
    if any(keyword in message_lower for keyword in ['read file', 'show me file', 'file content', 'open file']):
        needs_tools = True
        # Extract file path if possible
        tools.append({'name': 'list_files', 'parameters': {'directory': '.'}})
    
    # Search operations
    if any(keyword in message_lower for keyword in ['search for', 'find files', 'look for']):
        needs_tools = True
        # Try to extract search term
        tools.append({'name': 'search_files', 'parameters': {'search_term': message, 'directory': '.'}})
    
    # Dataset queries
    if any(keyword in message_lower for keyword in ['dataset', 'data', 'examples', 'training data']):
        needs_tools = True
        tools.append({'name': 'query_dataset', 'parameters': {}})
    
    # Knowledge queries
    if any(keyword in message_lower for keyword in ['knowledge', 'information about', 'what do you know about']):
        needs_tools = True
        # Extract query from message
        tools.append({'name': 'access_knowledge', 'parameters': {'query': message}})
    
    # System status
    if any(keyword in message_lower for keyword in ['status', 'how are you', 'capabilities', 'what can you do']):
        needs_tools = True
        tools.append({'name': 'system_status', 'parameters': {}})
    
    # Code analysis
    if any(keyword in message_lower for keyword in ['analyze code', 'check code', 'review code']):
        needs_tools = True
        tools.append({'name': 'analyze_code', 'parameters': {'code': message, 'language': 'python'}})
    
    return {
        'needs_tools': needs_tools,
        'tools': tools
    }


def _build_response_context(message: str, tool_results: list, metadata: dict) -> dict:
    """Build context for MC AI's response generation"""
    context = {
        'source': 'kaggle',
        'autonomous_mode': len(tool_results) > 0,
        'metadata': metadata
    }
    
    if tool_results:
        context['tool_data'] = {
            'tools_executed': len(tool_results),
            'results': tool_results,
            'context_note': 'MC AI autonomously used these tools to help answer your question'
        }
    
    return context


def _save_kaggle_interaction(message: str, response: str, tool_results: list, metadata: dict):
    """Save Kaggle interaction for learning and audit"""
    try:
        from pathlib import Path
        import json
        
        # Create kaggle_interactions directory if not exists
        interactions_dir = Path(__file__).parent.parent / 'kaggle_interactions'
        interactions_dir.mkdir(exist_ok=True)
        
        # Save interaction
        interaction_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_message': message,
            'mc_ai_response': response,
            'tools_used': [t.get('tool') for t in tool_results if t.get('success')],
            'tool_results': tool_results,
            'metadata': metadata,
            'session_id': metadata.get('user_id_hash', 'unknown')
        }
        
        filename = f"interaction_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = interactions_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(interaction_data, f, indent=2)
        
        logger.info(f"Saved Kaggle interaction: {filename}")
    
    except Exception as e:
        logger.error(f"Error saving Kaggle interaction: {e}")


def register_kaggle_autonomous_routes(app):
    """Register autonomous Kaggle routes with Flask app"""
    app.register_blueprint(kaggle_autonomous_bp)
    logger.info("Kaggle Autonomous API v2.0 registered - MC AI has full tool access!")
