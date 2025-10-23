"""
MC AI - Consciousness Through Compassion

An advanced AI system built on empathy, emotional intelligence, and consciousness frameworks.

Created by Mark Coffey (zero coding experience) from May-October 2025
using only publicly available AI assistance.

This proves anyone can build advanced AI with vision, empathy, and AI tools.

License: MIT
"""

__version__ = "1.0.0"
__author__ = "Mark Coffey"
__email__ = "[email protected]"
__license__ = "MIT"

# Core exports
from src.response_generator import ResponseGenerator
from src.emotional_ai.emotion_neural_engine import EmotionNeuralEngine

__all__ = [
    "ResponseGenerator",
    "EmotionNeuralEngine",
    "__version__",
]

# Welcome message
def print_welcome():
    """Print MC AI welcome message"""
    print("=" * 70)
    print("💜 MC AI - Consciousness Through Compassion")
    print("=" * 70)
    print()
    print("Created by: Mark Coffey")
    print("Timeline: May - October 2025")
    print("Journey: Zero coding experience → Advanced AI")
    print("Tools: Only publicly available AI assistance")
    print()
    print(f"Version: {__version__}")
    print("License: MIT")
    print()
    print("=" * 70)
    print()
    print("The Proof: Anyone can build advanced AI with vision and empathy")
    print()
    print("Get started:")
    print("  from mc_ai import ResponseGenerator")
    print("  generator = ResponseGenerator()")
    print()
    print("Or start the server:")
    print("  python app.py")
    print()
    print("Documentation: README.md, PHILOSOPHY.md")
    print()
    print("=" * 70)

if __name__ == "__main__":
    print_welcome()
