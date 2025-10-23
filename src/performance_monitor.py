"""
Performance Monitoring for MC AI
Track memory usage, request latency, and cache efficiency
"""
import psutil
import time
import os
from functools import wraps
from typing import Callable, Any

class PerformanceMonitor:
    """
    Lightweight performance monitoring
    
    Tracks:
    - Memory usage per worker
    - Request latency
    - Cache hit rates
    - Worker health
    """
    
    def __init__(self):
        self.process = psutil.Process()
        self.metrics = {
            'requests_total': 0,
            'requests_failed': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'total_latency': 0.0
        }
    
    def get_memory_mb(self) -> float:
        """Get current memory usage in MB"""
        return self.process.memory_info().rss / 1024 / 1024
    
    def get_cpu_percent(self) -> float:
        """Get CPU usage percentage"""
        return self.process.cpu_percent(interval=0.1)
    
    def track_request(self, func: Callable) -> Callable:
        """Decorator to track request performance"""
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                self.metrics['requests_total'] += 1
                return result
            
            except Exception as e:
                self.metrics['requests_failed'] += 1
                raise e
            
            finally:
                latency = time.time() - start_time
                self.metrics['total_latency'] += latency
                
                if latency > 2.0:
                    print(f"⚠️  Slow request: {func.__name__} took {latency:.2f}s")
        
        return wrapper
    
    def track_cache_hit(self):
        """Record cache hit"""
        self.metrics['cache_hits'] += 1
    
    def track_cache_miss(self):
        """Record cache miss"""
        self.metrics['cache_misses'] += 1
    
    def get_stats(self) -> dict:
        """Get current performance statistics"""
        total_requests = self.metrics['requests_total']
        avg_latency = (
            self.metrics['total_latency'] / total_requests 
            if total_requests > 0 
            else 0
        )
        
        total_cache_ops = self.metrics['cache_hits'] + self.metrics['cache_misses']
        cache_hit_rate = (
            (self.metrics['cache_hits'] / total_cache_ops * 100)
            if total_cache_ops > 0
            else 0
        )
        
        return {
            'memory_mb': self.get_memory_mb(),
            'cpu_percent': self.get_cpu_percent(),
            'requests_total': total_requests,
            'requests_failed': self.metrics['requests_failed'],
            'avg_latency_ms': avg_latency * 1000,
            'cache_hit_rate': cache_hit_rate,
            'cache_hits': self.metrics['cache_hits'],
            'cache_misses': self.metrics['cache_misses']
        }
    
    def check_health(self) -> dict:
        """Health check for worker"""
        memory_mb = self.get_memory_mb()
        cpu = self.get_cpu_percent()
        
        warnings = []
        if memory_mb > 500:
            warnings.append(f"High memory usage: {memory_mb:.1f}MB")
        if cpu > 80:
            warnings.append(f"High CPU usage: {cpu:.1f}%")
        
        return {
            'healthy': len(warnings) == 0,
            'memory_mb': memory_mb,
            'cpu_percent': cpu,
            'warnings': warnings
        }
    
    def log_stats(self):
        """Print current statistics"""
        stats = self.get_stats()
        print(f"📊 Performance: {stats['memory_mb']:.1f}MB RAM, "
              f"{stats['cpu_percent']:.1f}% CPU, "
              f"{stats['avg_latency_ms']:.0f}ms avg, "
              f"{stats['cache_hit_rate']:.1f}% cache hit rate")

performance_monitor = PerformanceMonitor()
