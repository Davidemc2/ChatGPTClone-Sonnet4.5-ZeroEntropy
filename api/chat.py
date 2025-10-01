"""
Zero Entropy ChatGPT Clone - Vercel Serverless Chat API
Enhanced with NEON PostgreSQL and pgvector for production deployment
"""

import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import logging

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import openai
import psycopg2
from pgvector.psycopg2 import register_vector
import numpy as np
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Zero Entropy ChatGPT Clone", version="2.0.0")

# CORS configuration for Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Global variables for caching
_embedding_model = None
_db_connection = None

def get_embedding_model():
    """Lazy load embedding model for serverless efficiency"""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _embedding_model

def get_db_connection():
    """Get database connection with pgvector support"""
    global _db_connection
    if _db_connection is None or _db_connection.closed:
        _db_connection = psycopg2.connect(DATABASE_URL)
        register_vector(_db_connection)
    return _db_connection

# Pydantic models
class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    use_rag: bool = Field(True, description="Enable RAG enhancement")
    max_tokens: int = Field(1000, description="Maximum response tokens")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI response")
    conversation_id: str = Field(..., description="Conversation ID")
    entropy_score: float = Field(..., description="Response entropy/uncertainty score")
    sources_used: List[str] = Field(default_factory=list, description="RAG sources used")
    processing_time: float = Field(..., description="Processing time in seconds")

class KnowledgeDocument(BaseModel):
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

