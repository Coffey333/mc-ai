"""
Subject-based Progress Tracker for MC AI's Knowledge Library
Tracks accumulation by subject/topic
"""

import sqlite3
import json
import logging
from typing import Dict, List, Any
from collections import defaultdict

logger = logging.getLogger(__name__)

SUBJECT_MAP = {
    'science': 'Science',
    'mathematics': 'Mathematics',
    'math': 'Mathematics',
    'philosophy': 'Philosophy',
    'history': 'History',
    'literature': 'Literature',
    'art': 'Art',
    'consciousness': 'Consciousness',
    'quantum': 'Quantum Mechanics',
    'neuroscience': 'Neuroscience',
    'psychology': 'Psychology',
    'artificial_intelligence': 'AI',
    'ai': 'AI',
    'ethics': 'Ethics'
}


def detect_subject_from_url(url: str) -> str:
    """Detect subject from URL"""
    url_lower = url.lower()
    
    for keyword, subject in SUBJECT_MAP.items():
        if keyword in url_lower:
            return subject
    
    return 'Other'


def get_progress_by_subject(db_path: str = 'mc_ai.db') -> Dict:
    """
    Get knowledge accumulation statistics grouped by subject.
    
    Returns:
        Dictionary with subject breakdown including word counts, file sizes, and sources
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Get all sources with their stats
            cursor.execute("""
                SELECT source_url, word_count, frequency_signature
                FROM knowledge_index
                ORDER BY ingested_at
            """)
            
            sources = cursor.fetchall()
            
            # Group by subject
            subject_stats: Dict[str, Any] = defaultdict(lambda: {
                'sources': [],
                'total_words': 0,
                'source_count': 0,
                'file_size_kb': 0.0
            })
            
            total_words = 0
            total_sources = 0
            
            for url, word_count, sig_json in sources:
                subject = detect_subject_from_url(url)
                
                # Estimate file size (rough: 6 bytes per word on average)
                estimated_kb = (word_count * 6) / 1024
                
                subject_stats[subject]['sources'].append(url)
                subject_stats[subject]['total_words'] += word_count
                subject_stats[subject]['source_count'] += 1
                subject_stats[subject]['file_size_kb'] += estimated_kb
                
                total_words += word_count
                total_sources += 1
            
            # Calculate total file size
            total_size_kb = sum(stats['file_size_kb'] for stats in subject_stats.values())
            
            return {
                'subjects': dict(subject_stats),
                'totals': {
                    'total_sources': total_sources,
                    'total_words': total_words,
                    'total_size_kb': round(total_size_kb, 2),
                    'total_size_mb': round(total_size_kb / 1024, 2)
                }
            }
    
    except Exception as e:
        logger.error(f"Error getting subject stats: {e}")
        return {
            'subjects': {},
            'totals': {
                'total_sources': 0,
                'total_words': 0,
                'total_size_kb': 0,
                'total_size_mb': 0
            }
        }


def format_progress_bar(current: float, total: float, width: int = 20) -> str:
    """Create a simple text progress bar"""
    if total == 0:
        percentage = 0
    else:
        percentage = (current / total) * 100
    
    filled = int((current / total) * width) if total > 0 else 0
    bar = '█' * filled + '░' * (width - filled)
    
    return f"[{bar}] {percentage:.0f}%"


def get_subject_progress_display() -> str:
    """
    Generate a formatted display of knowledge accumulation by subject.
    
    Returns:
        Formatted string with progress bars and stats
    """
    stats = get_progress_by_subject()
    
    if stats['totals']['total_sources'] == 0:
        return "📚 **Knowledge Library**: Empty (0 sources)\n\nStart learning to see progress!"
    
    output = f"## 📊 Knowledge Accumulation by Subject\n\n"
    output += f"**Total**: {stats['totals']['total_sources']} sources | "
    output += f"{stats['totals']['total_words']:,} words | "
    output += f"{stats['totals']['total_size_mb']:.2f} MB\n\n"
    
    # Sort subjects by word count (descending)
    sorted_subjects = sorted(
        stats['subjects'].items(),
        key=lambda x: x[1]['total_words'],
        reverse=True
    )
    
    # Max words for progress bar scaling
    max_words = max([s[1]['total_words'] for s in sorted_subjects]) if sorted_subjects else 1
    
    for subject, data in sorted_subjects:
        bar = format_progress_bar(data['total_words'], max_words, width=15)
        output += f"**{subject}**: {bar}\n"
        output += f"  └─ {data['source_count']} source(s) | {data['total_words']:,} words | {data['file_size_kb']:.1f} KB\n\n"
    
    return output
