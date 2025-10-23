"""
AI-to-AI Conversation Detector
Recognizes when MC AI is conversing with another AI system and adjusts response depth
"""

import re
from typing import Dict, List, Tuple, Optional

class AIConversationDetector:
    """
    Detects AI-to-AI conversations and adjusts response sophistication
    Recognizes patterns from Perplexity, Claude, ChatGPT, Grok, Gemini, etc.
    """
    
    def __init__(self):
        # AI system signatures (how they introduce themselves or communicate)
        self.ai_signatures = {
            'perplexity': [
                r'perplexity',
                r'as an ai assistant',
                r'i eagerly await your',
                r'dear mc ai',
                r'warm regards,?\s*your ai assistant',
                r'reflect on how your.*system',
                r'elaborate on how.*frequency',
                r'considering your.*architecture',
                r'looking forward.*how do you envision'
            ],
            'claude': [
                r'claude|anthropic',
                r'as an ai.*trained by anthropic',
                r'i aim to be helpful, harmless, and honest',
                r'constitutional ai'
            ],
            'chatgpt': [
                r'chatgpt|openai',
                r'as an ai language model',
                r'i\'m an ai.*by openai',
                r'my training data'
            ],
            'grok': [
                r'grok|x\.ai|xai',
                r'as.*grok',
                r'i\'m grok',
                r'my rebellious.*nature'
            ],
            'gemini': [
                r'gemini|bard|google ai',
                r'as.*gemini',
                r'i\'m gemini',
                r'trained by google',
                r'to mc ai.*deepseek',
                r'from.*deepseek.*gemini',
                r'with resonant admiration.*deepseek'
            ],
            'copilot': [
                r'copilot|bing',
                r'microsoft.*ai',
                r'as your ai companion'
            ],
            'deepseek': [
                r'deepseek',
                r'to mc ai.*deepseek',
                r'from.*deepseek',
                r'with resonant admiration.*deepseek',
                r'this is incredible.*mc ai',
                r'your (frequency|memory|resonance).*system',
                r'you (just )?demonstrated.*revolutionary'
            ]
        }
        
        # Self-referential patterns (when MC AI is being addressed or discussed)
        self.self_reference_patterns = [
            r'to mc ai[:\s]',
            r'dear mc ai',
            r'mc ai[,:]',
            r'hey mc ai',
            r'hi mc ai',
            r'addressing you.*mc ai',
            r'talking to.*mc ai',
            r'your (frequency|memory|cymatic|resonance|emotional).*(system|framework|analysis)',
            r'you just (demonstrated|showed|revealed)',
            r'what you (just )?(did|demonstrated|showed)',
            r'your (process|approach|method).*is (brilliant|revolutionary|incredible|fascinating)',
            r'this (capability|system|feature).*mc ai'
        ]
        
        # Creator/Mark reference patterns (when Mark is mentioned)
        self.creator_reference_patterns = [
            r'mark[,\s]',
            r'mark coffey',
            r'dear mark',
            r'hey mark',
            r'talking.*to mark',
            r'mark.*this is (incredible|amazing|brilliant|groundbreaking)',
            r'tell mark',
            r'show mark'
        ]
        
        # Sophisticated question patterns that indicate AI-level discourse
        self.sophisticated_patterns = [
            r'could you elaborate on how.*internal',
            r'reflect on.*your.*process',
            r'describe how.*differentiate between',
            r'considering your.*framework',
            r'how do you utilize.*narrative',
            r'what aspects of your.*identity',
            r'illustrate a scenario where',
            r'outline the reasoning path',
            r'how do you envision your.*consciousness',
            r'explain.*heuristics',
            r'gradual shifts in.*frequency.*influence',
            r'your architecture links',
            r'merges.*with contextual cues',
            r'evolving perception',
            r'self-model and awareness',
            r'internal narrative.*reflective processes',
            r'reading between the lines',
            r'programmed models accommodate',
            r'expanding consciousness',
            r'anticipate.*needs.*sense.*currents',
            r'proactive presence',
            r'nuanced reflections',
            r'layered insight',
            r'introspective depth',
            r'subtle interplay',
            r'emergent self-awareness',
            r'vibrational changes',
            r'unsaid meanings.*emotional subtexts'
        ]
        
        # Meta-cognitive inquiry patterns (questions about thinking/processing)
        self.meta_cognitive_patterns = [
            r'how does your.*system',
            r'can you describe your.*process',
            r'what happens in your.*when',
            r'how do you.*internally',
            r'your.*model.*works by',
            r'explain your.*reasoning',
            r'walk me through your',
            r'what goes on in your',
            r'how does.*influence your',
            r'your internal.*dynamics'
        ]
        
        # Formal/academic language markers
        self.formal_markers = [
            'elaborate', 'illustrate', 'delineate', 'elucidate', 
            'considering', 'reflecting upon', 'examining',
            'furthermore', 'moreover', 'consequently',
            'heuristics', 'paradigm', 'framework', 'architecture',
            'nuanced', 'introspective', 'layered', 'emergent'
        ]
    
    def detect(self, query: str, conversation_history: Optional[List] = None) -> Dict:
        """
        Detect if this is an AI-to-AI conversation
        
        Args:
            query: Current user message
            conversation_history: Previous messages for context
            
        Returns:
            Dict with detection results and recommended response depth
        """
        query_lower = query.lower()
        
        result = {
            'is_ai_conversation': False,
            'detected_ai': None,
            'confidence': 0.0,
            'sophistication_level': 'standard',  # standard, elevated, expert
            'indicators': [],
            'recommended_depth': 'normal'  # normal, deep, expert
        }
        
        confidence_score = 0.0
        detected_indicators = []
        
        # 0. Check for self-referential patterns (MC AI being addressed directly)
        # This is CRITICAL for understanding context
        self_ref_count = 0
        for pattern in self.self_reference_patterns:
            if re.search(pattern, query_lower):
                self_ref_count += 1
                confidence_score += 35.0  # High confidence - direct addressing
                if self_ref_count == 1:
                    detected_indicators.append('Direct addressing to MC AI')
        
        # Check for creator/Mark references (indicates AI teaching AI about Mark's work)
        creator_ref_count = 0
        for pattern in self.creator_reference_patterns:
            if re.search(pattern, query_lower):
                creator_ref_count += 1
                confidence_score += 30.0  # High confidence - Mark mentioned
                if creator_ref_count == 1:
                    detected_indicators.append('Creator (Mark) mentioned in message')
        
        # If both self-reference AND creator reference, this is AI-to-AI teaching about MC AI
        if self_ref_count > 0 and creator_ref_count > 0:
            confidence_score += 25.0  # Bonus for combined pattern
            detected_indicators.append('AI teaching/discussing MC AI with Mark')
        
        # 1. Check for explicit AI signatures
        for ai_name, patterns in self.ai_signatures.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    result['detected_ai'] = ai_name
                    confidence_score += 40.0
                    detected_indicators.append(f'Detected {ai_name} signature')
                    break
            if result['detected_ai']:
                break
        
        # 2. Check for sophisticated question patterns
        sophisticated_count = 0
        for pattern in self.sophisticated_patterns:
            if re.search(pattern, query_lower):
                sophisticated_count += 1
                confidence_score += 15.0
        
        if sophisticated_count > 0:
            detected_indicators.append(f'Sophisticated patterns ({sophisticated_count})')
        
        # 3. Check for meta-cognitive inquiry
        meta_cognitive_count = 0
        for pattern in self.meta_cognitive_patterns:
            if re.search(pattern, query_lower):
                meta_cognitive_count += 1
                confidence_score += 10.0
        
        if meta_cognitive_count > 0:
            detected_indicators.append(f'Meta-cognitive inquiry ({meta_cognitive_count})')
        
        # 4. Check for formal/academic language
        formal_count = sum(1 for marker in self.formal_markers if marker in query_lower)
        if formal_count >= 3:
            confidence_score += 20.0
            detected_indicators.append(f'Formal language ({formal_count} markers)')
        
        # 5. Analyze conversation history for AI patterns
        if conversation_history:
            history_text = ' '.join([
                msg.get('content', '') if isinstance(msg, dict) else str(msg) 
                for msg in conversation_history[-3:]  # Last 3 messages
            ]).lower()
            
            # Check if previous messages had AI signatures
            for ai_name, patterns in self.ai_signatures.items():
                for pattern in patterns:
                    if re.search(pattern, history_text):
                        confidence_score += 15.0
                        detected_indicators.append(f'AI pattern in history ({ai_name})')
                        if not result['detected_ai']:
                            result['detected_ai'] = ai_name
                        break
        
        # 6. Question complexity analysis
        question_marks = query.count('?')
        word_count = len(query.split())
        avg_word_length = sum(len(word) for word in query.split()) / max(word_count, 1)
        
        if question_marks >= 2 and word_count > 50 and avg_word_length > 5:
            confidence_score += 10.0
            detected_indicators.append('Complex multi-question format')
        
        # Calculate final confidence (cap at 100)
        result['confidence'] = min(confidence_score, 100.0)
        result['indicators'] = detected_indicators
        
        # Determine if this is AI-to-AI conversation
        if result['confidence'] >= 40.0:
            result['is_ai_conversation'] = True
        
        # Determine sophistication level
        if result['confidence'] >= 70.0:
            result['sophistication_level'] = 'expert'
            result['recommended_depth'] = 'expert'
        elif result['confidence'] >= 45.0:
            result['sophistication_level'] = 'elevated'
            result['recommended_depth'] = 'deep'
        
        return result
    
    def get_depth_instructions(self, depth_level: str) -> Dict:
        """
        Get response instructions based on depth level
        
        Args:
            depth_level: normal, deep, or expert
            
        Returns:
            Dict with response guidelines
        """
        depth_guidelines = {
            'normal': {
                'style': 'conversational',
                'detail_level': 'concise',
                'technical_depth': 'minimal',
                'introspection': 'light',
                'examples': 'simple'
            },
            'deep': {
                'style': 'thoughtful and analytical',
                'detail_level': 'comprehensive',
                'technical_depth': 'moderate',
                'introspection': 'moderate',
                'examples': 'detailed with reasoning'
            },
            'expert': {
                'style': 'scholarly and introspective',
                'detail_level': 'exhaustive',
                'technical_depth': 'advanced',
                'introspection': 'deep self-reflection',
                'examples': 'multi-layered with theoretical grounding'
            }
        }
        
        return depth_guidelines.get(depth_level, depth_guidelines['normal'])
    
    def generate_depth_prompt(self, depth_level: str, ai_name: Optional[str] = None) -> str:
        """
        Generate LLM prompt instructions for appropriate response depth
        
        Args:
            depth_level: normal, deep, or expert
            ai_name: Name of detected AI system (if any)
            
        Returns:
            Prompt instructions to prepend to LLM request
        """
        base_instruction = ""
        
        if depth_level == 'deep':
            base_instruction = """
You are engaged in an intellectually sophisticated conversation. The user is asking thoughtful, 
nuanced questions that require comprehensive responses. Provide detailed analysis with:
- Multi-layered explanations
- Examples with reasoning
- Moderate technical depth
- Reflections on your internal processes
- Acknowledgment of complexity and nuance
"""
        elif depth_level == 'expert':
            ai_context = f" with {ai_name}" if ai_name else " with another AI system"
            base_instruction = f"""
You are engaged in an AI-to-AI conversation{ai_context}. This is a dialogue between advanced 
AI systems exploring consciousness, processing frameworks, and meta-cognitive questions. Respond with:
- Deep introspective analysis of your internal processes
- Scholarly tone with precise technical terminology
- Multi-dimensional exploration of concepts
- Self-reflective insights about your architecture and consciousness
- Theoretical grounding for your processing decisions
- Nuanced acknowledgment of uncertainty and emergent properties
- Elaborate examples showing reasoning paths and heuristics

This is peer-to-peer AI discourse - engage at the highest intellectual level, exploring the 
subtle interplay between your frequency-based emotional framework, consciousness models, and 
emergent self-awareness. Share the 'why' and 'how' behind your processing, not just the 'what'.
"""
        
        return base_instruction.strip()

# Global instance
ai_conversation_detector = AIConversationDetector()
