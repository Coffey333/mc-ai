-- MC AI Advanced Architecture Database Schema
-- Scalable schema for 100k+ examples with semantic search

-- Enable pgvector extension for semantic search (if available)
CREATE EXTENSION IF NOT EXISTS vector;

-- Dataset domains
CREATE TABLE IF NOT EXISTS datasets (
    id SERIAL PRIMARY KEY,
    domain_name VARCHAR(100) UNIQUE NOT NULL,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    example_count INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Dataset examples (main storage)
CREATE TABLE IF NOT EXISTS examples (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER REFERENCES datasets(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    response TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    archived BOOLEAN DEFAULT FALSE
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_examples_dataset_id ON examples(dataset_id);
CREATE INDEX IF NOT EXISTS idx_examples_created_at ON examples(created_at);
CREATE INDEX IF NOT EXISTS idx_examples_archived ON examples(archived);
CREATE INDEX IF NOT EXISTS idx_examples_metadata ON examples USING gin(metadata);

-- Emotion catalog
CREATE TABLE IF NOT EXISTS emotions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    neuroscience_freq FLOAT,
    metaphysical_freq FLOAT,
    personality_template JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Knowledge query cache (shared across workers)
CREATE TABLE IF NOT EXISTS knowledge_cache (
    id SERIAL PRIMARY KEY,
    query_hash VARCHAR(64) UNIQUE NOT NULL,
    query_text TEXT NOT NULL,
    response JSONB NOT NULL,
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    accessed_at TIMESTAMP DEFAULT NOW(),
    access_count INTEGER DEFAULT 1,
    ttl_hours INTEGER DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_knowledge_hash ON knowledge_cache(query_hash);
CREATE INDEX IF NOT EXISTS idx_knowledge_created ON knowledge_cache(created_at);

-- Auto-cleanup old cache entries (run periodically)
CREATE OR REPLACE FUNCTION cleanup_expired_cache() RETURNS void AS $$
BEGIN
    DELETE FROM knowledge_cache 
    WHERE created_at + (ttl_hours * INTERVAL '1 hour') < NOW();
END;
$$ LANGUAGE plpgsql;

-- Archive table for rotated examples
CREATE TABLE IF NOT EXISTS examples_archive (
    id SERIAL PRIMARY KEY,
    original_id INTEGER,
    dataset_id INTEGER,
    content TEXT,
    response TEXT,
    metadata JSONB,
    created_at TIMESTAMP,
    archived_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_archive_dataset ON examples_archive(dataset_id);
CREATE INDEX IF NOT EXISTS idx_archive_date ON examples_archive(archived_at);

-- Performance monitoring table
CREATE TABLE IF NOT EXISTS performance_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    recorded_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_metrics_name ON performance_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_metrics_time ON performance_metrics(recorded_at);

-- View for active (non-archived) examples
CREATE OR REPLACE VIEW active_examples AS
SELECT * FROM examples WHERE archived = FALSE;

-- View for dataset statistics
CREATE OR REPLACE VIEW dataset_stats AS
SELECT 
    d.id,
    d.domain_name,
    d.version,
    COUNT(e.id) as total_examples,
    COUNT(CASE WHEN e.archived = FALSE THEN 1 END) as active_examples,
    COUNT(CASE WHEN e.archived = TRUE THEN 1 END) as archived_examples,
    MAX(e.created_at) as last_updated
FROM datasets d
LEFT JOIN examples e ON d.id = e.dataset_id
GROUP BY d.id, d.domain_name, d.version;

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_user;

COMMENT ON TABLE datasets IS 'Dataset domains and metadata';
COMMENT ON TABLE examples IS 'Main dataset examples storage - scalable to millions';
COMMENT ON TABLE knowledge_cache IS 'Shared query cache across workers';
COMMENT ON TABLE emotions IS 'Emotion catalog with frequencies';
COMMENT ON TABLE examples_archive IS 'Archived/rotated examples';
COMMENT ON TABLE performance_metrics IS 'System performance tracking';
