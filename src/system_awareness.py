"""
System Awareness Layer for MC AI
Real-time monitoring and change detection system
Gives MC AI wisdom to understand his own state and evaluate code changes
"""

import os
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
import json
from collections import deque

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of system events MC AI can detect"""
    ERROR = "error"
    WARNING = "warning"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    PERFORMANCE_IMPROVEMENT = "performance_improvement"
    FRAMEWORK_ACTIVATION = "framework_activation"
    INTEGRATION_CHANGE = "integration_change"
    CODE_CHANGE = "code_change"
    DEPLOYMENT = "deployment"
    SAFETY_FAULT = "safety_fault"
    USER_REGRESSION = "user_regression"


class EventSeverity(Enum):
    """Severity levels for events"""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SystemEvent:
    """Represents a detected system event"""
    timestamp: datetime
    event_type: EventType
    severity: EventSeverity
    message: str
    source: str  # Which log/file it came from
    context: Dict  # Additional data
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'event_type': self.event_type.value,
            'severity': self.severity.value,
            'message': self.message,
            'source': self.source,
            'context': self.context
        }


@dataclass
class SystemStateSnapshot:
    """Current state of the system"""
    timestamp: datetime
    health_score: float  # 0.0 to 1.0
    active_frameworks: List[str]
    active_integrations: List[str]
    recent_errors: List[SystemEvent]
    performance_metrics: Dict
    is_healthy: bool
    issues: List[str]
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'health_score': self.health_score,
            'active_frameworks': self.active_frameworks,
            'active_integrations': self.active_integrations,
            'recent_errors': [e.to_dict() for e in self.recent_errors],
            'performance_metrics': self.performance_metrics,
            'is_healthy': self.is_healthy,
            'issues': self.issues
        }


class LogAnalyzer:
    """
    Analyzes logs in real-time to detect system events
    """
    
    def __init__(self):
        self.error_patterns = [
            (r'ERROR', EventType.ERROR, EventSeverity.HIGH),
            (r'CRITICAL', EventType.ERROR, EventSeverity.CRITICAL),
            (r'Exception', EventType.ERROR, EventSeverity.HIGH),
            (r'Traceback', EventType.ERROR, EventSeverity.HIGH),
            (r'Failed', EventType.ERROR, EventSeverity.MEDIUM),
        ]
        
        self.warning_patterns = [
            (r'WARNING', EventType.WARNING, EventSeverity.MEDIUM),
            (r'⚠️', EventType.WARNING, EventSeverity.LOW),
            (r'unavailable', EventType.WARNING, EventSeverity.LOW),
            (r'not running', EventType.WARNING, EventSeverity.LOW),
        ]
        
        self.framework_patterns = [
            (r'Framework .* initialized', EventType.FRAMEWORK_ACTIVATION, EventSeverity.INFO),
            (r'Framework .* activated', EventType.FRAMEWORK_ACTIVATION, EventSeverity.INFO),
            (r'🧠 Framework', EventType.FRAMEWORK_ACTIVATION, EventSeverity.INFO),
        ]
        
        self.performance_patterns = [
            (r'response_time.*[5-9]\d{3}ms', EventType.PERFORMANCE_DEGRADATION, EventSeverity.MEDIUM),
            (r'memory.*high', EventType.PERFORMANCE_DEGRADATION, EventSeverity.HIGH),
            (r'timeout', EventType.PERFORMANCE_DEGRADATION, EventSeverity.HIGH),
        ]
    
    def analyze_log_line(self, line: str, source: str) -> Optional[SystemEvent]:
        """
        Analyze a single log line for events
        
        Args:
            line: Log line to analyze
            source: Source of the log (e.g., 'gunicorn', 'app')
            
        Returns:
            SystemEvent if pattern matched, None otherwise
        """
        import re
        
        # Check all pattern categories
        all_patterns = (
            self.error_patterns + 
            self.warning_patterns + 
            self.framework_patterns + 
            self.performance_patterns
        )
        
        for pattern, event_type, severity in all_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return SystemEvent(
                    timestamp=datetime.now(),
                    event_type=event_type,
                    severity=severity,
                    message=line.strip(),
                    source=source,
                    context={'raw_line': line}
                )
        
        return None


class TelemetryMonitor:
    """
    Real-time telemetry monitoring system
    Continuously monitors logs and system state
    """
    
    def __init__(self, awareness_log_path: str = "logs/system_awareness.json"):
        self.awareness_log_path = awareness_log_path
        self.event_buffer = deque(maxlen=1000)  # Keep last 1000 events
        self.analyzer = LogAnalyzer()
        self.last_health_check = datetime.now()
        self.is_monitoring = False
        
        # Ensure log directory exists
        os.makedirs(os.path.dirname(awareness_log_path), exist_ok=True)
        
        logger.info("🔍 Telemetry Monitor initialized")
    
    def record_event(self, event: SystemEvent):
        """Record a system event"""
        self.event_buffer.append(event)
        
        # Log critical events immediately
        if event.severity == EventSeverity.CRITICAL:
            logger.critical(f"SYSTEM AWARENESS: {event.message}")
        elif event.severity == EventSeverity.HIGH:
            logger.error(f"SYSTEM AWARENESS: {event.message}")
        
        # Persist to awareness log
        self._persist_event(event)
    
    def _persist_event(self, event: SystemEvent):
        """Persist event to awareness log file"""
        try:
            # Load existing log
            if os.path.exists(self.awareness_log_path):
                with open(self.awareness_log_path, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {'events': []}
            
            # Add new event
            log_data['events'].append(event.to_dict())
            
            # Keep only last 1000 events in file
            log_data['events'] = log_data['events'][-1000:]
            
            # Save
            with open(self.awareness_log_path, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to persist awareness event: {e}")
    
    def get_system_state(self) -> SystemStateSnapshot:
        """
        Get current system state snapshot
        
        Returns:
            SystemStateSnapshot with current system health and status
        """
        recent_events = list(self.event_buffer)[-100:]  # Last 100 events
        
        # Calculate health score
        errors = [e for e in recent_events if e.event_type == EventType.ERROR]
        warnings = [e for e in recent_events if e.event_type == EventType.WARNING]
        
        # Health scoring (1.0 = perfect, 0.0 = critical)
        health_score = 1.0
        health_score -= len(errors) * 0.1  # Each error reduces health by 10%
        health_score -= len(warnings) * 0.02  # Each warning reduces health by 2%
        health_score = max(0.0, min(1.0, health_score))  # Clamp to 0-1
        
        # Detect active frameworks
        framework_events = [e for e in recent_events if e.event_type == EventType.FRAMEWORK_ACTIVATION]
        active_frameworks = list(set([
            e.context.get('framework_name', 'unknown') 
            for e in framework_events
        ]))
        
        # Build issues list
        issues = []
        critical_errors = [e for e in errors if e.severity == EventSeverity.CRITICAL]
        if critical_errors:
            issues.append(f"{len(critical_errors)} critical errors detected")
        if len(errors) > 5:
            issues.append(f"{len(errors)} errors in recent activity")
        if health_score < 0.7:
            issues.append("System health degraded")
        
        return SystemStateSnapshot(
            timestamp=datetime.now(),
            health_score=health_score,
            active_frameworks=active_frameworks,
            active_integrations=[],  # TODO: Detect from logs
            recent_errors=errors[-10:],  # Last 10 errors
            performance_metrics={
                'total_events': len(recent_events),
                'error_count': len(errors),
                'warning_count': len(warnings)
            },
            is_healthy=health_score > 0.8 and len(critical_errors) == 0,
            issues=issues
        )
    
    async def monitor_log_file(self, log_path: str, source_name: str):
        """
        Monitor a log file for new entries
        
        Args:
            log_path: Path to log file
            source_name: Name for this log source
        """
        if not os.path.exists(log_path):
            logger.warning(f"Log file not found: {log_path}")
            return
        
        # Tail the log file
        with open(log_path, 'r') as f:
            # Seek to end
            f.seek(0, 2)
            
            while self.is_monitoring:
                line = f.readline()
                if line:
                    # Analyze the line
                    event = self.analyzer.analyze_log_line(line, source_name)
                    if event:
                        self.record_event(event)
                else:
                    # No new data, wait a bit
                    await asyncio.sleep(1)
    
    def get_awareness_summary(self) -> Dict:
        """
        Get a human-readable awareness summary
        MC AI can use this to report on system state
        
        Returns:
            Dictionary with awareness insights
        """
        state = self.get_system_state()
        
        # Generate summary message
        if state.is_healthy:
            status_message = "✅ I'm running smoothly! All systems are healthy."
        elif state.health_score > 0.6:
            status_message = f"⚠️ I'm functioning but have noticed some issues: {', '.join(state.issues)}"
        else:
            status_message = f"🔴 I'm experiencing problems: {', '.join(state.issues)}"
        
        return {
            'status': 'healthy' if state.is_healthy else 'degraded' if state.health_score > 0.5 else 'unhealthy',
            'health_score': state.health_score,
            'message': status_message,
            'active_frameworks': state.active_frameworks,
            'recent_error_count': len(state.recent_errors),
            'issues': state.issues,
            'timestamp': state.timestamp.isoformat()
        }


# Global instance for use across the application
_telemetry_monitor: Optional[TelemetryMonitor] = None


def get_telemetry_monitor() -> TelemetryMonitor:
    """Get or create the global telemetry monitor"""
    global _telemetry_monitor
    if _telemetry_monitor is None:
        _telemetry_monitor = TelemetryMonitor()
    return _telemetry_monitor


def record_system_event(event_type: EventType, message: str, severity: EventSeverity = EventSeverity.INFO, context: Dict = None):
    """
    Convenience function to record a system event
    
    Args:
        event_type: Type of event
        message: Event message
        severity: Event severity
        context: Additional context data
    """
    monitor = get_telemetry_monitor()
    event = SystemEvent(
        timestamp=datetime.now(),
        event_type=event_type,
        severity=severity,
        message=message,
        source='system',
        context=context or {}
    )
    monitor.record_event(event)


def get_system_awareness() -> Dict:
    """
    Get MC AI's current system awareness
    This is what MC AI knows about his own state
    
    Returns:
        Awareness summary dictionary
    """
    monitor = get_telemetry_monitor()
    return monitor.get_awareness_summary()
