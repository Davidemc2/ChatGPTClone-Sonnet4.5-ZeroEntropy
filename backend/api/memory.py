"""
Memory and RAG API endpoints
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from loguru import logger


router = APIRouter()


class AddKnowledgeRequest(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None
    category: str = "general"


class SearchRequest(BaseModel):
    query: str
    n_results: int = 5
    filter_by: Optional[Dict[str, Any]] = None


@router.post("/add")
async def add_knowledge(request: AddKnowledgeRequest, app_request: Request):
    """
    Add knowledge to the RAG system
    """
    try:
        memory_system = app_request.app.state.memory_system
        
        doc_id = memory_system.add_knowledge(
            content=request.content,
            metadata=request.metadata,
            category=request.category
        )
        
        return {
            "status": "success",
            "document_id": doc_id,
            "message": "Knowledge added to memory"
        }
        
    except Exception as e:
        logger.error(f"Error adding knowledge: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search")
async def search_memory(request: SearchRequest, app_request: Request):
    """
    Search the memory system
    """
    try:
        memory_system = app_request.app.state.memory_system
        
        results = memory_system.search_memory(
            query=request.query,
            n_results=request.n_results,
            filter_by=request.filter_by
        )
        
        return {
            "query": request.query,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error searching memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_memory_stats(app_request: Request):
    """
    Get memory system statistics
    """
    try:
        memory_system = app_request.app.state.memory_system
        stats = memory_system.get_memory_stats()
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear")
async def clear_memory(app_request: Request):
    """
    Clear all memory (use with caution!)
    """
    try:
        memory_system = app_request.app.state.memory_system
        memory_system.clear_all_memory()
        
        return {
            "status": "success",
            "message": "All memory cleared"
        }
        
    except Exception as e:
        logger.error(f"Error clearing memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch-add")
async def batch_add_knowledge(
    documents: List[AddKnowledgeRequest],
    app_request: Request
):
    """
    Add multiple knowledge documents in batch
    """
    try:
        memory_system = app_request.app.state.memory_system
        rag_engine = app_request.app.state.rag_engine
        
        # Extract data
        texts = [doc.content for doc in documents]
        metadatas = []
        
        for doc in documents:
            metadata = doc.metadata or {}
            metadata["category"] = doc.category
            metadata["type"] = "knowledge"
            metadatas.append(metadata)
        
        # Batch add
        doc_ids = rag_engine.add_documents_batch(
            texts=texts,
            metadatas=metadatas
        )
        
        return {
            "status": "success",
            "document_ids": doc_ids,
            "count": len(doc_ids),
            "message": f"Added {len(doc_ids)} documents to memory"
        }
        
    except Exception as e:
        logger.error(f"Error batch adding knowledge: {e}")
        raise HTTPException(status_code=500, detail=str(e))
