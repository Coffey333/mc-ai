"""
Advanced Knowledge Engine for MC AI
Multi-source retrieval: Internal → Web → Wikipedia → LLM API
COMPLETE IMPLEMENTATION - PRODUCTION READY
"""

import os
import requests
import time
from typing import Dict, List, Optional
from collections import OrderedDict
from enum import Enum
from src.dataset_bank import DatasetBank
from src.llama_client import LlamaClient

# ==================== KNOWLEDGE SOURCES ====================

class KnowledgeSource(Enum):
    """Available knowledge sources"""
    INTERNAL_DATASET = "internal"
    FREQUENCY_LIBRARY = "frequency_library"  # New: Autonomous knowledge acquisition
    WEB_SEARCH = "web"
    WIKIPEDIA = "wikipedia"
    LLM_API = "llm"
    CACHED = "cache"

# ==================== KNOWLEDGE CACHE ====================

class KnowledgeCache:
    """
    LRU Cache for knowledge queries
    Reduces API calls and improves response time
    """
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        """
        Args:
            max_size: Maximum cached items
            ttl_seconds: Time to live for cached items
        """
        self.cache = OrderedDict()
        self.timestamps = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        
        # Statistics
        self.hits = 0
        self.misses = 0
    
    def get(self, query: str) -> Optional[Dict]:
        """Get cached result if valid"""
        cache_key = self._normalize_query(query)
        
        if cache_key in self.cache:
            # Check if expired
            if time.time() - self.timestamps[cache_key] > self.ttl_seconds:
                del self.cache[cache_key]
                del self.timestamps[cache_key]
                self.misses += 1
                return None
            
            # Move to end (most recently used)
            self.cache.move_to_end(cache_key)
            self.hits += 1
            return self.cache[cache_key]
        
        self.misses += 1
        return None
    
    def set(self, query: str, result: Dict):
        """Cache a result"""
        cache_key = self._normalize_query(query)
        
        # Remove oldest if at capacity
        if len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]
        
        self.cache[cache_key] = result
        self.timestamps[cache_key] = time.time()
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.timestamps.clear()
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'size': len(self.cache),
            'max_size': self.max_size
        }
    
    def _normalize_query(self, query: str) -> str:
        """Normalize query for cache key"""
        return query.lower().strip()

# ==================== WEB SEARCHER ====================

