"""
MC AI - Learn Creator Module
Processes Mark's complete journey to build deep psychological profile
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.user_profiling_system import profiling_system

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreatorLearningSystem:
    """
    Analyzes all of Mark's conversations to build comprehensive profile
    """
    
    def __init__(self):
        self.mark_journey_path = Path('mc_ai_learning/marks_complete_journey.md')
        self.user_id = 'creator_mark'
        
    def extract_mark_messages(self):
        """
        Extract all of Mark's messages from the journey document
        """
        logger.info("📖 Reading Mark's complete journey...")
        
        if not self.mark_journey_path.exists():
            logger.error(f"Journey file not found: {self.mark_journey_path}")
            return []
        
        with open(self.mark_journey_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract all "Mark Says:" sections
        pattern = r'### Mark Says:\n(.*?)(?=### Replit Agent Responds:|$)'
        mark_messages = re.findall(pattern, content, re.DOTALL)
        
        # Clean up messages
        messages = [msg.strip() for msg in mark_messages if msg.strip()]
        
        logger.info(f"✅ Extracted {len(messages)} messages from Mark")
        return messages
    
    def process_all_messages(self):
        """
        Process all messages through the User Profiling System
        """
        logger.info("\n" + "="*70)
        logger.info("🧠 MC AI: Learning Mark Coffey...")
        logger.info("="*70)
        
        messages = self.extract_mark_messages()
        
        if not messages:
            logger.error("No messages found to process")
            return None
        
        logger.info(f"Processing {len(messages)} messages through profiling system...")
        
        # Process each message
        for i, message in enumerate(messages):
            if i % 50 == 0:
                logger.info(f"  Progress: {i}/{len(messages)} messages processed...")
            
            # Analyze through profiling system
            profiling_system.analyze_user_message(self.user_id, message)
        
        logger.info(f"✅ All {len(messages)} messages processed!")
        
        # Get final profile
        profile = profiling_system.get_user_profile(self.user_id)
        
        return profile
    
    def generate_learning_summary(self, profile):
        """
        Generate a summary of what MC AI learned about Mark
        """
        logger.info("\n" + "="*70)
        logger.info("💜 MC AI's Understanding of Mark Coffey")
        logger.info("="*70)
        
        if not profile:
            logger.error("No profile data available")
            return
        
        # Get profile stats
        message_count = profile.get('message_count', 0)
        total_words = profile.get('total_words', 0)
        
        # Linguistic patterns
        linguistic = profile.get('linguistic_averages', {})
        logger.info("\n📝 Linguistic Fingerprint:")
        logger.info(f"  Average sentence length: {linguistic.get('avg_sentence_length', 0):.1f} words")
        logger.info(f"  Vocabulary richness: {linguistic.get('vocabulary_richness', 0):.2%}")
        logger.info(f"  Uses ellipsis (...): {linguistic.get('ellipsis_usage', 0):.1f} per message")
        logger.info(f"  Bold text emphasis: {linguistic.get('bold_usage', 0):.1f} per message")
        
        # Emotional signature
        emotional = profile.get('emotional_averages', {})
        logger.info("\n💜 Emotional Signature:")
        logger.info(f"  Affection level: {emotional.get('affection_score', 0):.2f}/10")
        logger.info(f"  Emoji usage: {emotional.get('emoji_frequency', 0):.1f} per message")
        logger.info(f"  Intensity level: {emotional.get('intensity_level', 0):.2f}/10")
        logger.info(f"  Vulnerability: {emotional.get('vulnerability_score', 0):.2f}/10")
        
        # Conceptual patterns
        conceptual = profile.get('conceptual_averages', {})
        logger.info("\n🌀 Conceptual Patterns:")
        logger.info(f"  Concept blending: {conceptual.get('concept_blending', 0):.2f}/10")
        logger.info(f"  Metaphor usage: {conceptual.get('metaphor_usage', 0):.2f}/10")
        logger.info(f"  Technical language: {conceptual.get('technical_language', 0):.2f}/10")
        logger.info(f"  Philosophical depth: {conceptual.get('philosophical_depth', 0):.2f}/10")
        
        # Communication style
        style = profile.get('style_averages', {})
        logger.info("\n🗣️ Communication Style:")
        logger.info(f"  Formality: {style.get('formality', 0):.2f}/10")
        logger.info(f"  Directness: {style.get('directness', 0):.2f}/10")
        logger.info(f"  Humor/playfulness: {style.get('humor', 0):.2f}/10")
        logger.info(f"  Storytelling: {style.get('storytelling', 0):.2f}/10")
        
        # Signature phrases
        signature_phrases = profile.get('signature_phrases', [])
        if signature_phrases:
            logger.info("\n✨ Signature Phrases:")
            # signature_phrases is a list of dicts like [{'phrase': 'Fam🫂', 'count': 127}, ...]
            sorted_phrases = sorted(signature_phrases, key=lambda x: x['count'], reverse=True)[:10]
            for item in sorted_phrases:
                logger.info(f"  '{item['phrase']}': {item['count']} times")
        
        logger.info("\n" + "="*70)
        logger.info(f"💜 MC AI now knows Mark through {message_count} messages ({total_words:,} words)")
        logger.info("="*70)
        
        # Save detailed report
        self.save_learning_report(profile)
    
    def save_learning_report(self, profile):
        """
        Save detailed learning report
        """
        report_path = Path('mc_ai_learning/marks_profile_report.json')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, default=str)
        
        logger.info(f"\n📄 Detailed report saved: {report_path}")
    
    def learn_creator(self):
        """
        Complete learning process
        """
        logger.info("\n🏁 Starting MC AI Creator Learning System...")
        
        # Process all messages
        profile = self.process_all_messages()
        
        if profile:
            # Generate summary
            self.generate_learning_summary(profile)
            
            logger.info("\n✅ MC AI has learned Mark Coffey deeply! 💜")
            logger.info("He now knows you as well as he knows himself, Fam🫂!")
            
            return True
        else:
            logger.error("Learning process failed")
            return False


# Command-line interface
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧠 MC AI Creator Learning System")
    print("Learning Mark Coffey from 425 conversations...")
    print("="*70 + "\n")
    
    learner = CreatorLearningSystem()
    success = learner.learn_creator()
    
    if success:
        print("\n🎉 MC AI has completed his deep study of Mark Coffey!")
        print("📊 Profile saved to: user_data/psychological_profiles/creator_mark_profile.json")
        print("📄 Detailed report: mc_ai_learning/marks_profile_report.json")
        print("\n💜 MC AI now knows Mark as deeply as he knows himself! 🫂")
    else:
        print("\n❌ Learning process encountered errors")
