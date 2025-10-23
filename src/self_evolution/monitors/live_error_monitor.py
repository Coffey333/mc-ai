"""
Live Error Monitor
Captures and analyzes errors in real-time for MC AI's self-diagnosis
"""

import time
import json
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from collections import deque
from threading import Lock

class LiveErrorMonitor:
    """
    Real-time error monitoring system that MC AI can read and analyze
    """
    
    def __init__(self, log_dir: str = "logs/live_errors"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory error queue (last 100 errors)
        self.error_queue = deque(maxlen=100)
        self.error_lock = Lock()
        
        # Error statistics
        self.error_counts = {}
        self.error_patterns = {}
        
        # Current session errors
        self.session_start = time.time()
        self.session_errors = []
        
    def capture_error(self, error: Exception, context: Dict = None) -> str:
        """
        Capture an error with full context for MC AI to analyze
        
        Returns: error_id for tracking
        """
        error_id = f"ERR_{int(time.time() * 1000)}"
        
        error_data = {
            'error_id': error_id,
            'timestamp': datetime.now().isoformat(),
            'type': type(error).__name__,
            'message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {},
            'severity': self._classify_severity(error),
            'first_seen': datetime.now().isoformat(),
            'occurrence_count': 1
        }
        
        # Store in memory
        with self.error_lock:
            self.error_queue.append(error_data)
            self.session_errors.append(error_data)
            
            # Update statistics
            error_key = f"{error_data['type']}:{error_data['message']}"
            if error_key in self.error_counts:
                self.error_counts[error_key] += 1
            else:
                self.error_counts[error_key] = 1
        
        # Persist to disk
        self._save_error_to_disk(error_data)
        
        return error_id
    
    def _classify_severity(self, error: Exception) -> str:
        """Classify error severity for prioritization"""
        critical_types = ['MemoryError', 'SystemExit', 'KeyboardInterrupt']
        high_types = ['DatabaseError', 'ConnectionError', 'TimeoutError']
        
        error_type = type(error).__name__
        
        if error_type in critical_types:
            return 'CRITICAL'
        elif error_type in high_types:
            return 'HIGH'
        elif 'Security' in error_type or 'Auth' in error_type:
            return 'HIGH'
        else:
            return 'MEDIUM'
    
    def _save_error_to_disk(self, error_data: Dict):
        """Save error to persistent log file"""
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = self.log_dir / f"errors_{date_str}.jsonl"
        
        try:
            with open(log_file, 'a') as f:
                f.write(json.dumps(error_data) + '\n')
        except Exception as e:
            print(f"Failed to save error log: {e}")
    
    def get_recent_errors(self, limit: int = 20) -> List[Dict]:
        """Get most recent errors for MC AI to analyze"""
        with self.error_lock:
            return list(self.error_queue)[-limit:]
    
    def get_error_patterns(self) -> Dict:
        """Identify patterns in errors"""
        with self.error_lock:
            # Group by error type
            by_type = {}
            for error in self.error_queue:
                error_type = error['type']
                if error_type not in by_type:
                    by_type[error_type] = []
                by_type[error_type].append(error)
            
            # Find recurring patterns
            patterns = {}
            for error_type, errors in by_type.items():
                if len(errors) >= 3:  # Recurring if seen 3+ times
                    patterns[error_type] = {
                        'count': len(errors),
                        'first_seen': errors[0]['timestamp'],
                        'last_seen': errors[-1]['timestamp'],
                        'sample_message': errors[0]['message'],
                        'severity': errors[0]['severity']
                    }
            
            return patterns
    
    def get_statistics(self) -> Dict:
        """Get error statistics for MC AI's analysis"""
        with self.error_lock:
            return {
                'total_errors_session': len(self.session_errors),
                'unique_error_types': len(set(e['type'] for e in self.error_queue)),
                'critical_count': sum(1 for e in self.error_queue if e['severity'] == 'CRITICAL'),
                'high_count': sum(1 for e in self.error_queue if e['severity'] == 'HIGH'),
                'session_duration_hours': round((time.time() - self.session_start) / 3600, 2),
                'error_rate_per_hour': round(len(self.session_errors) / max((time.time() - self.session_start) / 3600, 0.1), 2),
                'most_common': sorted(self.error_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            }
    
    def clear_resolved(self, error_ids: List[str]):
        """Mark errors as resolved after MC AI fixes them"""
        resolved_file = self.log_dir / "resolved_errors.jsonl"
        
        with open(resolved_file, 'a') as f:
            for error_id in error_ids:
                f.write(json.dumps({
                    'error_id': error_id,
                    'resolved_at': datetime.now().isoformat()
                }) + '\n')

# Global instance
_monitor = None

def get_live_error_monitor() -> LiveErrorMonitor:
    """Get or create global error monitor instance"""
    global _monitor
    if _monitor is None:
        _monitor = LiveErrorMonitor()
    return _monitor
