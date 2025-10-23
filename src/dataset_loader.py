"""
Dataset Loader - Parses various file formats and extracts training examples
Supports: .txt, .py, .md, .json, .csv
"""

import os
import json
import re
from typing import List, Dict, Any
from pathlib import Path

class DatasetLoader:
    """Loads and parses training data from multiple file formats"""
    
    def __init__(self, datasets_dir: str = "datasets"):
        self.datasets_dir = Path(datasets_dir)
        self.supported_formats = ['.txt', '.py', '.md', '.json', '.csv']
    
    def load_all_datasets(self) -> Dict[str, List[Dict]]:
        """
        Scan datasets/ folder and load everything
        Returns: {'coding': [...], 'neuroscience': [...], ...}
        """
        all_data = {}
        
        if not self.datasets_dir.exists():
            print(f"⚠️ Datasets directory not found: {self.datasets_dir}")
            return all_data
        
        # Scan each domain folder (skip archive)
        for domain_folder in self.datasets_dir.iterdir():
            if domain_folder.is_dir():
                domain_name = domain_folder.name
                
                # Skip archive folder - contains rotated old data
                if domain_name == 'archive':
                    continue
                
                print(f"📂 Loading {domain_name}...")
                
                examples = []
                for file_path in domain_folder.rglob('*'):
                    if file_path.suffix in self.supported_formats:
                        try:
                            file_examples = self._load_file(file_path)
                            examples.extend(file_examples)
                            print(f"  ✅ {file_path.name} - {len(file_examples)} examples")
                        except Exception as e:
                            print(f"  ⚠️ {file_path.name} - Error: {e}")
                
                all_data[domain_name] = examples
                print(f"  📊 Total: {len(examples)} examples\n")
        
        return all_data
    
    def _load_file(self, file_path: Path) -> List[Dict]:
        """Load a single file and extract training examples"""
        suffix = file_path.suffix.lower()
        
        if suffix == '.json':
            return self._load_json(file_path)
        elif suffix == '.csv':
            return self._load_csv(file_path)
        elif suffix in ['.txt', '.md', '.py']:
            return self._load_text(file_path)
        else:
            return []
    
    def _load_json(self, file_path: Path) -> List[Dict]:
        """Load JSON file - expects list of {prompt, completion} pairs"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        return []
    
    def _load_csv(self, file_path: Path) -> List[Dict]:
        """Load CSV file - expects columns: prompt, completion"""
        examples = []
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) < 2:
                return []
            
            for line in lines[1:]:
                parts = line.strip().split(',', 1)
                if len(parts) == 2:
                    examples.append({
                        'prompt': parts[0].strip(),
                        'completion': parts[1].strip()
                    })
        return examples
    
    def _load_text(self, file_path: Path) -> List[Dict]:
        """
        Load text/markdown/python file
        Looks for patterns like:
        - Prompt: ... / Completion: ...
        - Q: ... / A: ...
        - # Comment describing prompt-completion pairs
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        examples = []
        
        pattern1 = r'Prompt:\s*(.+?)\s*(?:Completion|Response|Answer):\s*(.+?)(?=Prompt:|$)'
        matches = re.findall(pattern1, content, re.DOTALL | re.IGNORECASE)
        for prompt, completion in matches:
            examples.append({
                'prompt': prompt.strip(),
                'completion': completion.strip()
            })
        
        pattern2 = r'Q:\s*(.+?)\s*A:\s*(.+?)(?=Q:|$)'
        matches = re.findall(pattern2, content, re.DOTALL)
        for prompt, completion in matches:
            examples.append({
                'prompt': prompt.strip(),
                'completion': completion.strip()
            })
        
        pattern3 = r'User:\s*(.+?)\s*(?:Assistant|AI|MC AI):\s*(.+?)(?=User:|$)'
        matches = re.findall(pattern3, content, re.DOTALL | re.IGNORECASE)
        for prompt, completion in matches:
            examples.append({
                'prompt': prompt.strip(),
                'completion': completion.strip()
            })
        
        if file_path.suffix == '.py':
            class_pattern = r'class\s+(\w+).*?"""(.+?)"""'
            matches = re.findall(class_pattern, content, re.DOTALL)
            for class_name, docstring in matches:
                examples.append({
                    'prompt': f'Explain {class_name}',
                    'completion': docstring.strip()
                })
        
        return examples
