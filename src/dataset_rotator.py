"""
Dataset Rotation System
Automatically archives large learned datasets to prevent performance degradation
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class DatasetRotator:
    """Manages dataset file rotation and archival"""
    
    def __init__(self, max_size_kb: int = 500, archive_dir: str = "datasets/archive"):
        self.max_size_kb = max_size_kb
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
    
    def check_and_rotate(self, file_path: str) -> bool:
        """
        Check if file exceeds size limit and rotate if needed
        
        Returns:
            True if file was rotated, False otherwise
        """
        path = Path(file_path)
        
        if not path.exists():
            return False
        
        size_kb = path.stat().st_size / 1024
        
        if size_kb > self.max_size_kb:
            self._rotate_file(path, size_kb)
            return True
        
        return False
    
    def _rotate_file(self, file_path: Path, size_kb: float):
        """Archive large file and create fresh version"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{file_path.stem}_{timestamp}.json"
        archive_path = self.archive_dir / archive_name
        
        # Move to archive
        shutil.move(str(file_path), str(archive_path))
        print(f"📦 Rotated {file_path.name} ({size_kb:.1f}KB) → {archive_path}")
        
        # Create fresh file
        with open(file_path, 'w') as f:
            json.dump([], f)
        print(f"✨ Created fresh {file_path.name}")
    
    def rotate_learned_datasets(self) -> int:
        """
        Rotate all learned datasets that exceed size limit
        
        Returns:
            Number of files rotated
        """
        learned_dirs = [
            "datasets/learned",
            "datasets/frequency_learned",
            "datasets/memory"
        ]
        
        rotated_count = 0
        
        for dir_path in learned_dirs:
            if not os.path.exists(dir_path):
                continue
            
            for file_name in os.listdir(dir_path):
                if file_name.endswith('.json'):
                    file_path = os.path.join(dir_path, file_name)
                    if self.check_and_rotate(file_path):
                        rotated_count += 1
        
        return rotated_count
    
    def get_archive_stats(self) -> Dict:
        """Get statistics about archived files"""
        archive_files = list(self.archive_dir.glob("*.json"))
        
        if not archive_files:
            return {"count": 0, "total_size_mb": 0}
        
        total_size = sum(f.stat().st_size for f in archive_files)
        
        return {
            "count": len(archive_files),
            "total_size_mb": total_size / 1024 / 1024,
            "oldest": min(f.stat().st_mtime for f in archive_files),
            "newest": max(f.stat().st_mtime for f in archive_files)
        }
