"""
Pydantic models and schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class Message(BaseModel):
    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Session(BaseModel):
    id: str
    created_at: str
    updated_at: str
    messages: List[Message] = []
    metadata: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None


class Document(BaseModel):
    id: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    similarity: Optional[float] = None
    entropy_score: Optional[float] = None


class RAGResult(BaseModel):
    content: str
    metadata: Dict[str, Any]
    similarity: float
    entropy_score: float
    final_score: float
