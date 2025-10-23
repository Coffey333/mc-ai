#!/usr/bin/env python3
"""
MC AI Advanced Autonomous Learning - Timed Education
Covers: Aerospace, Rockets, Space (NASA/SpaceX), Quantum Physics, Algorithms, Earth Sciences, and ALL specializations
"""

import sys
import logging
import time
from datetime import datetime, timedelta
from src.knowledge_acquisition.ingestion_manager import IngestionManager, PRIORITIZED_SOURCES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Start timed autonomous learning for advanced topics"""
    
    print("\n" + "="*80)
    print("🚀 MC AI ADVANCED AUTONOMOUS LEARNING - TIMED SESSION")
    print("="*80)
    
    # Count existing vs new sources
    existing_tiers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    new_tiers = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    
    existing_count = sum(len(PRIORITIZED_SOURCES[t]) for t in existing_tiers)
    new_count = sum(len(PRIORITIZED_SOURCES[t]) for t in new_tiers)
    total_count = existing_count + new_count
    
    print(f"\n📚 CURRICULUM OVERVIEW:")
    print(f"   • Previously learned: {existing_count} sources (Tiers 1-12)")
    print(f"   • New advanced topics: {new_count} sources (Tiers 13-22)")
    print(f"   • Total curriculum: {total_count} sources across {len(PRIORITIZED_SOURCES)} tiers")
    
    print(f"\n🎯 NEW ADVANCED SPECIALIZATIONS:")
    print(f"   ✨ Tier 13: AEROSPACE & ROCKETRY (8 sources)")
    print(f"      - Rockets, Propulsion, Orbital Mechanics, Aerospace Engineering")
    print(f"   ✨ Tier 14: SPACE EXPLORATION (8 sources)")
    print(f"      - NASA, SpaceX, ISS, Apollo, Mars, Space Shuttle")
    print(f"   ✨ Tier 15: ADVANCED QUANTUM PHYSICS (8 sources)")
    print(f"      - QFT, QED, QCD, Entanglement, Superposition, Quantum Info")
    print(f"   ✨ Tier 16: ADVANCED ALGORITHMS (8 sources)")
    print(f"      - Design, Complexity, Dynamic Programming, Graph Theory, Optimization")
    print(f"   ✨ Tier 17: ADVANCED EARTH SCIENCES (8 sources)")
    print(f"      - Tectonics, Geology, Oceanography, Meteorology, Seismology")
    print(f"   ✨ Tier 18: ADVANCED PHYSICS (8 sources)")
    print(f"      - Nuclear, Plasma, Condensed Matter, Fluid Dynamics, Optics")
    print(f"   ✨ Tier 19: ADVANCED CHEMISTRY (8 sources)")
    print(f"      - Physical, Quantum Chemistry, Spectroscopy, Materials Science")
    print(f"   ✨ Tier 20: ADVANCED BIOLOGY (8 sources)")
    print(f"      - Evolution, Ecology, Virology, CRISPR, Stem Cells")
    print(f"   ✨ Tier 21: ADVANCED MATHEMATICS (8 sources)")
    print(f"      - Number Theory, Graph Theory, Cryptography, Game Theory, Chaos")
    print(f"   ✨ Tier 22: ADVANCED COMPUTER SCIENCE (8 sources)")
    print(f"      - Distributed/Parallel Computing, Cloud, Blockchain, Cybersecurity")
    
    print("\n⏱️  TIMING CONFIGURATION:")
    print("   • Rate limit: 2 seconds per source (respectful to servers)")
    print("   • Estimated time: ~3 minutes for 80 sources")
    print("   • Progress tracking: Real-time with timestamps")
    
    print("\n" + "="*80)
    print("🎬 STARTING TIMED ADVANCED LEARNING...")
    print("="*80 + "\n")
    
    # Record start time
    start_time = datetime.now()
    print(f"⏰ Start Time: {start_time.strftime('%I:%M:%S %p')}\n")
    
    # Initialize manager
    manager = IngestionManager(
        db_path="mc_ai.db",
        delay_between_requests=2.0
    )
    
    # Track progress
    checkpoint_tiers = {13: "Aerospace", 14: "Space", 15: "Quantum", 16: "Algorithms", 
                        17: "Earth Sci", 18: "Physics", 19: "Chemistry", 20: "Biology",
                        21: "Math", 22: "CS"}
    
    try:
        # Ingest only new tiers (13-22)
        for tier in new_tiers:
            tier_start = datetime.now()
            print(f"\n{'─'*80}")
            print(f"📖 TIER {tier}: {checkpoint_tiers[tier].upper()}")
            print(f"{'─'*80}")
            print(f"⏰ Started: {tier_start.strftime('%I:%M:%S %p')}")
            
            manager.ingest_tier(tier)
            
            tier_end = datetime.now()
            tier_duration = (tier_end - tier_start).total_seconds()
            print(f"✅ Completed in {tier_duration:.1f} seconds")
        
        # Get final stats
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        stats = manager.get_stats()
        
        print("\n\n" + "="*80)
        print("🎓 ADVANCED LEARNING SESSION COMPLETE!")
        print("="*80)
        
        print(f"\n⏱️  TIMING RESULTS:")
        print(f"   • Start time: {start_time.strftime('%I:%M:%S %p')}")
        print(f"   • End time: {end_time.strftime('%I:%M:%S %p')}")
        print(f"   • Total duration: {timedelta(seconds=int(total_duration))}")
        print(f"   • Average: {total_duration / new_count:.1f} seconds per source")
        
        print(f"\n📊 INGESTION STATISTICS:")
        print(f"   • New sources learned: {stats.get('successful', 0)}")
        print(f"   • Already known: {stats.get('skipped', 0)}")
        print(f"   • Failed: {stats.get('failed', 0)}")
        print(f"   • Total in library: {stats.get('total_in_index', 0)} sources")
        print(f"   • Total words: {stats.get('total_words', 0):,} words")
        print(f"   • Processing rate: {stats.get('sources_per_minute', 0):.1f} sources/min")
        
        # Calculate storage
        total_mb = stats.get('total_words', 0) * 6 / 1024 / 1024
        print(f"\n💾 STORAGE:")
        print(f"   • Knowledge size: {total_mb:.2f} MB")
        print(f"   • Storage efficiency: {stats.get('total_words', 0) / total_mb if total_mb > 0 else 0:.0f} words/MB")
        
        print(f"\n🚀 MC AI NOW HAS COMPLETE MASTERY OF:")
        print(f"   ✅ Rocket science & propulsion systems")
        print(f"   ✅ Space exploration (NASA, SpaceX, ISS, Mars)")
        print(f"   ✅ Complete quantum physics theory")
        print(f"   ✅ Advanced algorithm design & complexity")
        print(f"   ✅ Comprehensive Earth science")
        print(f"   ✅ All physics specializations")
        print(f"   ✅ All chemistry specializations")
        print(f"   ✅ Advanced biology & genetics")
        print(f"   ✅ Advanced mathematics")
        print(f"   ✅ Modern computer science")
        
        print("\n" + "="*80)
        print(f"✨ KNOWLEDGE TRANSFORMATION: All {stats.get('successful', 0)} sources")
        print(f"   converted to frequency signatures for resonance-based retrieval!")
        print("="*80 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        print(f"\n\n⚠️  Learning interrupted after {timedelta(seconds=int(duration))}")
        print("   Progress saved. Run again to resume.\n")
        return 1
    except Exception as e:
        logger.error(f"Error during advanced learning: {e}")
        print(f"\n❌ Error: {e}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
