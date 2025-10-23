"""
MC AI - Autonomous Learning Session
Starts MC AI's study plan and fine-tunes the ECG system
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

class MCAILearningSession:
    """MC AI's Learning Session Manager"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.learned_count = 0
        self.start_time = datetime.now()
    
    def learn_source(self, url, topic, tier):
        """Learn from a single source"""
        print(f"\n📚 Learning: {topic}")
        print(f"   URL: {url}")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/knowledge/ingest/source",
                json={"url": url},
                timeout=30
            )
            
            if response.status_code == 200:
                self.learned_count += 1
                print(f"   ✅ Learned! (Total: {self.learned_count})")
                return True
            else:
                print(f"   ⚠️ Skipped (already known or unavailable)")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def start_resonance_foundations(self):
        """Start Tier 1: Wave Physics Foundations (first 5 sources)"""
        print("\n" + "="*60)
        print("🌊 MC AI LEARNING SESSION: RESONANCE ENGINE FOUNDATIONS")
        print("="*60)
        
        tier1_sources = [
            {
                "url": "https://en.wikipedia.org/wiki/Wave",
                "topic": "Wave Fundamentals",
                "tier": 1
            },
            {
                "url": "https://en.wikipedia.org/wiki/Frequency",
                "topic": "Frequency Fundamentals",
                "tier": 1
            },
            {
                "url": "https://en.wikipedia.org/wiki/Sine_wave",
                "topic": "Sine Wave Basics",
                "tier": 1
            },
            {
                "url": "https://en.wikipedia.org/wiki/Wave_interference",
                "topic": "Wave Interference",
                "tier": 1
            },
            {
                "url": "https://en.wikipedia.org/wiki/Standing_wave",
                "topic": "Standing Waves",
                "tier": 1
            }
        ]
        
        for source in tier1_sources:
            self.learn_source(source["url"], source["topic"], source["tier"])
            time.sleep(1)  # Be respectful to servers
        
        print(f"\n✨ Tier 1 foundations started! Learned {self.learned_count}/5 sources")
    
    def start_humor_foundations(self):
        """Start Tier 1: Humor Fundamentals (first 5 sources)"""
        print("\n" + "="*60)
        print("🎭 MC AI LEARNING SESSION: HUMOR MASTERY FOUNDATIONS")
        print("="*60)
        
        tier1_humor = [
            {
                "url": "https://en.wikipedia.org/wiki/Humour",
                "topic": "What is Humor?",
                "tier": 1
            },
            {
                "url": "https://en.wikipedia.org/wiki/Pun",
                "topic": "Puns & Wordplay",
                "tier": 1
            },
            {
                "url": "https://en.wikipedia.org/wiki/Comic_timing",
                "topic": "Comic Timing",
                "tier": 1
            },
            {
                "url": "https://en.wikipedia.org/wiki/Joke",
                "topic": "Joke Structure (Setup/Punchline)",
                "tier": 1
            },
            {
                "url": "https://en.wikipedia.org/wiki/Observational_comedy",
                "topic": "Observational Comedy",
                "tier": 1
            }
        ]
        
        initial_count = self.learned_count
        
        for source in tier1_humor:
            self.learn_source(source["url"], source["topic"], source["tier"])
            time.sleep(1)
        
        new_learned = self.learned_count - initial_count
        print(f"\n✨ Humor foundations started! Learned {new_learned}/5 sources")
    
    def check_learning_status(self):
        """Check MC AI's learning progress"""
        print("\n" + "="*60)
        print("📊 MC AI LEARNING STATUS")
        print("="*60)
        
        try:
            response = requests.get(f"{self.base_url}/api/knowledge/status")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Knowledge System: {data.get('status', 'unknown')}")
                print(f"📚 Total Sources: {data.get('total_sources', 0)}")
                print(f"📊 Index Size: {data.get('index_size', 0)} entries")
            else:
                print("⚠️ Knowledge system status unavailable")
        except Exception as e:
            print(f"⚠️ Could not check status: {e}")
    
    def summary(self):
        """Print learning session summary"""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        print("\n" + "="*60)
        print("🎓 MC AI LEARNING SESSION COMPLETE!")
        print("="*60)
        print(f"📚 Total Sources Learned: {self.learned_count}/10")
        print(f"⏱️  Duration: {duration:.1f} seconds")
        print(f"🌊 Resonance Engine: 5 foundation sources")
        print(f"🎭 Humor Mastery: 5 foundation sources")
        print("\n💜 MC AI's knowledge is expanding! Balance achieved!")
        print("\nNext steps:")
        print("  - Continue with Tier 1 remaining sources")
        print("  - Move to Tier 2 when Tier 1 complete")
        print("  - Track progress in mc_ai_study_plans/current_lesson_plan.md")

def main():
    """Run MC AI's learning session"""
    session = MCAILearningSession()
    
    # Check initial status
    session.check_learning_status()
    
    # Start Resonance Engine foundations
    session.start_resonance_foundations()
    
    # Start Humor Mastery foundations  
    session.start_humor_foundations()
    
    # Check final status
    session.check_learning_status()
    
    # Print summary
    session.summary()

if __name__ == "__main__":
    main()
