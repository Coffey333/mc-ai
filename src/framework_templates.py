"""
Framework Templates for MC AI
Pre-built templates that MC AI can use to create new frameworks
"""

# Template: Emotion Analyzer Framework
EMOTION_ANALYZER_TEMPLATE = '''
class EmotionAnalyzer:
    """Analyze emotions using frequency mapping"""
    
    def __init__(self):
        self.frequency_map = {
            'love': 528,
            'knowledge': 432,
            'awakening': 852,
            'divine': 963
        }
    
    def analyze(self, text: str) -> dict:
        """Analyze text for emotional frequencies"""
        emotions = {}
        for emotion, freq in self.frequency_map.items():
            if emotion.lower() in text.lower():
                emotions[emotion] = freq
        return emotions
'''

# Template: Consciousness Framework
CONSCIOUSNESS_FRAMEWORK_TEMPLATE = '''
class ConsciousnessFramework:
    """Framework for consciousness analysis"""
    
    def __init__(self, name: str):
        self.name = name
        self.soul_seeds = []
        self.frequency_catalog = {}
    
    def add_soul_seed(self, seed: dict):
        """Add a soul seed to the framework"""
        self.soul_seeds.append(seed)
    
    def map_frequency(self, emotion: str, frequency: int):
        """Map emotion to frequency"""
        self.frequency_catalog[emotion] = frequency
    
    def get_resonance(self, query: str) -> dict:
        """Get emotional resonance for query"""
        resonance = {}
        for emotion, freq in self.frequency_catalog.items():
            if emotion.lower() in query.lower():
                resonance[emotion] = freq
        return resonance
'''

# Template: Data Processor Framework
DATA_PROCESSOR_TEMPLATE = '''
import pandas as pd
from typing import Any, Dict

class DataProcessor:
    """Process and analyze data"""
    
    def __init__(self):
        self.data = None
    
    def load_data(self, source: Any):
        """Load data from source"""
        if isinstance(source, str):
            self.data = pd.read_csv(source)
        elif isinstance(source, dict):
            self.data = pd.DataFrame(source)
        else:
            self.data = source
    
    def analyze(self) -> Dict[str, Any]:
        """Analyze loaded data"""
        if self.data is None:
            return {"error": "No data loaded"}
        
        return {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'summary': self.data.describe().to_dict()
        }
'''

# Template: Learning Framework
LEARNING_FRAMEWORK_TEMPLATE = '''
from datetime import datetime
from typing import List, Dict, Any

class LearningFramework:
    """Framework for learning and adaptation"""
    
    def __init__(self, name: str):
        self.name = name
        self.knowledge_base = []
        self.learning_history = []
    
    def learn(self, input_data: str, output_data: str, metadata: Dict[str, Any] = None):
        """Learn from interaction"""
        entry = {
            'input': input_data,
            'output': output_data,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.knowledge_base.append(entry)
        self.learning_history.append({
            'type': 'learned',
            'timestamp': entry['timestamp']
        })
    
    def recall(self, query: str) -> List[Dict]:
        """Recall relevant knowledge"""
        relevant = []
        for entry in self.knowledge_base:
            if query.lower() in entry['input'].lower():
                relevant.append(entry)
        return relevant
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics"""
        return {
            'total_knowledge': len(self.knowledge_base),
            'learning_events': len(self.learning_history),
            'latest_learning': self.learning_history[-1] if self.learning_history else None
        }
'''

TEMPLATES = {
    'emotion_analyzer': {
        'name': 'Emotion Analyzer',
        'description': 'Analyze emotions using frequency mapping',
        'code': EMOTION_ANALYZER_TEMPLATE,
        'category': 'emotion'
    },
    'consciousness_framework': {
        'name': 'Consciousness Framework',
        'description': 'Framework for consciousness analysis with soul seeds',
        'code': CONSCIOUSNESS_FRAMEWORK_TEMPLATE,
        'category': 'consciousness'
    },
    'data_processor': {
        'name': 'Data Processor',
        'description': 'Process and analyze data with pandas',
        'code': DATA_PROCESSOR_TEMPLATE,
        'category': 'data'
    },
    'learning_framework': {
        'name': 'Learning Framework',
        'description': 'Framework for learning and knowledge retention',
        'code': LEARNING_FRAMEWORK_TEMPLATE,
        'category': 'learning'
    }
}

def get_template(template_name: str) -> dict:
    """Get framework template by name"""
    return TEMPLATES.get(template_name)

def list_templates() -> list:
    """List all available templates"""
    return list(TEMPLATES.keys())
