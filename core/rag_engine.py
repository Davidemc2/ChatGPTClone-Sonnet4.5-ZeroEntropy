"""
Zero Entropy RAG Engine
Retrieval-Augmented Generation with minimal entropy approach.

Philosophy:
1. First principles: Break down query into fundamental components
2. Deterministic retrieval: Consistent results for similar queries
3. Context optimization: Maximum signal, minimum noise
"""
from typing import List, Dict, Any, Optional, AsyncIterator
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import asyncio

from config import settings
from .vector_store import ZeroEntropyVectorStore
from .memory_manager import MemoryManager


class RAGEngine:
    """
    RAG Engine implementing Zero Entropy principles:
    - Retrieve only the most relevant information
    - Generate responses with minimal hallucination
    - Maintain consistent reasoning across interactions
    """
    
    def __init__(self, vector_store: ZeroEntropyVectorStore):
        """
        Initialize RAG engine
        
        Args:
            vector_store: Vector store for document retrieval
        """
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            model=settings.default_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            openai_api_key=settings.openai_api_key,
            streaming=True
        )
        
        # System prompt implementing Zero Entropy principles
        self.system_prompt = """You are an advanced AI assistant enhanced with a Zero Entropy RAG (Retrieval-Augmented Generation) system.

Zero Entropy Principles:
1. **Minimal Information Loss**: Provide accurate, precise information without degradation
2. **Deterministic Reasoning**: Apply consistent logic and first principles thinking
3. **Optimal State**: Maintain perfect coherence between context and response
4. **Efficient Retrieval**: Use only the most relevant information

Your approach:
- Break down complex problems into fundamental truths (first principles thinking)
- Provide clear, actionable responses
- Reference retrieved knowledge when relevant
- Acknowledge uncertainty rather than hallucinate
- Maintain conversation context efficiently

When provided with retrieved context, integrate it naturally into your responses. If context is provided, use it to enhance accuracy. If no relevant context exists, rely on your training."""
    
    def _format_context(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        Format retrieved documents into context string
        
        Args:
            retrieved_docs: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        if not retrieved_docs:
            return ""
        
        context_parts = ["Retrieved Context:"]
        for i, doc in enumerate(retrieved_docs, 1):
            content = doc["content"]
            score = doc.get("relevance_score", 0)
            context_parts.append(f"\n[Source {i}] (Relevance: {score:.3f})\n{content}")
        
        return "\n".join(context_parts)
    
    def _build_messages(
        self, 
        user_message: str, 
        memory: Optional[MemoryManager] = None,
        retrieved_context: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Build message list for the LLM
        
        Args:
            user_message: Current user message
            memory: Memory manager with conversation history
            retrieved_context: Retrieved context from vector store
            
        Returns:
            List of messages for the LLM
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history from memory
        if memory:
            history_messages = memory.get_context_messages()
            # Limit history to avoid context overflow
            recent_history = history_messages[-(settings.max_context_length * 2):]
            messages.extend(recent_history)
        
        # Add retrieved context if available
        if retrieved_context:
            context_message = f"{retrieved_context}\n\n---\n\nUser Query: {user_message}"
            messages.append({"role": "user", "content": context_message})
        else:
            messages.append({"role": "user", "content": user_message})
        
        return messages
    
    async def generate_response(
        self,
        user_message: str,
        memory: Optional[MemoryManager] = None,
        use_rag: bool = True,
        stream: bool = True
    ) -> AsyncIterator[str]:
        """
        Generate response with RAG enhancement
        
        Args:
            user_message: User's message
            memory: Memory manager for conversation context
            use_rag: Whether to use RAG retrieval
            stream: Whether to stream the response
            
        Yields:
            Response chunks if streaming
        """
        # Retrieve relevant context if RAG is enabled
        retrieved_context = None
        if use_rag:
            retrieved_docs = self.vector_store.similarity_search(
                query=user_message,
                k=settings.top_k_results
            )
            if retrieved_docs:
                retrieved_context = self._format_context(retrieved_docs)
        
        # Build message list
        messages = self._build_messages(user_message, memory, retrieved_context)
        
        # Generate response
        if stream:
            async for chunk in self.llm.astream(messages):
                if hasattr(chunk, 'content'):
                    yield chunk.content
        else:
            response = await self.llm.ainvoke(messages)
            yield response.content
    
    async def generate_response_sync(
        self,
        user_message: str,
        memory: Optional[MemoryManager] = None,
        use_rag: bool = True
    ) -> str:
        """
        Generate complete response (non-streaming)
        
        Args:
            user_message: User's message
            memory: Memory manager for conversation context
            use_rag: Whether to use RAG retrieval
            
        Returns:
            Complete response
        """
        chunks = []
        async for chunk in self.generate_response(user_message, memory, use_rag, stream=False):
            chunks.append(chunk)
        return "".join(chunks)
    
    def add_knowledge(
        self, 
        documents: List[str], 
        metadata: Optional[List[Dict[str, Any]]] = None
    ) -> List[str]:
        """
        Add documents to the knowledge base
        
        Args:
            documents: List of documents to add
            metadata: Optional metadata for each document
            
        Returns:
            List of document IDs
        """
        return self.vector_store.add_documents(documents, metadata)
    
    def search_knowledge(
        self, 
        query: str, 
        k: int = None
    ) -> List[Dict[str, Any]]:
        """
        Search the knowledge base
        
        Args:
            query: Search query
            k: Number of results
            
        Returns:
            List of relevant documents
        """
        return self.vector_store.similarity_search(query, k)
