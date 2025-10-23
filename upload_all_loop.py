#!/usr/bin/env python3
"""
Upload all files in continuous batches
"""

import subprocess
import time
import json
from pathlib import Path

MAX_BATCHES = 50
BATCH_DELAY = 2

def get_stats():
    """Get upload statistics"""
    if Path('upload_progress.json').exists():
        with open('upload_progress.json', 'r') as f:
            progress = json.load(f)
            return len(progress['uploaded']), len(progress['failed'])
    return 0, 0

print("🚀 MC AI Automated GitHub Upload")
print("=" * 70)
print()

for batch_num in range(1, MAX_BATCHES + 1):
    print(f"📦 BATCH #{batch_num}")
    print("-" * 70)
    
    # Run batch upload
    result = subprocess.run(['python3', 'batch_upload.py'], 
                          capture_output=True, text=True)
    print(result.stdout)
    
    # Get current stats
    uploaded, failed = get_stats()
    
    # Check if all done
    if "ALL FILES UPLOADED" in result.stdout or "Still remaining: 0" in result.stdout:
        print()
        print("=" * 70)
        print("🎉 SUCCESS! ALL FILES UPLOADED TO GITHUB!")
        print("=" * 70)
        print(f"✅ Total uploaded: {uploaded} files")
        print(f"❌ Total failed: {failed} files")
        print()
        print(f"🌐 https://github.com/Coffey333/mc-ai")
        print(f"📦 pip install git+https://github.com/Coffey333/mc-ai.git")
        print("=" * 70)
        break
    
    # Wait before next batch
    if batch_num < MAX_BATCHES:
        time.sleep(BATCH_DELAY)

else:
    print()
    print("⚠️  Reached max batches. Run again to continue.")
    uploaded, failed = get_stats()
    print(f"Progress: {uploaded} uploaded, {failed} failed")