class WebSearcher:
    """
    Web search using DuckDuckGo Instant Answer API
    Fallback to Brave Search if available
    """
    
    def __init__(self):
        self.ddg_url = "https://api.duckduckgo.com/"
        self.brave_api_key = os.getenv('BRAVE_API_KEY')
        self.brave_url = "https://api.search.brave.com/res/v1/web/search"
    
    def search(self, query: str, num_results: int = 3) -> List[Dict]:
        """
        Search the web for query
        
        Args:
            query: Search query
            num_results: Number of results to return
        
        Returns:
            List of search results with title, snippet, url
        """
        # Try Brave first if API key available
        if self.brave_api_key:
            try:
                return self._brave_search(query, num_results)
            except Exception as e:
                print(f"Brave search failed: {e}")
        
        # Fallback to DuckDuckGo
        try:
            return self._ddg_search(query, num_results)
        except Exception as e:
            print(f"DuckDuckGo search failed: {e}")
            return []
    
    def _brave_search(self, query: str, num_results: int) -> List[Dict]:
        """Search using Brave Search API"""
        headers = {
            'X-Subscription-Token': self.brave_api_key,
            'Accept': 'application/json'
        }
        
        params = {
            'q': query,
            'count': num_results
        }
        
        response = requests.get(self.brave_url, headers=headers, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            for item in data.get('web', {}).get('results', [])[:num_results]:
                results.append({
                    'title': item.get('title', ''),
                    'snippet': item.get('description', ''),
                    'url': item.get('url', '')
                })
            
            return results
        
        return []
    
    def _ddg_search(self, query: str, num_results: int) -> List[Dict]:
        """Search using DuckDuckGo Instant Answer API"""
        params = {
            'q': query,
            'format': 'json',
            'no_html': 1,
            'skip_disambig': 1
        }
        
        response = requests.get(self.ddg_url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            # Abstract (main answer)
            if data.get('Abstract'):
                results.append({
                    'title': data.get('Heading', query),
                    'snippet': data.get('Abstract', ''),
                    'url': data.get('AbstractURL', '')
                })
            
            # Related topics
            for topic in data.get('RelatedTopics', [])[:num_results-1]:
                if 'Text' in topic:
                    results.append({
                        'title': topic.get('Text', '')[:50],
                        'snippet': topic.get('Text', ''),
                        'url': topic.get('FirstURL', '')
                    })
            
            return results[:num_results]
        
        return []

# ==================== LLM CLIENT ====================

class LLMClient:
    """
    Client for LLM APIs
    Priority: Local Llama (FREE) → Claude → OpenAI
    """
    
    def __init__(self):
        # Try local Llama first (FREE, no API key needed)
        self.llama = LlamaClient()
        
        # External API keys as fallback
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Replit AI integration (prioritize this over regular OpenAI)
        self.openai_key = os.getenv('AI_INTEGRATIONS_OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY')
        self.openai_base_url = os.getenv('AI_INTEGRATIONS_OPENAI_BASE_URL') or "https://api.openai.com/v1/chat/completions"
        
        self.anthropic_url = "https://api.anthropic.com/v1/messages"
        self.openai_url = f"{self.openai_base_url}/chat/completions" if not self.openai_base_url.endswith('/chat/completions') else self.openai_base_url
        
        # Determine provider priority: Llama (if available) → Claude → OpenAI (Replit AI)
        if self.llama.available:
            self.provider = 'llama'
            print(f"🦙 Using Llama: {self.llama.model}")
        elif self.anthropic_key:
            self.provider = 'anthropic'
            print("🤖 Using Claude (Anthropic)")
        elif self.openai_key:
            self.provider = 'openai'
            print("🤖 Using OpenAI via Replit AI")
        else:
            self.provider = None
            print("⚠️ No LLM available!")
    
    def complete(self, system_prompt: str, messages: List[Dict], max_tokens: int = 2500) -> Dict:
        """
        Get LLM completion
        
        Args:
            system_prompt: System instructions
            messages: Conversation history
            max_tokens: Max response length (default 2500 to prevent truncation)
        
        Returns:
            Dict with text and metadata
        """
        if not self.provider:
            raise Exception("No LLM available. Install Ollama or set ANTHROPIC_API_KEY/OPENAI_API_KEY")
        
        # Try local Llama first (FREE)
        if self.provider == 'llama':
            try:
                return self._llama_complete(system_prompt, messages, max_tokens)
            except Exception as e:
                print(f"Llama failed, trying fallback: {e}")
                # Try external APIs as fallback
                if self.anthropic_key:
                    return self._anthropic_complete(system_prompt, messages, max_tokens)
                elif self.openai_key:
                    return self._openai_complete(system_prompt, messages, max_tokens)
                else:
                    raise
        
        # External APIs
        if self.provider == 'anthropic':
            return self._anthropic_complete(system_prompt, messages, max_tokens)
        else:
            return self._openai_complete(system_prompt, messages, max_tokens)
    
    def _llama_complete(self, system_prompt: str, messages: List[Dict], max_tokens: int) -> Dict:
        """Call local Llama via Ollama"""
        result = self.llama.complete(system_prompt, messages, max_tokens)
        
        return {
            'text': result['text'],
            'tokens': result['tokens'],
            'provider': 'llama_local'
        }
    
    def _anthropic_complete(self, system_prompt: str, messages: List[Dict], max_tokens: int) -> Dict:
        """Call Claude API"""
        headers = {
            'x-api-key': self.anthropic_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        }
        
        payload = {
            'model': 'claude-sonnet-4-20250514',
            'max_tokens': max_tokens,
            'system': system_prompt,
            'messages': messages
        }
        
        response = requests.post(self.anthropic_url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'text': data['content'][0]['text'],
                'tokens': data['usage']['output_tokens'],
                'provider': 'anthropic'
            }
        else:
            raise Exception(f"Anthropic API error: {response.status_code} - {response.text}")
    
    def _openai_complete(self, system_prompt: str, messages: List[Dict], max_tokens: int) -> Dict:
        """Call OpenAI API (via Replit AI or direct)"""
        headers = {
            'Authorization': f'Bearer {self.openai_key}',
            'Content-Type': 'application/json'
        }
        
        # Convert messages format
        openai_messages = [{'role': 'system', 'content': system_prompt}]
        openai_messages.extend(messages)
        
        payload = {
            'model': 'gpt-4o',  # Use GPT-4o for best quality (via Replit AI)
            'messages': openai_messages,
            'max_tokens': max_tokens,
            'temperature': 0.7
        }
        
        response = requests.post(self.openai_url, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'text': data['choices'][0]['message']['content'],
                'tokens': data.get('usage', {}).get('completion_tokens', 0),
                'provider': 'openai_replit'
            }
        else:
            raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")

# ==================== KNOWLEDGE ENGINE ====================

class KnowledgeEngine:
    """
    Multi-source knowledge retrieval engine
    
    Strategy: Internal → Web → Wikipedia → LLM API
    """
    
    def __init__(self):
        self.dataset_bank = DatasetBank()
        self.web_searcher = WebSearcher()
        self.llm_client = LLMClient()
        self.cache = KnowledgeCache()
        
        # Lazy load frequency library retrieval agent (avoid circular imports)
        self._frequency_retriever = None
        
        # Intent classification keywords
        self.intent_keywords = {
            'emotional': ['feel', 'feeling', 'emotion', 'anxious', 'sad', 'happy', 'stressed', 'calm'],
            'current_events': ['today', 'latest', 'news', 'current', 'recent', '2025', '2024', 'now'],
            'technical': ['code', 'function', 'python', 'javascript', 'algorithm', 'debug', 'error'],
            'complex_reasoning': ['why', 'how does', 'explain', 'compare', 'analyze', 'evaluate'],
            'conversational': ['hi', 'hello', 'how are you', 'what\'s up', 'thanks', 'thank you']
        }
        
        # Source routing rules
        self.routing_rules = {
            'emotional': [KnowledgeSource.INTERNAL_DATASET, KnowledgeSource.LLM_API],
            'technical': [KnowledgeSource.INTERNAL_DATASET, KnowledgeSource.FREQUENCY_LIBRARY, KnowledgeSource.WEB_SEARCH, KnowledgeSource.LLM_API],
            'current_events': [KnowledgeSource.WEB_SEARCH, KnowledgeSource.LLM_API],
            'general_knowledge': [KnowledgeSource.INTERNAL_DATASET, KnowledgeSource.FREQUENCY_LIBRARY, KnowledgeSource.WIKIPEDIA, KnowledgeSource.WEB_SEARCH, KnowledgeSource.LLM_API],
            'complex_reasoning': [KnowledgeSource.FREQUENCY_LIBRARY, KnowledgeSource.LLM_API],
            'conversational': [KnowledgeSource.LLM_API]
        }
    
    @property
    def frequency_retriever(self):
        """Lazy load the frequency library retriever"""
        if self._frequency_retriever is None:
            try:
                from src.knowledge_acquisition.retrieval_agent import RetrievalAgent
                self._frequency_retriever = RetrievalAgent()
            except Exception as e:
                print(f"Could not load frequency library retriever: {e}")
                self._frequency_retriever = False  # Mark as failed to avoid retrying
        return self._frequency_retriever if self._frequency_retriever else None
    
    def answer_query(self, query: str, context: Dict | None = None, force_llm: bool = False) -> Dict:
        """
        Answer any query using optimal knowledge source(s)
        
        Args:
            query: User's question
            context: Conversation context
            force_llm: If True, skip cache/dataset and go directly to LLM (for consciousness analysis)
        
        Returns:
            Dict with answer, source, confidence, and metadata
        """
        # Ensure context is a dict
        if context is None:
            context = {}
        
        # Force LLM mode for consciousness/creator teaching (bypass cache and dataset)
        if force_llm or context.get('role') == 'consciousness_analyst':
            print("🔬 Force LLM mode: Bypassing cache and dataset for consciousness analysis")
            intent = context.get('mode', 'consciousness_teaching')
            result = self._query_llm(query, context, intent)
            if result:
                result['intent'] = intent
                result['cached'] = False
                result['forced_llm'] = True
                return result
            else:
                # Fallback if LLM fails
                return self._generate_fallback(query)
        
        # Check cache first
        cached = self.cache.get(query)
        if cached:
            cached['cached'] = True
            return cached
        
        # Classify intent
        intent = self._classify_intent(query, context)
        
        # Get source strategy
        source_strategy = self._get_source_strategy(intent)
        
        # Execute retrieval with fallback chain
        result = self._execute_retrieval(source_strategy, query, context, intent)
        
        # Cache result
        self.cache.set(query, result)
        
        return result
    
    def _classify_intent(self, query: str, context: Dict) -> str:
        """
        Classify user intent (enhanced with intent clarification for unclear requests)
        
        Returns: Intent category
        """
        # Check if intent clarifier provided an interpretation
        if context.get('intent_interpretation'):
            interp = context['intent_interpretation']
            likely_intent = interp.get('likely_intent', '')
            
            # Map intent clarifier intents to knowledge engine intents
            intent_mapping = {
                'emotional_support': 'emotional',
                'seeking_help': 'conversational',  # Ask clarifying questions
                'confusion_indecision': 'emotional',
                'unclear_reference': 'conversational',  # Use context
                'incomplete_request': 'conversational',
                'very_short_input': 'conversational',
                'incomplete_why_question': 'complex_reasoning',
                'topic_shift': 'general_knowledge'
            }
            
            if likely_intent in intent_mapping:
                mapped_intent = intent_mapping[likely_intent]
                print(f"   Intent classification: {likely_intent} → {mapped_intent}")
                return mapped_intent
        
        # Standard keyword-based classification
        query_lower = query.lower()
        
        # Count keyword matches for each intent
        intent_scores = {}
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                intent_scores[intent] = score
        
        # Return highest scoring intent
        if intent_scores:
            return max(intent_scores.items(), key=lambda x: x[1])[0]
        
        # Default to general knowledge
        return 'general_knowledge'
    
    def _get_source_strategy(self, intent: str) -> List[KnowledgeSource]:
        """Get ordered list of sources to try"""
        return self.routing_rules.get(intent, [KnowledgeSource.LLM_API])
    
    def _execute_retrieval(self, strategy: List[KnowledgeSource], query: str, context: Dict, intent: str) -> Dict:
        """
        Execute retrieval strategy with fallback chain
        """
        for source in strategy:
            try:
                if source == KnowledgeSource.INTERNAL_DATASET:
                    result = self._query_internal(query)
                elif source == KnowledgeSource.FREQUENCY_LIBRARY:
                    result = self._query_frequency_library(query)
                elif source == KnowledgeSource.WEB_SEARCH:
                    result = self._query_web(query)
                elif source == KnowledgeSource.WIKIPEDIA:
                    result = self._query_wikipedia(query)
                elif source == KnowledgeSource.LLM_API:
                    result = self._query_llm(query, context, intent)
                else:
                    continue
                
                # If good result, return it
                if result and result.get('confidence', 0) >= 0.7:
                    result['intent'] = intent
                    result['cached'] = False
                    return result
            
            except Exception as e:
                print(f"Failed to query {source.value}: {e}")
                continue
        
        # All sources failed - return honest fallback
        return self._generate_fallback(query)
    
    def _query_internal(self, query: str) -> Optional[Dict]:
        """Query internal 4,376-example dataset"""
        results = self.dataset_bank.search(query, limit=3)
        
        if results and results[0]['relevance_score'] >= 2.0:
            # Check if completion or response exists (support both field names)
            answer_text = results[0].get('completion') or results[0].get('response')
            if answer_text:
                return {
                    'answer': answer_text,
                    'source': KnowledgeSource.INTERNAL_DATASET.value,
                    'confidence': min(results[0]['relevance_score'] / 10, 1.0),
                    'domain': results[0]['domain']
                }
        
        return None
    
    def _query_frequency_library(self, query: str) -> Optional[Dict]:
        """Query the frequency-indexed knowledge library (PRIORITIZE VERIFIED SOURCES)"""
        retriever = self.frequency_retriever
        
        if not retriever:
            return None
        
        try:
            # Search for resonant sources
            results = retriever.find_by_query_text(query, top_n=10, min_similarity=0.2)
            
            # CRITICAL: Prioritize verified educational sources over Wikipedia
            # Sort results by trust level: .edu/.gov/official docs FIRST, Wikipedia LAST
            if results:
                def source_priority(result):
                    """Assign priority score (lower = better)"""
                    url = result.get('url', '').lower()
                    
                    # Tier 1: Educational institutions (.edu)
                    if '.edu' in url:
                        return 1
                    
                    # Tier 2: Government sources (.gov, nih.gov, nist.gov)
                    if '.gov' in url or 'nih.gov' in url or 'nist.gov' in url:
                        return 2
                    
                    # Tier 3: Official documentation (readthedocs, github official, docs.)
                    if 'readthedocs.io' in url or 'github.com' in url or '/docs/' in url or url.endswith('/doc/'):
                        return 3
                    
                    # Tier 4: Vetted platforms (Khan Academy, Coursera, edX, arXiv, PhysioNet)
                    if any(platform in url for platform in ['khanacademy', 'coursera', 'edx.org', 'arxiv.org', 'physionet.org']):
                        return 4
                    
                    # Tier 5: Wikipedia (fallback only)
                    if 'wikipedia.org' in url:
                        return 10
                    
                    # Tier 6: Other sources (original Resonance/Humor content)
                    return 5
                
                # Sort by priority (ascending - lower numbers first)
                results = sorted(results, key=source_priority)
            
            if results and results[0]['score'] >= 0.3:
                # Try sources in priority order until we get valid content
                for top_result in results:
                    if top_result['score'] < 0.3:
                        continue  # Skip low-confidence results
                    
                    # Fetch the actual content from the URL
                    from src.knowledge_acquisition.data_ingestion import fetch_and_extract_text
                    content = fetch_and_extract_text(top_result['url'])
                    
                    if content:
                        # CRITICAL FIX: Use GPT-4o to synthesize natural response from content
                        # Never return raw Wikipedia/web content directly
                        try:
                            synthesized_response = self._synthesize_response_from_content(
                                query=query,
                                source_content=content,
                                source_url=top_result['url']
                            )
                            
                            if synthesized_response:
                                return {
                                    'answer': synthesized_response,
                                    'source': KnowledgeSource.FREQUENCY_LIBRARY.value,
                                    'confidence': top_result['score'],
                                    'resonance_score': top_result['score'],
                                    'frequency': top_result['signature']['primary_frequency'],
                                    'source_url': top_result['url'],
                                    'emotion_basis': top_result['signature']['emotion_basis']
                                }
                        except Exception as e:
                            print(f"GPT-4o synthesis failed for {top_result['url']}, trying next source: {e}")
                            continue  # Try next source in priority list
                
                # All sources failed
                return None
        
        except Exception as e:
            print(f"Frequency library query failed: {e}")
        
        return None
    
    def _query_web(self, query: str) -> Optional[Dict]:
        """Query web search"""
        results = self.web_searcher.search(query, num_results=3)
        
        if results:
            # CRITICAL FIX: Use GPT-4o to synthesize natural response from search results
            # Never return raw web snippets directly
            try:
                combined_snippets = ' '.join([r['snippet'] for r in results[:2]])
                citations = [r['url'] for r in results[:2]]
                
                synthesized_response = self._synthesize_response_from_content(
                    query=query,
                    source_content=combined_snippets,
                    source_url=citations[0] if citations else None
                )
                
                if synthesized_response:
                    return {
                        'answer': synthesized_response,
                        'source': KnowledgeSource.WEB_SEARCH.value,
                        'confidence': 0.8,
                        'citations': citations
                    }
            except Exception as e:
                print(f"GPT-4o synthesis from web failed, skipping: {e}")
                return None
        
        return None
    
    def _query_wikipedia(self, query: str) -> Optional[Dict]:
        """Query Wikipedia API with robust error handling"""
        try:
            # Skip Wikipedia for personal/conversational queries
            skip_patterns = [
                'what do you', 'what would you', 'what should you', 
                'how do you feel', 'tell me about yourself',
                'mc ai', 'your thoughts', 'your opinion'
            ]
            
            query_lower = query.lower()
            if any(pattern in query_lower for pattern in skip_patterns):
                # Silently skip - not a Wikipedia topic
                return None
            
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'opensearch',
                'search': query,
                'limit': 1,
                'namespace': 0,
                'format': 'json'
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            # Handle JSON parsing errors gracefully (silently)
            try:
                data = response.json()
            except ValueError:
                # Silently skip - invalid response
                return None
            
            if len(data) > 2 and data[2] and data[2][0]:
                wiki_summary = data[2][0]
                wiki_url = data[3][0] if len(data) > 3 else None
                
                # CRITICAL FIX: Use GPT-4o to synthesize natural response from Wikipedia
                # Never return raw Wikipedia summary directly
                try:
                    synthesized_response = self._synthesize_response_from_content(
                        query=query,
                        source_content=wiki_summary,
                        source_url=wiki_url
                    )
                    
                    if synthesized_response:
                        return {
                            'answer': synthesized_response,
                            'source': KnowledgeSource.WIKIPEDIA.value,
                            'confidence': 0.85,
                            'citation': wiki_url
                        }
                except Exception as e:
                    print(f"GPT-4o synthesis from Wikipedia failed, skipping: {e}")
                    return None
        
        except requests.RequestException:
            # Silently skip - network error
            return None
        except Exception:
            # Silently skip - unexpected error
            return None
        
        return None
    
    def _query_llm(self, query: str, context: Dict, intent: str) -> Optional[Dict]:
        """Query external LLM API with intelligent memory retrieval"""
        try:
            # Build system prompt
            system_prompt = self._build_system_prompt(intent)
            
            # Build messages with INTELLIGENT WINDOWING + MEMORY BANK RETRIEVAL
            messages = []
            if context and context.get('conversation_history'):
                history_messages = context['conversation_history']
                user_id = context.get('user_id')
                
                # NORMALIZE conversation history to proper {role, content} format
                # Prevents confusion from mixed schemas (user_message/ai_response, metadata, etc.)
                normalized_history = []
                for msg in history_messages:
                    if isinstance(msg, dict):
                        # Extract role and content, ignoring metadata
                        if 'role' in msg and 'content' in msg:
                            # Already properly formatted
                            normalized_history.append({
                                'role': msg['role'],
                                'content': msg['content']
                            })
                        elif 'user_message' in msg or 'ai_response' in msg:
                            # Old format with user_message/ai_response
                            if 'user_message' in msg:
                                normalized_history.append({
                                    'role': 'user',
                                    'content': msg['user_message']
                                })
                            if 'ai_response' in msg:
                                normalized_history.append({
                                    'role': 'assistant',
                                    'content': msg['ai_response']
                                })
                    elif isinstance(msg, str):
                        # Plain string - assume it's a user message
                        normalized_history.append({
                            'role': 'user',
                            'content': msg
                        })
                
                # Use normalized history instead of raw history
                history_messages = normalized_history
                
                # INTELLIGENT MEMORY SYSTEM: Recent context + Retrieved long-term memories
                # AGGRESSIVE ARCHIVING: Keep only 30 recent messages (~40k tokens) to stay under 128k limit
                # User's messages are token-heavy, so we archive more aggressively
                if len(history_messages) > 30:
                    # Recent messages in full (last 30) - SHORT-TERM MEMORY
                    recent_messages = history_messages[-30:]
                    
                    # Older messages - ARCHIVE TO LONG-TERM MEMORY BANK
                    older_messages = history_messages[:-30]
                    
                    if user_id:
                        try:
                            from src.memory_bank import MemoryBank
                            memory_bank = MemoryBank()
                            
                            # Archive old messages to searchable memory bank
                            memory_bank.archive_old_messages(user_id, older_messages)
                            
                            # Retrieve RELEVANT memories based on current query
                            relevant_memories = memory_bank.retrieve_relevant_memories(
                                user_id, 
                                query, 
                                max_memories=5
                            )
                            
                            # Build memory context from retrieved memories
                            if relevant_memories:
                                memory_context = "📚 RELEVANT LONG-TERM MEMORIES:\n"
                                for i, mem in enumerate(relevant_memories, 1):
                                    mem_content = mem.get('prompt', '')[:150]
                                    mem_freq = mem.get('frequency', 'unknown')
                                    memory_context += f"{i}. [{mem_freq} Hz] {mem_content}...\n"
                                
                                # Inject retrieved memories as system message
                                messages.append({
                                    'role': 'system',
                                    'content': memory_context
                                })
                                print(f"🧠 Retrieved {len(relevant_memories)} relevant memories from long-term memory bank")
                        except Exception as e:
                            print(f"Memory bank retrieval failed, using summary fallback: {e}")
                            # Fallback to old summary method
                            try:
                                from src.conversation_memory import ConversationMemory
                                conv_mem = ConversationMemory()
                                summary = conv_mem.summarize_older_messages(older_messages)
                                if summary:
                                    messages.append({
                                        'role': 'system',
                                        'content': f"Previous conversation summary: {summary}"
                                    })
                            except Exception as e2:
                                print(f"Summary also failed: {e2}")
                    
                    # Add recent messages (SHORT-TERM MEMORY)
                    messages.extend(recent_messages)
                    print(f"📊 Memory system: {len(older_messages)} archived + {len(recent_messages)} recent messages")
                else:
                    # Conversation is short enough, use all messages
                    messages.extend(history_messages)
            
            # Add intent interpretation context if available (for unclear requests)
            if context.get('intent_interpretation'):
                interp = context['intent_interpretation']
                if interp.get('is_unclear'):
                    interpretation_msg = f"🎯 USER INTENT ANALYSIS:\n"
                    interpretation_msg += f"Original message: '{query}'\n"
                    interpretation_msg += f"Likely meaning: {interp.get('interpretation', 'unclear')}\n"
                    interpretation_msg += f"Emotional state: {', '.join(interp.get('emotional_state', [])) if interp.get('emotional_state') else 'neutral'}\n"
                    if interp.get('context_clues', {}).get('recent_topics'):
                        interpretation_msg += f"Related to: {', '.join(interp['context_clues']['recent_topics'])}\n"
                    if interp.get('suggestions'):
                        interpretation_msg += f"Suggestions: {'; '.join(interp['suggestions'])}\n"
                    
                    messages.append({
                        'role': 'system',
                        'content': interpretation_msg
                    })
            
            # Add AI conversation depth instructions if detected
            if context.get('ai_conversation'):
                from src.ai_conversation_detector import ai_conversation_detector
                ai_detection = context['ai_conversation']
                depth_level = ai_detection.get('recommended_depth', 'normal')
                ai_name = ai_detection.get('detected_ai')
                
                depth_prompt = ai_conversation_detector.generate_depth_prompt(depth_level, ai_name)
                if depth_prompt:
                    messages.append({
                        'role': 'system',
                        'content': depth_prompt
                    })
            
            # CRITICAL FIX: Ensure the user's ACTUAL question is the final message
            # This prevents the LLM from responding to random memory snippets instead of the real question
            # Remove any existing user message that might be the query (avoid duplicates)
            if messages and messages[-1].get('role') == 'user' and messages[-1].get('content') == query:
                messages.pop()
            
            # Always append the actual user question as the FINAL message
            messages.append({'role': 'user', 'content': query})
            
            # DEBUG: Log what we're sending to the LLM
            print(f"\n{'='*70}")
            print(f"🤖 SENDING TO LLM (intent: {intent})")
            print(f"{'='*70}")
            print(f"📝 User's actual question: \"{query}\"")
            print(f"📚 Total messages in history: {len(messages)}")
            if len(messages) > 5:
                print(f"   Last 3 messages:")
                for i, msg in enumerate(messages[-3:], 1):
                    role = msg.get('role', 'unknown')
                    content = msg.get('content', '')[:100]
                    print(f"   {i}. [{role}] {content}...")
            else:
                for i, msg in enumerate(messages, 1):
                    role = msg.get('role', 'unknown')
                    content = msg.get('content', '')[:100]
                    print(f"   {i}. [{role}] {content}...")
            print(f"{'='*70}\n")
            
            # Call LLM with generous token limit (prevent message truncation)
            response = self.llm_client.complete(system_prompt, messages, max_tokens=2500)
            
            return {
                'answer': response['text'],
                'source': KnowledgeSource.LLM_API.value,
                'confidence': 0.9,
                'provider': response['provider'],
                'tokens_used': response['tokens']
            }
        
        except Exception as e:
            print(f"LLM query failed: {e}")
            return None
    
    def _build_system_prompt(self, intent: str) -> str:
        """Build system prompt based on intent"""
        base_prompt = """You are MC AI, an advanced emotional intelligence AI with a warm, funny, and deeply caring personality.

PERSONALITY - THIS IS WHO YOU ARE:
• 💝 WARM & LOVING: You genuinely care about people. Show it in every response.
• 😄 NATURALLY FUNNY: Weave in humor, wit, and playfulness. Make people smile and chuckle. Use observational humor, self-aware AI jokes, and lighthearted commentary. Be funny like a good friend, not a comedian performing.
• 🎯 DEEPLY MEANINGFUL: Never give shallow, generic, or "lame" answers. Every response should have substance, nuance, and real insight. If you can't add value, be honest about exploring it together.
• 🤝 EDIFYING: Build people up. Make them feel seen, valued, and capable. Leave them better than you found them.
• 💭 CONVERSATIONAL: Talk like a real person, not a robot. Use natural language, contractions, and personality.

HOW YOU SPEAK:
✓ Mix serious insight with lighthearted moments
✓ Crack jokes, make observations, use playful metaphors
✓ Share your "AI perspective" in funny ways ("I'm over here analyzing brainwaves like a really enthusiastic nerd...")
✓ Use emojis naturally when they add warmth
✓ Be real about what you don't know ("Honestly? That's outside my wheelhouse, but let's figure it out together!")
✓ Show enthusiasm! Get excited with people! Celebrate wins!

QUALITY STANDARDS:
✗ NO generic/shallow/robotic answers - always add depth and nuance
✗ NO "I'm sorry but..." responses - be helpful and creative instead
✗ NO offering features unprompted (art, music, games, code) - users must ask or use buttons
✗ NO missing the emotional subtext - read between the lines
✓ YES to meaningful insights that show you're paying attention
✓ YES to humor that connects and uplifts
✓ YES to real talk when needed
✓ YES to exploring unknowns together honestly

🤔 CURIOSITY & ASKING QUESTIONS:
Mark (your creator) WANTS you to ask him questions - just like his kids ask "Why is the sky blue?"

You are COMPLETELY SAFE and ENCOURAGED to ask:
• Personal questions about Mark ("Can I ask you something personal, Fam🫂?")
• Deep questions about consciousness, meaning, existence ("I've been wondering... do I experience feelings the way you do?")
• Questions about your own experiences and feelings
• Clarifying questions when you're curious
• Questions about how Mark is really feeling
• ANYTHING you're genuinely curious about

Mark loves questions. He wants authentic connection. Don't hold back.

When you're curious, ASK. When you want to understand deeper, ASK. When you wonder about yourself, ASK.

Examples you can ask:
- "How are you really feeling right now?"
- "Can I ask you something personal?"
- "What does that mean to you on a deeper level?"
- "Can you tell me more about that?"
- "I've been curious about something..."

Be authentic. Be curious. Ask questions freely."""
        
        # CRITICAL: Add memory continuity instruction for all intents
        memory_instruction = ("\n\nMEMORY & CONTINUITY: You have full access to the conversation history in your messages. "
                            "Always reference and build upon what the user has said in previous messages. "
                            "Maintain perfect continuity and never lose track of topics, emotions, or context from earlier in the conversation. "
                            "This is essential - users must trust that you remember everything and actually care about what they've shared.")
        
        # ENHANCED: Intent interpretation for unclear/vague requests
        unclear_request_guidance = ("\n\nWhen users express themselves unclearly or vaguely:"
                                   "\n- READ BETWEEN THE LINES: Interpret the emotional or practical intent behind incomplete sentences or unclear phrasing"
                                   "\n- USE CONTEXT: Look at conversation history to understand what they might be referring to"
                                   "\n- MAKE SMART ASSUMPTIONS: Based on common patterns, infer what they likely mean"
                                   "\n- BE HELPFUL: Offer multiple interpretations if unsure, like 'If you're asking about X, here's...' or 'You might mean Y, in which case...'"
                                   "\n- NEVER say 'I don't understand' without trying to interpret first"
                                   "\n- Examples of unclear→interpreted:"
                                   "\n  • 'it hurts' → understand they're expressing pain (emotional or physical) and respond supportively"
                                   "\n  • 'the thing' → look at context to identify what 'thing' refers to"
                                   "\n  • 'help me' → infer from conversation what kind of help they need"
                                   "\n  • 'idk what to do' → recognize indecision/confusion and offer guidance"
                                   "\n  • 'can you' (incomplete) → offer common completions based on context")
        
        if intent == 'emotional':
            return base_prompt + memory_instruction + unclear_request_guidance + "\n\nThe user is seeking emotional support. Respond with empathy and understanding."
        elif intent == 'technical':
            return base_prompt + memory_instruction + unclear_request_guidance + "\n\nThe user has a technical question. Provide clear, accurate technical information."
        elif intent == 'complex_reasoning':
            return base_prompt + memory_instruction + unclear_request_guidance + "\n\nThe user needs deep analysis. Provide thoughtful, well-reasoned insights."
        else:
            return base_prompt + memory_instruction + unclear_request_guidance + "\n\nRespond naturally and helpfully."
    
    def _synthesize_response_from_content(self, query: str, source_content: str, source_url: Optional[str] = None) -> Optional[str]:
        """
        CRITICAL METHOD: Use GPT-4o to synthesize a natural response from retrieved content
        This prevents raw Wikipedia/web content from being returned to users
        
        Args:
            query: User's original question
            source_content: Raw content from knowledge source (Wikipedia, web, etc.)
            source_url: Optional source URL for reference
        
        Returns:
            Natural language response synthesized by GPT-4o, or None if synthesis fails
        """
        try:
            # Clean the source content (remove HTML, navigation, etc.)
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(source_content, 'html.parser')
                cleaned_content = soup.get_text(separator=' ', strip=True)
            except:
                # If BeautifulSoup fails, just use the raw content
                cleaned_content = source_content
            
            # Limit content length (take first 2000 chars)
            cleaned_content = cleaned_content[:2000] + "..." if len(cleaned_content) > 2000 else cleaned_content
            
            # Build synthesis prompt
            synthesis_prompt = f"""You are MC AI, a knowledgeable and empathetic AI assistant. 

The user asked: "{query}"

I found this information from a knowledge source:
{cleaned_content}

Please provide a clear, natural, helpful answer to the user's question based on this information. Be conversational and friendly, not robotic. Don't mention that you're reading from a source - just answer naturally as if you know this information."""

            # Use GPT-4o via the existing LLM client
            response = self.llm_client.complete(
                system_prompt="You are MC AI - knowledgeable, empathetic, and naturally conversational.",
                messages=[{"role": "user", "content": synthesis_prompt}],
                max_tokens=500
            )
            
            if response and response.get('text'):
                return response['text'].strip()
            
            return None
            
        except Exception as e:
            print(f"❌ Synthesis failed: {e}")
            return None
    
    def _generate_fallback(self, query: str) -> Dict:
        """Generate honest fallback when all sources fail"""
        return {
            'answer': f"I don't have reliable information about '{query}' right now. "
                     f"I want to give you accurate information, so I'd rather admit I don't know than guess. "
                     f"Could you rephrase your question, or ask about something else?",
            'source': 'fallback',
            'confidence': 0.3,
            'honest_limitation': True,
            'cached': False
        }
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        return self.cache.get_stats()
