"""
Vector Store Implementation for Zero Entropy RAG System

Handles:
- Efficient vector storage and retrieval
- Semantic similarity search
- Knowledge organization with entropy principles
- Document management and deduplication

Zero Entropy Principles:
- Organized knowledge structure
- Efficient retrieval with minimal noise
- Deduplication to prevent information redundancy
"""

import asyncio
import os
from typing import List, Dict, Optional, Tuple
import numpy as np
from dataclasses import dataclass
from datetime import datetime
import hashlib
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import json


@dataclass
class DocumentResult:
    """Document retrieval result with metadata"""
    content: str
    relevance_score: float
    source: str
    document_id: str
    metadata: Dict


@dataclass 
class DocumentChunk:
    """Document chunk for processing"""
    content: str
    source: str
    chunk_id: str
    metadata: Dict


class VectorStore:
    """
    Vector Store with Zero Entropy optimization
    
    Features:
    - High-precision semantic search
    - Automatic deduplication
    - Organized knowledge structure
    - Efficient storage and retrieval
    """
    
    def __init__(self, persist_directory: str = "./data/vector_store"):
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self.embedding_model = None
        
        # Zero Entropy Configuration
        self.chunk_size = 512  # Optimal chunk size for coherence
        self.overlap_size = 50  # Minimal overlap to prevent information loss
        self.similarity_threshold = 0.7  # High threshold for precision
        
        # Document tracking for deduplication
        self.document_hashes: set = set()
        
    async def initialize(self):
        """Initialize vector store with Zero Entropy optimization"""
        print("🗃️ Initializing Vector Store...")
        
        # Create persistence directory
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection("zero_entropy_knowledge")
            print(f"📚 Loaded existing collection with {self.collection.count()} documents")
        except:
            self.collection = self.client.create_collection(
                name="zero_entropy_knowledge",
                metadata={"description": "Zero Entropy enhanced knowledge base"}
            )
            print("📚 Created new knowledge collection")
            
        # Initialize embedding model
        print("🤖 Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load existing document hashes for deduplication
        await self._load_document_hashes()
        
        print("✅ Vector Store initialized")
        
    async def _load_document_hashes(self):
        """Load existing document hashes for deduplication"""
        try:
            # Get all documents to build hash set
            results = self.collection.get(include=["metadatas"])
            
            for metadata in results.get("metadatas", []):
                if "content_hash" in metadata:
                    self.document_hashes.add(metadata["content_hash"])
                    
            print(f"📋 Loaded {len(self.document_hashes)} document hashes")
        except Exception as e:
            print(f"⚠️ Could not load document hashes: {e}")
            
    async def add_document(
        self, 
        content: str, 
        source: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Add document to vector store with Zero Entropy principles
        
        Features:
        - Automatic deduplication
        - Optimal chunking
        - Metadata enrichment
        """
        
        if not content.strip():
            return False
            
        # Calculate content hash for deduplication
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Check for duplicates (Zero Entropy: no redundant information)
        if content_hash in self.document_hashes:
            print(f"🔍 Document already exists (hash: {content_hash[:8]}...)")
            return False
            
        try:
            # Chunk document for optimal processing
            chunks = await self._chunk_document(content, source, metadata)
            
            # Process chunks
            ids = []
            documents = []
            embeddings = []
            metadatas = []
            
            for chunk in chunks:
                # Generate embedding
                embedding = self.embedding_model.encode(chunk.content).tolist()
                
                # Prepare data
                ids.append(chunk.chunk_id)
                documents.append(chunk.content)
                embeddings.append(embedding)
                metadatas.append({
                    **chunk.metadata,
                    "content_hash": content_hash,
                    "added_timestamp": datetime.now().isoformat(),
                    "chunk_length": len(chunk.content),
                    "source": source
                })
                
            # Add to collection
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
            
            # Update hash tracking
            self.document_hashes.add(content_hash)
            
            print(f"✅ Added document: {len(chunks)} chunks from {source}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding document: {e}")
            return False
            
    async def _chunk_document(
        self, 
        content: str, 
        source: str, 
        metadata: Optional[Dict] = None
    ) -> List[DocumentChunk]:
        """
        Chunk document with Zero Entropy optimization
        
        Principles:
        - Optimal chunk size for coherence
        - Minimal overlap to preserve context
        - Logical boundaries when possible
        """
        
        chunks = []
        base_metadata = metadata or {}
        
        # Simple chunking strategy (can be enhanced with more sophisticated methods)
        words = content.split()
        
        for i in range(0, len(words), self.chunk_size - self.overlap_size):
            chunk_words = words[i:i + self.chunk_size]
            chunk_content = " ".join(chunk_words)
            
            if len(chunk_content.strip()) < 50:  # Skip very small chunks
                continue
                
            chunk_id = f"{source}_{i}_{hashlib.md5(chunk_content.encode()).hexdigest()[:8]}"
            
            chunk = DocumentChunk(
                content=chunk_content.strip(),
                source=source,
                chunk_id=chunk_id,
                metadata={
                    **base_metadata,
                    "chunk_index": len(chunks),
                    "chunk_start": i,
                    "chunk_end": min(i + self.chunk_size, len(words))
                }
            )
            
            chunks.append(chunk)
            
        return chunks
        
    async def similarity_search(
        self, 
        query: str, 
        k: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> List[DocumentResult]:
        """
        Perform similarity search with Zero Entropy filtering
        
        Features:
        - High-precision retrieval
        - Relevance scoring
        - Optional metadata filtering
        """
        
        if not query.strip():
            return []
            
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search with ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(k, 20),  # Get more results for filtering
                where=filter_metadata,
                include=["documents", "distances", "metadatas"]
            )
            
            # Process results
            document_results = []
            
            for i, (doc, distance, metadata) in enumerate(zip(
                results["documents"][0],
                results["distances"][0], 
                results["metadatas"][0]
            )):
                # Convert distance to similarity score (lower distance = higher similarity)
                relevance_score = max(0.0, 1.0 - distance)
                
                # Apply Zero Entropy threshold
                if relevance_score >= self.similarity_threshold:
                    result = DocumentResult(
                        content=doc,
                        relevance_score=relevance_score,
                        source=metadata.get("source", "unknown"),
                        document_id=results["ids"][0][i],
                        metadata=metadata
                    )
                    document_results.append(result)
                    
            # Sort by relevance (highest first)
            document_results.sort(key=lambda x: x.relevance_score, reverse=True)
            
            return document_results[:k]
            
        except Exception as e:
            print(f"❌ Error in similarity search: {e}")
            return []
            
    async def get_document_count(self) -> int:
        """Get total number of documents in the store"""
        try:
            return self.collection.count()
        except:
            return 0
            
    async def delete_document(self, document_id: str) -> bool:
        """Delete document by ID"""
        try:
            self.collection.delete(ids=[document_id])
            return True
        except Exception as e:
            print(f"❌ Error deleting document: {e}")
            return False
            
    async def update_document(
        self, 
        document_id: str, 
        content: str, 
        metadata: Optional[Dict] = None
    ) -> bool:
        """Update existing document"""
        try:
            # Generate new embedding
            embedding = self.embedding_model.encode(content).tolist()
            
            # Update document
            self.collection.update(
                ids=[document_id],
                documents=[content],
                embeddings=[embedding],
                metadatas=[metadata or {}]
            )
            return True
        except Exception as e:
            print(f"❌ Error updating document: {e}")
            return False
            
    async def search_by_metadata(
        self, 
        metadata_filter: Dict, 
        limit: int = 10
    ) -> List[DocumentResult]:
        """Search documents by metadata filters"""
        try:
            results = self.collection.get(
                where=metadata_filter,
                limit=limit,
                include=["documents", "metadatas"]
            )
            
            document_results = []
            
            for doc, metadata, doc_id in zip(
                results["documents"],
                results["metadatas"], 
                results["ids"]
            ):
                result = DocumentResult(
                    content=doc,
                    relevance_score=1.0,  # Exact match
                    source=metadata.get("source", "unknown"),
                    document_id=doc_id,
                    metadata=metadata
                )
                document_results.append(result)
                
            return document_results
            
        except Exception as e:
            print(f"❌ Error in metadata search: {e}")
            return []
            
    async def get_statistics(self) -> Dict:
        """Get vector store statistics"""
        try:
            total_docs = await self.get_document_count()
            
            return {
                "total_documents": total_docs,
                "total_hashes": len(self.document_hashes),
                "chunk_size": self.chunk_size,
                "similarity_threshold": self.similarity_threshold,
                "model_name": "all-MiniLM-L6-v2",
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return {}
            
    async def reset_collection(self) -> bool:
        """Reset the entire collection (use with caution)"""
        try:
            self.client.delete_collection("zero_entropy_knowledge")
            self.collection = self.client.create_collection(
                name="zero_entropy_knowledge",
                metadata={"description": "Zero Entropy enhanced knowledge base"}
            )
            self.document_hashes.clear()
            print("🔄 Collection reset successfully")
            return True
        except Exception as e:
            print(f"❌ Error resetting collection: {e}")
            return False
            
    async def shutdown(self):
        """Shutdown vector store"""
        print("🔄 Shutting down Vector Store...")
        # ChromaDB handles cleanup automatically

