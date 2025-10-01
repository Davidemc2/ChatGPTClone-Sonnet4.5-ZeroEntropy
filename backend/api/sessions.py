"""
Session management API endpoints
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
from loguru import logger
import uuid


router = APIRouter()


class CreateSessionRequest(BaseModel):
    metadata: Optional[Dict[str, Any]] = None


@router.get("/")
async def list_sessions(app_request: Request):
    """
    List all chat sessions
    """
    try:
        memory_system = app_request.app.state.memory_system
        sessions = memory_system.list_sessions()
        
        return {
            "sessions": sessions,
            "count": len(sessions)
        }
        
    except Exception as e:
        logger.error(f"Error listing sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def create_session(request: CreateSessionRequest, app_request: Request):
    """
    Create a new chat session
    """
    try:
        memory_system = app_request.app.state.memory_system
        session_id = str(uuid.uuid4())
        
        session = memory_system.create_session(
            session_id=session_id,
            metadata=request.metadata
        )
        
        return session
        
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}")
async def get_session(session_id: str, app_request: Request):
    """
    Get session details
    """
    try:
        memory_system = app_request.app.state.memory_system
        session = memory_system.get_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return session
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{session_id}")
async def delete_session(session_id: str, app_request: Request):
    """
    Delete a session
    """
    try:
        memory_system = app_request.app.state.memory_system
        
        if memory_system.delete_session(session_id):
            return {
                "status": "success",
                "message": f"Session {session_id} deleted"
            }
        else:
            raise HTTPException(status_code=404, detail="Session not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))
