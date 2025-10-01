"""
Chat Controller - API endpoints for chat functionality

Handles:
- Chat completions with RAG enhancement
- Conversation management
- Real-time streaming responses
- System health monitoring

Zero Entropy Principles:
- Structured request/response handling
- Consistent error responses
- Optimal performance patterns
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import logging

from ..models.chat_models import (
    ChatRequest, ChatApiResponse, ConversationRequest, ConversationResponse,
    SystemStatusResponse, ErrorResponse, ChatStreamRequest
)
from ..core.zero_entropy_rag import ZeroEntropyRAG
from ..core.vector_store import VectorStore
from ..utils.entropy_calculator import EntropyCalculator


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# In-memory conversation storage (in production, use Redis or database)
conversation_storage: Dict[str, List] = {}


# Dependency injection functions (these will be overridden by main.py)
def get_rag_engine():
    """Dependency injection for RAG engine"""
    from main import get_rag_engine
    return get_rag_engine()

def get_vector_store():
    """Dependency injection for vector store"""
    from main import get_vector_store
    return get_vector_store()


@router.post("/chat", response_model=ChatApiResponse)
async def chat_completion(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    rag_engine: ZeroEntropyRAG = Depends(get_rag_engine)
) -> ChatApiResponse:
    """
    Generate chat completion with Zero Entropy RAG enhancement
    
    Features:
    - RAG-enhanced responses
    - Conversation context management
    - Entropy optimization
    - Performance monitoring
    """
    
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
        
        # Log request
        logger.info(f"Chat request: {conversation_id[:12]}... - {len(request.message)} chars")
        
        # Generate response using Zero Entropy RAG
        response = await rag_engine.generate_response(
            message=request.message,
            conversation_id=conversation_id,
            user_context=request.user_context
        )
        
        # Calculate response entropy metrics
        entropy_calculator = EntropyCalculator()
        entropy_metrics = await entropy_calculator.calculate_comprehensive_metrics(
            response.content
        )
        
        # Build API response
        api_response = ChatApiResponse(
            response=response.content,
            conversation_id=conversation_id,
            rag_used=request.use_rag and (response.context_used is not None),
            context_summary=response.context_used.get_context_summary() if response.context_used else None,
            entropy_metrics={
                "shannon_entropy": entropy_metrics.shannon_entropy,
                "certainty_score": entropy_metrics.certainty_score,
                "semantic_coherence": entropy_metrics.semantic_coherence,
                "overall_quality": entropy_metrics.overall_quality
            },
            metadata=response.metadata
        )
        
        # Store conversation in background
        background_tasks.add_task(
            _store_conversation_message,
            conversation_id,
            request.message,
            response.content
        )
        
        # Log success
        logger.info(f"Chat response: {conversation_id[:12]}... - Quality: {entropy_metrics.overall_quality:.2f}")
        
        return api_response
        
    except Exception as e:
        logger.error(f"Chat completion error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )


@router.post("/chat/stream")
async def chat_completion_stream(
    request: ChatStreamRequest,
    rag_engine: ZeroEntropyRAG = Depends(get_rag_engine)
):
    """
    Stream chat completion response (placeholder for future implementation)
    
    Note: Full streaming implementation would require WebSockets or SSE
    """
    
    try:
        # For now, return the regular response in a streaming format
        conversation_id = request.conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
        
        response = await rag_engine.generate_response(
            message=request.message,
            conversation_id=conversation_id,
            user_context=request.user_context
        )
        
        async def generate_stream():
            """Generate streaming response"""
            # Simple word-by-word streaming simulation
            words = response.content.split()
            for i, word in enumerate(words):
                chunk = {
                    "content": word + " ",
                    "done": False,
                    "conversation_id": conversation_id
                }
                yield f"data: {json.dumps(chunk)}\n\n"
                await asyncio.sleep(0.05)  # Simulate streaming delay
                
            # Final chunk
            final_chunk = {
                "content": "",
                "done": True,
                "conversation_id": conversation_id
            }
            yield f"data: {json.dumps(final_chunk)}\n\n"
            
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache"}
        )
        
    except Exception as e:
        logger.error(f"Streaming error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating streaming response: {str(e)}"
        )


@router.get("/conversation/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    limit: int = 20
) -> ConversationResponse:
    """
    Get conversation history with entropy analysis
    """
    
    try:
        # Get conversation from storage
        messages = conversation_storage.get(conversation_id, [])
        
        # Limit messages
        limited_messages = messages[-limit:] if len(messages) > limit else messages
        
        # Calculate conversation entropy status
        entropy_calculator = EntropyCalculator()
        if messages:
            # Analyze entropy trend of recent messages
            recent_content = " ".join([msg.get("content", "") for msg in limited_messages[-5:]])
            entropy_metrics = await entropy_calculator.calculate_comprehensive_metrics(recent_content)
            entropy_status = await entropy_calculator.get_entropy_status(entropy_metrics.shannon_entropy)
        else:
            entropy_status = "No messages"
            
        return ConversationResponse(
            conversation_id=conversation_id,
            messages=limited_messages,
            total_messages=len(messages),
            entropy_status=entropy_status
        )
        
    except Exception as e:
        logger.error(f"Get conversation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving conversation: {str(e)}"
        )


@router.delete("/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    Delete conversation history
    """
    
    try:
        if conversation_id in conversation_storage:
            del conversation_storage[conversation_id]
            logger.info(f"Deleted conversation: {conversation_id}")
            return {"message": f"Conversation {conversation_id} deleted successfully"}
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Conversation {conversation_id} not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete conversation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting conversation: {str(e)}"
        )


