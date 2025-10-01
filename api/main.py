"""
FastAPI Backend for Zero Entropy ChatGPT Clone

Architecture:
- RESTful API endpoints for standard operations
- WebSocket support for real-time streaming
- Modular design following Unix philosophy
"""
from fastapi import FastAPI, WebSocket, HTTPException, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import asyncio
import json

from config import settings
from core import ZeroEntropyVectorStore, MemoryManager, RAGEngine


# Initialize FastAPI app
app = FastAPI(
    title="Zero Entropy ChatGPT Clone",
    description="ChatGPT clone enhanced with RAG system based on Zero Entropy principles",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
vector_store = None
rag_engine = None
active_sessions: Dict[str, MemoryManager] = {}


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global vector_store, rag_engine
    
    print("🚀 Initializing Zero Entropy ChatGPT Clone...")
    print(f"📊 Model: {settings.default_model}")
    print(f"🗄️  Vector Store: {settings.chroma_persist_dir}")
    
    # Initialize vector store
    vector_store = ZeroEntropyVectorStore()
    
    # Initialize RAG engine
    rag_engine = RAGEngine(vector_store)
    
    print("✅ System initialized successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down...")


# Pydantic models for API
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    use_rag: bool = True
    stream: bool = False


class ChatResponse(BaseModel):
    response: str
    session_id: str


class KnowledgeAddRequest(BaseModel):
    documents: List[str]
    metadata: Optional[List[Dict[str, Any]]] = None


class KnowledgeSearchRequest(BaseModel):
    query: str
    k: Optional[int] = None


class SessionInfo(BaseModel):
    session_id: str
    message_count: int
    created_at: str


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Zero Entropy ChatGPT Clone",
        "version": "1.0.0",
        "status": "operational",
        "principles": [
            "First Principles Thinking",
            "Minimal Entropy",
            "Modular Architecture",
            "Deterministic Retrieval"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "vector_store": "operational",
        "rag_engine": "operational",
        "active_sessions": len(active_sessions)
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint (non-streaming)
    
    Args:
        request: Chat request with message and options
        
    Returns:
        Chat response with assistant message
    """
    # Get or create session
    session_id = request.session_id or str(uuid.uuid4())
    
    if session_id not in active_sessions:
        active_sessions[session_id] = MemoryManager(session_id, vector_store)
    
    memory = active_sessions[session_id]
    
    # Generate response
    response_text = await rag_engine.generate_response_sync(
        user_message=request.message,
        memory=memory,
        use_rag=request.use_rag
    )
    
    # Store in memory
    memory.add_exchange(request.message, response_text)
    
    return ChatResponse(
        response=response_text,
        session_id=session_id
    )


@app.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time streaming chat
    
    Args:
        websocket: WebSocket connection
        session_id: Session identifier
    """
    await websocket.accept()
    
    # Get or create session
    if session_id not in active_sessions:
        active_sessions[session_id] = MemoryManager(session_id, vector_store)
    
    memory = active_sessions[session_id]
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            user_message = data.get("message", "")
            use_rag = data.get("use_rag", True)
            
            if not user_message:
                continue
            
            # Stream response
            response_chunks = []
            async for chunk in rag_engine.generate_response(
                user_message=user_message,
                memory=memory,
                use_rag=use_rag,
                stream=True
            ):
                response_chunks.append(chunk)
                await websocket.send_json({
                    "type": "chunk",
                    "content": chunk
                })
            
            # Send completion signal
            full_response = "".join(response_chunks)
            await websocket.send_json({
                "type": "complete",
                "full_response": full_response
            })
            
            # Store in memory
            memory.add_exchange(user_message, full_response)
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected: {session_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()


@app.post("/knowledge/add")
async def add_knowledge(request: KnowledgeAddRequest):
    """
    Add documents to the knowledge base
    
    Args:
        request: Documents and metadata to add
        
    Returns:
        Document IDs
    """
    doc_ids = rag_engine.add_knowledge(
        documents=request.documents,
        metadata=request.metadata
    )
    
    return {
        "status": "success",
        "document_ids": doc_ids,
        "count": len(doc_ids)
    }


@app.post("/knowledge/search")
async def search_knowledge(request: KnowledgeSearchRequest):
    """
    Search the knowledge base
    
    Args:
        request: Search query and parameters
        
    Returns:
        Relevant documents
    """
    results = rag_engine.search_knowledge(
        query=request.query,
        k=request.k
    )
    
    return {
        "status": "success",
        "results": results,
        "count": len(results)
    }


@app.get("/sessions")
async def list_sessions():
    """List all active sessions"""
    sessions = []
    for session_id, memory in active_sessions.items():
        summary = memory.get_summary()
        sessions.append(SessionInfo(
            session_id=session_id,
            message_count=summary["message_count"],
            created_at=summary["created_at"]
        ))
    
    return {
        "sessions": sessions,
        "count": len(sessions)
    }


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session details"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    memory = active_sessions[session_id]
    return {
        "session_id": session_id,
        "summary": memory.get_summary(),
        "messages": memory.get_messages()
    }


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    memory = active_sessions[session_id]
    memory.clear()
    del active_sessions[session_id]
    
    return {"status": "success", "message": "Session deleted"}


@app.post("/sessions/{session_id}/search")
async def search_session_memory(session_id: str, query: str, k: int = 3):
    """Search through a session's conversation history"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    memory = active_sessions[session_id]
    results = memory.search_memory(query, k)
    
    return {
        "status": "success",
        "results": results,
        "count": len(results)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
