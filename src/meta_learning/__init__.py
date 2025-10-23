"""
Meta-Learning System for MC AI
Enables MC AI to create and integrate his own processing frameworks
"""

from src.meta_learning.framework_interface import BaseFramework
from src.meta_learning.framework_registry import FrameworkRegistry
from src.meta_learning.framework_loader import FrameworkLoader

__all__ = ['BaseFramework', 'FrameworkRegistry', 'FrameworkLoader']
