#!/usr/bin/env python3
"""
MC AI Creative & Practical Learning - Timed Session
Teaches: Children's education, Legal expertise, Cooking, Crafting, Inventing, Imagination
"""

import sys
import logging
from datetime import datetime, timedelta
from src.knowledge_acquisition.ingestion_manager import IngestionManager, PRIORITIZED_SOURCES

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Start creative and practical skills learning"""
    
    print("\n" + "="*80)
    print("🎨 MC AI CREATIVE & PRACTICAL LEARNING - TIMED SESSION")
    print("="*80)
    
    creative_tiers = [23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
    new_count = sum(len(PRIORITIZED_SOURCES[t]) for t in creative_tiers)
    
    print(f"\n📚 CREATIVE & PRACTICAL CURRICULUM:")
    print(f"   • New creative sources: {new_count} across 10 specialized tiers")
    
    print(f"\n🎯 NEW CAPABILITIES TO ACQUIRE:")
    print(f"\n   ✨ Tier 23: CHILDREN'S LITERATURE & FAIRY TALES (8 sources)")
    print(f"      📖 Fairy tales, Folklore, Fables, Nursery rhymes")
    print(f"      🧚 Andersen, Brothers Grimm, Aesop's Fables")
    print(f"      → Make learning magical and engaging for kids!")
    
    print(f"\n   ✨ Tier 24: CHILD DEVELOPMENT & EDUCATION (8 sources)")
    print(f"      👶 Developmental stages, Educational psychology")
    print(f"      🎓 Pedagogy, Piaget's theory, Montessori method")
    print(f"      → Understand how children learn at every age!")
    
    print(f"\n   ✨ Tier 25: LEGAL FOUNDATIONS (8 sources)")
    print(f"      ⚖️  Constitutional, Criminal, Civil, Common Law")
    print(f"      📜 Contract Law, Tort Law, Evidence Law")
    print(f"      → Build super-lawyer level knowledge!")
    
    print(f"\n   ✨ Tier 26: ADVANCED LEGAL (8 sources)")
    print(f"      🏛️  Legal procedures, Trials, Briefs")
    print(f"      💼 IP Law, Corporate Law, Human Rights")
    print(f"      → Complete legal expertise!")
    
    print(f"\n   ✨ Tier 27: CULINARY ARTS FUNDAMENTALS (8 sources)")
    print(f"      🍳 Cooking basics, Baking, Food science")
    print(f"      🥗 Nutrition, Recipes, Gastronomy")
    print(f"      → Master the art of cooking!")
    
    print(f"\n   ✨ Tier 28: ADVANCED COOKING (8 sources)")
    print(f"      🇫🇷 French, Italian, Chinese, Japanese cuisine")
    print(f"      🧪 Molecular gastronomy, Fermentation")
    print(f"      → Become a culinary expert!")
    
    print(f"\n   ✨ Tier 29: CRAFTS & DIY (8 sources)")
    print(f"      🪵 Woodworking, Sewing, Knitting, Pottery")
    print(f"      🎨 Painting, Sculpture, Origami")
    print(f"      → Create with hands and imagination!")
    
    print(f"\n   ✨ Tier 30: INVENTION & INNOVATION (8 sources)")
    print(f"      💡 Innovation, Creativity, Design thinking")
    print(f"      🔧 Patents, Prototyping, Engineering design")
    print(f"      → Invent and bring ideas to life!")
    
    print(f"\n   ✨ Tier 31: POPULAR CULTURE & TRENDS (8 sources)")
    print(f"      🎮 Video games, Animation, Comics")
    print(f"      🦸 Superheroes, Disney, Storytelling")
    print(f"      → Connect with kids through pop culture!")
    
    print(f"\n   ✨ Tier 32: IMAGINATION & CREATIVITY BOOSTERS (8 sources)")
    print(f"      🌈 Metaphor, Analogy, Lateral thinking")
    print(f"      😄 Humor, Riddles, Brainstorming, Mind maps")
    print(f"      → Enable cross-referencing for creative imagination!")
    
    print(f"\n💫 WHY THIS MATTERS:")
    print(f"   ✓ Teach children with fairy tales and fun stories")
    print(f"   ✓ Provide legal advice like a super-lawyer")
    print(f"   ✓ Share cooking recipes and techniques")
    print(f"   ✓ Guide crafting projects step-by-step")
    print(f"   ✓ Help invent and design new things")
    print(f"   ✓ Use metaphors and analogies to explain complex topics")
    print(f"   ✓ Be creative, funny, and engaging!")
    
    print("\n⏱️  TIMING:")
    print("   • Rate: 2 seconds per source")
    print("   • Estimated: ~3 minutes for 80 sources")
    
    print("\n" + "="*80)
    print("🎬 STARTING CREATIVE LEARNING SESSION...")
    print("="*80 + "\n")
    
    start_time = datetime.now()
    print(f"⏰ Start Time: {start_time.strftime('%I:%M:%S %p')}\n")
    
    manager = IngestionManager(db_path="mc_ai.db", delay_between_requests=2.0)
    
    tier_names = {
        23: "📚 FAIRY TALES", 24: "👶 CHILD DEVELOPMENT", 25: "⚖️  LEGAL BASICS",
        26: "🏛️  ADVANCED LEGAL", 27: "🍳 COOKING BASICS", 28: "👨‍🍳 ADVANCED COOKING",
        29: "🎨 CRAFTS & DIY", 30: "💡 INVENTION", 31: "🎮 POP CULTURE",
        32: "🌈 IMAGINATION"
    }
    
    try:
        for tier in creative_tiers:
            tier_start = datetime.now()
            print(f"\n{'─'*80}")
            print(f"TIER {tier}: {tier_names[tier]}")
            print(f"{'─'*80}")
            print(f"⏰ Started: {tier_start.strftime('%I:%M:%S %p')}")
            
            manager.ingest_tier(tier)
            
            tier_end = datetime.now()
            tier_duration = (tier_end - tier_start).total_seconds()
            print(f"✅ Completed in {tier_duration:.1f} seconds")
        
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        stats = manager.get_stats()
        
        print("\n\n" + "="*80)
        print("🎓 CREATIVE & PRACTICAL LEARNING COMPLETE!")
        print("="*80)
        
        print(f"\n⏱️  SESSION TIMING:")
        print(f"   • Start: {start_time.strftime('%I:%M:%S %p')}")
        print(f"   • End: {end_time.strftime('%I:%M:%S %p')}")
        print(f"   • Duration: {timedelta(seconds=int(total_duration))}")
        print(f"   • Speed: {total_duration / new_count:.1f} sec/source")
        
        print(f"\n📊 LEARNING RESULTS:")
        print(f"   • New skills acquired: {stats.get('successful', 0)} sources")
        print(f"   • Already known: {stats.get('skipped', 0)}")
        print(f"   • Total library: {stats.get('total_in_index', 0)} sources")
        print(f"   • Total knowledge: {stats.get('total_words', 0):,} words")
        print(f"   • Knowledge size: {(stats.get('total_words', 0) * 6 / 1024 / 1024):.2f} MB")
        
        print(f"\n🎨 MC AI NOW HAS:")
        print(f"   ✅ Children's teaching expertise (fairy tales, fables, folklore)")
        print(f"   ✅ Developmental psychology (all ages 0-18)")
        print(f"   ✅ Super-lawyer knowledge (constitutional to corporate law)")
        print(f"   ✅ Culinary mastery (cooking, baking, world cuisines)")
        print(f"   ✅ Crafting skills (woodwork, sewing, pottery, painting)")
        print(f"   ✅ Invention expertise (design thinking, prototyping)")
        print(f"   ✅ Pop culture fluency (games, animation, storytelling)")
        print(f"   ✅ Creative imagination (metaphor, analogy, humor, riddles)")
        
        print(f"\n💡 CROSS-REFERENCING EXAMPLES:")
        print(f"   🔗 Explain quantum physics using fairy tale metaphors")
        print(f"   🔗 Teach coding through game design analogies")
        print(f"   🔗 Compare legal contracts to recipe instructions")
        print(f"   🔗 Relate rocket science to cooking chemistry")
        print(f"   🔗 Use superhero stories to explain ethics")
        
        print("\n" + "="*80)
        print("✨ MC AI IS NOW A CREATIVE, PRACTICAL, UNIVERSAL EXPERT!")
        print("="*80 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Interrupted. Progress saved.\n")
        return 1
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
