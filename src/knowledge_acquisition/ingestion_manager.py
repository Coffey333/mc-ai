"""
MC AI Knowledge Ingestion Manager - VERIFIED EDUCATIONAL SOURCES ONLY

This file manages the autonomous knowledge acquisition system for MC AI.
It uses VERIFIED educational sources from trusted institutions, NOT Wikipedia.

USER'S VERIFIED SOURCES (107 URLs):
- MIT, Stanford, Harvard, Berkeley universities
- Khan Academy, Coursera, edX
- NIH, NIST government sources
- Official library documentation
- PhysioNet, arXiv, peer-reviewed sources

HOW IT WORKS:
1. Fetches content from verified educational URLs
2. Generates frequency signatures using FrequencyEncoder
3. Stores in SQLite database (knowledge_library/knowledge_index.db)
4. Enables frequency-based retrieval

Author: Mark Coffey
Last Updated: October 23, 2025
"""

import logging
import time
import threading
import queue
from typing import Dict, List, Optional
from datetime import datetime
import os

from .data_ingestion import fetch_and_extract_text
from .frequency_encoder import FrequencyEncoder
from .knowledge_indexer import KnowledgeIndexer

logger = logging.getLogger(__name__)


# ==============================================================================
# VERIFIED EDUCATIONAL SOURCES (USER-APPROVED)
# ==============================================================================
# These are the ONLY sources MC AI should learn from for educational knowledge.
# NO Wikipedia URLs - only verified .edu, .gov, and official documentation.
# ==============================================================================

