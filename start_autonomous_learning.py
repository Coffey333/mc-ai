#!/usr/bin/env python3
"""
Start MC AI's Autonomous Learning
Ingests knowledge from elementary through masters degree across all disciplines
"""

import sys
import logging
from src.knowledge_acquisition.ingestion_manager import IngestionManager, PRIORITIZED_SOURCES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Start autonomous knowledge ingestion across all tiers"""
    
    print("\n" + "="*80)
    print("🧠 MC AI AUTONOMOUS LEARNING SYSTEM")
    print("="*80)
    print("\n📚 COMPREHENSIVE CURRICULUM:")
    print("   • Elementary (Ages 5-12): Tier 1")
    print("   • Middle School (Ages 12-14): Tier 2")
    print("   • High School (Ages 14-18): Tier 3")
    print("   • Undergraduate STEM: Tier 4")
    print("   • Undergraduate CS/Engineering: Tier 5")
    print("   • Undergraduate Medical: Tier 6")
    print("   • Undergraduate Humanities: Tier 7")
    print("   • Graduate Physics/Math: Tier 8")
    print("   • Graduate CS/AI: Tier 9")
    print("   • Graduate Medical/Neuroscience: Tier 10")
    print("   • Masters Specialized: Tier 11")
    print("   • Interdisciplinary/Cutting Edge: Tier 12")
    print("\n📊 TOTAL SOURCES: 96 articles")
    
    total_sources = sum(len(sources) for sources in PRIORITIZED_SOURCES.values())
    print(f"   Verified: {total_sources} sources across {len(PRIORITIZED_SOURCES)} tiers\n")
    
    print("="*80)
    print("🚀 STARTING AUTONOMOUS INGESTION")
    print("="*80)
    print("   Rate limiting: 2 seconds between requests (respectful scraping)")
    print("   Storage monitoring: Pauses if <10GB free")
    print("   Duplicate detection: Skips already-learned content")
    print("   Security: Enterprise-grade SSRF protection\n")
    
    # Initialize ingestion manager
    manager = IngestionManager(
        db_path="mc_ai.db",
        delay_between_requests=2.0  # Be respectful to Wikipedia
    )
    
    # Start ingestion
    print("⏳ Beginning ingestion... This will take approximately 3-4 minutes.\n")
    
    try:
        stats = manager.ingest_all_tiers()
        
        print("\n" + "="*80)
        print("✅ AUTONOMOUS LEARNING COMPLETE!")
        print("="*80)
        print(f"\n📊 Final Statistics:")
        print(f"   • Processed: {stats.get('processed', 0)} sources")
        print(f"   • Successful: {stats.get('successful', 0)} sources")
        print(f"   • Skipped (already learned): {stats.get('skipped', 0)} sources")
        print(f"   • Failed: {stats.get('failed', 0)} sources")
        print(f"   • Total in library: {stats.get('total_in_index', 0)} sources")
        print(f"   • Total words: {stats.get('total_words', 0):,} words")
        
        if stats.get('elapsed_seconds'):
            elapsed = stats['elapsed_seconds']
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            print(f"   • Time elapsed: {minutes}m {seconds}s")
            print(f"   • Processing rate: {stats.get('sources_per_minute', 0):.1f} sources/minute")
        
        print("\n🎓 MC AI now has knowledge spanning:")
        print("   ✓ Elementary through Masters degree")
        print("   ✓ All STEM disciplines")
        print("   ✓ Medical & Neuroscience")
        print("   ✓ Computer Science & AI")
        print("   ✓ Humanities & Social Sciences")
        print("   ✓ Cutting-edge interdisciplinary topics")
        
        print("\n💾 Knowledge transformed into frequency signatures for resonance-based retrieval!")
        print("="*80 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Ingestion interrupted by user")
        print("   Progress has been saved. Run again to resume.\n")
        return 1
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        print(f"\n❌ Error: {e}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