# Zero Entropy RAG Engine
class ZeroEntropyRAG:
    def __init__(self):
        self.embedding_model = get_embedding_model()
        self.entropy_threshold = 0.7  # Minimum entropy for knowledge acceptance
        
    def calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text"""
        if not text:
            return 0.0
        
        # Character frequency analysis
        char_counts = {}
        for char in text.lower():
            char_counts[char] = char_counts.get(char, 0) + 1
        
        # Calculate Shannon entropy
        text_length = len(text)
        entropy = 0.0
        for count in char_counts.values():
            probability = count / text_length
            if probability > 0:
                entropy -= probability * np.log2(probability)
        
        return min(entropy / 8.0, 1.0)  # Normalize to 0-1 range
    
    def chunk_document(self, content: str, chunk_size: int = 500) -> List[str]:
        """Split document into optimal chunks with minimal information loss"""
        sentences = content.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Filter chunks by entropy threshold
        high_quality_chunks = []
        for chunk in chunks:
            entropy = self.calculate_entropy(chunk)
            if entropy >= self.entropy_threshold:
                high_quality_chunks.append(chunk)
        
        return high_quality_chunks
    
    async def store_document(self, document: KnowledgeDocument) -> bool:
        """Store document in PostgreSQL with vector embeddings"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Chunk document
            chunks = self.chunk_document(document.content)
            
            for i, chunk in enumerate(chunks):
                # Generate embedding
                embedding = self.embedding_model.encode(chunk).tolist()
                
                # Store in database
                cursor.execute("""
                    INSERT INTO knowledge_base (title, content, chunk_index, embedding, metadata, entropy_score)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    document.title,
                    chunk,
                    i,
                    embedding,
                    json.dumps(document.metadata),
                    self.calculate_entropy(chunk)
                ))
            
            conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error storing document: {e}")
            return False
    
    async def retrieve_relevant_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve most relevant context using vector similarity"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Vector similarity search with entropy filtering
            cursor.execute("""
                SELECT title, content, entropy_score, metadata,
                       embedding <-> %s as distance
                FROM knowledge_base 
                WHERE entropy_score >= %s
                ORDER BY embedding <-> %s
                LIMIT %s
            """, (query_embedding, self.entropy_threshold, query_embedding, limit))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "title": row[0],
                    "content": row[1],
                    "entropy_score": row[2],
                    "metadata": json.loads(row[3]) if row[3] else {},
                    "similarity_score": 1 - row[4]  # Convert distance to similarity
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []

# Initialize RAG engine
rag_engine = ZeroEntropyRAG()

# Database initialization
async def init_database():
    """Initialize PostgreSQL database with required tables"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Enable pgvector extension
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
        
        # Create knowledge base table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                embedding vector(384),
                metadata JSONB,
                entropy_score FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                title VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
                role VARCHAR(20) NOT NULL,
                content TEXT NOT NULL,
                entropy_score FLOAT,
                sources_used JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_embedding ON knowledge_base USING ivfflat (embedding vector_cosine_ops)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_updated ON conversations(updated_at DESC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id, created_at)")
        
        conn.commit()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization error: {e}")

# API Routes
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_database()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Zero Entropy ChatGPT Clone",
        "version": "2.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint with Zero Entropy RAG enhancement"""
    start_time = datetime.now()
    
    try:
        # Get or create conversation
        conn = get_db_connection()
        cursor = conn.cursor()
        
        conversation_id = request.conversation_id
        if not conversation_id:
            cursor.execute("INSERT INTO conversations (title) VALUES (%s) RETURNING id", (f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}",))
            conversation_id = cursor.fetchone()[0]
            conn.commit()
        
        # Retrieve conversation history
        cursor.execute("""
            SELECT role, content FROM messages 
            WHERE conversation_id = %s 
            ORDER BY created_at ASC 
            LIMIT 20
        """, (conversation_id,))
        
        history = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
        
        # RAG enhancement
        relevant_context = []
        sources_used = []
        
        if request.use_rag:
            relevant_context = await rag_engine.retrieve_relevant_context(request.message)
            sources_used = [ctx["title"] for ctx in relevant_context]
        
        # Prepare messages for OpenAI
        messages = [
            {
                "role": "system",
                "content": f"""You are a Zero Entropy AI assistant - you provide highly accurate, low-uncertainty responses.

ZERO ENTROPY PRINCIPLES:
- Minimize uncertainty in your responses
- Use only high-confidence information
- Be precise and factual
- Acknowledge when you're uncertain

{f"RELEVANT CONTEXT: {chr(10).join([ctx['content'] for ctx in relevant_context])}" if relevant_context else ""}

Provide helpful, accurate responses while maintaining minimal entropy (uncertainty)."""
            }
        ]
        
        # Add conversation history
        messages.extend(history[-10:])  # Last 10 messages for context
        
        # Add current user message
        messages.append({"role": "user", "content": request.message})
        
        # Generate response using OpenAI
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=0.3,  # Lower temperature for reduced entropy
            top_p=0.9
        )
        
        ai_response = response.choices[0].message.content
        
        # Calculate entropy score
        entropy_score = rag_engine.calculate_entropy(ai_response)
        
        # Store messages in database
        cursor.execute("""
            INSERT INTO messages (conversation_id, role, content, entropy_score, sources_used)
            VALUES (%s, %s, %s, %s, %s)
        """, (conversation_id, "user", request.message, None, None))
        
        cursor.execute("""
            INSERT INTO messages (conversation_id, role, content, entropy_score, sources_used)
            VALUES (%s, %s, %s, %s, %s)
        """, (conversation_id, "assistant", ai_response, entropy_score, json.dumps(sources_used)))
        
        # Update conversation timestamp
        cursor.execute("UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = %s", (conversation_id,))
        
        conn.commit()
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return ChatResponse(
            response=ai_response,
            conversation_id=str(conversation_id),
            entropy_score=entropy_score,
            sources_used=sources_used,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/knowledge")
async def add_knowledge(document: KnowledgeDocument):
    """Add document to knowledge base"""
    try:
        success = await rag_engine.store_document(document)
        if success:
            return {"status": "success", "message": "Document added to knowledge base"}
        else:
            raise HTTPException(status_code=500, detail="Failed to store document")
    except Exception as e:
        logger.error(f"Knowledge endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations")
async def get_conversations():
    """Get list of conversations"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.id, c.title, c.created_at, c.updated_at,
                   COUNT(m.id) as message_count
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id
            GROUP BY c.id, c.title, c.created_at, c.updated_at
            ORDER BY c.updated_at DESC
            LIMIT 50
        """)
        
        conversations = []
        for row in cursor.fetchall():
            conversations.append({
                "id": str(row[0]),
                "title": row[1],
                "created_at": row[2].isoformat(),
                "updated_at": row[3].isoformat(),
                "message_count": row[4]
            })
        
        return {"conversations": conversations}
        
    except Exception as e:
        logger.error(f"Conversations endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations/{conversation_id}/messages")
async def get_conversation_messages(conversation_id: str):
    """Get messages for a specific conversation"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT role, content, entropy_score, sources_used, created_at
            FROM messages
            WHERE conversation_id = %s
            ORDER BY created_at ASC
        """, (conversation_id,))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                "role": row[0],
                "content": row[1],
                "entropy_score": row[2],
                "sources_used": json.loads(row[3]) if row[3] else [],
                "timestamp": row[4].isoformat()
            })
        
        return {"messages": messages}
        
    except Exception as e:
        logger.error(f"Messages endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Vercel serverless function handler
def handler(request, response):
    """Vercel serverless function handler"""
    return app(request, response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

