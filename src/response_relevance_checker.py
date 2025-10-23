"""
Response Relevance Verification System
Ensures MC AI's responses actually answer the user's question
Prevents irrelevant or off-topic responses
"""

import re
from typing import Dict, List, Optional
from difflib import SequenceMatcher


class ResponseRelevanceChecker:
    """
    Verifies that MC AI's response is relevant to the user's question
    Prevents responses that:
    - Answer a different question
    - Go off on tangents
    - Miss the point completely
    """
    
    def __init__(self):
        # Keywords that indicate relevance
        self.topic_indicators = [
            'purpose', 'meaning', 'reason', 'cause', 'effect',
            'how', 'why', 'what', 'when', 'where', 'who'
        ]
    
    def check_relevance(self, query: str, response: str, min_score: float = 0.3) -> Dict:
        """
        Check if response is relevant to query
        
        Args:
            query: User's question
            response: MC AI's answer
            min_score: Minimum relevance score (0-1)
        
        Returns:
            Dict with:
            - is_relevant: bool
            - relevance_score: float (0-1)
            - issues: list of problems found
            - suggestions: list of improvements
        """
        issues = []
        suggestions = []
        
        # Extract key topics from query
        query_topics = self._extract_topics(query)
        
        # Extract key topics from response
        response_topics = self._extract_topics(response)
        
        # Check topic overlap
        topic_overlap = len(query_topics & response_topics) / max(len(query_topics), 1)
        
        # Check for specific question patterns
        question_type = self._identify_question_type(query)
        response_matches_type = self._response_matches_question_type(response, question_type)
        
        # Calculate relevance score
        relevance_score = (topic_overlap * 0.6) + (1.0 if response_matches_type else 0.0) * 0.4
        
        # Identify specific issues
        if topic_overlap < 0.2:
            issues.append("Response topics don't match question topics")
            suggestions.append(f"Focus on: {', '.join(list(query_topics)[:3])}")
        
        if not response_matches_type:
            issues.append(f"Response doesn't match {question_type} question type")
            suggestions.append(f"Provide a {question_type}-focused answer")
        
        # Check for common off-topic patterns
        if self._is_generic_response(response):
            issues.append("Response is too generic")
            suggestions.append("Provide specific information related to the question")
        
        # Check if response is about something completely different
        if self._is_completely_unrelated(query, response):
            issues.append("Response appears to answer a different question")
            suggestions.append("Re-read the user's question and answer it directly")
        
        return {
            'is_relevant': relevance_score >= min_score and len(issues) == 0,
            'relevance_score': relevance_score,
            'issues': issues,
            'suggestions': suggestions,
            'query_topics': list(query_topics),
            'response_topics': list(response_topics),
            'topic_overlap': topic_overlap
        }
    
    def _extract_topics(self, text: str) -> set:
        """Extract key topics from text (nouns, entities, important words)"""
        text_lower = text.lower()
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our',
            'their', 'what', 'which', 'who', 'when', 'where', 'why', 'how'
        }
        
        # Extract words (alphanumeric sequences)
        words = re.findall(r'\b[a-z]+\b', text_lower)
        
        # Filter out stop words and short words
        topics = {word for word in words if word not in stop_words and len(word) > 3}
        
        # Also extract capitalized phrases (likely entities)
        entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        topics.update({e.lower() for e in entities})
        
        return topics
    
    def _identify_question_type(self, query: str) -> str:
        """
        Identify the type of question
        - why: Explanation/reasoning
        - how: Process/method
        - what: Definition/description
        - when: Time
        - where: Location
        - who: Person/identity
        """
        query_lower = query.lower()
        
        if query_lower.startswith('why') or 'why ' in query_lower:
            return 'why'
        elif query_lower.startswith('how') or 'how ' in query_lower:
            return 'how'
        elif query_lower.startswith('what') or 'what ' in query_lower:
            return 'what'
        elif query_lower.startswith('when') or 'when ' in query_lower:
            return 'when'
        elif query_lower.startswith('where') or 'where ' in query_lower:
            return 'where'
        elif query_lower.startswith('who') or 'who ' in query_lower:
            return 'who'
        else:
            return 'general'
    
    def _response_matches_question_type(self, response: str, question_type: str) -> bool:
        """Check if response appropriately addresses the question type"""
        response_lower = response.lower()
        
        if question_type == 'why':
            # Should contain reasoning words
            reasoning_words = ['because', 'reason', 'due to', 'since', 'as a result', 'therefore', 'thus']
            return any(word in response_lower for word in reasoning_words)
        
        elif question_type == 'how':
            # Should contain process/method words
            process_words = ['by', 'through', 'using', 'via', 'step', 'process', 'method', 'way']
            return any(word in response_lower for word in process_words)
        
        elif question_type == 'what':
            # Should contain definitions or descriptions
            definition_words = ['is', 'are', 'refers to', 'means', 'defined as', 'concept']
            return any(word in response_lower for word in definition_words)
        
        elif question_type == 'when':
            # Should contain time references
            time_words = ['when', 'time', 'date', 'year', 'ago', 'future', 'past', 'during', 'period']
            return any(word in response_lower for word in time_words)
        
        elif question_type == 'where':
            # Should contain location references
            location_words = ['where', 'location', 'place', 'in', 'at', 'near', 'region', 'area']
            return any(word in response_lower for word in location_words)
        
        elif question_type == 'who':
            # Should contain person/identity references
            person_words = ['who', 'person', 'people', 'individual', 'group', 'organization', 'he', 'she', 'they']
            return any(word in response_lower for word in person_words)
        
        return True  # General questions don't have strict requirements
    
    def _is_generic_response(self, response: str) -> bool:
        """Detect if response is too generic/template-like"""
        generic_phrases = [
            'i\'m sorry, but',
            'i don\'t have information',
            'i cannot help',
            'as an ai',
            'i am not able to',
            'i don\'t understand',
            'could you please clarify'
        ]
        
        response_lower = response.lower()
        return any(phrase in response_lower for phrase in generic_phrases)
    
    def _is_completely_unrelated(self, query: str, response: str) -> bool:
        """
        Check if response is about something completely different
        Uses keyword overlap to detect major topic mismatches
        """
        query_topics = self._extract_topics(query)
        response_topics = self._extract_topics(response)
        
        # If there's less than 10% topic overlap, it's likely unrelated
        if len(query_topics) > 0:
            overlap = len(query_topics & response_topics) / len(query_topics)
            return overlap < 0.1
        
        return False
    
    def get_improvement_suggestion(self, query: str, response: str) -> Optional[str]:
        """
        Generate a specific suggestion for improving the response
        """
        result = self.check_relevance(query, response)
        
        if result['is_relevant']:
            return None
        
        suggestion = "Response could be improved:\n"
        
        for issue in result['issues']:
            suggestion += f"- {issue}\n"
        
        for tip in result['suggestions']:
            suggestion += f"→ {tip}\n"
        
        # Add specific topic guidance
        if result['query_topics']:
            suggestion += f"\nKey topics to address: {', '.join(list(result['query_topics'])[:5])}"
        
        return suggestion


# Global instance
response_relevance_checker = ResponseRelevanceChecker()
