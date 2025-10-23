"""
Retrieval Agent (Librarian) for MC AI
Finds relevant knowledge sources based on frequency resonance
"""

import logging
import json
import sqlite3
from typing import Dict, List, Optional
from .knowledge_indexer import KnowledgeIndexer
from .frequency_encoder import FrequencyEncoder

logger = logging.getLogger(__name__)


class RetrievalAgent:
    """
    The Librarian: Finds resonant knowledge sources from the frequency index
    """
    
    def __init__(self, db_path: str = "mc_ai.db"):
        """Initialize the retrieval agent"""
        self.indexer = KnowledgeIndexer(db_path)
        self.encoder = FrequencyEncoder()
        logger.info("RetrievalAgent (Librarian) initialized")
    
    def find_resonant_sources(
        self, 
        query_signature: Dict, 
        top_n: int = 5,
        min_similarity: float = 0.1
    ) -> List[Dict]:
        """
        Find the most resonant knowledge sources for a query.
        
        Args:
            query_signature: Frequency signature of the query
            top_n: Number of top results to return
            min_similarity: Minimum similarity threshold (0.0 to 1.0)
            
        Returns:
            List of dictionaries with:
            - url: Source URL
            - score: Similarity score
            - signature: Full frequency signature
        """
        if not query_signature:
            logger.warning("Cannot search with empty query signature")
            return []
        
        results = []
        
        try:
            # SQL prefilter: reduce candidate set before Python scoring
            catalog_type = query_signature.get('catalog_type')
            primary_freq = query_signature.get('primary_frequency', 240)
            
            # Get candidates within frequency band (±30 Hz) and matching catalog
            all_entries = self._get_candidates_by_frequency(
                primary_freq - 30, 
                primary_freq + 30,
                catalog_type
            )
            
            # Fallback to all if prefilter returns nothing
            if not all_entries:
                logger.info("Frequency prefilter returned no candidates, falling back to full scan")
                all_entries = self.indexer.get_all_signatures()
            
            logger.info(f"Searching {len(all_entries)} indexed sources (after SQL prefilter)...")
            
            # Calculate similarity for each entry
            for url, stored_signature in all_entries:
                try:
                    similarity = self.encoder.calculate_similarity(
                        query_signature,
                        stored_signature
                    )
                    
                    if similarity >= min_similarity:
                        results.append({
                            'url': url,
                            'score': similarity,
                            'signature': stored_signature
                        })
                
                except Exception as e:
                    logger.error(f"Error comparing signature for {url}: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            # Sort by similarity score (descending)
            results.sort(key=lambda x: x['score'], reverse=True)
            
            # Return top N results
            top_results = results[:top_n]
            
            logger.info(
                f"Found {len(top_results)} resonant sources "
                f"(from {len(results)} above threshold)"
            )
            
            return top_results
        
        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return []
    
    def find_by_query_text(
        self,
        query_text: str,
        top_n: int = 5,
        min_similarity: float = 0.1
    ) -> List[Dict]:
        """
        Convenience method: Find resonant sources directly from query text.
        
        Args:
            query_text: The query text to search for
            top_n: Number of results to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of result dictionaries
        """
        if not query_text or len(query_text) < 10:
            logger.warning("Query text too short for meaningful search")
            return []
        
        # Generate query signature
        query_signature = self.encoder.encode_text(query_text)
        
        if not query_signature:
            logger.error("Failed to generate query signature")
            return []
        
        # Search for resonant sources
        return self.find_resonant_sources(query_signature, top_n, min_similarity)
    
    def find_by_frequency_range(
        self,
        min_freq: float,
        max_freq: float,
        catalog_type: Optional[str] = None,
        limit: int = 10
    ) -> List[str]:
        """
        Find sources within a specific frequency range.
        
        Args:
            min_freq: Minimum frequency in Hz
            max_freq: Maximum frequency in Hz
            catalog_type: 'neuroscience' or 'metaphysical' (optional filter)
            limit: Maximum number of results
            
        Returns:
            List of URLs matching the criteria
        """
        try:
            with sqlite3.connect(self.indexer.db_path) as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT source_url, primary_frequency
                    FROM knowledge_index
                    WHERE primary_frequency BETWEEN ? AND ?
                """
                params: List = [min_freq, max_freq]
                
                if catalog_type:
                    query += " AND catalog_type = ?"
                    params.append(catalog_type)
                
                query += f" LIMIT {limit}"
                
                cursor.execute(query, params)
                results = [row[0] for row in cursor.fetchall()]
                
                logger.info(
                    f"Found {len(results)} sources in range "
                    f"{min_freq}-{max_freq}Hz"
                )
                
                return results
        
        except sqlite3.Error as e:
            logger.error(f"Database error during frequency range search: {e}")
            return []
    
    def _get_candidates_by_frequency(
        self, 
        min_freq: float, 
        max_freq: float, 
        catalog_type: Optional[str] = None
    ) -> List[tuple]:
        """
        SQL prefilter: Get candidates by frequency range and catalog.
        Uses indexed columns for fast filtering.
        """
        try:
            with sqlite3.connect(self.indexer.db_path) as conn:
                cursor = conn.cursor()
                
                if catalog_type:
                    query = """
                        SELECT source_url, frequency_signature
                        FROM knowledge_index
                        WHERE primary_frequency BETWEEN ? AND ?
                          AND catalog_type = ?
                        ORDER BY ABS(primary_frequency - ?)
                        LIMIT 500
                    """
                    params = (min_freq, max_freq, catalog_type, (min_freq + max_freq) / 2)
                else:
                    query = """
                        SELECT source_url, frequency_signature
                        FROM knowledge_index
                        WHERE primary_frequency BETWEEN ? AND ?
                        ORDER BY ABS(primary_frequency - ?)
                        LIMIT 500
                    """
                    params = (min_freq, max_freq, (min_freq + max_freq) / 2)
                
                cursor.execute(query, params)
                results = []
                
                for url, sig_json in cursor.fetchall():
                    try:
                        signature = json.loads(sig_json)
                        results.append((url, signature))
                    except json.JSONDecodeError:
                        logger.warning(f"Could not parse signature for {url}")
                        continue
                
                logger.info(f"SQL prefilter returned {len(results)} candidates")
                return results
        
        except Exception as e:
            logger.error(f"Error in SQL prefilter: {e}")
            return []
    
    def get_library_stats(self) -> Dict:
        """Get statistics about the knowledge library"""
        stats = self.indexer.get_stats()
        
        # Add some calculated metrics
        if stats.get('total_sources', 0) > 0:
            stats['avg_words_per_source'] = (
                stats['total_words'] / stats['total_sources']
            )
        else:
            stats['avg_words_per_source'] = 0
        
        return stats
