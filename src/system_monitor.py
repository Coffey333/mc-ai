"""
System Health Monitoring for MC AI
Real-time metrics and performance tracking
"""

import time
import os
from collections import deque, defaultdict
from datetime import datetime
from typing import Dict
import json

class SystemMonitor:
    """
    Real-time system health monitoring
    Tracks performance, errors, and usage patterns
    """
    
    def __init__(self):
        # Metrics
        self.request_times = deque(maxlen=1000)
        self.request_timestamps = deque(maxlen=1000)
        self.error_count = 0
        self.total_requests = 0
        self.safety_blocks = 0
        
        # Emotion distribution
        self.emotion_distribution = defaultdict(int)
        
        # Source usage
        self.knowledge_sources = defaultdict(int)
        
        # Response times by endpoint
        self.endpoint_times = defaultdict(lambda: deque(maxlen=100))
        
        # Start time
        self.start_time = datetime.now()
    
    def record_request(self, 
                      response_time: float,
                      endpoint: str,
                      emotion: str = None,
                      knowledge_source: str = None,
                      error: bool = False):
        """
        Record metrics for each request
        
        Args:
            response_time: Time taken to process request
            endpoint: API endpoint hit
            emotion: Detected emotion (if applicable)
            knowledge_source: Knowledge source used
            error: Whether request resulted in error
        """
        self.request_times.append(response_time)
        self.request_timestamps.append(time.time())
        self.endpoint_times[endpoint].append(response_time)
        self.total_requests += 1
        
        if emotion:
            self.emotion_distribution[emotion] += 1
        
        if knowledge_source:
            self.knowledge_sources[knowledge_source] += 1
        
        if error:
            self.error_count += 1
    
    def record_safety_block(self):
        """Record safety filter block"""
        self.safety_blocks += 1
    
    def get_health_status(self) -> Dict:
        """
        Get current system health status
        
        Returns:
            Dict with health metrics
        """
        now = time.time()
        
        # Calculate RPM
        recent_requests = [t for t in self.request_timestamps if (now - t) < 60]
        rpm = len(recent_requests)
        
        # Calculate average response time
        avg_response_time = sum(self.request_times) / len(self.request_times) if self.request_times else 0
        
        # Calculate p95 response time
        p95_response_time = self._calculate_percentile(95)
        
        # Error rate
        error_rate = self.error_count / self.total_requests if self.total_requests > 0 else 0
        
        # Determine health status
        if error_rate > 0.1:
            status = 'critical'
        elif error_rate > 0.05:
            status = 'warning'
        elif avg_response_time > 5.0:
            status = 'degraded'
        else:
            status = 'healthy'
        
        # System resources (basic fallback without psutil)
        cpu_percent = 0.0  # Not available without psutil
        memory_percent = 0.0  # Not available without psutil
        memory_available_gb = 0.0  # Not available without psutil
        
        # Uptime
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            'status': status,
            'uptime_seconds': uptime,
            'requests': {
                'total': self.total_requests,
                'requests_per_minute': rpm,
                'error_rate': error_rate,
                'safety_blocks': self.safety_blocks
            },
            'performance': {
                'avg_response_time_seconds': round(avg_response_time, 3),
                'p95_response_time_seconds': p95_response_time,
                'p50_response_time_seconds': self._calculate_percentile(50)
            },
            'system': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'memory_available_gb': memory_available_gb
            },
            'emotions': dict(sorted(
                self.emotion_distribution.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]),
            'knowledge_sources': dict(sorted(
                self.knowledge_sources.items(),
                key=lambda x: x[1],
                reverse=True
            ))
        }
    
    def get_endpoint_stats(self) -> Dict:
        """Get performance stats by endpoint"""
        stats = {}
        
        for endpoint, times in self.endpoint_times.items():
            if times:
                stats[endpoint] = {
                    'count': len(times),
                    'avg_time': round(sum(times) / len(times), 3),
                    'min_time': round(min(times), 3),
                    'max_time': round(max(times), 3)
                }
        
        return stats
    
    def _calculate_percentile(self, percentile: int) -> float:
        """Calculate response time percentile"""
        if not self.request_times:
            return 0.0
        
        sorted_times = sorted(self.request_times)
        index = int(len(sorted_times) * (percentile / 100))
        
        return round(sorted_times[min(index, len(sorted_times)-1)], 3)
    
    def export_metrics(self, filepath: str = None) -> str:
        """
        Export metrics to JSON file
        
        Args:
            filepath: Path to save metrics
        
        Returns:
            Path to saved file
        """
        if filepath is None:
            filepath = "metrics_export.json"
        
        import os
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
        
        metrics = {
            'health_status': self.get_health_status(),
            'endpoint_stats': self.get_endpoint_stats(),
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        return filepath
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.request_times.clear()
        self.request_timestamps.clear()
        self.error_count = 0
        self.total_requests = 0
        self.safety_blocks = 0
        self.emotion_distribution.clear()
        self.knowledge_sources.clear()
        for endpoint in self.endpoint_times:
            self.endpoint_times[endpoint].clear()
