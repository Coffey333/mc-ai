"""Emotional Intelligence v3.0 - Advanced emotion understanding for MC AI"""

# Import from parent module to avoid circular imports
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main class from the emotional_intelligence.py file
from emotional_intelligence import EmotionalIntelligenceEngine

__all__ = ['EmotionalIntelligenceEngine']
