"""
Zero Entropy ChatGPT Clone - Main Application
Built with First Principles | Optimized for Production
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from dotenv import load_dotenv

from api import chat, memory, sessions
from core.rag_engine import RAGEngine
from core.memory_system import MemorySystem
from core.llm_client import LLMClient

# Load environment variables
load_dotenv()

# Global instances
rag_engine = None
memory_system = None
llm_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup application resources"""
    global rag_engine, memory_system, llm_client
    
    logger.info("🚀 Initializing Zero Entropy ChatGPT Clone")
    
    # Create data directory if it doesn't exist
    os.makedirs(os.getenv("DATA_DIR", "./data"), exist_ok=True)
    
    # Initialize core components
    logger.info("📦 Loading embedding model...")
    rag_engine = RAGEngine()
    await rag_engine.initialize()
    
    logger.info("🧠 Initializing memory system...")
    memory_system = MemorySystem(rag_engine)
    
    logger.info("🤖 Connecting to LLM...")
    llm_client = LLMClient()
    
    # Store in app state
    app.state.rag_engine = rag_engine
    app.state.memory_system = memory_system
    app.state.llm_client = llm_client
    
    logger.info("✅ Application ready!")
    
    yield
    
    # Cleanup
    logger.info("🔄 Shutting down...")
    if rag_engine:
        await rag_engine.close()


# Create FastAPI app
app = FastAPI(
    title="Zero Entropy ChatGPT Clone",
    description="Advanced ChatGPT clone with RAG-enhanced memory system",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(memory.router, prefix="/api/memory", tags=["memory"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Zero Entropy ChatGPT Clone",
        "version": "1.0.0",
        "status": "operational",
        "philosophy": "First Principles | Zero Entropy | Linux Methodology"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "rag_engine": "ready" if rag_engine else "not_initialized",
        "memory_system": "ready" if memory_system else "not_initialized",
        "llm_client": "ready" if llm_client else "not_initialized"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"🌐 Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
