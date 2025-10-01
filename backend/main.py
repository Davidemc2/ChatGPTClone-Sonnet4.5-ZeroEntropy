"""
ChatGPT Clone with Zero Entropy Enhanced RAG System
Main FastAPI application entry point

Architecture Philosophy:
- First Principles: Breaking down chat AI to core components
- Zero Entropy: Minimizing uncertainty in knowledge retrieval
- Modular Design: Clear separation of concerns
- Scalability: Built for 10x growth from day one
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from src.api.chat_controller import router as chat_router
from src.api.knowledge_controller import router as knowledge_router
from src.core.zero_entropy_rag import ZeroEntropyRAG
from src.core.vector_store import VectorStore

# Load environment variables
load_dotenv()

# Global instances for dependency injection
rag_engine = None
vector_store = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup application lifecycle"""
    global rag_engine, vector_store
    
    # Initialize core systems
    print("🚀 Initializing Zero Entropy RAG System...")
    
    # Initialize vector store with Zero Entropy principles
    vector_store = VectorStore()
    await vector_store.initialize()
    
    # Initialize RAG engine
    rag_engine = ZeroEntropyRAG(vector_store)
    await rag_engine.initialize()
    
    print("✅ System ready - Zero entropy achieved")
    
    yield
    
    # Cleanup
    print("🔄 Shutting down systems...")
    if rag_engine:
        await rag_engine.shutdown()
    if vector_store:
        await vector_store.shutdown()


# Create FastAPI app with lifecycle management
app = FastAPI(
    title="ChatGPT Clone - Zero Entropy Enhanced",
    description="A ChatGPT clone with enhanced RAG system built on Zero Entropy methodologies",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])
app.include_router(knowledge_router, prefix="/api/v1", tags=["knowledge"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """System health check with entropy status"""
    return {
        "status": "healthy",
        "system": "ChatGPT Clone - Zero Entropy Enhanced",
        "entropy_status": "minimized",
        "rag_engine": "active" if rag_engine else "inactive",
        "vector_store": "active" if vector_store else "inactive"
    }

# Dependency injection functions
def get_rag_engine():
    """Get RAG engine instance"""
    if not rag_engine:
        raise HTTPException(status_code=503, detail="RAG engine not initialized")
    return rag_engine

def get_vector_store():
    """Get vector store instance"""
    if not vector_store:
        raise HTTPException(status_code=503, detail="Vector store not initialized")
    return vector_store


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )