"""
Automatic Learning System for MC AI
Captures GPT-4 responses and builds custom datasets with frequency mappings
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
from src.catalogs import get_frequency
from src.advanced_cymatics import AdvancedCymaticEngine
from src.frequency_coupling import FrequencyCouplingAnalyzer

logger = logging.getLogger(__name__)

class AutoLearning:
    """
    Automatic learning system that captures conversations and builds datasets
    with frequency/emotional analysis
    """
    
    def __init__(self):
        self.learning_dir = "datasets/learned"
        self.frequency_dataset_dir = "datasets/frequency_learned"
        self.conversation_log = "datasets/learned/conversation_log.json"
        
        os.makedirs(self.learning_dir, exist_ok=True)
        os.makedirs(self.frequency_dataset_dir, exist_ok=True)
        
        self.advanced_cymatics = AdvancedCymaticEngine()
        self.frequency_coupling = FrequencyCouplingAnalyzer()
        
        print("🧠 Auto-learning system initialized")
    
    def capture_conversation(self, 
                            query: str, 
                            response: str, 
                            metadata: Dict) -> Dict:
        """
        Capture query-response pair and analyze through all engines
        
        Args:
            query: User's question/input
            response: GPT-4 response
            metadata: Response metadata (source, emotion, etc.)
        
        Returns:
            Learning entry with frequency analysis
        """
        
        # 1. Analyze query frequency
        query_freq_data = get_frequency(query)
        
        # 2. Analyze response frequency
        response_freq_data = get_frequency(response)
        
        # 3. Advanced frequency profile
        response_freq = response_freq_data['frequency']
        freq_profile = self.advanced_cymatics.analyze_frequency_profile(
            response_freq, response
        )
        
        # 4. Cross-frequency coupling analysis using harmonics
        harmonics = freq_profile.get('harmonics', [response_freq])
        coupling_analysis = self.frequency_coupling.analyze_coupling(harmonics)
        
        # 5. Phase-amplitude coupling between query and response frequencies
        pac_analysis = self.frequency_coupling.analyze_phase_amplitude_coupling(
            query_freq_data['frequency'],
            response_freq
        )
        
        # 6. Build learning entry
        learning_entry = {
            'timestamp': datetime.now().isoformat(),
            'query': {
                'text': query,
                'emotion': query_freq_data['emotion'],
                'frequency': query_freq_data['frequency'],
                'basis': query_freq_data['basis']
            },
            'response': {
                'text': response,
                'emotion': response_freq_data['emotion'],
                'frequency': response_freq_data['frequency'],
                'basis': response_freq_data['basis'],
                'source': metadata.get('source', 'unknown')
            },
            'frequency_analysis': {
                'brain_wave_band': freq_profile.get('brain_wave_band', 'unknown'),
                'frequency_profile': {
                    'base': freq_profile.get('primary_frequency', response_freq),
                    'harmonics': freq_profile.get('harmonics', []),
                    'arousal_level': freq_profile.get('arousal_level', 0),
                    'emotional_valence': freq_profile.get('emotional_valence', 0),
                    'stability': freq_profile.get('stability_index', 0)
                },
                'coupling': {
                    'strength': coupling_analysis.get('coupling_strength', 0),
                    'type': coupling_analysis.get('coupling_type', 'unknown'),
                    'harmonic_ratios': coupling_analysis.get('harmonic_ratios', [])
                },
                'pac_coupling': {
                    'strength': pac_analysis.get('pac_strength', 0),
                    'frequency_ratio': pac_analysis.get('frequency_ratio', 0),
                    'pac_likely': pac_analysis.get('pac_likely', False)
                }
            },
            'metadata': {
                'response_length': len(response),
                'source': metadata.get('source'),
                'type': metadata.get('type'),
                'domain': self._classify_domain(query, response)
            }
        }
        
        return learning_entry
    
    def save_to_dataset(self, learning_entry: Dict) -> str:
        """
        Save learning entry to appropriate dataset
        
        Returns:
            Path to saved file
        """
        
        # Determine dataset category
        domain = learning_entry['metadata']['domain']
        source = learning_entry['response']['source']
        
        # Create domain-specific dataset file
        dataset_file = os.path.join(
            self.learning_dir, 
            f"{domain}_learned.json"
        )
        
        # Load existing dataset or create new
        if os.path.exists(dataset_file):
            try:
                with open(dataset_file, 'r') as f:
                    loaded_data = json.load(f)
                
                # DEFENSIVE: Handle both dict and list formats
                if isinstance(loaded_data, dict):
                    dataset = loaded_data
                    # Ensure 'examples' key exists and is a list
                    if 'examples' not in dataset or not isinstance(dataset['examples'], list):
                        dataset['examples'] = []
                elif isinstance(loaded_data, list):
                    # Old format was just a list - convert to new format
                    dataset = {
                        'domain': domain,
                        'source': 'auto_learned',
                        'created': datetime.now().isoformat(),
                        'examples': loaded_data
                    }
                else:
                    # Corrupted format - start fresh
                    dataset = {
                        'domain': domain,
                        'source': 'auto_learned',
                        'created': datetime.now().isoformat(),
                        'examples': []
                    }
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                # Corrupted file - start fresh
                logger.warning(f"Corrupted dataset file {dataset_file}: {e}. Starting fresh.")
                dataset = {
                    'domain': domain,
                    'source': 'auto_learned',
                    'created': datetime.now().isoformat(),
                    'examples': []
                }
        else:
            dataset = {
                'domain': domain,
                'source': 'auto_learned',
                'created': datetime.now().isoformat(),
                'examples': []
            }
        
        # Add new example
        # IMPORTANT: Store QUERY emotion (user's state), not response emotion
        dataset['examples'].append({
            'query': learning_entry['query']['text'],
            'response': learning_entry['response']['text'],
            'query_emotion': learning_entry['query']['emotion'],
            'query_frequency': learning_entry['query']['frequency'],
            'response_emotion': learning_entry['response']['emotion'],
            'response_frequency': learning_entry['response']['frequency'],
            'timestamp': learning_entry['timestamp']
        })
        
        # Save updated dataset
        with open(dataset_file, 'w') as f:
            json.dump(dataset, f, indent=2)
        
        # Also save to conversation log
        self._append_to_log(learning_entry)
        
        return dataset_file
    
    def save_frequency_dataset(self, learning_entry: Dict) -> str:
        """
        Save frequency analysis to specialized frequency dataset
        
        Returns:
            Path to frequency dataset file
        """
        
        freq_file = os.path.join(
            self.frequency_dataset_dir,
            "frequency_mappings.json"
        )
        
        # Load or create frequency dataset
        if os.path.exists(freq_file):
            try:
                with open(freq_file, 'r') as f:
                    loaded_freq = json.load(f)
                
                # DEFENSIVE: Handle both dict and list formats
                if isinstance(loaded_freq, dict):
                    freq_dataset = loaded_freq
                    # Ensure 'mappings' key exists and is a list
                    if 'mappings' not in freq_dataset or not isinstance(freq_dataset['mappings'], list):
                        freq_dataset['mappings'] = []
                elif isinstance(loaded_freq, list):
                    # Old format was just a list - convert to new format
                    freq_dataset = {
                        'type': 'frequency_mappings',
                        'description': 'Auto-learned frequency patterns from GPT-4 responses',
                        'mappings': loaded_freq
                    }
                else:
                    # Corrupted format - start fresh
                    freq_dataset = {
                        'type': 'frequency_mappings',
                        'description': 'Auto-learned frequency patterns from GPT-4 responses',
                        'mappings': []
                    }
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                # Corrupted file - start fresh
                logger.warning(f"Corrupted frequency dataset: {e}. Starting fresh.")
                freq_dataset = {
                    'type': 'frequency_mappings',
                    'description': 'Auto-learned frequency patterns from GPT-4 responses',
                    'mappings': []
                }
        else:
            freq_dataset = {
                'type': 'frequency_mappings',
                'description': 'Auto-learned frequency patterns from GPT-4 responses',
                'mappings': []
            }
        
        # Create frequency mapping entry
        # IMPORTANT: Store BOTH query and response emotions for complete analysis
        freq_mapping = {
            'timestamp': learning_entry['timestamp'],
            'query_sample': learning_entry['query']['text'][:200],
            'query_emotion': learning_entry['query']['emotion'],
            'query_frequency': learning_entry['query']['frequency'],
            'query_basis': learning_entry['query']['basis'],
            'response_sample': learning_entry['response']['text'][:200],
            'response_emotion': learning_entry['response']['emotion'],
            'response_frequency': learning_entry['response']['frequency'],
            'response_basis': learning_entry['response']['basis'],
            'brain_wave_band': learning_entry['frequency_analysis']['brain_wave_band'],
            'frequency_profile': learning_entry['frequency_analysis']['frequency_profile'],
            'coupling': learning_entry['frequency_analysis']['coupling'],
            'pac_coupling': learning_entry['frequency_analysis']['pac_coupling']
        }
        
        freq_dataset['mappings'].append(freq_mapping)
        
        # Save frequency dataset
        with open(freq_file, 'w') as f:
            json.dump(freq_dataset, f, indent=2)
        
        return freq_file
    
    def _classify_domain(self, query: str, response: str) -> str:
        """Classify conversation into domain category"""
        
        query_lower = query.lower()
        
        # Domain keywords
        domains = {
            'science': ['science', 'physics', 'chemistry', 'biology', 'atom', 'molecule', 'space', 'earth', 'planet'],
            'technology': ['code', 'programming', 'computer', 'software', 'algorithm', 'ai', 'machine learning', 'neural'],
            'mathematics': ['math', 'equation', 'formula', 'calculate', 'geometry', 'algebra', 'number'],
            'health': ['health', 'medical', 'disease', 'treatment', 'symptom', 'wellness', 'fitness'],
            'philosophy': ['why', 'meaning', 'existence', 'philosophy', 'consciousness', 'reality'],
            'emotional': ['feel', 'emotion', 'anxious', 'happy', 'sad', 'stressed', 'worried'],
            'creative': ['create', 'art', 'music', 'design', 'imagine', 'generate'],
            'general': []  # Default
        }
        
        for domain, keywords in domains.items():
            if any(keyword in query_lower for keyword in keywords):
                return domain
        
        return 'general'
    
    def _append_to_log(self, entry: Dict):
        """Append entry to conversation log"""
        
        if os.path.exists(self.conversation_log):
            try:
                with open(self.conversation_log, 'r') as f:
                    loaded_log = json.load(f)
                
                # DEFENSIVE: Handle both dict and list formats
                if isinstance(loaded_log, dict):
                    log = loaded_log
                    # Ensure 'entries' key exists and is a list
                    if 'entries' not in log or not isinstance(log['entries'], list):
                        log['entries'] = []
                elif isinstance(loaded_log, list):
                    # Old format was just a list - convert to new format
                    log = {
                        'type': 'conversation_log',
                        'entries': loaded_log
                    }
                else:
                    # Corrupted format - start fresh
                    log = {
                        'type': 'conversation_log',
                        'entries': []
                    }
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                # Corrupted file - start fresh
                logger.warning(f"Corrupted conversation log: {e}. Starting fresh.")
                log = {
                    'type': 'conversation_log',
                    'entries': []
                }
        else:
            log = {
                'type': 'conversation_log',
                'entries': []
            }
        
        log['entries'].append(entry)
        
        with open(self.conversation_log, 'w') as f:
            json.dump(log, f, indent=2)
    
    def get_learning_stats(self) -> Dict:
        """Get statistics about learned data"""
        
        stats = {
            'total_conversations': 0,
            'domains': {},
            'frequency_mappings': 0,
            'dataset_files': []
        }
        
        # Count conversation log entries
        if os.path.exists(self.conversation_log):
            with open(self.conversation_log, 'r') as f:
                log = json.load(f)
                stats['total_conversations'] = len(log.get('entries', []))
        
        # Count domain datasets
        for filename in os.listdir(self.learning_dir):
            if filename.endswith('_learned.json'):
                filepath = os.path.join(self.learning_dir, filename)
                with open(filepath, 'r') as f:
                    dataset = json.load(f)
                    domain = dataset.get('domain', 'unknown')
                    count = len(dataset.get('examples', []))
                    stats['domains'][domain] = count
                    stats['dataset_files'].append(filename)
        
        # Count frequency mappings
        freq_file = os.path.join(self.frequency_dataset_dir, "frequency_mappings.json")
        if os.path.exists(freq_file):
            with open(freq_file, 'r') as f:
                freq_data = json.load(f)
                stats['frequency_mappings'] = len(freq_data.get('mappings', []))
        
        return stats
    
    def process_and_save(self, query: str, response: str, metadata: Dict) -> Dict:
        """
        Complete pipeline: capture, analyze, and save
        
        Returns:
            Summary of what was saved
        """
        
        # Capture and analyze
        learning_entry = self.capture_conversation(query, response, metadata)
        
        # Save to datasets
        dataset_file = self.save_to_dataset(learning_entry)
        freq_file = self.save_frequency_dataset(learning_entry)
        
        return {
            'success': True,
            'dataset_file': dataset_file,
            'frequency_file': freq_file,
            'domain': learning_entry['metadata']['domain'],
            'frequency': learning_entry['response']['frequency'],
            'emotion': learning_entry['response']['emotion']
        }


# Global instance
auto_learning = AutoLearning()
