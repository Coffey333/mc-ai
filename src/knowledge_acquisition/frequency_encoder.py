"""
Frequency Encoder for MC AI
Transforms text into compact frequency signatures using MC AI's cymatic analysis
"""

import logging
import numpy as np
from typing import Dict, Optional
import hashlib

logger = logging.getLogger(__name__)


class FrequencyEncoder:
    """
    Encodes text data into frequency signatures using MC AI's dual-catalog system
    and cymatic pattern analysis
    """
    
    def __init__(self):
        """Initialize the frequency encoder with MC AI's analysis engines"""
        from src.catalogs import get_frequency, detect_catalog_context
        from src.cymatic import CymaticTransformer
        from src.frequency_coupling import FrequencyCouplingAnalyzer
        
        self.get_frequency = get_frequency
        self.detect_catalog = detect_catalog_context
        self.cymatic = CymaticTransformer()
        self.coupling_analyzer = FrequencyCouplingAnalyzer()
        
        logger.info("FrequencyEncoder initialized with MC AI's analysis engines")
    
    def encode_text(self, text: str, min_length: int = 10) -> Optional[Dict]:
        """
        Transforms text into a compact frequency signature.
        
        Args:
            text: The input text to encode
            min_length: Minimum text length (default 10, lower for queries)
            
        Returns:
            Dictionary containing frequency signature with:
            - content_hash: Unique identifier for the text
            - primary_frequency: Base frequency from emotion/content analysis
            - catalog_type: neuroscience or metaphysical
            - harmonic_ladder: Phi-scaled harmonic series
            - cymatic_metrics: Symmetry, complexity, coherence
            - coupling_data: Cross-frequency coupling analysis
            - text_features: Basic statistical features
            - signature_version: For future compatibility
        """
        if not text or len(text) < min_length:
            logger.warning(f"Text too short to encode meaningfully (min: {min_length} chars)")
            return None
        
        try:
            # 1. Generate content hash for uniqueness
            content_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]
            
            # 2. Extract primary frequency using MC AI's emotion analysis
            freq_data = self.get_frequency(text)
            primary_freq = freq_data.get('frequency', 240)  # Default to neutral
            catalog_type = freq_data.get('catalog', 'neuroscience')
            emotion_basis = freq_data.get('emotion', 'neutral')
            
            # 3. Perform cymatic transformation to get harmonic signature
            cymatic_result = self.cymatic.transform(
                text=text,
                base_freq=primary_freq,
                layers=7  # 7 harmonics for comprehensive analysis
            )
            
            # 4. Extract text features for additional context
            text_features = self._extract_text_features(text)
            
            # 5. Create compact signature
            signature = {
                'content_hash': content_hash,
                'primary_frequency': float(primary_freq),
                'catalog_type': catalog_type,
                'emotion_basis': emotion_basis,
                'harmonic_ladder': [float(h) for h in cymatic_result['harmonic_ladder']],
                'cymatic_metrics': {
                    'symmetry': float(cymatic_result['symmetry']),
                    'complexity': float(cymatic_result['complexity']),
                    'coherence': float(cymatic_result['coherence'])
                },
                'coupling_data': cymatic_result.get('coupling', {
                    'coupling_strength': 0.5,
                    'coupling_type': 'unknown'
                }),
                'text_features': text_features,
                'signature_version': '1.0'
            }
            
            logger.info(f"Generated signature: {primary_freq}Hz ({catalog_type}) - {emotion_basis}")
            return signature
        
        except Exception as e:
            logger.error(f"Error encoding text: {e}")
            return None
    
    def _extract_text_features(self, text: str) -> Dict:
        """Extract basic statistical features from text"""
        words = text.split()
        
        # Calculate word frequencies for top keywords
        word_freq = {}
        for word in words:
            word_lower = word.lower().strip('.,!?;:')
            if len(word_lower) > 3:  # Ignore short words
                word_freq[word_lower] = word_freq.get(word_lower, 0) + 1
        
        # Get top 10 keywords
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'length': len(text),
            'word_count': len(words),
            'avg_word_length': np.mean([len(w) for w in words]) if words else 0,
            'unique_words': len(set(words)),
            'top_keywords': [kw[0] for kw in top_keywords]
        }
    
    def calculate_similarity(self, sig1: Dict, sig2: Dict) -> float:
        """
        Calculate resonance similarity between two frequency signatures.
        
        Uses multiple dimensions:
        1. Harmonic overlap (primary metric)
        2. Cymatic pattern similarity
        3. Coupling compatibility
        
        Args:
            sig1, sig2: Frequency signature dictionaries
            
        Returns:
            Similarity score from 0.0 (no resonance) to 1.0 (perfect resonance)
        """
        try:
            scores = []
            
            # 1. Harmonic resonance (50% weight)
            harmonics1 = set(np.round(sig1.get('harmonic_ladder', []), 1))
            harmonics2 = set(np.round(sig2.get('harmonic_ladder', []), 1))
            
            if harmonics1 and harmonics2:
                intersection = len(harmonics1.intersection(harmonics2))
                union = len(harmonics1.union(harmonics2))
                harmonic_score = intersection / union if union > 0 else 0.0
                scores.append(('harmonic', harmonic_score, 0.50))
            
            # 2. Cymatic pattern similarity (30% weight)
            metrics1 = sig1.get('cymatic_metrics', {})
            metrics2 = sig2.get('cymatic_metrics', {})
            
            if metrics1 and metrics2:
                # Compare each metric
                sym_diff = abs(metrics1.get('symmetry', 0.5) - metrics2.get('symmetry', 0.5))
                comp_diff = abs(metrics1.get('complexity', 0.5) - metrics2.get('complexity', 0.5))
                coh_diff = abs(metrics1.get('coherence', 0.5) - metrics2.get('coherence', 0.5))
                
                cymatic_score = 1.0 - (sym_diff + comp_diff + coh_diff) / 3.0
                scores.append(('cymatic', cymatic_score, 0.30))
            
            # 3. Catalog compatibility (20% weight)
            same_catalog = sig1.get('catalog_type') == sig2.get('catalog_type')
            catalog_score = 1.0 if same_catalog else 0.5
            scores.append(('catalog', catalog_score, 0.20))
            
            # Calculate weighted average
            if scores:
                total_similarity = sum(score * weight for _, score, weight in scores)
                logger.debug(f"Similarity scores: {scores} -> {total_similarity:.3f}")
                return float(total_similarity)
            
            return 0.0
        
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
