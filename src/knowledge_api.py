"""
Knowledge Acquisition API for MC AI
RESTful endpoints for managing autonomous knowledge ingestion and retrieval
"""

from flask import Blueprint, jsonify, request
import logging
from src.knowledge_acquisition.ingestion_manager import IngestionManager, PRIORITIZED_SOURCES
from src.knowledge_acquisition.retrieval_agent import RetrievalAgent
from src.knowledge_acquisition.knowledge_indexer import initialize_index_db

logger = logging.getLogger(__name__)

knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/api/knowledge')

# Initialize database on module load
initialize_index_db()


@knowledge_bp.route('/status', methods=['GET'])
def get_knowledge_status():
    """Get knowledge library status and statistics"""
    try:
        agent = RetrievalAgent()
        stats = agent.get_library_stats()
        
        return jsonify({
            'status': 'success',
            'library_stats': stats,
            'storage_used_mb': stats.get('total_words', 0) * 5 / 1024 / 1024,  # Rough estimate
            'message': f"Knowledge library contains {stats.get('total_sources', 0)} sources"
        })
    
    except Exception as e:
        logger.error(f"Error getting knowledge status: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@knowledge_bp.route('/ingest/source', methods=['POST'])
def ingest_single_source():
    """
    Ingest a single custom knowledge source.
    
    Body: {
        "url": "https://example.com",
        "name": "Example Source",
        "description": "Optional description",
        "priority": "medium"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'status': 'error',
                'error': 'URL is required'
            }), 400
        
        manager = IngestionManager(delay_between_requests=0.5)
        
        success = manager.add_custom_source(
            url=data['url'],
            name=data.get('name', 'Custom Source'),
            description=data.get('description', ''),
            priority=data.get('priority', 'medium')
        )
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Source successfully ingested',
                'stats': manager.get_stats()
            })
        else:
            return jsonify({
                'status': 'error',
                'error': 'Failed to ingest source'
            }), 500
    
    except Exception as e:
        logger.error(f"Error ingesting source: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@knowledge_bp.route('/ingest/tier', methods=['POST'])
def ingest_tier():
    """
    Ingest sources from a specific priority tier.
    
    Body: {
        "tier": 1,
        "max_sources": 5
    }
    """
    try:
        data = request.get_json()
        
        tier = data.get('tier', 1) if data else 1
        max_sources = data.get('max_sources') if data else None
        
        if tier not in PRIORITIZED_SOURCES:
            return jsonify({
                'status': 'error',
                'error': f'Invalid tier: {tier}'
            }), 400
        
        manager = IngestionManager(delay_between_requests=1.0)
        stats = manager.ingest_tier(tier, max_sources)
        
        return jsonify({
            'status': 'success',
            'message': f'Tier {tier} ingestion complete',
            'stats': stats
        })
    
    except Exception as e:
        logger.error(f"Error ingesting tier: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@knowledge_bp.route('/ingest/all', methods=['POST'])
def ingest_all_tiers():
    """
    Ingest sources from all tiers.
    
    Body: {
        "max_per_tier": {
            "1": 5,
            "2": 3,
            "3": 2
        }
    }
    """
    try:
        data = request.get_json()
        max_per_tier = data.get('max_per_tier') if data else None
        
        # Convert string keys to integers if needed
        if max_per_tier:
            max_per_tier = {int(k): v for k, v in max_per_tier.items()}
        
        manager = IngestionManager(delay_between_requests=1.0)
        stats = manager.ingest_all_tiers(max_per_tier)
        
        return jsonify({
            'status': 'success',
            'message': 'Full ingestion complete',
            'stats': stats
        })
    
    except Exception as e:
        logger.error(f"Error during full ingestion: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@knowledge_bp.route('/search', methods=['POST'])
def search_knowledge():
    """
    Search the knowledge library for resonant sources.
    
    Body: {
        "query": "What is consciousness?",
        "top_n": 5,
        "min_similarity": 0.1
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'status': 'error',
                'error': 'Query is required'
            }), 400
        
        query = data['query']
        top_n = data.get('top_n', 5)
        min_similarity = data.get('min_similarity', 0.1)
        
        agent = RetrievalAgent()
        results = agent.find_by_query_text(query, top_n, min_similarity)
        
        # Format results for response
        formatted_results = []
        for result in results:
            formatted_results.append({
                'url': result['url'],
                'score': result['score'],
                'frequency': result['signature']['primary_frequency'],
                'emotion': result['signature']['emotion_basis'],
                'catalog': result['signature']['catalog_type'],
                'word_count': result['signature']['text_features']['word_count']
            })
        
        return jsonify({
            'status': 'success',
            'query': query,
            'results_count': len(formatted_results),
            'results': formatted_results
        })
    
    except Exception as e:
        logger.error(f"Error searching knowledge: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@knowledge_bp.route('/sources', methods=['GET'])
def list_prioritized_sources():
    """List all available prioritized sources"""
    try:
        sources_by_tier = {}
        
        for tier, sources in PRIORITIZED_SOURCES.items():
            sources_by_tier[f"tier_{tier}"] = [
                {
                    'name': s['name'],
                    'url': s['url'],
                    'priority': s['priority'],
                    'description': s['description']
                }
                for s in sources
            ]
        
        return jsonify({
            'status': 'success',
            'sources': sources_by_tier,
            'total_sources': sum(len(s) for s in PRIORITIZED_SOURCES.values())
        })
    
    except Exception as e:
        logger.error(f"Error listing sources: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@knowledge_bp.route('/frequency-range', methods=['GET'])
def search_by_frequency():
    """
    Search for sources by frequency range.
    
    Query params:
    - min_freq: Minimum frequency in Hz
    - max_freq: Maximum frequency in Hz
    - catalog: neuroscience or metaphysical (optional)
    - limit: Max results (default 10)
    """
    try:
        min_freq = float(request.args.get('min_freq', 0))
        max_freq = float(request.args.get('max_freq', 1000))
        catalog = request.args.get('catalog')
        limit = int(request.args.get('limit', 10))
        
        agent = RetrievalAgent()
        urls = agent.find_by_frequency_range(min_freq, max_freq, catalog, limit)
        
        return jsonify({
            'status': 'success',
            'frequency_range': f"{min_freq}-{max_freq}Hz",
            'catalog_filter': catalog or 'all',
            'results_count': len(urls),
            'urls': urls
        })
    
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'error': 'Invalid frequency or limit parameter'
        }), 400
    except Exception as e:
        logger.error(f"Error in frequency search: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500
