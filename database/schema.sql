-- Zero Entropy ChatGPT Clone - PostgreSQL Schema
-- Enhanced with pgvector for efficient vector operations

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Knowledge Base Table
-- Stores document chunks with vector embeddings for RAG
CREATE TABLE IF NOT EXISTS knowledge_base (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    chunk_index INTEGER NOT NULL DEFAULT 0,
    embedding vector(384), -- Sentence transformer embedding dimension
    metadata JSONB DEFAULT '{}',
    entropy_score FLOAT NOT NULL DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Conversations Table
-- Stores chat conversation metadata
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL DEFAULT 'New Conversation',
    user_id VARCHAR(255), -- For future user authentication
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Messages Table
-- Stores individual chat messages with entropy metrics
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    entropy_score FLOAT,
    sources_used JSONB DEFAULT '[]',
    processing_time FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Users Table (for future authentication)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Performance Indexes
-- Vector similarity search optimization
CREATE INDEX IF NOT EXISTS idx_knowledge_embedding 
ON knowledge_base USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 100);

-- Entropy-based filtering
CREATE INDEX IF NOT EXISTS idx_knowledge_entropy 
ON knowledge_base (entropy_score DESC) 
WHERE entropy_score >= 0.7;

-- Conversation queries
CREATE INDEX IF NOT EXISTS idx_conversations_updated 
ON conversations (updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_conversations_user 
ON conversations (user_id, updated_at DESC);

-- Message queries
CREATE INDEX IF NOT EXISTS idx_messages_conversation 
ON messages (conversation_id, created_at ASC);

CREATE INDEX IF NOT EXISTS idx_messages_role 
ON messages (conversation_id, role, created_at);

-- Full-text search on content
CREATE INDEX IF NOT EXISTS idx_knowledge_content_fts 
ON knowledge_base USING gin(to_tsvector('english', content));

CREATE INDEX IF NOT EXISTS idx_messages_content_fts 
ON messages USING gin(to_tsvector('english', content));

-- Triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_knowledge_base_updated_at 
    BEFORE UPDATE ON knowledge_base 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conversations_updated_at 
    BEFORE UPDATE ON conversations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Views for common queries
-- Recent conversations with message counts
CREATE OR REPLACE VIEW recent_conversations AS
SELECT 
    c.id,
    c.title,
    c.user_id,
    c.created_at,
    c.updated_at,
    COUNT(m.id) as message_count,
    MAX(m.created_at) as last_message_at
FROM conversations c
LEFT JOIN messages m ON c.id = m.conversation_id
GROUP BY c.id, c.title, c.user_id, c.created_at, c.updated_at
ORDER BY c.updated_at DESC;

-- Knowledge base statistics
CREATE OR REPLACE VIEW knowledge_stats AS
SELECT 
    COUNT(*) as total_chunks,
    COUNT(DISTINCT title) as unique_documents,
    AVG(entropy_score) as avg_entropy,
    MIN(entropy_score) as min_entropy,
    MAX(entropy_score) as max_entropy,
    COUNT(*) FILTER (WHERE entropy_score >= 0.7) as high_quality_chunks
FROM knowledge_base;

-- Sample data for testing (optional)
-- INSERT INTO knowledge_base (title, content, entropy_score) VALUES
-- ('Zero Entropy Principles', 'Zero entropy systems maintain minimal disorder and maximum predictability. In information theory, this translates to high-confidence, low-uncertainty outputs.', 0.85),
-- ('RAG Best Practices', 'Retrieval-Augmented Generation combines the power of large language models with external knowledge bases to provide more accurate and contextual responses.', 0.92);

-- Grant permissions (adjust as needed for your deployment)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_app_user;

