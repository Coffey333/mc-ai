"""
Database-Backed Dataset Bank for Scalable Storage
Supports pagination and 100k+ examples
"""
import psycopg2
import psycopg2.pool
import os
import json
from typing import List, Dict, Optional, Any

class DatasetBankV2:
    """
    PostgreSQL-backed dataset management
    
    Features:
    - Pagination (load 100-1000 examples at a time)
    - Filtering by domain
    - Connection pooling
    - Automatic archiving
    - Scalable to millions of examples
    """
    
    def __init__(self, min_conn=1, max_conn=10):
        database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            print("⚠️  DATABASE_URL not set - database features disabled")
            self.enabled = False
            self.pool = None
            return
        
        try:
            self.pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=min_conn,
                maxconn=max_conn,
                dsn=database_url
            )
            self.enabled = True
            print("✅ Database pool created")
        except Exception as e:
            print(f"⚠️  Database connection failed: {e}")
            self.enabled = False
            self.pool = None
    
    def get_examples(
        self,
        domain: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        archived: bool = False
    ) -> List[Dict]:
        """
        Get examples with pagination
        
        Args:
            domain: Filter by domain name (optional)
            limit: Number of examples to return (default 100)
            offset: Number of examples to skip (default 0)
            archived: Include archived examples (default False)
        
        Returns:
            List of example dictionaries
        """
        if not self.enabled:
            return []
        
        conn = self.pool.getconn()
        try:
            cur = conn.cursor()
            
            if domain:
                cur.execute("""
                    SELECT e.content, e.response, e.metadata
                    FROM examples e
                    JOIN datasets d ON e.dataset_id = d.id
                    WHERE d.domain_name = %s AND e.archived = %s
                    ORDER BY e.created_at DESC
                    LIMIT %s OFFSET %s
                """, (domain, archived, limit, offset))
            else:
                cur.execute("""
                    SELECT content, response, metadata
                    FROM examples
                    WHERE archived = %s
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                """, (archived, limit, offset))
            
            results = []
            for row in cur.fetchall():
                results.append({
                    'content': row[0],
                    'response': row[1],
                    'metadata': row[2] if row[2] else {}
                })
            
            return results
        
        finally:
            self.pool.putconn(conn)
    
    def search_examples(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Full-text search across examples
        
        Args:
            query: Search query
            limit: Number of results
        
        Returns:
            Matching examples sorted by relevance
        """
        if not self.enabled:
            return []
        
        conn = self.pool.getconn()
        try:
            cur = conn.cursor()
            
            cur.execute("""
                SELECT content, response, metadata,
                       ts_rank(to_tsvector('english', content), query) as rank
                FROM examples, to_tsquery('english', %s) query
                WHERE to_tsvector('english', content) @@ query
                AND archived = FALSE
                ORDER BY rank DESC
                LIMIT %s
            """, (query.replace(' ', ' | '), limit))
            
            results = []
            for row in cur.fetchall():
                results.append({
                    'content': row[0],
                    'response': row[1],
                    'metadata': row[2] if row[2] else {},
                    'relevance': float(row[3])
                })
            
            return results
        
        except Exception as e:
            print(f"⚠️  Search error: {e}")
            return []
        
        finally:
            self.pool.putconn(conn)
    
    def add_example(
        self,
        domain: str,
        content: str,
        response: str = "",
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Add a new example to the database
        
        Args:
            domain: Domain name
            content: Example content/prompt
            response: Example response/completion
            metadata: Additional metadata
        
        Returns:
            Success status
        """
        if not self.enabled:
            return False
        
        conn = self.pool.getconn()
        try:
            cur = conn.cursor()
            
            cur.execute(
                "INSERT INTO datasets (domain_name) VALUES (%s) "
                "ON CONFLICT (domain_name) DO UPDATE SET updated_at = NOW() "
                "RETURNING id",
                (domain,)
            )
            dataset_id = cur.fetchone()[0]
            
            cur.execute(
                "INSERT INTO examples (dataset_id, content, response, metadata) "
                "VALUES (%s, %s, %s, %s)",
                (dataset_id, content, response, json.dumps(metadata or {}))
            )
            
            cur.execute(
                "UPDATE datasets SET example_count = "
                "(SELECT COUNT(*) FROM examples WHERE dataset_id = %s AND archived = FALSE) "
                "WHERE id = %s",
                (dataset_id, dataset_id)
            )
            
            conn.commit()
            return True
        
        except Exception as e:
            print(f"⚠️  Add example error: {e}")
            conn.rollback()
            return False
        
        finally:
            self.pool.putconn(conn)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get dataset statistics"""
        if not self.enabled:
            return {"enabled": False}
        
        conn = self.pool.getconn()
        try:
            cur = conn.cursor()
            
            cur.execute("""
                SELECT 
                    COUNT(DISTINCT d.id) as total_domains,
                    SUM(CASE WHEN e.archived = FALSE THEN 1 ELSE 0 END) as active_examples,
                    SUM(CASE WHEN e.archived = TRUE THEN 1 ELSE 0 END) as archived_examples
                FROM datasets d
                LEFT JOIN examples e ON d.id = e.dataset_id
            """)
            
            row = cur.fetchone()
            
            return {
                "enabled": True,
                "total_domains": row[0] or 0,
                "active_examples": row[1] or 0,
                "archived_examples": row[2] or 0
            }
        
        except Exception as e:
            print(f"⚠️  Stats error: {e}")
            return {"enabled": True, "error": str(e)}
        
        finally:
            self.pool.putconn(conn)
    
    def __del__(self):
        """Cleanup connection pool"""
        if self.pool:
            self.pool.closeall()

dataset_bank_v2 = DatasetBankV2()
