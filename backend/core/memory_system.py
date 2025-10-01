"""
Memory System - Zero Entropy Memory Management

Implements:
1. Session-based short-term memory
2. Persistent long-term memory via RAG
3. Entropy-minimized context management
4. Memory consolidation and compression
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger
from collections import deque


class MemorySystem:
    """
    Zero Entropy Memory System
    
    Maintains minimal-entropy memory states with:
    - Deterministic context retrieval
    - Automatic memory consolidation
    - Hierarchical organization
    """
    
    def __init__(self, rag_engine):
        self.rag_engine = rag_engine
        self.sessions_db_path = os.getenv("SESSIONS_DB", "./data/sessions.json")
        self.max_context_messages = int(os.getenv("MAX_CONTEXT_MESSAGES", "10"))
        self.enable_long_term_memory = os.getenv("ENABLE_LONG_TERM_MEMORY", "true").lower() == "true"
        self.consolidation_threshold = int(os.getenv("MEMORY_CONSOLIDATION_THRESHOLD", "10"))
        
        # In-memory session storage
        self.sessions: Dict[str, Dict] = {}
        self._load_sessions()
    
    def _load_sessions(self):
        """Load sessions from persistent storage"""
        try:
            if os.path.exists(self.sessions_db_path):
                with open(self.sessions_db_path, 'r') as f:
                    self.sessions = json.load(f)
                logger.info(f"Loaded {len(self.sessions)} sessions from disk")
        except Exception as e:
            logger.warning(f"Could not load sessions: {e}")
            self.sessions = {}
    
    def _save_sessions(self):
        """Save sessions to persistent storage"""
        try:
            os.makedirs(os.path.dirname(self.sessions_db_path), exist_ok=True)
            with open(self.sessions_db_path, 'w') as f:
                json.dump(self.sessions, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save sessions: {e}")
    
    def create_session(self, session_id: str, metadata: Optional[Dict] = None) -> Dict:
        """Create a new chat session"""
        session = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "messages": [],
            "metadata": metadata or {},
            "summary": ""
        }
        
        self.sessions[session_id] = session
        self._save_sessions()
        
        logger.info(f"Created session: {session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def list_sessions(self) -> List[Dict]:
        """List all sessions"""
        return list(self.sessions.values())
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self._save_sessions()
            logger.info(f"Deleted session: {session_id}")
            return True
        return False
    
    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ):
        """
        Add message to session with Zero Entropy principles
        """
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        session = self.sessions[session_id]
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        session["messages"].append(message)
        session["updated_at"] = datetime.now().isoformat()
        
        # Store in long-term memory if enabled
        if self.enable_long_term_memory and role == "user":
            self._store_in_long_term_memory(session_id, message)
        
        # Check if consolidation needed
        if len(session["messages"]) >= self.consolidation_threshold:
            self._consolidate_memory(session_id)
        
        self._save_sessions()
    
    def get_context(
        self,
        session_id: str,
        include_rag: bool = True,
        query: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Get conversation context with Zero Entropy retrieval
        
        Returns:
            List of messages for LLM context
        """
        context_messages = []
        
        # 1. Get recent conversation history (short-term memory)
        if session_id in self.sessions:
            session = self.sessions[session_id]
            recent_messages = session["messages"][-self.max_context_messages:]
            
            # Add session summary if exists (consolidated memory)
            if session.get("summary"):
                context_messages.append({
                    "role": "system",
                    "content": f"Previous conversation summary: {session['summary']}"
                })
            
            # Add recent messages
            for msg in recent_messages:
                context_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # 2. Retrieve relevant long-term memories via RAG
        if include_rag and query and self.enable_long_term_memory:
            relevant_memories = self._retrieve_relevant_memories(
                session_id,
                query
            )
            
            if relevant_memories:
                # Insert relevant memories before recent context
                memory_context = self._format_memories_for_context(relevant_memories)
                context_messages.insert(0, {
                    "role": "system",
                    "content": memory_context
                })
        
        return context_messages
    
    def _store_in_long_term_memory(self, session_id: str, message: Dict):
        """Store message in RAG-based long-term memory"""
        try:
            metadata = {
                "session_id": session_id,
                "role": message["role"],
                "timestamp": message["timestamp"],
                "type": "conversation_memory"
            }
            
            self.rag_engine.add_document(
                text=message["content"],
                metadata=metadata
            )
            
            logger.debug(f"Stored message in long-term memory: {session_id}")
            
        except Exception as e:
            logger.error(f"Error storing in long-term memory: {e}")
    
    def _retrieve_relevant_memories(
        self,
        session_id: str,
        query: str,
        n_results: int = 3
    ) -> List[Dict]:
        """Retrieve relevant memories from long-term storage"""
        try:
            # Search with session filter
            results = self.rag_engine.retrieve(
                query=query,
                n_results=n_results,
                filter_metadata={"session_id": session_id}
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving memories: {e}")
            return []
    
    def _format_memories_for_context(self, memories: List[Dict]) -> str:
        """Format retrieved memories for LLM context"""
        if not memories:
            return ""
        
        formatted = "Relevant context from earlier in the conversation:\n\n"
        
        for i, memory in enumerate(memories, 1):
            content = memory["content"]
            timestamp = memory["metadata"].get("timestamp", "")
            formatted += f"{i}. [{timestamp}] {content}\n"
        
        return formatted
    
    def _consolidate_memory(self, session_id: str):
        """
        Consolidate session memory to reduce entropy
        
        Zero Entropy Principle: Compress redundant information
        while preserving essential context
        """
        if session_id not in self.sessions:
            return
        
        session = self.sessions[session_id]
        messages = session["messages"]
        
        if len(messages) < self.consolidation_threshold:
            return
        
        try:
            # Simple consolidation: Keep only key information
            # In production, use LLM to generate intelligent summary
            
            # Keep last N messages, summarize older ones
            recent_messages = messages[-self.max_context_messages:]
            older_messages = messages[:-self.max_context_messages]
            
            if older_messages:
                # Create simple summary
                summary_parts = []
                for msg in older_messages:
                    if msg["role"] == "user":
                        summary_parts.append(f"User asked: {msg['content'][:100]}")
                
                session["summary"] = " | ".join(summary_parts[-5:])  # Keep last 5
                session["messages"] = recent_messages
                
                logger.info(f"Consolidated memory for session {session_id}")
                self._save_sessions()
                
        except Exception as e:
            logger.error(f"Error consolidating memory: {e}")
    
    def add_knowledge(
        self,
        content: str,
        metadata: Optional[Dict] = None,
        category: str = "general"
    ) -> str:
        """
        Add external knowledge to long-term memory
        
        Use this to inject domain-specific knowledge, facts, or context
        """
        try:
            doc_metadata = metadata or {}
            doc_metadata["type"] = "knowledge"
            doc_metadata["category"] = category
            doc_metadata["added_at"] = datetime.now().isoformat()
            
            doc_id = self.rag_engine.add_document(
                text=content,
                metadata=doc_metadata
            )
            
            logger.info(f"Added knowledge to memory: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error adding knowledge: {e}")
            raise
    
    def search_memory(
        self,
        query: str,
        n_results: int = 5,
        filter_by: Optional[Dict] = None
    ) -> List[Dict]:
        """Search across all memories"""
        try:
            results = self.rag_engine.retrieve(
                query=query,
                n_results=n_results,
                filter_metadata=filter_by
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching memory: {e}")
            return []
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        rag_stats = self.rag_engine.get_stats()
        
        return {
            "active_sessions": len(self.sessions),
            "long_term_memories": rag_stats.get("total_documents", 0),
            "max_context_messages": self.max_context_messages,
            "consolidation_threshold": self.consolidation_threshold,
            "long_term_memory_enabled": self.enable_long_term_memory
        }
    
    def clear_all_memory(self):
        """Clear all memory (sessions and RAG)"""
        self.sessions = {}
        self._save_sessions()
        self.rag_engine.clear_collection()
        logger.warning("All memory cleared")
