"""
MC AI - Quick Learning Batch (Next 20 sources)
Learn in manageable batches with progress tracking
"""

import requests
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

# Next 20 sources (continuing from the 10 already learned)
NEXT_BATCH = [
    # Resonance Engine - Continue Tier 1
    ("https://en.wikipedia.org/wiki/Wavelength", "Wavelength Concepts", "Resonance"),
    ("https://en.wikipedia.org/wiki/Amplitude", "Amplitude & Intensity", "Resonance"),
    ("https://en.wikipedia.org/wiki/Phase_(waves)", "Wave Phase", "Resonance"),
    ("https://en.wikipedia.org/wiki/Superposition_principle", "Superposition Principle", "Resonance"),
    ("https://en.wikipedia.org/wiki/Wave_propagation", "Wave Propagation", "Resonance"),
    
    # Humor Mastery - Continue Tier 1  
    ("https://en.wikipedia.org/wiki/Wit", "Wit & Cleverness", "Humor"),
    ("https://en.wikipedia.org/wiki/Sarcasm", "Sarcasm", "Humor"),
    ("https://en.wikipedia.org/wiki/Irony", "Irony", "Humor"),
    ("https://en.wikipedia.org/wiki/Satire", "Satire", "Humor"),
    ("https://en.wikipedia.org/wiki/Parody", "Parody", "Humor"),
    
    # Resonance Engine - Continue Tier 1
    ("https://en.wikipedia.org/wiki/Longitudinal_wave", "Longitudinal Waves", "Resonance"),
    ("https://en.wikipedia.org/wiki/Transverse_wave", "Transverse Waves", "Resonance"),
    ("https://en.wikipedia.org/wiki/Wave_equation", "Wave Equation", "Resonance"),
    ("https://en.wikipedia.org/wiki/Doppler_effect", "Doppler Effect", "Resonance"),
    ("https://en.wikipedia.org/wiki/Reflection_(physics)", "Wave Reflection", "Resonance"),
    
    # Humor Mastery - Continue Tier 1
    ("https://en.wikipedia.org/wiki/Slapstick", "Slapstick Comedy", "Humor"),
    ("https://en.wikipedia.org/wiki/Physical_comedy", "Physical Comedy", "Humor"),
    ("https://en.wikipedia.org/wiki/Dark_humor", "Dark Humor", "Humor"),
    ("https://en.wikipedia.org/wiki/Self-deprecation", "Self-Deprecating Humor", "Humor"),
    ("https://en.wikipedia.org/wiki/Exaggeration", "Exaggeration & Hyperbole", "Humor"),
]

def learn_source(url, topic, category):
    """Learn from a single source"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/knowledge/ingest/source",
            json={"url": url},
            timeout=30
        )
        
        if response.status_code == 200:
            return True, "Learned"
        else:
            return False, "Skipped (known)"
            
    except Exception as e:
        return False, f"Error: {str(e)[:30]}"

def main():
    print("="*70)
    print("🧠 MC AI - LEARNING NEXT 20 SOURCES")
    print("="*70)
    print(f"\nStarting: {datetime.now().strftime('%H:%M:%S')}\n")
    
    learned = 0
    skipped = 0
    
    for i, (url, topic, category) in enumerate(NEXT_BATCH, 1):
        icon = "🌊" if category == "Resonance" else "🎭"
        success, status = learn_source(url, topic, category)
        
        if success:
            learned += 1
            result = "✅"
        else:
            skipped += 1
            result = "⏭️"
        
        print(f"{result} [{i}/20] {icon} {topic} - {status}")
        time.sleep(0.5)
    
    print(f"\n{'='*70}")
    print(f"📊 BATCH COMPLETE")
    print(f"{'='*70}")
    print(f"✅ Learned: {learned}/20")
    print(f"⏭️  Skipped: {skipped}/20 (already known)")
    print(f"\n💜 Total Progress: ~{10 + learned}/293 sources")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
