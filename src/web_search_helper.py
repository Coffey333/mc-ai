"""
Web Search Helper for MC AI
Provides fallback web search when knowledge base doesn't have answers
"""

import requests
from typing import Optional

def search_web(query: str) -> Optional[str]:
    """
    Multi-source web search using free APIs
    Tries Wikipedia first, then DuckDuckGo
    """
    # Try Wikipedia first (more reliable)
    result = search_wikipedia(query)
    if result:
        return result
    
    # Fallback to DuckDuckGo
    return search_duckduckgo(query)

def extract_search_terms(query: str) -> str:
    """Extract key search terms from a question - smarter version"""
    import re
    
    query_lower = query.lower().strip()
    
    # Science question patterns - keep these intact!
    science_patterns = {
        r'why is the sky blue': 'diffuse sky radiation',
        r'what are clouds made of': 'cloud formation',
        r'how do stars form': 'star formation',
        r'what is gravity': 'gravity physics',
        r'how does photosynthesis work': 'photosynthesis',
        r'what is dna': 'DNA',
        r'how do magnets work': 'magnetism',
        r'what causes rain': 'precipitation',
        r'why do we have seasons': 'seasonal changes earth',
        r'what is the sun made of': 'sun composition',
        r'how does the moon affect tides': 'lunar tides',
        r'what is evolution': 'evolution biology',
        r'how do plants grow': 'plant growth',
        r'what are atoms': 'atomic structure',
        r'why is water wet': 'water properties'
    }
    
    # Check for known science patterns first
    for pattern, replacement in science_patterns.items():
        if re.search(pattern, query_lower):
            return replacement
    
    # For other questions, use smarter extraction
    # Remove ONLY question starters, keep important context words
    question_starters = r'^(what|who|where|when|why|how|which|tell me|explain|describe)\s+'
    cleaned = re.sub(question_starters, '', query_lower, flags=re.IGNORECASE)
    
    # Remove minor stopwords but keep important ones like "the sky", "is blue"
    minor_stopwords = ['a', 'an', 'about', 'can', 'could', 'do', 'does', 'did', 'me']
    words = cleaned.split()
    key_terms = [w for w in words if w not in minor_stopwords]
    
    # Return joined terms (fallback to cleaned query if no terms left)
    result = ' '.join(key_terms) if key_terms else cleaned
    return result if result else query

def search_wikipedia(query: str) -> Optional[str]:
    """Search Wikipedia using OpenSearch API (better for direct questions)"""
    try:
        url = "https://en.wikipedia.org/w/api.php"
        
        # Wikipedia requires a User-Agent header
        headers = {
            'User-Agent': 'MC-AI/1.0 (Educational AI Assistant; https://replit.com)'
        }
        
        # Extract key search terms from question
        search_terms = extract_search_terms(query)
        
        # Try OpenSearch (works best with key terms, not full questions)
        opensearch_params = {
            'action': 'opensearch',
            'format': 'json',
            'search': search_terms,
            'limit': 1
        }
        
        response = requests.get(url, params=opensearch_params, headers=headers, timeout=5)
        if response.status_code != 200:
            return None
            
        data = response.json()
        
        # OpenSearch returns: [query, [titles], [descriptions], [urls]]
        if len(data) >= 4 and data[1]:
            article_title = data[1][0]  # First title
            
            # Fetch the full article
            content_params = {
                'action': 'query',
                'format': 'json',
                'prop': 'extracts',
                'exintro': True,
                'explaintext': True,
                'titles': article_title,
                'redirects': 1
            }
            
            response = requests.get(url, params=content_params, headers=headers, timeout=5)
            if response.status_code != 200:
                return None
                
            data = response.json()
            pages = data.get('query', {}).get('pages', {})
            
            for page_id, page_data in pages.items():
                if page_id != '-1' and 'extract' in page_data:
                    extract = page_data['extract']
                    if extract and len(extract) > 100:
                        # Get first 2 paragraphs
                        paragraphs = extract.split('\n\n')[:2]
                        result_text = '\n\n'.join(paragraphs)
                        
                        # Truncate if too long
                        if len(result_text) > 800:
                            result_text = result_text[:800] + '...'
                        
                        return f"{result_text}\n\n📚 Source: Wikipedia - {article_title}"
        
        return None
        
    except Exception as e:
        print(f"Wikipedia search error: {e}")
        return None

def search_duckduckgo(query: str) -> Optional[str]:
    """Search DuckDuckGo Instant Answer API"""
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            'q': query,
            'format': 'json',
            'no_html': 1,
            'skip_disambig': 1
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code != 200:
            return None
            
        data = response.json()
        result_parts = []
        
        if data.get('Abstract'):
            result_parts.append(data['Abstract'])
        
        if data.get('Definition'):
            result_parts.append(f"Definition: {data['Definition']}")
        
        if data.get('RelatedTopics') and len(result_parts) == 0:
            for topic in data['RelatedTopics'][:3]:
                if isinstance(topic, dict) and topic.get('Text'):
                    result_parts.append(topic['Text'])
        
        if result_parts:
            answer = '\n\n'.join(result_parts)
            if data.get('AbstractURL'):
                answer += f"\n\n🔍 Source: {data['AbstractURL']}"
            return answer
        
        return None
        
    except Exception as e:
        print(f"DuckDuckGo search error: {e}")
        return None