@router.get("/conversations")
async def list_conversations():
    """
    List all active conversations
    """
    
    try:
        conversations = []
        
        for conv_id, messages in conversation_storage.items():
            last_message = messages[-1] if messages else None
            conversations.append({
                "conversation_id": conv_id,
                "message_count": len(messages),
                "last_message_time": last_message.get("timestamp") if last_message else None,
                "last_message_preview": last_message.get("content", "")[:100] if last_message else ""
            })
            
        # Sort by last message time
        conversations.sort(
            key=lambda x: x.get("last_message_time", ""),
            reverse=True
        )
        
        return {
            "conversations": conversations,
            "total_count": len(conversations),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"List conversations error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing conversations: {str(e)}"
        )


@router.get("/system/status", response_model=SystemStatusResponse)
async def get_system_status(
    rag_engine: ZeroEntropyRAG = Depends(get_rag_engine),
    vector_store: VectorStore = Depends(get_vector_store)
) -> SystemStatusResponse:
    """
    Get comprehensive system status and health metrics
    """
    
    try:
        # Get RAG engine status
        rag_status = await rag_engine.get_system_entropy_status()
        
        # Get vector store statistics
        vector_stats = await vector_store.get_statistics()
        
        # Calculate system uptime (simplified)
        uptime = "System running"  # In production, calculate actual uptime
        
        return SystemStatusResponse(
            status="healthy",
            uptime=uptime,
            rag_engine_status="active",
            vector_store_status="active",
            total_documents=vector_stats.get("total_documents", 0),
            entropy_metrics={
                "entropy_threshold": rag_status.get("entropy_threshold", 0.3),
                "confidence_threshold": rag_status.get("confidence_threshold", 0.7),
                "system_entropy": 0.2  # Placeholder for calculated system entropy
            }
        )
        
    except Exception as e:
        logger.error(f"System status error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting system status: {str(e)}"
        )


@router.post("/system/reset")
async def reset_system(
    rag_engine: ZeroEntropyRAG = Depends(get_rag_engine),
    vector_store: VectorStore = Depends(get_vector_store)
):
    """
    Reset system state (use with caution)
    """
    
    try:
        # Clear conversation storage
        conversation_storage.clear()
        
        # Reset vector store (optional - commented for safety)
        # await vector_store.reset_collection()
        
        logger.warning("System reset requested")
        
        return {
            "message": "System reset completed",
            "conversations_cleared": True,
            "vector_store_reset": False,  # Set to True if vector store was reset
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"System reset error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error resetting system: {str(e)}"
        )


# Background task functions

async def _store_conversation_message(
    conversation_id: str,
    user_message: str,
    assistant_response: str
):
    """Store conversation message in background"""
    
    try:
        if conversation_id not in conversation_storage:
            conversation_storage[conversation_id] = []
            
        # Add user message
        conversation_storage[conversation_id].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Add assistant response
        conversation_storage[conversation_id].append({
            "role": "assistant",
            "content": assistant_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Limit conversation history (prevent memory bloat)
        max_messages = 100
        if len(conversation_storage[conversation_id]) > max_messages:
            conversation_storage[conversation_id] = \
                conversation_storage[conversation_id][-max_messages:]
                
        logger.info(f"Stored conversation: {conversation_id[:12]}...")
        
    except Exception as e:
        logger.error(f"Error storing conversation: {str(e)}")


# Health check endpoint

@router.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "service": "chat_controller",
        "timestamp": datetime.now().isoformat()
    }