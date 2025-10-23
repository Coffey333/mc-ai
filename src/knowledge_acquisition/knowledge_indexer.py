"""
Knowledge Indexer for MC AI
Stores and manages the frequency signature index in SQLite
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

DB_PATH = "mc_ai.db"


def initialize_index_db(db_path: str = DB_PATH) -> bool:
    """
    Initializes the knowledge_index table in the database.
    
    Args:
        db_path: Path to the SQLite database
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Create main index table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_index (
                    source_url TEXT PRIMARY KEY,
                    content_hash TEXT UNIQUE NOT NULL,
                    frequency_signature TEXT NOT NULL,
                    primary_frequency REAL,
                    catalog_type TEXT,
                    emotion_basis TEXT,
                    word_count INTEGER,
                    ingested_at TEXT NOT NULL,
                    last_accessed TEXT,
                    access_count INTEGER DEFAULT 0
                );
            """)
            
            # Create index for faster frequency lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_primary_frequency 
                ON knowledge_index(primary_frequency);
            """)
            
            # Create index for catalog type
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_catalog_type 
                ON knowledge_index(catalog_type);
            """)
            
            # Create statistics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ingestion_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total_sources INTEGER DEFAULT 0,
                    total_words INTEGER DEFAULT 0,
                    avg_frequency REAL DEFAULT 0,
                    last_updated TEXT
                );
            """)
            
            # Initialize stats if empty
            cursor.execute("SELECT COUNT(*) FROM ingestion_stats")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO ingestion_stats (total_sources, total_words, last_updated)
                    VALUES (0, 0, ?)
                """, (datetime.now().isoformat(),))
            
            conn.commit()
            logger.info("Knowledge index database initialized successfully")
            return True
    
    except sqlite3.Error as e:
        logger.error(f"Database error during initialization: {e}")
        return False


class KnowledgeIndexer:
    """Manages the knowledge index database"""
    
    def __init__(self, db_path: str = DB_PATH):
        """Initialize the indexer"""
        self.db_path = db_path
        initialize_index_db(db_path)
    
    def add_to_index(self, url: str, signature: Dict) -> bool:
        """
        Adds or updates a URL and its frequency signature in the index.
        
        Args:
            url: Source URL
            signature: Frequency signature dictionary
            
        Returns:
            True if successful, False otherwise
        """
        if not url or not signature:
            logger.warning("Cannot add to index: missing URL or signature")
            return False
        
        try:
            sig_json = json.dumps(signature)
            timestamp = datetime.now().isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Insert or replace
                cursor.execute("""
                    INSERT OR REPLACE INTO knowledge_index
                    (source_url, content_hash, frequency_signature, primary_frequency, 
                     catalog_type, emotion_basis, word_count, ingested_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    url,
                    signature.get('content_hash', ''),
                    sig_json,
                    signature.get('primary_frequency', 240.0),
                    signature.get('catalog_type', 'neuroscience'),
                    signature.get('emotion_basis', 'neutral'),
                    signature.get('text_features', {}).get('word_count', 0),
                    timestamp
                ))
                
                # Update statistics
                self._update_stats(cursor)
                
                conn.commit()
            
            logger.info(f"Successfully indexed: {url}")
            return True
        
        except sqlite3.IntegrityError as e:
            logger.warning(f"Duplicate content detected for {url}: {e}")
            return False
        except sqlite3.Error as e:
            logger.error(f"Database error adding index for {url}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error indexing {url}: {e}")
            return False
    
    def is_indexed(self, url: str) -> bool:
        """Check if a URL is already in the index"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT 1 FROM knowledge_index WHERE source_url = ? LIMIT 1",
                    (url,)
                )
                return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logger.error(f"Error checking index for {url}: {e}")
            return False
    
    def get_signature(self, url: str) -> Optional[Dict]:
        """Retrieve the frequency signature for a URL"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT frequency_signature FROM knowledge_index WHERE source_url = ?",
                    (url,)
                )
                result = cursor.fetchone()
                
                if result:
                    return json.loads(result[0])
                return None
        
        except sqlite3.Error as e:
            logger.error(f"Error retrieving signature for {url}: {e}")
            return None
    
    def get_all_signatures(self, limit: Optional[int] = None) -> List[tuple]:
        """
        Get all URLs and their signatures from the index.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of (url, signature_dict) tuples
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT source_url, frequency_signature FROM knowledge_index"
                if limit:
                    query += f" LIMIT {limit}"
                
                cursor.execute(query)
                results = []
                
                for url, sig_json in cursor.fetchall():
                    try:
                        signature = json.loads(sig_json)
                        results.append((url, signature))
                    except json.JSONDecodeError:
                        logger.warning(f"Could not parse signature for {url}")
                
                return results
        
        except sqlite3.Error as e:
            logger.error(f"Error retrieving all signatures: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """Get index statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT total_sources, total_words, avg_frequency, last_updated
                    FROM ingestion_stats
                    ORDER BY id DESC LIMIT 1
                """)
                
                result = cursor.fetchone()
                if result:
                    return {
                        'total_sources': result[0],
                        'total_words': result[1],
                        'avg_frequency': result[2],
                        'last_updated': result[3]
                    }
                
                return {
                    'total_sources': 0,
                    'total_words': 0,
                    'avg_frequency': 0.0,
                    'last_updated': None
                }
        
        except sqlite3.Error as e:
            logger.error(f"Error retrieving stats: {e}")
            return {}
    
    def _update_stats(self, cursor):
        """Update ingestion statistics"""
        cursor.execute("""
            UPDATE ingestion_stats
            SET total_sources = (SELECT COUNT(*) FROM knowledge_index),
                total_words = (SELECT SUM(word_count) FROM knowledge_index),
                avg_frequency = (SELECT AVG(primary_frequency) FROM knowledge_index),
                last_updated = ?
        """, (datetime.now().isoformat(),))
