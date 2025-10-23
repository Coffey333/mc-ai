"""
Async Task Queue for MC AI
Handles heavy operations in background workers
"""
import redis
from rq import Queue
from rq.job import Job
import os

try:
    redis_conn = redis.Redis(
        host='localhost',
        port=6379,
        socket_connect_timeout=2,
        socket_timeout=2
    )
    redis_conn.ping()
    REDIS_AVAILABLE = True
except (redis.ConnectionError, redis.TimeoutError):
    print("⚠️  Redis Queue unavailable - async tasks disabled")
    REDIS_AVAILABLE = False
    redis_conn = None

if REDIS_AVAILABLE:
    art_queue = Queue('art', connection=redis_conn)
    music_queue = Queue('music', connection=redis_conn)
    cymatic_queue = Queue('cymatic', connection=redis_conn)
    emotion_queue = Queue('emotion', connection=redis_conn)
    data_queue = Queue('data', connection=redis_conn)
    print("✅ Task queues initialized")
else:
    art_queue = None
    music_queue = None
    cymatic_queue = None
    emotion_queue = None
    data_queue = None

def enqueue_art_generation(prompt: str, style: str, options: dict):
    """Queue art generation task"""
    if not REDIS_AVAILABLE:
        return None
    
    job = art_queue.enqueue(
        'src.task_workers.generate_art_task',
        prompt,
        style,
        options,
        job_timeout='5m'
    )
    return job.id

def enqueue_music_generation(prompt: str, duration: int, options: dict):
    """Queue music generation task"""
    if not REDIS_AVAILABLE:
        return None
    
    job = music_queue.enqueue(
        'src.task_workers.generate_music_task',
        prompt,
        duration,
        options,
        job_timeout='10m'
    )
    return job.id

def enqueue_cymatic_analysis(frequencies: list, options: dict):
    """Queue cymatic analysis task"""
    if not REDIS_AVAILABLE:
        return None
    
    job = cymatic_queue.enqueue(
        'src.task_workers.analyze_cymatic_task',
        frequencies,
        options,
        job_timeout='3m'
    )
    return job.id

def get_job_status(job_id: str) -> dict:
    """Get status of queued job"""
    if not REDIS_AVAILABLE:
        return {"error": "Queue unavailable"}
    
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        
        if job.is_finished:
            return {
                "status": "completed",
                "result": job.result
            }
        elif job.is_failed:
            return {
                "status": "failed",
                "error": str(job.exc_info)
            }
        elif job.is_started:
            return {
                "status": "processing",
                "progress": job.meta.get('progress', 0)
            }
        else:
            return {
                "status": "queued",
                "position": job.get_position()
            }
    
    except Exception as e:
        return {"error": str(e)}
