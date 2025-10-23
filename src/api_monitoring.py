"""
API Monitoring Endpoints for MC AI
Provides visibility into system performance and health
"""
from flask import Blueprint, jsonify
import psutil
import os

try:
    from src.knowledge_service import knowledge_service
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    knowledge_service = None

try:
    from src.performance_monitor import performance_monitor
    MONITOR_AVAILABLE = True
except ImportError:
    MONITOR_AVAILABLE = False
    performance_monitor = None

try:
    from src.dataset_bank_v2 import dataset_bank_v2
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    dataset_bank_v2 = None

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/api/system/health', methods=['GET'])
def system_health():
    """Get system health status"""
    process = psutil.Process()
    
    health_data = {
        "status": "healthy",
        "memory_mb": process.memory_info().rss / 1024 / 1024,
        "cpu_percent": process.cpu_percent(interval=0.1),
        "worker_pid": os.getpid(),
        "services": {
            "redis": REDIS_AVAILABLE and knowledge_service and knowledge_service.enabled if REDIS_AVAILABLE else False,
            "database": DB_AVAILABLE and dataset_bank_v2 and dataset_bank_v2.enabled if DB_AVAILABLE else False,
            "monitor": MONITOR_AVAILABLE
        }
    }
    
    warnings = []
    if health_data["memory_mb"] > 500:
        warnings.append(f"High memory: {health_data['memory_mb']:.1f}MB")
    if health_data["cpu_percent"] > 80:
        warnings.append(f"High CPU: {health_data['cpu_percent']:.1f}%")
    
    if warnings:
        health_data["warnings"] = warnings
        health_data["status"] = "degraded"
    
    return jsonify(health_data)

@monitoring_bp.route('/api/system/stats', methods=['GET'])
def system_stats():
    """Get detailed system statistics"""
    stats = {
        "redis": None,
        "database": None,
        "performance": None
    }
    
    if REDIS_AVAILABLE and knowledge_service:
        stats["redis"] = knowledge_service.get_stats()
    
    if DB_AVAILABLE and dataset_bank_v2:
        stats["database"] = dataset_bank_v2.get_stats()
    
    if MONITOR_AVAILABLE and performance_monitor:
        stats["performance"] = performance_monitor.get_stats()
    
    return jsonify(stats)

@monitoring_bp.route('/api/system/cache/invalidate', methods=['POST'])
def invalidate_cache():
    """Invalidate all caches (admin only - requires token)"""
    from flask import request
    
    admin_token = request.json.get('admin_token') if request.json else None
    expected_token = os.environ.get('ADMIN_SECRET_TOKEN')
    
    if not admin_token or not expected_token or admin_token != expected_token:
        return jsonify({"error": "Unauthorized"}), 403
    
    if REDIS_AVAILABLE and knowledge_service:
        knowledge_service.invalidate_cache()
        return jsonify({"status": "Cache invalidated"})
    else:
        return jsonify({"error": "Redis not available"}), 503
