#!/usr/bin/env python3
"""
Example: Adding Knowledge to the RAG System

This script demonstrates how to add documents to the Zero Entropy RAG system.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import ZeroEntropyVectorStore

# Sample knowledge about Zero Entropy principles
ZERO_ENTROPY_KNOWLEDGE = [
    """
    Zero Entropy Principles in AI Systems:
    
    1. Minimal Information Loss: Design systems that preserve the maximum amount 
    of meaningful information throughout processing pipelines. In RAG systems, 
    this means using dense vector representations that capture semantic meaning 
    without degradation.
    
    2. Deterministic Retrieval: Given the same query, the system should return 
    consistent results. This is achieved through stable embedding models and 
    consistent similarity metrics (cosine similarity).
    
    3. Optimal State: The system maintains perfect coherence between stored 
    knowledge and retrieved context. This requires careful chunking strategies 
    and metadata management.
    """,
    
    """
    First Principles Thinking (Elon Musk Methodology):
    
    - Break down complex problems to their fundamental truths
    - Question all assumptions systematically
    - Reason up from basic physics/logic, not by analogy
    - Example: "What is physically/mathematically required to solve this?"
    
    Applied to AI:
    - What is fundamentally needed for understanding? → Context
    - What is needed for generation? → Language model
    - What connects them? → Retrieval mechanism
    - This leads naturally to RAG architecture
    """,
    
    """
    Unix Philosophy Applied to Software:
    
    1. Do One Thing Well: Each module has a single, clear responsibility
       - vector_store.py: Only vector operations
       - memory_manager.py: Only conversation state
       - rag_engine.py: Only RAG orchestration
    
    2. Composability: Small tools combine to create complex systems
       - Vector Store + Memory + RAG Engine = Complete ChatGPT
    
    3. Simplicity: Keep it simple, avoid unnecessary complexity
       - Use standard protocols (HTTP, WebSocket)
       - Plain text storage where possible
       - Clear, readable code over clever tricks
    """,
    
    """
    RAG System Architecture:
    
    Retrieval-Augmented Generation combines:
    - Information Retrieval: Find relevant documents
    - Language Generation: Create coherent responses
    
    Key Components:
    1. Embedding Model: Converts text to vectors (e.g., OpenAI text-embedding-3-small)
    2. Vector Store: Stores and searches embeddings (e.g., ChromaDB)
    3. Chunking Strategy: Splits documents optimally (recursive splitting)
    4. Retrieval Mechanism: Finds top-K most relevant chunks
    5. Context Assembly: Combines retrieved info with user query
    6. Generation: LLM produces final response
    
    Benefits:
    - Reduces hallucination by grounding in facts
    - Enables knowledge updates without retraining
    - Provides source attribution
    """,
    
    """
    Vector Embeddings Explained:
    
    Text embeddings convert words/sentences into dense numerical vectors that 
    capture semantic meaning. Similar concepts have similar vectors.
    
    Example (simplified):
    - "king" - "man" + "woman" ≈ "queen"
    - "Paris" is close to "France" in vector space
    
    In RAG systems:
    - Documents are embedded once and stored
    - Queries are embedded at runtime
    - Cosine similarity finds most relevant documents
    - Top-K results provide context for generation
    
    This enables semantic search: finding by meaning, not just keywords.
    """
]

def main():
    """Add knowledge to the vector store"""
    print("🚀 Adding knowledge to Zero Entropy RAG system...")
    
    # Initialize vector store
    vector_store = ZeroEntropyVectorStore()
    
    # Prepare metadata
    metadata = [
        {"source": "zero_entropy_principles", "topic": "architecture"},
        {"source": "first_principles", "topic": "methodology"},
        {"source": "unix_philosophy", "topic": "design"},
        {"source": "rag_architecture", "topic": "technical"},
        {"source": "embeddings", "topic": "technical"}
    ]
    
    # Add documents
    doc_ids = vector_store.add_documents(ZERO_ENTROPY_KNOWLEDGE, metadata)
    
    print(f"✅ Added {len(doc_ids)} documents to the knowledge base")
    print(f"📝 Document IDs: {doc_ids[:2]}... (showing first 2)")
    
    # Test retrieval
    print("\n🔍 Testing retrieval...")
    query = "What is first principles thinking?"
    results = vector_store.similarity_search(query, k=2)
    
    print(f"\nQuery: '{query}'")
    print(f"Found {len(results)} relevant documents:\n")
    
    for i, result in enumerate(results, 1):
        print(f"--- Result {i} (score: {result['relevance_score']:.3f}) ---")
        print(result['content'][:200] + "...\n")
    
    print("✅ Knowledge successfully added and tested!")

if __name__ == "__main__":
    main()
