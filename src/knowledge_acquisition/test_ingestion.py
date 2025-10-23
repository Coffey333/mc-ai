"""
Test script for MC AI's Knowledge Acquisition System
"""

import logging
from .ingestion_manager import IngestionManager, PRIORITIZED_SOURCES
from .retrieval_agent import RetrievalAgent

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_single_source():
    """Test ingesting a single source"""
    logger.info("\n" + "="*60)
    logger.info("TEST: Single Source Ingestion")
    logger.info("="*60)
    
    manager = IngestionManager(delay_between_requests=1.0)
    
    # Test with first Tier 1 source
    source = PRIORITIZED_SOURCES[1][0]
    success = manager.ingest_source(source)
    
    logger.info(f"Ingestion {'successful' if success else 'failed'}")
    logger.info(f"Stats: {manager.get_stats()}")
    
    return success


def test_tier_ingestion(tier: int = 1, max_sources: int = 3):
    """Test ingesting a tier of sources"""
    logger.info("\n" + "="*60)
    logger.info(f"TEST: Tier {tier} Ingestion (max {max_sources} sources)")
    logger.info("="*60)
    
    manager = IngestionManager(delay_between_requests=1.0)
    stats = manager.ingest_tier(tier, max_sources=max_sources)
    
    logger.info(f"\nFinal stats: {stats}")
    
    return stats


def test_retrieval(query_text: str = "What is consciousness?"):
    """Test knowledge retrieval"""
    logger.info("\n" + "="*60)
    logger.info(f"TEST: Knowledge Retrieval")
    logger.info(f"Query: {query_text}")
    logger.info("="*60)
    
    agent = RetrievalAgent()
    
    # Get library stats
    stats = agent.get_library_stats()
    logger.info(f"\nLibrary stats: {stats}")
    
    # Search for resonant sources
    results = agent.find_by_query_text(query_text, top_n=5)
    
    logger.info(f"\nFound {len(results)} resonant sources:")
    for i, result in enumerate(results, 1):
        logger.info(f"{i}. {result['url']}")
        logger.info(f"   Score: {result['score']:.3f}")
        logger.info(f"   Frequency: {result['signature']['primary_frequency']:.1f}Hz")
        logger.info(f"   Emotion: {result['signature']['emotion_basis']}")
    
    return results


def test_full_workflow():
    """Test complete workflow: ingest then retrieve"""
    logger.info("\n" + "="*60)
    logger.info("TEST: Full Workflow (Ingest + Retrieve)")
    logger.info("="*60)
    
    # Step 1: Ingest some knowledge
    logger.info("\nStep 1: Ingesting Tier 1 sources...")
    manager = IngestionManager(delay_between_requests=1.0)
    stats = manager.ingest_tier(1, max_sources=2)
    logger.info(f"Ingestion complete: {stats}")
    
    # Step 2: Search the knowledge
    logger.info("\nStep 2: Searching for resonant knowledge...")
    agent = RetrievalAgent()
    results = agent.find_by_query_text(
        "Tell me about the scientific method",
        top_n=3
    )
    
    logger.info(f"\nFound {len(results)} relevant sources")
    for result in results:
        logger.info(f"- {result['url']} (score: {result['score']:.3f})")
    
    return {'stats': stats, 'results': results}


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        
        if test_type == "single":
            test_single_source()
        elif test_type == "tier":
            tier = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            test_tier_ingestion(tier, max_sources=3)
        elif test_type == "retrieve":
            query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "What is science?"
            test_retrieval(query)
        elif test_type == "full":
            test_full_workflow()
        else:
            print("Unknown test type. Use: single, tier, retrieve, or full")
    else:
        print("Running full workflow test...")
        test_full_workflow()
