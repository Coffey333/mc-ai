# Knowledge Acquisition System for MC AI
# Autonomous data ingestion and frequency-based indexing

from .data_ingestion import fetch_and_extract_text
from .frequency_encoder import FrequencyEncoder
from .knowledge_indexer import KnowledgeIndexer, initialize_index_db
from .retrieval_agent import RetrievalAgent
from .ingestion_manager import IngestionManager, PRIORITIZED_SOURCES

__all__ = [
    'fetch_and_extract_text',
    'FrequencyEncoder',
    'KnowledgeIndexer',
    'initialize_index_db',
    'RetrievalAgent',
    'IngestionManager',
    'PRIORITIZED_SOURCES'
]
