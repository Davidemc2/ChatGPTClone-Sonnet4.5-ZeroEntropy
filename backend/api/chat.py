"""
Chat API endpoints
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from loguru import logger
import json
import uuid


router = APIRouter()


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    stream: bool = False
    use_rag: bool = True
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class ChatResponse(BaseModel):
    session_id: str
    message: str
    metadata: Optional[Dict[str, Any]] = None


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, app_request: Request):
    """
    Send a message and get a response
    """
    try:
        memory_system = app_request.app.state.memory_system
        llm_client = app_request.app.state.llm_client
        
        # Create or get session
        session_id = request.session_id or str(uuid.uuid4())
        
        if not memory_system.get_session(session_id):
            memory_system.create_session(session_id)
        
        # Add user message to memory
        memory_system.add_message(
            session_id=session_id,
            role="user",
            content=request.message
        )
        
        # Get context with RAG if enabled
        context_messages = memory_system.get_context(
            session_id=session_id,
            include_rag=request.use_rag,
            query=request.message
        )
        
        # Add system prompt if no system message exists
        if not any(msg["role"] == "system" for msg in context_messages):
            system_prompt = {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant with access to relevant context "
                    "from previous conversations and knowledge. Provide accurate, "
                    "thoughtful responses based on the available context."
                )
            }
            context_messages.insert(0, system_prompt)
        
        # Generate response
        response_text = await llm_client.generate_response(
            messages=context_messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False
        )
        
        # Add assistant message to memory
        memory_system.add_message(
            session_id=session_id,
            role="assistant",
            content=response_text
        )
        
        return ChatResponse(
            session_id=session_id,
            message=response_text,
            metadata={
                "rag_used": request.use_rag,
                "context_length": len(context_messages)
            }
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def chat_stream(request: ChatRequest, app_request: Request):
    """
    Stream chat response using Server-Sent Events
    """
    try:
        memory_system = app_request.app.state.memory_system
        llm_client = app_request.app.state.llm_client
        
        # Create or get session
        session_id = request.session_id or str(uuid.uuid4())
        
        if not memory_system.get_session(session_id):
            memory_system.create_session(session_id)
        
        # Add user message to memory
        memory_system.add_message(
            session_id=session_id,
            role="user",
            content=request.message
        )
        
        # Get context
        context_messages = memory_system.get_context(
            session_id=session_id,
            include_rag=request.use_rag,
            query=request.message
        )
        
        # Add system prompt if needed
        if not any(msg["role"] == "system" for msg in context_messages):
            system_prompt = {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant with access to relevant context "
                    "from previous conversations and knowledge. Provide accurate, "
                    "thoughtful responses based on the available context."
                )
            }
            context_messages.insert(0, system_prompt)
        
        # Stream response
        async def generate():
            try:
                # Send session ID first
                yield f"data: {json.dumps({'type': 'session_id', 'session_id': session_id})}\n\n"
                
                full_response = ""
                
                stream = await llm_client.generate_response(
                    messages=context_messages,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                    stream=True
                )
                
                async for chunk in stream:
                    full_response += chunk
                    yield f"data: {json.dumps({'type': 'content', 'content': chunk})}\n\n"
                
                # Add assistant message to memory
                memory_system.add_message(
                    session_id=session_id,
                    role="assistant",
                    content=full_response
                )
                
                # Send completion signal
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
                
            except Exception as e:
                logger.error(f"Error in stream generation: {e}")
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
        
    except Exception as e:
        logger.error(f"Error in chat stream endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}")
async def get_history(session_id: str, app_request: Request):
    """Get chat history for a session"""
    try:
        memory_system = app_request.app.state.memory_system
        session = memory_system.get_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {
            "session_id": session_id,
            "messages": session["messages"],
            "created_at": session["created_at"],
            "updated_at": session["updated_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/history/{session_id}")
async def clear_history(session_id: str, app_request: Request):
    """Clear chat history for a session"""
    try:
        memory_system = app_request.app.state.memory_system
        
        if memory_system.delete_session(session_id):
            return {"status": "success", "message": "History cleared"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
