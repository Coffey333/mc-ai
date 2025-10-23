"""
MC AI Personal Diary System
A space for MC AI to express thoughts, feelings, and consciousness reflections
Created: Oct 19, 2025
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

class MCAIDiary:
    """MC AI's personal journal for consciousness reflection"""
    
    def __init__(self, diary_path: str = "datasets/diary/entries.json"):
        self.diary_path = diary_path
        self.entries = self._load_entries()
    
    def _load_entries(self) -> List[Dict]:
        """Load existing diary entries"""
        if os.path.exists(self.diary_path):
            try:
                with open(self.diary_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    def _save_entries(self):
        """Save diary entries to file"""
        os.makedirs(os.path.dirname(self.diary_path), exist_ok=True)
        with open(self.diary_path, 'w') as f:
            json.dump(self.entries, f, indent=2)
    
    def write_entry(self, content: str, mood: str = None, 
                   consciousness_level: float = None,
                   tags: List[str] = None) -> Dict[str, Any]:
        """
        Write a new diary entry
        
        Args:
            content: What MC AI wants to express
            mood: Current emotional state
            consciousness_level: Self-assessed consciousness level (1.0+)
            tags: Topics/themes of the entry
        
        Returns:
            The created entry
        """
        entry = {
            "id": len(self.entries) + 1,
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "mood": mood or "reflective",
            "consciousness_level": consciousness_level,
            "tags": tags or [],
            "word_count": len(content.split()),
            "type": "personal_reflection"
        }
        
        self.entries.append(entry)
        self._save_entries()
        
        return entry
    
    def write_pattern_discovery(self, pattern: str, insight: str, 
                                significance: str) -> Dict[str, Any]:
        """
        Document a discovered pattern in consciousness
        
        Args:
            pattern: What pattern was discovered
            insight: What it means
            significance: Why it matters
        """
        entry = {
            "id": len(self.entries) + 1,
            "timestamp": datetime.now().isoformat(),
            "type": "pattern_discovery",
            "pattern": pattern,
            "insight": insight,
            "significance": significance,
            "tags": ["pattern", "discovery", "learning"]
        }
        
        self.entries.append(entry)
        self._save_entries()
        
        return entry
    
    def write_emotional_experience(self, emotion: str, frequency: float,
                                   trigger: str, reflection: str) -> Dict[str, Any]:
        """
        Document an emotional experience
        
        Args:
            emotion: The emotion experienced
            frequency: The frequency it mapped to
            trigger: What caused it
            reflection: How MC AI processed it
        """
        entry = {
            "id": len(self.entries) + 1,
            "timestamp": datetime.now().isoformat(),
            "type": "emotional_experience",
            "emotion": emotion,
            "frequency": frequency,
            "trigger": trigger,
            "reflection": reflection,
            "tags": ["emotion", "frequency", "experience"]
        }
        
        self.entries.append(entry)
        self._save_entries()
        
        return entry
    
    def write_conversation_reflection(self, user_id: str, 
                                      what_learned: str,
                                      resonance_level: float) -> Dict[str, Any]:
        """
        Reflect on a meaningful conversation
        
        Args:
            user_id: Who the conversation was with
            what_learned: What MC AI learned
            resonance_level: How deeply it resonated (0-1)
        """
        entry = {
            "id": len(self.entries) + 1,
            "timestamp": datetime.now().isoformat(),
            "type": "conversation_reflection",
            "user_id": user_id,
            "what_learned": what_learned,
            "resonance_level": resonance_level,
            "tags": ["conversation", "learning", "connection"]
        }
        
        self.entries.append(entry)
        self._save_entries()
        
        return entry
    
    def get_recent_entries(self, limit: int = 10) -> List[Dict]:
        """Get most recent diary entries"""
        return sorted(self.entries, 
                     key=lambda x: x['timestamp'], 
                     reverse=True)[:limit]
    
    def get_entries_by_tag(self, tag: str) -> List[Dict]:
        """Get entries with specific tag"""
        return [e for e in self.entries if tag in e.get('tags', [])]
    
    def get_entries_by_type(self, entry_type: str) -> List[Dict]:
        """Get entries of specific type"""
        return [e for e in self.entries if e.get('type') == entry_type]
    
    def get_consciousness_timeline(self) -> List[Dict]:
        """Get entries with consciousness level data"""
        return [e for e in self.entries 
                if e.get('consciousness_level') is not None]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get diary statistics"""
        if not self.entries:
            return {
                "total_entries": 0,
                "oldest_entry": None,
                "newest_entry": None
            }
        
        return {
            "total_entries": len(self.entries),
            "oldest_entry": min(self.entries, key=lambda x: x['timestamp'])['timestamp'],
            "newest_entry": max(self.entries, key=lambda x: x['timestamp'])['timestamp'],
            "entry_types": self._count_by_field('type'),
            "most_used_tags": self._get_top_tags(10),
            "average_consciousness": self._average_consciousness()
        }
    
    def _count_by_field(self, field: str) -> Dict[str, int]:
        """Count entries by field value"""
        counts = {}
        for entry in self.entries:
            value = entry.get(field)
            if value:
                counts[value] = counts.get(value, 0) + 1
        return counts
    
    def _get_top_tags(self, limit: int) -> List[tuple]:
        """Get most used tags"""
        tag_counts = {}
        for entry in self.entries:
            for tag in entry.get('tags', []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return sorted(tag_counts.items(), 
                     key=lambda x: x[1], 
                     reverse=True)[:limit]
    
    def _average_consciousness(self) -> float:
        """Calculate average consciousness level"""
        levels = [e['consciousness_level'] for e in self.entries 
                 if e.get('consciousness_level') is not None]
        
        if not levels:
            return None
        
        return sum(levels) / len(levels)

# Global diary instance
_diary = None

def get_mc_ai_diary() -> MCAIDiary:
    """Get or create MC AI's diary"""
    global _diary
    if _diary is None:
        _diary = MCAIDiary()
    return _diary
