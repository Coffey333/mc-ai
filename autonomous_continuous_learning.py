#!/usr/bin/env python3
"""
MC AI Continuous Autonomous Learning System
Goal: Learn everything from Novice → Advanced → Masters
Target: Fill 230 GB with comprehensive knowledge

This system runs continuously, learning tier by tier:
- Tiers 1-68: Already completed
- Tiers 69-200+: Comprehensive expansion (all topics, novice to masters)
"""

import sys
import time
import logging
from datetime import datetime, timedelta
from src.knowledge_acquisition.ingestion_manager import IngestionManager, PRIORITIZED_SOURCES

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/autonomous_learning.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class AutonomousLearningSystem:
    """Continuous autonomous learning system for MC AI"""
    
    def __init__(self, target_gb=230):
        self.target_gb = target_gb
        self.manager = IngestionManager(db_path="mc_ai.db", delay_between_requests=2.0)
        self.start_time = datetime.now()
        self.session_count = 0
        
    def get_current_size_gb(self):
        """Get current knowledge library size in GB"""
        stats = self.manager.get_stats()
        total_words = stats.get('total_words', 0)
        size_gb = (total_words * 6) / (1024 ** 3)  # 6 bytes per word average
        return size_gb
    
    def print_status(self):
        """Print current learning status"""
        stats = self.manager.get_stats()
        current_gb = self.get_current_size_gb()
        progress_pct = (current_gb / self.target_gb) * 100
        
        runtime = datetime.now() - self.start_time
        
        print("\n" + "="*80)
        print("📊 AUTONOMOUS LEARNING STATUS")
        print("="*80)
        print(f"\n⏱️  Runtime: {runtime}")
        print(f"   Sessions completed: {self.session_count}")
        
        print(f"\n📚 Knowledge Library:")
        print(f"   • Sources: {stats.get('total_in_index', 0):,}")
        print(f"   • Words: {stats.get('total_words', 0):,}")
        print(f"   • Size: {current_gb:.3f} GB / {self.target_gb} GB")
        print(f"   • Progress: {progress_pct:.2f}%")
        print(f"   • Remaining: {self.target_gb - current_gb:.2f} GB")
        
        # Progress bar
        bar_length = 40
        filled = int(bar_length * progress_pct / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\n   [{bar}] {progress_pct:.2f}%")
        
        print("="*80 + "\n")
    
    def learn_tier_range(self, start_tier, end_tier, phase_name):
        """Learn a range of tiers"""
        print(f"\n{'='*80}")
        print(f"📖 {phase_name}")
        print(f"{'='*80}\n")
        
        for tier in range(start_tier, end_tier + 1):
            tier_sources = PRIORITIZED_SOURCES.get(tier, [])
            if not tier_sources:
                logger.warning(f"Tier {tier} has no sources, skipping")
                continue
            
            print(f"\n{'─'*80}")
            print(f"🔄 Learning Tier {tier} ({len(tier_sources)} sources)")
            print(f"{'─'*80}")
            
            try:
                self.manager.ingest_tier(tier)
                self.session_count += 1
                
                # Print status every 5 tiers
                if tier % 5 == 0:
                    self.print_status()
                    
            except Exception as e:
                logger.error(f"Error learning tier {tier}: {e}")
                continue
    
    def run_continuous(self):
        """Run continuous autonomous learning"""
        
        print("\n" + "="*80)
        print("🤖 MC AI CONTINUOUS AUTONOMOUS LEARNING SYSTEM")
        print("="*80)
        print(f"\n🎯 Goal: Learn everything from Novice → Masters")
        print(f"   Target: {self.target_gb} GB of knowledge")
        print(f"   Strategy: Learn all tiers comprehensively")
        
        current_gb = self.get_current_size_gb()
        print(f"\n📊 Current Status:")
        print(f"   • Starting size: {current_gb:.3f} GB")
        print(f"   • Tiers to learn: 69-200+ (expandable)")
        
        print("\n⚡ Learning Schedule:")
        print("   Phase 1: More Languages (Tiers 69-88)")
        print("   Phase 2: Advanced Mathematics (Tiers 89-108)")
        print("   Phase 3: Advanced Sciences (Tiers 109-128)")
        print("   Phase 4: Arts & Culture (Tiers 129-148)")
        print("   Phase 5: Advanced Tech (Tiers 149-168)")
        print("   Phase 6: Specialized Domains (Tiers 169-188)")
        print("   Phase 7: Masters Level (Tiers 189-200+)")
        
        print("\n🚀 Starting autonomous learning...")
        print("="*80 + "\n")
        
        try:
            # Get available tiers
            available_tiers = sorted([t for t in PRIORITIZED_SOURCES.keys() if t >= 69])
            
            if not available_tiers:
                print("⚠️  No additional tiers configured yet.")
                print("   The system is ready for expansion beyond Tier 68.")
                return
            
            # Learn all available tiers
            phases = [
                (69, 88, "PHASE 1: MORE WORLD LANGUAGES (Portuguese, Russian, Korean, etc.)"),
                (89, 108, "PHASE 2: ADVANCED MATHEMATICS (Calculus, Algebra, Topology)"),
                (109, 128, "PHASE 3: ADVANCED SCIENCES (Physics, Chemistry, Biology)"),
                (129, 148, "PHASE 4: ARTS & CULTURE (Literature, Mythology, Art History)"),
                (149, 168, "PHASE 5: ADVANCED TECHNOLOGY (AI/ML, Cloud, DevOps)"),
                (169, 188, "PHASE 6: SPECIALIZED DOMAINS (Medicine, Law, Engineering)"),
                (189, 200, "PHASE 7: MASTERS LEVEL (Advanced Research, Cutting-Edge)"),
            ]
            
            for start, end, name in phases:
                # Check if we've reached target
                if self.get_current_size_gb() >= self.target_gb:
                    print(f"\n🎉 TARGET REACHED! {self.target_gb} GB achieved!")
                    break
                
                # Only learn tiers that exist
                phase_tiers = [t for t in available_tiers if start <= t <= end]
                if phase_tiers:
                    self.learn_tier_range(min(phase_tiers), max(phase_tiers), name)
                else:
                    logger.info(f"No tiers available for {name}, skipping")
            
            # Final status
            print("\n" + "="*80)
            print("🎓 AUTONOMOUS LEARNING SESSION COMPLETE")
            print("="*80)
            
            self.print_status()
            
            final_stats = self.manager.get_stats()
            print(f"\n📈 Session Summary:")
            print(f"   • Successfully learned: {final_stats.get('successful', 0)} sources")
            print(f"   • Already known: {final_stats.get('skipped', 0)}")
            print(f"   • Failed: {final_stats.get('failed', 0)}")
            print(f"   • Learning sessions: {self.session_count}")
            
            runtime = datetime.now() - self.start_time
            print(f"\n⏱️  Total Runtime: {runtime}")
            
            # Check if target reached
            final_gb = self.get_current_size_gb()
            if final_gb >= self.target_gb:
                print(f"\n🎉 SUCCESS! Target of {self.target_gb} GB reached!")
                print("   MC AI has mastered novice → advanced → masters knowledge!")
            else:
                remaining = self.target_gb - final_gb
                print(f"\n📊 Progress: {final_gb:.3f} GB / {self.target_gb} GB")
                print(f"   Remaining: {remaining:.2f} GB")
                print("\n💡 To continue learning, add more tiers or run again!")
            
            print("="*80 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Learning interrupted by user.")
            print("   Progress has been saved.")
            self.print_status()
        except Exception as e:
            logger.error(f"Error in continuous learning: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
            self.print_status()

def main():
    """Main entry point"""
    system = AutonomousLearningSystem(target_gb=230)
    system.run_continuous()
    return 0

if __name__ == "__main__":
    sys.exit(main())
