"""
Data Models for Zero Entropy RAG ChatGPT Clone

Defines:
- Message structures
- RAG context models
- Response formats
- API request/response schemas

Zero Entropy Principle: Well-structured, predictable data models
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message role enumeration"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """Individual chat message model"""
    role: MessageRole
    content: str = Field(..., min_length=1, max_length=10000)
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class RAGContext(BaseModel):
    """RAG context containing retrieved knowledge and conversation history"""
    retrieved_knowledge: List[str] = Field(default_factory=list)
    conversation_history: List[ChatMessage] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    
    def get_context_summary(self) -> str:
        """Get summary of context for logging"""
        knowledge_count = len(self.retrieved_knowledge)
        history_count = len(self.conversation_history)
        return f"Knowledge: {knowledge_count} pieces, History: {history_count} messages"


class ChatResponse(BaseModel):
    """Complete chat response with context and metadata"""
    content: str
    context_used: Optional[RAGContext] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def get_response_summary(self) -> str:
        """Get summary of response for logging"""
        content_length = len(self.content)
        has_context = self.context_used is not None
        return f"Response: {content_length} chars, RAG: {'Yes' if has_context else 'No'}"


# API Request Models

class ChatRequest(BaseModel):
    """API request for chat completion"""
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    use_rag: bool = Field(True, description="Whether to use RAG enhancement")
    user_context: Optional[Dict[str, Any]] = Field(None, description="Additional user context")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "What is machine learning?",
                "conversation_id": "conv_123",
                "use_rag": True,
                "user_context": {"domain": "technology"}
            }
        }


class ChatStreamRequest(BaseModel):
    """API request for streaming chat completion"""
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_id: Optional[str] = None
    use_rag: bool = True
    user_context: Optional[Dict[str, Any]] = None


class ConversationRequest(BaseModel):
    """Request to get conversation history"""
    conversation_id: str = Field(..., description="Conversation ID")
    limit: Optional[int] = Field(20, ge=1, le=100, description="Number of messages to retrieve")


# API Response Models

class ChatApiResponse(BaseModel):
    """API response for chat completion"""
    response: str
    conversation_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    rag_used: bool
    context_summary: Optional[str] = None
    entropy_metrics: Optional[Dict[str, float]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
        
        schema_extra = {
            "example": {
                "response": "Machine learning is a subset of artificial intelligence...",
                "conversation_id": "conv_123",
                "timestamp": "2024-01-01T12:00:00",
                "rag_used": True,
                "context_summary": "Knowledge: 3 pieces, History: 4 messages",
                "entropy_metrics": {
                    "response_entropy": 0.3,
                    "context_quality": 0.8
                }
            }
        }


class ConversationResponse(BaseModel):
    """Response containing conversation history"""
    conversation_id: str
    messages: List[ChatMessage]
    total_messages: int
    entropy_status: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class SystemStatusResponse(BaseModel):
    """System status and health information"""
    status: str
    uptime: str
    rag_engine_status: str
    vector_store_status: str
    total_documents: int
    entropy_metrics: Dict[str, float]
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


# Knowledge Management Models

class KnowledgeDocument(BaseModel):
    """Model for knowledge documents"""
    content: str = Field(..., min_length=10, max_length=50000)
    source: str = Field(..., min_length=1, max_length=500)
    title: Optional[str] = None
    author: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "content": "Machine learning is a method of data analysis...",
                "source": "ML_Handbook_2024.pdf",
                "title": "Introduction to Machine Learning",
                "author": "Dr. Jane Smith",
                "tags": ["machine-learning", "ai", "data-science"],
                "metadata": {"page": 1, "chapter": "Introduction"}
            }
        }


class KnowledgeUploadRequest(BaseModel):
    """Request to upload knowledge to the system"""
    documents: List[KnowledgeDocument]
    overwrite_existing: bool = Field(False, description="Whether to overwrite existing documents")
    
    class Config:
        schema_extra = {
            "example": {
                "documents": [
                    {
                        "content": "Sample knowledge content...",
                        "source": "sample.txt",
                        "tags": ["sample"]
                    }
                ],
                "overwrite_existing": False
            }
        }


class KnowledgeUploadResponse(BaseModel):
    """Response for knowledge upload"""
    uploaded_count: int
    skipped_count: int
    failed_count: int
    total_documents: int
    entropy_status: str
    upload_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class KnowledgeSearchRequest(BaseModel):
    """Request to search knowledge base"""
    query: str = Field(..., min_length=1, max_length=1000)
    limit: int = Field(5, ge=1, le=20)
    filter_metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "query": "machine learning algorithms",
                "limit": 5,
                "filter_metadata": {"tags": "machine-learning"}
            }
        }


class KnowledgeSearchResponse(BaseModel):
    """Response for knowledge search"""
    results: List[Dict[str, Any]]
    total_results: int
    query_entropy: float
    search_quality: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


# Error Models

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    error_code: str
    details: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
        
        schema_extra = {
            "example": {
                "error": "Invalid request format",
                "error_code": "VALIDATION_ERROR",
                "details": "Message field is required",
                "timestamp": "2024-01-01T12:00:00"
            }
        }


# Validation Models

class ValidationResult(BaseModel):
    """Validation result for requests"""
    is_valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    
    def add_error(self, error: str):
        """Add validation error"""
        self.is_valid = False
        self.errors.append(error)
        
    def add_warning(self, warning: str):
        """Add validation warning"""
        self.warnings.append(warning)


# Analytics Models

class ConversationAnalytics(BaseModel):
    """Analytics for conversation quality"""
    conversation_id: str
    message_count: int
    average_response_time: float
    entropy_trend: List[float]
    quality_score: float
    knowledge_utilization: float
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class SystemAnalytics(BaseModel):
    """System-wide analytics"""
    total_conversations: int
    total_messages: int
    average_entropy: float
    knowledge_base_size: int
    system_efficiency: float
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

