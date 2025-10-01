"""
Zero Entropy RAG Engine

Core principles implemented:
1. Minimal Uncertainty: High-precision retrieval with confidence scoring
2. Ordered Information Flow: Structured context injection
3. Deterministic Generation: Consistent response patterns
4. Knowledge Coherence: Maintaining information consistency

Philosophy: Zero entropy = maximum order = minimal uncertainty in AI responses
"""

import asyncio
from typing import List, Dict, Optional, Tuple
import numpy as np
from dataclasses import dataclass
from datetime import datetime
import json
import hashlib

from ..models.chat_models import ChatMessage, RAGContext, ChatResponse
from .vector_store import VectorStore
from .llm_integration import LLMIntegration
from ..utils.entropy_calculator import EntropyCalculator


@dataclass
class RetrievalResult:
    """Structured retrieval result with entropy metrics"""
    content: str
    relevance_score: float
    entropy_score: float  # Lower = more ordered/certain
    source: str
    timestamp: datetime
    confidence: float


class ZeroEntropyRAG:
    """
    Zero Entropy Enhanced RAG System
    
    Implements methodologies to minimize entropy (uncertainty) in:
    - Information retrieval
    - Context selection  
    - Response generation
    """
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.llm_integration = None
        self.entropy_calculator = EntropyCalculator()
        
        # Zero Entropy Configuration
        self.entropy_threshold = 0.3  # Maximum allowed entropy
        self.confidence_threshold = 0.7  # Minimum confidence for retrieval
        self.max_context_chunks = 5  # Limit context to prevent noise
        
        # Conversation memory for coherence
        self.conversation_memory: Dict[str, List[ChatMessage]] = {}
        self.context_cache: Dict[str, RAGContext] = {}
        
    async def initialize(self):
        """Initialize RAG engine with Zero Entropy optimization"""
        print("🧠 Initializing Zero Entropy RAG Engine...")
        
        # Initialize LLM integration
        self.llm_integration = LLMIntegration()
        await self.llm_integration.initialize()
        
        # Pre-warm systems for deterministic behavior
        await self._warm_up_systems()
        
        print("✅ Zero Entropy RAG Engine ready")
        
    async def _warm_up_systems(self):
        """Pre-warm systems to ensure consistent performance"""
        # Test retrieval system
        test_query = "system initialization test"
        await self.vector_store.similarity_search(test_query, k=1)
        
        # Test LLM integration
        await self.llm_integration.test_connection()
        
    async def generate_response(
        self, 
        message: str, 
        conversation_id: str,
        user_context: Optional[Dict] = None
    ) -> ChatResponse:
        """
        Generate response with Zero Entropy enhancement
        
        Process:
        1. Retrieve relevant knowledge with entropy filtering
        2. Select optimal context with minimal uncertainty
        3. Generate response with coherence checking
        4. Validate entropy levels in output
        """
        
        # Step 1: Retrieve and filter knowledge by entropy
        retrieval_results = await self._retrieve_with_entropy_filter(
            query=message,
            conversation_id=conversation_id
        )
        
        # Step 2: Build optimal context
        rag_context = await self._build_optimal_context(
            retrieval_results=retrieval_results,
            conversation_history=self._get_conversation_history(conversation_id),
            user_context=user_context
        )
        
        # Step 3: Generate response with LLM
        raw_response = await self.llm_integration.generate_response(
            message=message,
            context=rag_context
        )
        
        # Step 4: Post-process and validate entropy
        processed_response = await self._post_process_response(
            response=raw_response,
            context=rag_context,
            original_query=message
        )
        
        # Step 5: Update conversation memory
        await self._update_conversation_memory(
            conversation_id=conversation_id,
            user_message=message,
            assistant_response=processed_response.content,
            context_used=rag_context
        )
        
        return processed_response
        
    async def _retrieve_with_entropy_filter(
        self, 
        query: str, 
        conversation_id: str,
        k: int = 10
    ) -> List[RetrievalResult]:
        """
        Retrieve knowledge with entropy-based filtering
        
        Zero Entropy Principle: Only include high-certainty information
        """
        
        # Get raw retrieval results
        raw_results = await self.vector_store.similarity_search(
            query=query, 
            k=k
        )
        
        retrieval_results = []
        
        for result in raw_results:
            # Calculate entropy score for this piece of knowledge
            entropy_score = await self.entropy_calculator.calculate_text_entropy(
                result.content
            )
            
            # Calculate confidence based on similarity and entropy
            confidence = self._calculate_confidence(
                similarity_score=result.relevance_score,
                entropy_score=entropy_score
            )
            
            # Apply Zero Entropy filtering
            if (entropy_score <= self.entropy_threshold and 
                confidence >= self.confidence_threshold):
                
                retrieval_results.append(RetrievalResult(
                    content=result.content,
                    relevance_score=result.relevance_score,
                    entropy_score=entropy_score,
                    source=result.source,
                    timestamp=datetime.now(),
                    confidence=confidence
                ))
        
        # Sort by confidence (higher = better)
        retrieval_results.sort(key=lambda x: x.confidence, reverse=True)
        
        return retrieval_results[:self.max_context_chunks]
        
    async def _build_optimal_context(
        self,
        retrieval_results: List[RetrievalResult],
        conversation_history: List[ChatMessage],
        user_context: Optional[Dict] = None
    ) -> RAGContext:
        """
        Build optimal context with minimal entropy
        
        Zero Entropy Principle: Ordered, non-redundant information
        """
        
        # Deduplicate and order information by certainty
        ordered_knowledge = await self._order_knowledge_by_certainty(
            retrieval_results
        )
        
        # Build context with entropy optimization
        context = RAGContext(
            retrieved_knowledge=ordered_knowledge,
            conversation_history=conversation_history[-5:],  # Recent context only
            metadata={
                "total_entropy": sum(r.entropy_score for r in retrieval_results),
                "average_confidence": np.mean([r.confidence for r in retrieval_results]),
                "knowledge_sources": len(set(r.source for r in retrieval_results)),
                "timestamp": datetime.now().isoformat()
            }
        )
        
        return context
        
    async def _order_knowledge_by_certainty(
        self, 
        results: List[RetrievalResult]
    ) -> List[str]:
        """Order knowledge pieces by certainty (inverse of entropy)"""
        
        # Remove duplicate information to minimize entropy
        seen_hashes = set()
        unique_results = []
        
        for result in results:
            content_hash = hashlib.md5(result.content.encode()).hexdigest()
            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                unique_results.append(result)
        
        # Sort by certainty score (confidence / entropy)
        certainty_sorted = sorted(
            unique_results,
            key=lambda x: x.confidence / max(x.entropy_score, 0.01),
            reverse=True
        )
        
        return [result.content for result in certainty_sorted]
        
    def _calculate_confidence(
        self, 
        similarity_score: float, 
        entropy_score: float
    ) -> float:
        """
        Calculate confidence score based on similarity and entropy
        
        Zero Entropy Formula: High similarity + Low entropy = High confidence
        """
        
        # Normalize entropy (lower entropy = higher certainty)
        certainty = 1.0 - min(entropy_score, 1.0)
        
        # Combine similarity and certainty
        confidence = (similarity_score * 0.6) + (certainty * 0.4)
        
        return min(confidence, 1.0)
        
    async def _post_process_response(
        self,
        response: str,
        context: RAGContext,
        original_query: str
    ) -> ChatResponse:
        """Post-process response to ensure Zero Entropy principles"""
        
        # Calculate response entropy
        response_entropy = await self.entropy_calculator.calculate_text_entropy(
            response
        )
        
        # Validate response coherence
        coherence_score = await self._calculate_coherence(response, context)
        
        return ChatResponse(
            content=response,
            context_used=context,
            metadata={
                "response_entropy": response_entropy,
                "coherence_score": coherence_score,
                "generation_timestamp": datetime.now().isoformat(),
                "entropy_status": "optimal" if response_entropy < 0.5 else "elevated"
            }
        )
        
    async def _calculate_coherence(
        self, 
        response: str, 
        context: RAGContext
    ) -> float:
        """Calculate response coherence with context"""
        
        # Simplified coherence calculation
        # In production, this could use more sophisticated NLP techniques
        
        context_text = " ".join(context.retrieved_knowledge)
        
        # Basic keyword overlap
        response_words = set(response.lower().split())
        context_words = set(context_text.lower().split())
        
        if len(response_words) == 0:
            return 0.0
            
        overlap = len(response_words.intersection(context_words))
        coherence = overlap / len(response_words)
        
        return min(coherence, 1.0)
        
    def _get_conversation_history(self, conversation_id: str) -> List[ChatMessage]:
        """Get conversation history for context"""
        return self.conversation_memory.get(conversation_id, [])
        
    async def _update_conversation_memory(
        self,
        conversation_id: str,
        user_message: str,
        assistant_response: str,
        context_used: RAGContext
    ):
        """Update conversation memory with Zero Entropy principles"""
        
        if conversation_id not in self.conversation_memory:
            self.conversation_memory[conversation_id] = []
            
        # Add messages to memory
        self.conversation_memory[conversation_id].extend([
            ChatMessage(
                role="user",
                content=user_message,
                timestamp=datetime.now()
            ),
            ChatMessage(
                role="assistant", 
                content=assistant_response,
                timestamp=datetime.now()
            )
        ])
        
        # Limit memory size to prevent entropy buildup
        max_memory = 20  # 10 exchanges
        if len(self.conversation_memory[conversation_id]) > max_memory:
            self.conversation_memory[conversation_id] = \
                self.conversation_memory[conversation_id][-max_memory:]
                
    async def add_knowledge(self, content: str, source: str) -> bool:
        """Add knowledge to the system with entropy validation"""
        
        # Calculate entropy of new knowledge
        entropy_score = await self.entropy_calculator.calculate_text_entropy(content)
        
        # Only add low-entropy (high-certainty) knowledge
        if entropy_score <= self.entropy_threshold:
            await self.vector_store.add_document(content, source)
            return True
            
        return False
        
    async def get_system_entropy_status(self) -> Dict:
        """Get current system entropy status"""
        
        total_docs = await self.vector_store.get_document_count()
        
        return {
            "total_documents": total_docs,
            "entropy_threshold": self.entropy_threshold,
            "confidence_threshold": self.confidence_threshold,
            "system_status": "optimal",
            "last_updated": datetime.now().isoformat()
        }
        
    async def shutdown(self):
        """Shutdown RAG engine"""
        if self.llm_integration:
            await self.llm_integration.shutdown()