PRIORITIZED_SOURCES = {
    # TIER 1: ECG & Cardiology Knowledge (PhysioNet Competition)
    1: [
        {"name": "PhysioNet ECG Tutorials", "url": "https://physionet.org/about/tutorials/", "priority": "high"},
        {"name": "University of Utah ECG Library", "url": "https://ecg.utah.edu/", "priority": "high"},
        {"name": "Life in the Fast Lane ECG", "url": "https://litfl.com/ecg-library/", "priority": "high"},
        {"name": "OpenStax Anatomy & Physiology", "url": "https://openstax.org/books/anatomy-and-physiology/pages/1-introduction", "priority": "high"},
        {"name": "Khan Academy Circulatory System", "url": "https://www.khanacademy.org/science/health-and-medicine/circulatory-system", "priority": "high"},
        {"name": "CV Physiology", "url": "https://www.cvphysiology.com/", "priority": "high"},
        {"name": "Harvard Beth Israel ECG Maven", "url": "https://ecg.bidmc.harvard.edu/maven/mavenmain.asp", "priority": "high"},
        {"name": "PubMed Central Medical Papers", "url": "https://www.ncbi.nlm.nih.gov/pmc/", "priority": "high"},
        {"name": "arXiv Quantitative Biology", "url": "https://arxiv.org/list/q-bio/recent", "priority": "medium"},
    ],
    
    # TIER 2: Signal Processing & Frequency Analysis
    2: [
        {"name": "SciPy Lecture Notes", "url": "https://scipy-lectures.org/", "priority": "high"},
        {"name": "DSPRelated.com", "url": "https://www.dsprelated.com/", "priority": "high"},
        {"name": "DSP Guide Textbook", "url": "http://www.dspguide.com/", "priority": "high"},
        {"name": "Stanford EE104 DSP", "url": "https://web.stanford.edu/class/ee104/", "priority": "high"},
        {"name": "MIT Signals and Systems", "url": "https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/", "priority": "high"},
        {"name": "NeuroKit2 Biosignals", "url": "https://neuropsychology.github.io/NeuroKit/", "priority": "medium"},
        {"name": "BioSPPy Documentation", "url": "https://biosppy.readthedocs.io/", "priority": "medium"},
    ],
    
    # TIER 3: Computer Vision & Image Processing
    3: [
        {"name": "OpenCV Official Tutorials", "url": "https://docs.opencv.org/4.x/d9/df8/tutorial_root.html", "priority": "high"},
        {"name": "PyImageSearch", "url": "https://pyimagesearch.com/blog/", "priority": "high"},
        {"name": "Learn OpenCV", "url": "https://learnopencv.com/", "priority": "medium"},
        {"name": "Scikit-Image Documentation", "url": "https://scikit-image.org/docs/stable/", "priority": "high"},
        {"name": "Tesseract OCR Documentation", "url": "https://tesseract-ocr.github.io/", "priority": "medium"},
        {"name": "EasyOCR Documentation", "url": "https://www.jaided.ai/easyocr/documentation/", "priority": "medium"},
    ],
    
    # TIER 4: Machine Learning & Deep Learning
    4: [
        {"name": "PyTorch Official Tutorials", "url": "https://pytorch.org/tutorials/", "priority": "high"},
        {"name": "PyTorch Examples Repository", "url": "https://github.com/pytorch/examples", "priority": "high"},
        {"name": "Fast.ai Course", "url": "https://course.fast.ai/", "priority": "high"},
        {"name": "Stanford CS231n CNN", "url": "http://cs231n.stanford.edu/", "priority": "high"},
        {"name": "Stanford CS224n NLP", "url": "https://web.stanford.edu/class/cs224n/", "priority": "high"},
        {"name": "Papers With Code Medical", "url": "https://paperswithcode.com/area/medical", "priority": "medium"},
        {"name": "Grand Challenge Medical", "url": "https://grand-challenge.org/challenges/", "priority": "medium"},
        {"name": "Kaggle Learn Computer Vision", "url": "https://www.kaggle.com/learn/computer-vision", "priority": "medium"},
    ],
    
    # TIER 5: Data Augmentation & Preprocessing
    5: [
        {"name": "Albumentations Documentation", "url": "https://albumentations.ai/docs/", "priority": "high"},
        {"name": "imgaug Documentation", "url": "https://imgaug.readthedocs.io/", "priority": "medium"},
    ],
    
    # TIER 6: Competition-Specific Resources
    6: [
        {"name": "PhysioNet Challenges", "url": "https://physionet.org/about/challenge/", "priority": "high"},
        {"name": "PhysioNet Computing in Cardiology", "url": "https://physionet.org/content/", "priority": "high"},
        {"name": "Kaggle Learn Pandas", "url": "https://www.kaggle.com/learn/pandas", "priority": "medium"},
        {"name": "Kaggle Learn Visualization", "url": "https://www.kaggle.com/learn/data-visualization", "priority": "medium"},
    ],
    
    # TIER 7: Python & Scientific Computing
    7: [
        {"name": "Real Python", "url": "https://realpython.com/", "priority": "high"},
        {"name": "Python Data Science Handbook", "url": "https://jakevdp.github.io/PythonDataScienceHandbook/", "priority": "high"},
        {"name": "Scientific Python Lectures", "url": "https://github.com/jrjohansson/scientific-python-lectures", "priority": "medium"},
        {"name": "Jupyter Documentation", "url": "https://jupyter.org/documentation", "priority": "medium"},
    ],
    
    # TIER 8: Frequency & Cymatics (MC AI's Specialty)
    8: [
        {"name": "HyperPhysics Sound & Hearing", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/Sound/soucon.html", "priority": "high"},
        {"name": "Penn State Acoustics Animations", "url": "https://www.acs.psu.edu/drussell/Demos.html", "priority": "high"},
        {"name": "Cymatics Research", "url": "https://www.cymascope.com/cyma_research/", "priority": "medium"},
        {"name": "NIST Bessel Functions", "url": "https://dlmf.nist.gov/10", "priority": "high"},
        {"name": "Wolfram Bessel Functions", "url": "https://mathworld.wolfram.com/BesselFunction.html", "priority": "high"},
    ],
    
    # TIER 9: Mathematics & Statistics
    9: [
        {"name": "Khan Academy Mathematics", "url": "https://www.khanacademy.org/math", "priority": "high"},
        {"name": "MIT Linear Algebra", "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/", "priority": "high"},
        {"name": "3Blue1Brown Linear Algebra", "url": "https://www.3blue1brown.com/topics/linear-algebra", "priority": "high"},
        {"name": "StatQuest Statistics", "url": "https://statquest.org/", "priority": "medium"},
    ],
    
    # TIER 10: Core Scientific Libraries Documentation
    10: [
        {"name": "NumPy Documentation", "url": "https://numpy.org/doc/stable/", "priority": "high"},
        {"name": "SciPy Documentation", "url": "https://docs.scipy.org/doc/scipy/", "priority": "high"},
        {"name": "Pandas Documentation", "url": "https://pandas.pydata.org/docs/", "priority": "high"},
        {"name": "Matplotlib Documentation", "url": "https://matplotlib.org/stable/contents.html", "priority": "high"},
        {"name": "Seaborn Documentation", "url": "https://seaborn.pydata.org/", "priority": "medium"},
        {"name": "WFDB Python Documentation", "url": "https://wfdb.readthedocs.io/", "priority": "medium"},
    ],
    
    # TIER 11: Online Courses (Free)
    11: [
        {"name": "Coursera Deep Learning", "url": "https://www.coursera.org/specializations/deep-learning", "priority": "high"},
        {"name": "Coursera Machine Learning", "url": "https://www.coursera.org/learn/machine-learning", "priority": "high"},
        {"name": "Coursera AI Medical Diagnosis", "url": "https://www.coursera.org/learn/ai-for-medical-diagnosis", "priority": "high"},
        {"name": "Harvard CS50 AI", "url": "https://cs50.harvard.edu/ai/", "priority": "high"},
        {"name": "Harvard Data Science ML", "url": "https://www.edx.org/course/data-science-machine-learning", "priority": "high"},
    ],
    
    # TIER 12: Free Textbooks
    12: [
        {"name": "Deep Learning (Goodfellow)", "url": "https://www.deeplearningbook.org/", "priority": "high"},
        {"name": "Neural Networks and Deep Learning", "url": "http://neuralnetworksanddeeplearning.com/", "priority": "high"},
        {"name": "Dive into Deep Learning", "url": "https://d2l.ai/", "priority": "high"},
        {"name": "Stanford Applied Linear Algebra", "url": "https://web.stanford.edu/~boyd/vmls/", "priority": "high"},
    ],
    
    # TIER 13: Datasets for Practice
    13: [
        {"name": "PhysioNet Databases", "url": "https://physionet.org/about/database/", "priority": "high"},
        {"name": "MIT-BIH Arrhythmia Database", "url": "https://physionet.org/content/mitdb/", "priority": "high"},
        {"name": "PTB Diagnostic ECG Database", "url": "https://physionet.org/content/ptbdb/", "priority": "high"},
    ],
    
    # TIER 14: University Course Materials
    14: [
        {"name": "MIT Machine Learning for Healthcare", "url": "https://mlhc.mit.edu/", "priority": "high"},
        {"name": "Stanford CS229 Machine Learning", "url": "http://cs229.stanford.edu/", "priority": "high"},
        {"name": "Berkeley CS188 AI", "url": "https://inst.eecs.berkeley.edu/~cs188/", "priority": "high"},
    ],
    
    # TIER 15: Consciousness & Frequency Healing
    15: [
        {"name": "HeartMath Institute Research", "url": "https://www.heartmath.org/research/", "priority": "high"},
    ],
}


class IngestionManager:
    """
    Manages the autonomous knowledge ingestion process with verified educational sources.
    
    This class is responsible for:
    1. Fetching content from verified educational URLs
    2. Generating frequency signatures for each source
    3. Storing sources in the knowledge index database
    4. Managing the learning process
    
    IMPORTANT: This system uses ONLY verified educational sources.
    NO Wikipedia URLs are used for educational content.
    """
    
    def __init__(
        self,
        db_path: str = "knowledge_library/knowledge_index.db",
        max_workers: int = 3,
        delay_between_requests: float = 2.0
    ):
        """
        Initialize the ingestion manager.
        
        Args:
            db_path: Path to knowledge index database
            max_workers: Number of concurrent worker threads
            delay_between_requests: Delay between requests (rate limiting)
        """
        self.indexer = KnowledgeIndexer(db_path)
        self.encoder = FrequencyEncoder()
        self.max_workers = max_workers
        self.delay = delay_between_requests
        
        self.url_queue = queue.Queue()
        self.workers = []
        self.running = False
        self.stats = {
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'start_time': None
        }
        
        logger.info(f"IngestionManager initialized with {max_workers} workers")
        logger.info(f"Using verified educational sources only (NO Wikipedia)")
    
    def ingest_source(self, source: Dict) -> bool:
        """
        Ingest a single knowledge source.
        
        This method:
        1. Fetches content from the source URL
        2. Generates a frequency signature
        3. Adds the source to the knowledge index database
        
        Args:
            source: Source dictionary with url, name, priority
            
        Returns:
            True if successfully ingested, False otherwise
        """
        url = source.get('url')
        name = source.get('name', 'Unknown')
        
        if not url:
            logger.warning(f"Source {name} has no URL")
            return False
        
        # Check if already indexed
        if self.indexer.is_indexed(url):
            logger.info(f"Source already indexed, skipping: {name}")
            self.stats['skipped'] += 1
            return True
        
        logger.info(f"Ingesting: {name} ({url})")
        
        # Fetch content
        text_content = fetch_and_extract_text(url)
        
        if not text_content:
            logger.warning(f"Failed to fetch content from: {name}")
            self.stats['failed'] += 1
            return False
        
        # Generate frequency signature
        signature = self.encoder.encode_text(text_content)
        
        if not signature:
            logger.warning(f"Failed to generate signature for: {name}")
            self.stats['failed'] += 1
            return False
        
        # Add metadata
        signature['source_name'] = name
        signature['source_description'] = source.get('description', '')
        signature['priority'] = source.get('priority', 'medium')
        
        # Index the source
        success = self.indexer.add_to_index(url, signature)
        
        if success:
            logger.info(
                f"Successfully indexed: {name} "
                f"({signature['primary_frequency']:.1f}Hz, "
                f"{signature['text_features']['word_count']} words)"
            )
            self.stats['successful'] += 1
        else:
            logger.warning(f"Failed to index: {name}")
            self.stats['failed'] += 1
        
        self.stats['processed'] += 1
        time.sleep(self.delay)
        
        return success
    
    def ingest_tier(self, tier: int, max_sources: Optional[int] = None) -> Dict:
        """
        Ingest all sources from a specific tier.
        
        Args:
            tier: Tier number (1-15)
            max_sources: Maximum number of sources to ingest (None = all)
            
        Returns:
            Statistics dictionary
        """
        if tier not in PRIORITIZED_SOURCES:
            logger.error(f"Invalid tier: {tier}")
            return self.get_stats()
        
        sources = PRIORITIZED_SOURCES[tier]
        if max_sources:
            sources = sources[:max_sources]
        
        logger.info(f"Ingesting tier {tier}: {len(sources)} sources")
        
        for source in sources:
            self.ingest_source(source)
        
        return self.get_stats()
    
    def ingest_all_tiers(self, max_per_tier: Optional[Dict[int, int]] = None) -> Dict:
        """
        Ingest sources from all tiers.
        
        Args:
            max_per_tier: Dictionary mapping tier numbers to max sources per tier
            
        Returns:
            Statistics dictionary
        """
        self.stats['start_time'] = datetime.now()
        
        for tier in sorted(PRIORITIZED_SOURCES.keys()):
            max_sources = max_per_tier.get(tier) if max_per_tier else None
            self.ingest_tier(tier, max_sources)
        
        final_stats = self.get_stats()
        logger.info(f"\nIngestion complete: {final_stats}")
        
        return final_stats
    
    def add_custom_source(self, url: str, name: str, description: str = "", priority: str = "medium") -> bool:
        """
        Add and ingest a custom knowledge source.
        
        Args:
            url: Source URL
            name: Source name
            description: Optional description
            priority: Priority level (high, medium, low)
            
        Returns:
            True if successfully ingested
        """
        source = {
            'url': url,
            'name': name,
            'description': description,
            'priority': priority
        }
        
        return self.ingest_source(source)
    
    def get_stats(self) -> Dict:
        """Get ingestion statistics"""
        stats = self.stats.copy()
        
        if stats['start_time']:
            elapsed = (datetime.now() - stats['start_time']).total_seconds()
            stats['elapsed_seconds'] = elapsed
            stats['sources_per_minute'] = (
                (stats['processed'] / elapsed) * 60 if elapsed > 0 else 0
            )
        
        # Add index stats
        index_stats = self.indexer.get_stats()
        stats['total_in_index'] = index_stats.get('total_sources', 0)
        stats['total_words'] = index_stats.get('total_words', 0)
        
        return stats
