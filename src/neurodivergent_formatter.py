"""
Neurodivergent Response Formatter
Transforms complex responses into neurodivergent-safe format
"""

import re

class NeurodivergentFormatter:
    """Formats responses to be safe and clear for neurodivergent users"""
    
    @staticmethod
    def format_response(response_text, metadata=None):
        """
        Transform response into neurodivergent-safe format
        
        Rules:
        - Direct answer first
        - Short paragraphs
        - Clear sections
        - No metaphors/idioms
        - Simple language
        - Visual formatting (bullets, numbers, headers)
        """
        # Extract question if present
        question = metadata.get('original_query') if metadata else None
        
        # Split into sections
        sections = response_text.split('\n\n')
        
        formatted = []
        
        # If there's a question, answer it first
        if question and '?' in question:
            # Try to extract direct answer from first section
            first_section = sections[0] if sections else response_text[:200]
            
            # Look for yes/no or direct answers
            direct_answer = NeurodivergentFormatter._extract_direct_answer(first_section)
            if direct_answer:
                formatted.append(f"**Answer:** {direct_answer}\n")
        
        # Process sections
        for i, section in enumerate(sections):
            # Skip empty sections
            if not section.strip():
                continue
            
            # Check for metaphors and replace them
            section = NeurodivergentFormatter._simplify_metaphors(section)
            
            # Break long paragraphs
            section = NeurodivergentFormatter._break_long_paragraphs(section)
            
            # Add clear section headers if missing
            if i > 0 and not section.startswith('#') and not section.startswith('**'):
                # Don't add headers to lists or code blocks
                if not section.strip().startswith(('-', '*', '```', '1.', '2.')):
                    section = f"**More details:**\n{section}"
            
            formatted.append(section)
        
        result = '\n\n'.join(formatted)
        
        # Add offer for more information
        if not any(phrase in result.lower() for phrase in ['need more', 'want to know', 'questions?']):
            result += "\n\n**Questions?** Ask me anything you want to know more about."
        
        return result
    
    @staticmethod
    def _extract_direct_answer(text):
        """Try to extract a direct answer from text"""
        # Look for yes/no
        if re.search(r'\b(yes|no)\b', text.lower()[:100]):
            match = re.search(r'\b(yes|no)\b[,.]?\s+([^.!?]+[.!?])', text.lower())
            if match:
                return match.group(0).capitalize()
        
        # Look for "the answer is..."
        match = re.search(r'the answer is\s+([^.!?]+[.!?])', text.lower())
        if match:
            return match.group(1).capitalize()
        
        # Look for first complete sentence
        match = re.search(r'^([^.!?]+[.!?])', text)
        if match:
            answer = match.group(1).strip()
            # Only return if it's short and direct
            if len(answer) < 100:
                return answer
        
        return None
    
    @staticmethod
    def _simplify_metaphors(text):
        """Replace common metaphors with literal language"""
        metaphors = {
            r'piece of cake': 'easy to do',
            r'break a leg': 'good luck',
            r'pull.*leg': 'joking',
            r'raining cats and dogs': 'raining heavily',
            r'kick the bucket': 'die',
            r'hit the nail on the head': 'exactly right',
            r'bark up the wrong tree': 'looking in the wrong place',
            r'let the cat out of the bag': 'reveal a secret',
            r'spill the beans': 'tell the secret',
            r'break the ice': 'start a conversation',
            r'beat around the bush': 'avoid the point',
            r'cost an arm and a leg': 'very expensive',
            r'call it a day': 'stop working',
            r'cut corners': 'do something poorly to save time',
            r'get the ball rolling': 'start something',
            r'on the same page': 'agree/understand each other',
            r'think outside the box': 'think creatively',
            r'touch base': 'contact someone',
            r'low-hanging fruit': 'easy tasks',
            r'move the needle': 'make progress',
        }
        
        for metaphor, literal in metaphors.items():
            text = re.sub(metaphor, literal, text, flags=re.IGNORECASE)
        
        return text
    
    @staticmethod
    def _break_long_paragraphs(text):
        """Break paragraphs longer than 3 sentences into smaller chunks"""
        # Split by sentences
        sentences = re.split(r'([.!?]+\s+)', text)
        
        if len(sentences) <= 6:  # 3 sentences = 6 parts (sentence + delimiter)
            return text
        
        # Group into chunks of max 3 sentences
        chunks = []
        current_chunk = []
        
        for i in range(0, len(sentences), 2):
            if i + 1 < len(sentences):
                current_chunk.append(sentences[i] + sentences[i + 1])
            else:
                current_chunk.append(sentences[i])
            
            # After 3 sentences, start new chunk
            if len(current_chunk) == 3:
                chunks.append(''.join(current_chunk))
                current_chunk = []
        
        # Add remaining
        if current_chunk:
            chunks.append(''.join(current_chunk))
        
        return '\n\n'.join(chunks)
    
    @staticmethod
    def simplify_technical_content(text):
        """Simplify technical jargon for neurodivergent users"""
        # Add definitions for common technical terms
        simplifications = {
            r'implement(ation)?': 'create/build',
            r'utilize': 'use',
            r'facilitate': 'help with',
            r'paradigm': 'way of thinking',
            r'leverage': 'use',
            r'optimize': 'improve',
            r'iterate': 'repeat',
            r'robust': 'strong',
            r'seamless': 'smooth',
            r'intuitive': 'easy to understand',
        }
        
        for technical, simple in simplifications.items():
            text = re.sub(technical, simple, text, flags=re.IGNORECASE)
        
        return text
    
    @staticmethod
    def validate_safety(text):
        """
        Check if text is safe for neurodivergent users
        Returns warnings if unsafe elements found
        """
        warnings = []
        
        # Check for sarcasm indicators
        sarcasm_indicators = [
            r'yeah,? right',
            r'sure,? thing',
            r'obviously',
            r'of course not',
            r'as if'
        ]
        
        for indicator in sarcasm_indicators:
            if re.search(indicator, text, re.IGNORECASE):
                warnings.append(f"Possible sarcasm detected: {indicator}")
        
        # Check for ambiguous pronouns
        if re.search(r'\bthis\b|\bthat\b|\bit\b', text):
            # This is common, so only warn if excessive
            count = len(re.findall(r'\bthis\b|\bthat\b|\bit\b', text))
            if count > 10:
                warnings.append(f"Many ambiguous pronouns ({count}) - may be unclear")
        
        # Check for very long paragraphs
        paragraphs = text.split('\n\n')
        for i, para in enumerate(paragraphs):
            sentences = re.split(r'[.!?]+', para)
            if len(sentences) > 5:
                warnings.append(f"Paragraph {i+1} has {len(sentences)} sentences - may be overwhelming")
        
        # Check for multiple topics
        topic_indicators = [
            'also', 'additionally', 'another thing',
            'by the way', 'furthermore', 'moreover'
        ]
        topic_count = sum(1 for indicator in topic_indicators if indicator in text.lower())
        if topic_count > 3:
            warnings.append(f"Multiple topics detected ({topic_count}) - may cause confusion")
        
        return {
            'safe': len(warnings) == 0,
            'warnings': warnings
        }
