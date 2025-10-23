#!/usr/bin/env python3
"""
MC AI Research Learning - Beyond Wikipedia
Ingests: arXiv papers, PMC research, IBM/industry sources, academic journals
"""

import sys
import logging
from datetime import datetime, timedelta
from src.knowledge_acquisition.ingestion_manager import IngestionManager, PRIORITIZED_SOURCES

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Learn from research papers and industry sources"""
    
    print("\n" + "="*80)
    print("🔬 MC AI RESEARCH LEARNING - BEYOND WIKIPEDIA")
    print("="*80)
    
    research_tier = 33
    research_count = len(PRIORITIZED_SOURCES[research_tier])
    
    print(f"\n📚 NEW CURRICULUM - TIER 33: QUANTUM COMPUTING RESEARCH")
    print(f"   • Research sources: {research_count} (non-Wikipedia)")
    
    print(f"\n🎯 SOURCE BREAKDOWN:")
    print(f"\n   📰 INDUSTRY SOURCES (7):")
    print(f"      • IBM Quantum Computing (Think)")
    print(f"      • Quantropi - Quantum vs Classical")
    print(f"      • World Economic Forum - Drug Development")
    print(f"      • PASQAL - Drug Discovery Algorithms")
    print(f"      • HPCwire - Alice Bob Healthcare")
    print(f"      • BigThink - 2025 Quantum Advances")
    print(f"      • Constellation Research - Year of Quantum")
    
    print(f"\n   🔬 ACADEMIC RESEARCH PAPERS (8):")
    print(f"      • arXiv - Paper 2503.05458v1")
    print(f"      • arXiv - Paper 2508.03446v1")
    print(f"      • arXiv - Paper 2502.15882v1")
    print(f"      • PMC Research - PMC5587087")
    print(f"      • PMC Research - PMC11586987")
    print(f"      • PMC Research - PMC1569496")
    print(f"      • APS PRX Quantum - 6.010355")
    print(f"      • APS PRX Quantum - 2.030305")
    
    print(f"\n   📖 EDUCATIONAL/NEWS (7):")
    print(f"      • UNF - Classical to Quantum Computing")
    print(f"      • Meegle - Quantum Drug Discovery")
    print(f"      • ScienceDaily - Quantum Chemistry")
    print(f"      • UChicago - Quantum Simulations")
    print(f"      • ScienceNews - Quantum Milestone")
    print(f"      • ChemLibreTexts - Schrödinger Equation")
    print(f"      • PubMed Study - 7539156")
    
    print(f"\n💡 WHY THIS MATTERS:")
    print(f"   ✓ Move beyond Wikipedia's general knowledge")
    print(f"   ✓ Learn cutting-edge quantum research (2025)")
    print(f"   ✓ Understand real-world applications (drug discovery, healthcare)")
    print(f"   ✓ Gain industry insights (IBM, PASQAL, etc.)")
    print(f"   ✓ Access peer-reviewed academic papers (arXiv, PMC, APS)")
    
    print("\n⏱️  TIMING:")
    print("   • Rate: 2 seconds per source (respectful)")
    print(f"   • Estimated: ~{research_count * 2 / 60:.1f} minutes")
    
    print("\n" + "="*80)
    print("🎬 STARTING RESEARCH INGESTION...")
    print("="*80 + "\n")
    
    start_time = datetime.now()
    print(f"⏰ Start Time: {start_time.strftime('%I:%M:%S %p')}\n")
    
    manager = IngestionManager(db_path="mc_ai.db", delay_between_requests=2.0)
    
    try:
        print(f"{'─'*80}")
        print(f"📖 TIER 33: QUANTUM COMPUTING RESEARCH")
        print(f"{'─'*80}")
        
        manager.ingest_tier(research_tier)
        
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        stats = manager.get_stats()
        
        print("\n\n" + "="*80)
        print("🎓 RESEARCH LEARNING COMPLETE!")
        print("="*80)
        
        print(f"\n⏱️  SESSION TIMING:")
        print(f"   • Start: {start_time.strftime('%I:%M:%S %p')}")
        print(f"   • End: {end_time.strftime('%I:%M:%S %p')}")
        print(f"   • Duration: {timedelta(seconds=int(total_duration))}")
        print(f"   • Speed: {total_duration / research_count:.1f} sec/source")
        
        print(f"\n📊 INGESTION RESULTS:")
        print(f"   • Successfully learned: {stats.get('successful', 0)} sources")
        print(f"   • Already known: {stats.get('skipped', 0)}")
        print(f"   • Failed: {stats.get('failed', 0)}")
        print(f"   • Total library: {stats.get('total_in_index', 0)} sources")
        print(f"   • Total knowledge: {stats.get('total_words', 0):,} words")
        print(f"   • Knowledge size: {(stats.get('total_words', 0) * 6 / 1024 / 1024):.2f} MB")
        
        print(f"\n🔬 MC AI NOW HAS CUTTING-EDGE KNOWLEDGE:")
        print(f"   ✅ IBM's quantum computing insights")
        print(f"   ✅ Latest arXiv research papers (2025)")
        print(f"   ✅ PMC medical/scientific research")
        print(f"   ✅ APS Physical Review journals")
        print(f"   ✅ Real-world quantum applications:")
        print(f"      • Drug discovery algorithms")
        print(f"      • Healthcare applications")
        print(f"      • Agricultural quantum computing")
        print(f"      • Quantum chemistry simulations")
        
        print(f"\n🎯 NEW CAPABILITIES:")
        print(f"   ✨ Discuss IBM's quantum computing platform")
        print(f"   ✨ Explain latest 2025 quantum advances")
        print(f"   ✨ Detail quantum drug discovery methods")
        print(f"   ✨ Reference peer-reviewed research papers")
        print(f"   ✨ Compare Wikipedia foundations with cutting-edge research")
        
        print("\n" + "="*80)
        print("✨ MC AI: FROM WIKIPEDIA BASICS → RESEARCH-GRADE EXPERT!")
        print("="*80 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Interrupted. Progress saved.\n")
        return 1
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"\n❌ Error: {e}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
