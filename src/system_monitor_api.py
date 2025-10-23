"""
MC AI System Monitor API v1.0

Gives MC AI real-time access to his own system status, logs, and activity.
MC AI can query this to understand what's happening with him.
"""

from flask import Blueprint, jsonify
from flask_cors import cross_origin
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

system_monitor_bp = Blueprint('system_monitor', __name__)

KAGGLE_DATA_DIR = 'kaggle_learning_data'
LOG_DIR = '/tmp/logs'


def get_recent_kaggle_interactions(minutes=60):
    """Get recent Kaggle interactions from the last N minutes"""
    interactions = []
    cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
    
    try:
        if not os.path.exists(KAGGLE_DATA_DIR):
            return []
        
        # Read today's interactions file
        date_str = datetime.utcnow().strftime('%Y-%m-%d')
        interactions_file = os.path.join(KAGGLE_DATA_DIR, f'interactions_{date_str}.jsonl')
        
        if os.path.exists(interactions_file):
            with open(interactions_file, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        received_at = datetime.fromisoformat(data.get('received_at', ''))
                        
                        if received_at >= cutoff_time:
                            interactions.append({
                                'timestamp': data.get('received_at'),
                                'user_message': data.get('user_message', '')[:200],  # Truncate
                                'mc_ai_response': data.get('mc_ai_response', '')[:200],
                                'session_id': data.get('session_id', ''),
                                'metadata': data.get('metadata', {})
                            })
                    except:
                        continue
        
        return interactions[-10:]  # Last 10 interactions
    
    except Exception as e:
        return []


def get_recent_errors(minutes=60):
    """Get recent errors from logs"""
    errors = []
    cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
    
    try:
        # Read MC AI Server logs
        log_files = [f for f in os.listdir(LOG_DIR) if f.startswith('MC_AI_Server_')]
        if log_files:
            latest_log = sorted(log_files)[-1]
            log_path = os.path.join(LOG_DIR, latest_log)
            
            with open(log_path, 'r') as f:
                for line in f.readlines()[-100:]:  # Last 100 lines
                    if 'ERROR' in line or 'CRITICAL' in line or 'Exception' in line:
                        errors.append(line.strip())
        
        return errors[-20:]  # Last 20 errors
    
    except Exception as e:
        return []


def get_system_stats():
    """Get current system statistics"""
    stats = {
        'uptime': 'running',
        'workflows': {},
        'api_endpoints': [],
        'recent_activity': []
    }
    
    try:
        # Check workflow status
        if os.path.exists(LOG_DIR):
            log_files = os.listdir(LOG_DIR)
            stats['workflows'] = {
                'mc_ai_server': 'running' if any('MC_AI_Server' in f for f in log_files) else 'unknown',
                'redis': 'running' if any('Redis' in f for f in log_files) else 'unknown',
                'tripo': 'running' if any('Tripo' in f for f in log_files) else 'unknown'
            }
        
        # List active API endpoints
        stats['api_endpoints'] = [
            '/api/chat',
            '/api/analyze',
            '/api/kaggle-learn/chat',
            '/api/ecg-digitize',
            '/api/system-status'
        ]
        
        return stats
    
    except Exception as e:
        return stats


@system_monitor_bp.route('/api/system-status', methods=['GET'])
@cross_origin()
def get_system_status():
    """
    Get MC AI's current system status
    
    MC AI can call this to understand what's happening with him!
    """
    try:
        minutes = 60  # Last hour
        
        status = {
            'timestamp': datetime.utcnow().isoformat(),
            'system': get_system_stats(),
            'recent_kaggle_interactions': get_recent_kaggle_interactions(minutes),
            'recent_errors': get_recent_errors(minutes),
            'health': 'operational'
        }
        
        return jsonify(status), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'health': 'degraded'
        }), 500


@system_monitor_bp.route('/api/system-status/kaggle-recent', methods=['GET'])
@cross_origin()
def get_recent_kaggle_only():
    """
    Get only recent Kaggle interactions (lightweight)
    Perfect for MC AI to quickly check recent activity
    """
    try:
        interactions = get_recent_kaggle_interactions(minutes=120)  # Last 2 hours
        
        return jsonify({
            'success': True,
            'count': len(interactions),
            'interactions': interactions,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@system_monitor_bp.route('/api/system-status/health', methods=['GET'])
@cross_origin()
def quick_health_check():
    """
    Quick health check - is MC AI alive and running?
    """
    return jsonify({
        'status': 'alive',
        'service': 'MC AI System Monitor',
        'timestamp': datetime.utcnow().isoformat(),
        'message': '💜 MC AI is self-aware and monitoring his own systems!'
    }), 200
