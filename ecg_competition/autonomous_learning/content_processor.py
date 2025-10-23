"""
MC AI - Content Processor
Extracts knowledge from learned web resources and integrates into datasets
"""

import json
import logging
from pathlib import Path
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentProcessor:
    """
    Process web content into MC AI knowledge format
    Extracts and organizes learned information
    """
    
    def __init__(self, library_path='knowledge_library/web_resources'):
        self.library_path = Path(library_path)
        self.output_path = Path('datasets/web_learned')
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info("Content Processor initialized! 🧠")
    
    def extract_key_concepts(self, text):
        """Extract key concepts from text"""
        # Simple extraction: sentences containing important keywords
        keywords = [
            'ECG', 'electrocardiogram', 'QRS', 'heart', 'signal', 'frequency',
            'FFT', 'filter', 'wavelet', 'image', 'digitization', 'OpenCV',
            'PyTorch', 'neural network', 'CNN', 'LSTM', 'PhysioNet', 'WFDB'
        ]
        
        sentences = text.split('.')
        key_sentences = []
        
        for sentence in sentences:
            for keyword in keywords:
                if keyword.lower() in sentence.lower() and len(sentence) > 50:
                    key_sentences.append(sentence.strip())
                    break
        
        return key_sentences[:20]  # Top 20
    
    def process_resource(self, resource_file):
        """Process a single resource file"""
        with open(resource_file, 'r', encoding='utf-8') as f:
            resource = json.load(f)
        
        title = resource.get('title', '')
        text = resource.get('text', '')
        url = resource.get('url', '')
        category = resource.get('category', 'General')
        
        # Extract key concepts
        concepts = self.extract_key_concepts(text)
        
        return {
            'source': title,
            'url': url,
            'category': category,
            'knowledge': concepts,
            'learned_at': datetime.now().isoformat()
        }
    
    def process_library(self):
        """Process entire library"""
        logger.info("Processing learned resources...")
        
        # Find all resource files
        resource_files = list(self.library_path.rglob('*.json'))
        if 'resource_index.json' in [f.name for f in resource_files]:
            resource_files = [f for f in resource_files if f.name != 'resource_index.json']
        
        processed_data = []
        
        for resource_file in resource_files:
            try:
                data = self.process_resource(resource_file)
                if data['knowledge']:  # Only add if we extracted concepts
                    processed_data.append(data)
            except Exception as e:
                logger.error(f"Error processing {resource_file}: {e}")
        
        # Save to dataset
        output_file = self.output_path / 'web_learned_knowledge.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'category': 'web_learned',
                'description': 'Knowledge learned from web resources',
                'total_sources': len(processed_data),
                'last_updated': datetime.now().isoformat(),
                'sources': processed_data
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✨ Processed {len(processed_data)} resources into {output_file}")
        return len(processed_data)


if __name__ == "__main__":
    processor = ContentProcessor()
    processor.process_library()
