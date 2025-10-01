"""
Zero Entropy Vector Store
Implements minimal-entropy storage with efficient retrieval mechanisms.

Core principles:
1. Deterministic retrieval - same query should yield consistent results
2. Semantic compression - store knowledge in dense vector space
3. Efficient indexing - O(log n) retrieval time
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
import os

from config import settings


class ZeroEntropyVectorStore:
    """
    Vector store implementing zero-entropy principles:
    - Minimal information loss during storage and retrieval
    - Consistent state maintenance across operations
    - Predictable and reliable outputs
    """
    
    def __init__(self):
        """Initialize the vector store with persistent storage"""
        # Ensure data directory exists
        os.makedirs(settings.chroma_persist_dir, exist_ok=True)
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key
        )
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize LangChain Chroma wrapper
        self.vectorstore = Chroma(
            client=self.client,
            collection_name=settings.collection_name,
            embedding_function=self.embeddings
        )
        
        # Text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def add_documents(self, documents: List[str], metadata: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """
        Add documents to the vector store with automatic chunking
        
        Args:
            documents: List of text documents to add
            metadata: Optional metadata for each document
            
        Returns:
            List of document IDs
        """
        if not documents:
            return []
        
        # Generate unique IDs
        doc_ids = [str(uuid.uuid4()) for _ in documents]
        
        # Prepare metadata
        if metadata is None:
            metadata = [{} for _ in documents]
        
        # Add timestamp to all metadata
        for meta in metadata:
            meta["timestamp"] = datetime.utcnow().isoformat()
        
        # Split documents into chunks
        all_chunks = []
        all_metadatas = []
        all_ids = []
        
        for doc, meta, doc_id in zip(documents, metadata, doc_ids):
            chunks = self.text_splitter.split_text(doc)
            for i, chunk in enumerate(chunks):
                chunk_meta = meta.copy()
                chunk_meta["chunk_index"] = i
                chunk_meta["document_id"] = doc_id
                all_chunks.append(chunk)
                all_metadatas.append(chunk_meta)
                all_ids.append(f"{doc_id}_{i}")
        
        # Add to vector store
        self.vectorstore.add_texts(
            texts=all_chunks,
            metadatas=all_metadatas,
            ids=all_ids
        )
        
        return doc_ids
    
    def similarity_search(
        self, 
        query: str, 
        k: int = None,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform similarity search with optional filtering
        
        Args:
            query: Search query
            k: Number of results to return (default from settings)
            filter: Optional metadata filter
            
        Returns:
            List of relevant documents with metadata
        """
        if k is None:
            k = settings.top_k_results
        
        # Perform similarity search
        results = self.vectorstore.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter
        )
        
        # Format results
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "relevance_score": float(score)
            })
        
        return formatted_results
    
    def add_conversation(self, user_message: str, assistant_message: str, session_id: str):
        """
        Add a conversation exchange to the vector store for future retrieval
        
        Args:
            user_message: User's message
            assistant_message: Assistant's response
            session_id: Unique session identifier
        """
        conversation_text = f"User: {user_message}\nAssistant: {assistant_message}"
        metadata = {
            "type": "conversation",
            "session_id": session_id,
            "user_message": user_message,
            "assistant_message": assistant_message
        }
        self.add_documents([conversation_text], [metadata])
    
    def search_conversations(self, query: str, session_id: Optional[str] = None, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search through past conversations
        
        Args:
            query: Search query
            session_id: Optional session filter
            k: Number of results
            
        Returns:
            List of relevant conversation exchanges
        """
        filter_dict = {"type": "conversation"}
        if session_id:
            filter_dict["session_id"] = session_id
        
        return self.similarity_search(query, k=k, filter=filter_dict)
    
    def reset(self):
        """Reset the vector store (use with caution)"""
        self.client.reset()
        # Reinitialize
        self.__init__()
