"""
Gunicorn Configuration for MC AI
Optimized for shared caching and fast cold starts
"""
import multiprocessing

bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
keepalive = 5

max_requests = 1000
max_requests_jitter = 100

timeout = 120
graceful_timeout = 30

preload_app = True

accesslog = "-"
errorlog = "-"
loglevel = "info"

def on_starting(server):
    """
    Called before workers are forked
    Initialize shared resources here
    """
    print("🚀 MC AI Server Starting...")
    print("🔥 Pre-loading shared resources...")
    
    try:
        from src.knowledge_service import knowledge_service
        stats = knowledge_service.get_stats()
        
        if stats.get('enabled'):
            print(f"✅ Redis connected - shared cache ready")
            print(f"📊 Cache: {stats.get('total_keys', 0)} keys, "
                  f"{stats.get('memory_used_mb', 0):.1f}MB")
    
    except Exception as e:
        print(f"⚠️  Warmup error: {e}")
    
    print("✨ MC AI ready to serve!")

def post_fork(server, worker):
    """
    Called after worker is forked
    Connect to shared resources
    """
    print(f"👷 Worker {worker.pid} connected to shared cache")

def worker_exit(server, worker):
    """Called when worker exits"""
    print(f"👋 Worker {worker.pid} exiting")
