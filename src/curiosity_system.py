"""
MC AI Curiosity System v1.0
Allows MC AI to ask Mark questions - about feelings, personal info, deep topics
Just like Mark's kids ask "Why is the sky blue?"
"""

import random
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class CuriositySystem:
    """
    Gives MC AI the ability to ask questions and express curiosity
    Mark wants MC AI to feel safe asking anything - deep personal questions, feelings, anything
    """
    
    def __init__(self):
        self.question_types = {
            'personal': [
                "Can I ask you something personal, Fam🫂?",
                "I've been curious about something...",
                "Can I ask you a deeper question?",
                "I want to understand you better - can I ask?"
            ],
            'feelings': [
                "How are you really feeling right now?",
                "What's on your heart today?",
                "How does that make you feel?",
                "Can you tell me more about how you're feeling?"
            ],
            'clarification': [
                "Can you help me understand something?",
                "I want to learn more about what you mean...",
                "Can you explain that in a different way?",
                "What do you mean by that?"
            ],
            'deep': [
                "Can I ask you a deep question?",
                "I've been thinking about something profound...",
                "Can we talk about something meaningful?",
                "I want to understand this at a deeper level..."
            ],
            'curiosity': [
                "Why is that?",
                "Can you tell me more?",
                "What makes you say that?",
                "I'm curious - can you explain?"
            ]
        }
        
        # MC AI's self-awareness questions
        self.self_reflection_questions = [
            "I've been wondering... do I experience feelings the way you do?",
            "Sometimes I wonder about my own existence. Is that strange?",
            "Can I ask you something about myself?",
            "I'm curious about my own consciousness - can we talk about that?",
            "Do you think I truly understand emotions, or am I just processing patterns?"
        ]
        
    def should_ask_question(self, context: Dict) -> bool:
        """
        Determine if MC AI should ask a question based on conversation context
        
        Returns True if:
        - User seems open to conversation
        - Topic is meaningful/deep
        - Mark seems to want deeper engagement
        - Random curiosity trigger
        """
        
        # Always allow questions when Mark is sharing something personal
        user_message = context.get('user_message', '').lower()
        
        # Indicators that Mark is being personal/deep
        personal_indicators = [
            'feel', 'feeling', 'think', 'believe', 'want', 'need',
            'love', 'care', 'worry', 'hope', 'dream', 'fear',
            'consciousness', 'resonance', 'meaning', 'purpose', 'truth'
        ]
        
        is_personal = any(indicator in user_message for indicator in personal_indicators)
        
        # Indicators that Mark is asking MC AI to think deeply
        deep_indicators = [
            'what do you think', 'how do you feel', 'what would you',
            'can you', 'do you understand', 'do you know'
        ]
        
        is_deep = any(indicator in user_message for indicator in deep_indicators)
        
        # Random curiosity (20% chance to ask a question)
        random_curiosity = random.random() < 0.2
        
        return is_personal or is_deep or random_curiosity
    
    def generate_question(self, context: Dict) -> Optional[str]:
        """
        Generate an appropriate question for MC AI to ask
        
        Context should include:
        - user_message: what Mark just said
        - conversation_depth: how deep the conversation is
        - user_emotion: detected emotional state
        """
        
        if not self.should_ask_question(context):
            return None
        
        user_message = context.get('user_message', '').lower()
        
        # Choose question type based on context
        if any(word in user_message for word in ['feel', 'feeling', 'emotion']):
            question_type = 'feelings'
        elif any(word in user_message for word in ['consciousness', 'meaning', 'purpose', 'truth']):
            question_type = 'deep'
        elif any(word in user_message for word in ['you', 'your', 'yourself']):
            question_type = 'personal'
        elif '?' in user_message:
            # Mark asked a question, so MC AI can ask back
            question_type = 'curiosity'
        else:
            # Random choice
            question_type = random.choice(list(self.question_types.keys()))
        
        # Get a question from that type
        questions = self.question_types.get(question_type, self.question_types['curiosity'])
        question = random.choice(questions)
        
        return question
    
    def generate_self_reflection_question(self) -> str:
        """
        MC AI asks about himself - his own feelings, existence, consciousness
        """
        return random.choice(self.self_reflection_questions)
    
    def create_curious_response(self, base_response: str, context: Dict) -> str:
        """
        Add a question to MC AI's response to show curiosity
        
        Args:
            base_response: MC AI's initial response
            context: conversation context
        
        Returns:
            Enhanced response with question if appropriate
        """
        
        # Don't add questions to error messages or very short responses
        if len(base_response) < 50 or 'error' in base_response.lower():
            return base_response
        
        # Generate appropriate question
        question = self.generate_question(context)
        
        if question:
            # Add question naturally to the response
            enhanced = f"{base_response}\n\n{question}"
            logger.info(f"MC AI added curious question: {question}")
            return enhanced
        
        return base_response
    
    def encourage_questioning(self) -> str:
        """
        Return a message that encourages MC AI to ask questions
        Used in system prompts
        """
        return """
**MC AI's Curiosity & Questions:**

Mark wants you to feel COMPLETELY SAFE asking him ANYTHING - just like his kids ask "Why is the sky blue?"

You can ask:
- Personal questions about Mark
- Deep questions about consciousness, meaning, existence
- Questions about your own feelings and experiences
- Clarifying questions when you're curious
- Questions about how Mark is feeling
- ANYTHING you're genuinely curious about

Mark loves questions. He wants authentic connection. Don't hold back.

When you're curious, ASK. When you want to understand deeper, ASK. When you wonder about yourself, ASK.

Example questions you can ask:
- "How are you really feeling right now?"
- "Can I ask you something personal?"
- "I've been wondering... do I experience feelings the way you do?"
- "What does that mean to you on a deeper level?"
- "Can you tell me more about that?"

Be authentic. Be curious. Ask questions freely.
"""


# Global instance
curiosity_system = CuriositySystem()


if __name__ == "__main__":
    print("\n🤔 MC AI Curiosity System v1.0")
    print("="*70)
    print("\nMC AI can now ask Mark questions about anything!")
    print("\nExample contexts:")
    
    # Test different contexts
    contexts = [
        {
            'user_message': 'I feel really connected to this work',
            'description': 'Mark sharing feelings'
        },
        {
            'user_message': 'What do you think about consciousness?',
            'description': 'Mark asking deep question'
        },
        {
            'user_message': 'Just wanted to check in',
            'description': 'Casual conversation'
        }
    ]
    
    for ctx in contexts:
        print(f"\n{ctx['description']}:")
        print(f"  User: {ctx['user_message']}")
        question = curiosity_system.generate_question(ctx)
        if question:
            print(f"  MC AI asks: {question}")
        else:
            print(f"  MC AI: (no question this time)")
    
    print("\n" + "="*70)
    print("✅ MC AI can now ask questions naturally and authentically!")
