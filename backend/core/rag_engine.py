"""
RAG Engine - Zero Entropy Methodology Implementation

Key Principles:
1. Deterministic Retrieval: Consistent, reproducible results
2. Entropy Minimization: Reduce uncertainty in retrieved context
3. Ordered Knowledge States: Hierarchical organization of information
"""

import os
import hashlib
from typing import List, Dict, Any, Optional
import numpy as np
from loguru import logger
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings


class RAGEngine:
    """
    Advanced RAG engine implementing Zero Entropy principles
    """
    
    def __init__(self):
        self.embedding_model_name = os.getenv(
            "EMBEDDING_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store_path = os.getenv("VECTOR_STORE_PATH", "./data/chroma")
        self.max_results = int(os.getenv("MAX_RETRIEVAL_RESULTS", "5"))
        self.similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
        
        self.embedding_model = None
        self.chroma_client = None
        self.collection = None
        
    async def initialize(self):
        """Initialize the RAG engine components"""
        try:
            # Load embedding model
            logger.info(f"Loading embedding model: {self.embedding_model_name}")
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            
            # Initialize ChromaDB
            logger.info("Initializing ChromaDB...")
            os.makedirs(self.vector_store_path, exist_ok=True)
            
            self.chroma_client = chromadb.PersistentClient(
                path=self.vector_store_path,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self.collection = self.chroma_client.get_or_create_collection(
                name="zero_entropy_memory",
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"✅ RAG Engine initialized with {self.collection.count()} documents")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG engine: {e}")
            raise
    
    def generate_deterministic_id(self, text: str, metadata: Dict = None) -> str:
        """
        Generate deterministic ID for documents
        Zero Entropy Principle: Consistent identification
        """
        content = text
        if metadata:
            # Include relevant metadata for uniqueness
            content += str(sorted(metadata.items()))
        
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for text"""
        embedding = self.embedding_model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def add_document(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        doc_id: Optional[str] = None
    ) -> str:
        """
        Add document to vector store with Zero Entropy organization
        
        Args:
            text: Document text
            metadata: Document metadata
            doc_id: Optional custom ID (will generate deterministic ID if not provided)
            
        Returns:
            Document ID
        """
        try:
            if not doc_id:
                doc_id = self.generate_deterministic_id(text, metadata)
            
            # Create embedding
            embedding = self.create_embedding(text)
            
            # Prepare metadata
            doc_metadata = metadata or {}
            doc_metadata["text_length"] = len(text)
            doc_metadata["entropy_score"] = self._calculate_entropy_score(text)
            
            # Add to collection
            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[doc_metadata]
            )
            
            logger.debug(f"Added document {doc_id} to vector store")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            raise
    
    def add_documents_batch(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        doc_ids: Optional[List[str]] = None
    ) -> List[str]:
        """Add multiple documents in batch"""
        try:
            if not doc_ids:
                doc_ids = [
                    self.generate_deterministic_id(
                        text,
                        metadatas[i] if metadatas else None
                    )
                    for i, text in enumerate(texts)
                ]
            
            # Create embeddings
            embeddings = [self.create_embedding(text) for text in texts]
            
            # Prepare metadata
            if not metadatas:
                metadatas = [{} for _ in texts]
            
            for i, (text, metadata) in enumerate(zip(texts, metadatas)):
                metadata["text_length"] = len(text)
                metadata["entropy_score"] = self._calculate_entropy_score(text)
            
            # Add to collection
            self.collection.add(
                ids=doc_ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
            
            logger.info(f"Added {len(doc_ids)} documents to vector store")
            return doc_ids
            
        except Exception as e:
            logger.error(f"Error adding documents batch: {e}")
            raise
    
    def retrieve(
        self,
        query: str,
        n_results: Optional[int] = None,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents using Zero Entropy retrieval
        
        Zero Entropy Principles:
        1. Deterministic ranking
        2. Entropy-weighted scoring
        3. Redundancy elimination
        """
        try:
            n_results = n_results or self.max_results
            
            # Create query embedding
            query_embedding = self.create_embedding(query)
            
            # Query vector store
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results * 2,  # Get more for post-processing
                where=filter_metadata,
                include=["documents", "metadatas", "distances"]
            )
            
            if not results["documents"][0]:
                return []
            
            # Process and rank results with Zero Entropy methodology
            processed_results = self._process_retrieval_results(
                query,
                results,
                n_results
            )
            
            return processed_results
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    def _process_retrieval_results(
        self,
        query: str,
        results: Dict,
        n_results: int
    ) -> List[Dict[str, Any]]:
        """
        Process and rank retrieval results with Zero Entropy methodology
        
        Implements:
        1. Similarity thresholding
        2. Redundancy elimination (entropy-based)
        3. Deterministic ranking
        """
        processed = []
        seen_content = set()
        
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        
        for doc, metadata, distance in zip(documents, metadatas, distances):
            # Convert distance to similarity (cosine distance)
            similarity = 1 - distance
            
            # Apply similarity threshold
            if similarity < self.similarity_threshold:
                continue
            
            # Zero Entropy: Eliminate redundancy
            doc_fingerprint = self._generate_content_fingerprint(doc)
            if doc_fingerprint in seen_content:
                continue
            
            seen_content.add(doc_fingerprint)
            
            # Calculate final score with entropy weighting
            entropy_score = metadata.get("entropy_score", 0.5)
            final_score = similarity * (1 + entropy_score) / 2
            
            processed.append({
                "content": doc,
                "metadata": metadata,
                "similarity": similarity,
                "entropy_score": entropy_score,
                "final_score": final_score
            })
            
            if len(processed) >= n_results:
                break
        
        # Sort by final score (deterministic)
        processed.sort(key=lambda x: x["final_score"], reverse=True)
        
        return processed
    
    def _calculate_entropy_score(self, text: str) -> float:
        """
        Calculate information entropy score for text
        Higher score = more information density
        
        Zero Entropy Principle: Quantify information content
        """
        if not text:
            return 0.0
        
        # Simple entropy calculation based on character distribution
        from collections import Counter
        import math
        
        # Normalize text
        text = text.lower()
        char_counts = Counter(text)
        text_length = len(text)
        
        # Calculate Shannon entropy
        entropy = 0.0
        for count in char_counts.values():
            probability = count / text_length
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        # Normalize to 0-1 range (max entropy for ASCII is ~6.6 bits)
        normalized_entropy = min(entropy / 6.6, 1.0)
        
        return normalized_entropy
    
    def _generate_content_fingerprint(self, text: str) -> str:
        """Generate fingerprint for redundancy detection"""
        # Use first and last parts + length for quick comparison
        text_normalized = text.strip().lower()
        fingerprint = f"{text_normalized[:50]}_{text_normalized[-50:]}_{len(text)}"
        return hashlib.md5(fingerprint.encode()).hexdigest()[:8]
    
    def search_hybrid(
        self,
        query: str,
        keyword_boost: float = 0.3,
        n_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Hybrid search combining semantic and keyword matching
        """
        # Semantic search
        semantic_results = self.retrieve(query, n_results)
        
        # Simple keyword boosting
        query_keywords = set(query.lower().split())
        
        for result in semantic_results:
            content_keywords = set(result["content"].lower().split())
            keyword_overlap = len(query_keywords & content_keywords) / len(query_keywords)
            
            # Boost score based on keyword overlap
            result["final_score"] = (
                result["final_score"] * (1 - keyword_boost) +
                keyword_overlap * keyword_boost
            )
        
        # Re-sort
        semantic_results.sort(key=lambda x: x["final_score"], reverse=True)
        
        return semantic_results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get RAG engine statistics"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "embedding_model": self.embedding_model_name,
                "similarity_threshold": self.similarity_threshold,
                "max_results": self.max_results
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}
    
    def clear_collection(self):
        """Clear all documents from collection"""
        try:
            # Delete and recreate collection
            self.chroma_client.delete_collection(name="zero_entropy_memory")
            self.collection = self.chroma_client.create_collection(
                name="zero_entropy_memory",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Collection cleared")
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")
            raise
    
    async def close(self):
        """Cleanup resources"""
        logger.info("Closing RAG engine...")
