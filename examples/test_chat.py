#!/usr/bin/env python3
"""
Example: Testing the Chat System

This script demonstrates how to use the RAG engine programmatically.
"""
import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import ZeroEntropyVectorStore, MemoryManager, RAGEngine

async def main():
    """Test chat functionality"""
    print("🚀 Testing Zero Entropy Chat System...\n")
    
    # Initialize components
    print("📦 Initializing components...")
    vector_store = ZeroEntropyVectorStore()
    rag_engine = RAGEngine(vector_store)
    memory = MemoryManager("test_session", vector_store)
    
    # Test queries
    queries = [
        "What are the zero entropy principles?",
        "Explain first principles thinking",
        "How does the RAG system work?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*60}")
        print(f"Query {i}: {query}")
        print('='*60)
        
        # Generate response
        print("\n🤖 Assistant: ", end="", flush=True)
        
        full_response = ""
        async for chunk in rag_engine.generate_response(
            user_message=query,
            memory=memory,
            use_rag=True,
            stream=True
        ):
            print(chunk, end="", flush=True)
            full_response += chunk
        
        print("\n")
        
        # Add to memory
        memory.add_exchange(query, full_response)
        
        # Small delay
        await asyncio.sleep(1)
    
    # Show memory summary
    print("\n" + "="*60)
    print("📊 Session Summary")
    print("="*60)
    summary = memory.get_summary()
    print(f"Session ID: {summary['session_id']}")
    print(f"Total messages: {summary['message_count']}")
    print(f"Created at: {summary['created_at']}")
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    asyncio.run(main())
