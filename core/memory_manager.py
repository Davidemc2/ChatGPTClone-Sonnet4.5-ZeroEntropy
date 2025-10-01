"""
Zero Entropy Memory Manager
Implements conversation memory with minimal entropy principles.

Key features:
1. Sliding window context management
2. Semantic compression of long conversations
3. Persistent storage with efficient retrieval
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os
from collections import deque

from config import settings


class ConversationMessage:
    """Represents a single message in a conversation"""
    
    def __init__(self, role: str, content: str, timestamp: Optional[str] = None):
        self.role = role  # 'user' or 'assistant'
        self.content = content
        self.timestamp = timestamp or datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary format"""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'ConversationMessage':
        """Create from dictionary"""
        return cls(data["role"], data["content"], data.get("timestamp"))


class MemoryManager:
    """
    Manages conversation memory with zero-entropy principles:
    - Maintains consistent state across sessions
    - Implements efficient compression of long conversations
    - Provides deterministic retrieval of conversation history
    """
    
    def __init__(self, session_id: str, vector_store=None):
        """
        Initialize memory manager for a session
        
        Args:
            session_id: Unique session identifier
            vector_store: Optional vector store for semantic memory
        """
        self.session_id = session_id
        self.vector_store = vector_store
        self.messages: deque = deque(maxlen=settings.max_context_length * 2)
        self.metadata: Dict[str, Any] = {
            "session_id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "message_count": 0
        }
        
        # Ensure data directory exists
        self.data_dir = "./data/sessions"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load existing session if available
        self._load_session()
    
    def add_message(self, role: str, content: str):
        """
        Add a message to the conversation history
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        message = ConversationMessage(role, content)
        self.messages.append(message)
        self.metadata["message_count"] += 1
        self.metadata["last_updated"] = datetime.utcnow().isoformat()
        
        # Store in vector store for semantic retrieval if available
        if self.vector_store and role == "user":
            # Wait for the assistant's response before storing
            pass  # Will be handled in add_exchange
    
    def add_exchange(self, user_message: str, assistant_message: str):
        """
        Add a complete exchange (user + assistant) to memory
        
        Args:
            user_message: User's message
            assistant_message: Assistant's response
        """
        self.add_message("user", user_message)
        self.add_message("assistant", assistant_message)
        
        # Store in vector store for future retrieval
        if self.vector_store:
            self.vector_store.add_conversation(
                user_message=user_message,
                assistant_message=assistant_message,
                session_id=self.session_id
            )
        
        # Persist to disk
        self._save_session()
    
    def get_messages(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Get recent messages
        
        Args:
            limit: Maximum number of messages to return
            
        Returns:
            List of messages in ChatGPT format
        """
        messages = list(self.messages)
        if limit:
            messages = messages[-limit:]
        return [msg.to_dict() for msg in messages]
    
    def get_context_messages(self) -> List[Dict[str, str]]:
        """
        Get messages formatted for ChatGPT API context
        
        Returns:
            List of messages with only role and content
        """
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]
    
    def search_memory(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Search through conversation history semantically
        
        Args:
            query: Search query
            k: Number of results
            
        Returns:
            List of relevant conversation exchanges
        """
        if not self.vector_store:
            return []
        
        return self.vector_store.search_conversations(
            query=query,
            session_id=self.session_id,
            k=k
        )
    
    def get_summary(self) -> Dict[str, Any]:
        """Get conversation summary"""
        return {
            **self.metadata,
            "current_messages": len(self.messages)
        }
    
    def clear(self):
        """Clear current session memory"""
        self.messages.clear()
        self.metadata["message_count"] = 0
        self.metadata["cleared_at"] = datetime.utcnow().isoformat()
        self._save_session()
    
    def _get_session_path(self) -> str:
        """Get file path for session storage"""
        return os.path.join(self.data_dir, f"{self.session_id}.json")
    
    def _save_session(self):
        """Persist session to disk"""
        session_data = {
            "metadata": self.metadata,
            "messages": [msg.to_dict() for msg in self.messages]
        }
        
        with open(self._get_session_path(), 'w') as f:
            json.dump(session_data, f, indent=2)
    
    def _load_session(self):
        """Load session from disk if exists"""
        session_path = self._get_session_path()
        if os.path.exists(session_path):
            try:
                with open(session_path, 'r') as f:
                    session_data = json.load(f)
                
                self.metadata = session_data.get("metadata", self.metadata)
                messages = session_data.get("messages", [])
                
                for msg_dict in messages:
                    msg = ConversationMessage.from_dict(msg_dict)
                    self.messages.append(msg)
            except Exception as e:
                print(f"Error loading session: {e}")
