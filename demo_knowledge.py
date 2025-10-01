#!/usr/bin/env python3
"""
Demo script to add sample knowledge to the RAG system

This demonstrates how to enhance the AI with domain-specific knowledge
using the Zero Entropy memory system.
"""

import requests
import json

API_URL = "http://localhost:8000"

# Sample knowledge about Zero Entropy principles
SAMPLE_KNOWLEDGE = [
    {
        "content": """Zero Entropy Principle in AI Systems:
        
        Zero Entropy refers to minimizing uncertainty and maintaining highly ordered,
        deterministic states in information systems. In the context of RAG systems:
        
        1. Deterministic Retrieval: Consistent document identification using hashing
        2. Entropy Scoring: Quantifying information density using Shannon entropy
        3. Redundancy Elimination: Preventing duplicate context through fingerprinting
        4. Ordered Knowledge: Hierarchical organization with rich metadata
        
        This approach ensures reliable, reproducible, and efficient information retrieval.""",
        "category": "core_concepts",
        "metadata": {
            "topic": "zero_entropy",
            "importance": "high",
            "source": "system_documentation"
        }
    },
    {
        "content": """First Principles Thinking in Software Development:
        
        First principles thinking involves breaking down complex problems to their
        fundamental truths and reasoning up from there. Elon Musk popularized this
        approach in engineering:
        
        1. Question every assumption
        2. Break problems into basic elements
        3. Build solutions from scratch
        4. Optimize ruthlessly
        5. Avoid reasoning by analogy
        
        Applied to AI systems: instead of copying existing architectures, understand
        the core requirements and build the optimal solution.""",
        "category": "methodology",
        "metadata": {
            "topic": "first_principles",
            "importance": "high",
            "source": "philosophical_foundation"
        }
    },
    {
        "content": """Linux Development Philosophy:
        
        The Linux kernel development follows key principles that make it robust:
        
        1. Modularity: Each component does one thing well
        2. Composability: Components work together seamlessly
        3. Transparency: Code is readable and understandable
        4. Community-driven: Open collaboration and peer review
        5. Iterative improvement: Continuous refinement over time
        
        These principles apply to any large-scale software project, ensuring
        maintainability and scalability.""",
        "category": "methodology",
        "metadata": {
            "topic": "linux_philosophy",
            "importance": "high",
            "source": "development_methodology"
        }
    },
    {
        "content": """RAG (Retrieval-Augmented Generation) Systems:
        
        RAG enhances language models by retrieving relevant context before generation:
        
        Components:
        1. Retriever: Finds relevant documents using semantic search
        2. Augmenter: Injects retrieved context into the prompt
        3. Generator: LLM produces response with enhanced context
        
        Benefits:
        - Access to external knowledge
        - Reduced hallucinations
        - Dynamic information updates
        - Source attribution
        
        Zero Entropy RAG adds deterministic retrieval and entropy optimization.""",
        "category": "technical",
        "metadata": {
            "topic": "rag_systems",
            "importance": "high",
            "source": "technical_documentation"
        }
    },
    {
        "content": """Vector Embeddings and Semantic Search:
        
        Vector embeddings represent text as high-dimensional numerical vectors,
        where semantic similarity corresponds to vector proximity.
        
        Process:
        1. Encode text with embedding model (e.g., sentence-transformers)
        2. Store vectors in vector database (e.g., ChromaDB, Pinecone)
        3. Query by encoding search text
        4. Find nearest neighbors using cosine similarity
        
        Advantages:
        - Semantic understanding beyond keywords
        - Multilingual capability
        - Fuzzy matching
        - Scalable search
        
        This system uses sentence-transformers/all-MiniLM-L6-v2 for embeddings.""",
        "category": "technical",
        "metadata": {
            "topic": "embeddings",
            "importance": "medium",
            "source": "technical_documentation"
        }
    }
]


def add_knowledge(content, category, metadata):
    """Add knowledge to the RAG system"""
    try:
        response = requests.post(
            f"{API_URL}/api/memory/add",
            json={
                "content": content,
                "category": category,
                "metadata": metadata
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error adding knowledge: {e}")
        return None


def get_memory_stats():
    """Get memory system statistics"""
    try:
        response = requests.get(f"{API_URL}/api/memory/stats", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error getting stats: {e}")
        return None


def main():
    print("╔════════════════════════════════════════════════════════╗")
    print("║   Zero Entropy RAG - Knowledge Demo Script            ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    # Check backend health
    print("🔍 Checking backend connection...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
        else:
            print("⚠️  Backend returned unexpected status")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend at {API_URL}")
        print(f"   Error: {e}")
        print("\n   Please ensure the backend is running:")
        print("   cd backend && python main.py")
        return
    
    print()
    print("📚 Adding sample knowledge to RAG system...")
    print()
    
    success_count = 0
    for i, knowledge in enumerate(SAMPLE_KNOWLEDGE, 1):
        print(f"[{i}/{len(SAMPLE_KNOWLEDGE)}] Adding: {knowledge['metadata']['topic']}...", end=" ")
        result = add_knowledge(
            knowledge["content"],
            knowledge["category"],
            knowledge["metadata"]
        )
        if result:
            print("✅")
            success_count += 1
        else:
            print("❌")
    
    print()
    print(f"✨ Successfully added {success_count}/{len(SAMPLE_KNOWLEDGE)} knowledge items")
    print()
    
    # Get stats
    print("📊 Memory system statistics:")
    stats = get_memory_stats()
    if stats:
        print(f"   • Total documents: {stats.get('long_term_memories', 0)}")
        print(f"   • Active sessions: {stats.get('active_sessions', 0)}")
        print(f"   • Long-term memory: {'Enabled' if stats.get('long_term_memory_enabled') else 'Disabled'}")
    
    print()
    print("╔════════════════════════════════════════════════════════╗")
    print("║  🎉 Knowledge successfully loaded!                     ║")
    print("╠════════════════════════════════════════════════════════╣")
    print("║  Try asking the AI about:                             ║")
    print("║  • What is Zero Entropy?                              ║")
    print("║  • Explain first principles thinking                  ║")
    print("║  • How does RAG work?                                 ║")
    print("║  • What are vector embeddings?                        ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()


if __name__ == "__main__":
    main()
