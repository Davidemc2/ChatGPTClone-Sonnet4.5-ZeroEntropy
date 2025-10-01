"""
Knowledge Controller - API endpoints for knowledge management

Handles:
- Document upload and processing
- Knowledge base search
- Document management (CRUD)
- Entropy-based quality filtering

Zero Entropy Principles:
- High-quality knowledge curation
- Entropy-filtered document acceptance
- Efficient knowledge organization
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import List, Dict, Optional
import uuid
import json
import asyncio
from datetime import datetime
import logging

from ..models.chat_models import (
    KnowledgeDocument, KnowledgeUploadRequest, KnowledgeUploadResponse,
    KnowledgeSearchRequest, KnowledgeSearchResponse, ErrorResponse
)
from ..core.zero_entropy_rag import ZeroEntropyRAG
from ..core.vector_store import VectorStore
from ..utils.entropy_calculator import EntropyCalculator


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


# Dependency injection functions
def get_rag_engine():
    """Dependency injection for RAG engine"""
    from main import get_rag_engine
    return get_rag_engine()

def get_vector_store():
    """Dependency injection for vector store"""
    from main import get_vector_store
    return get_vector_store()


@router.post("/knowledge/upload", response_model=KnowledgeUploadResponse)
async def upload_knowledge(
    request: KnowledgeUploadRequest,
    rag_engine: ZeroEntropyRAG = Depends(get_rag_engine)
) -> KnowledgeUploadResponse:
    """
    Upload knowledge documents with Zero Entropy filtering
    
    Features:
    - Entropy-based quality filtering
    - Automatic deduplication
    - Batch processing
    - Quality metrics
    """
    
    try:
        upload_id = f"upload_{uuid.uuid4().hex[:8]}"
        logger.info(f"Knowledge upload started: {upload_id} - {len(request.documents)} documents")
        
        uploaded_count = 0
        skipped_count = 0
        failed_count = 0
        
        entropy_calculator = EntropyCalculator()
        
        for doc in request.documents:
            try:
                # Calculate document entropy for quality filtering
                entropy_metrics = await entropy_calculator.calculate_comprehensive_metrics(
                    doc.content
                )
                
                # Apply Zero Entropy filtering
                if entropy_metrics.overall_quality >= 0.6:  # Quality threshold
                    success = await rag_engine.add_knowledge(
                        content=doc.content,
                        source=doc.source
                    )
                    
                    if success:
                        uploaded_count += 1
                        logger.info(f"Uploaded: {doc.source} (Quality: {entropy_metrics.overall_quality:.2f})")
                    else:
                        skipped_count += 1  # Duplicate or other reason
                        logger.info(f"Skipped: {doc.source} (Duplicate)")
                else:
                    skipped_count += 1
                    logger.info(f"Skipped: {doc.source} (Low quality: {entropy_metrics.overall_quality:.2f})")
                    
            except Exception as e:
                failed_count += 1
                logger.error(f"Failed to process {doc.source}: {str(e)}")
                
        # Get updated document count
        vector_store = get_vector_store()
        total_documents = await vector_store.get_document_count()
        
        # Calculate entropy status
        entropy_status = "optimal" if uploaded_count > 0 else "no_changes"
        
        response = KnowledgeUploadResponse(
            uploaded_count=uploaded_count,
            skipped_count=skipped_count,
            failed_count=failed_count,
            total_documents=total_documents,
            entropy_status=entropy_status,
            upload_id=upload_id
        )
        
        logger.info(f"Upload completed: {upload_id} - {uploaded_count} uploaded, {skipped_count} skipped, {failed_count} failed")
        
        return response
        
    except Exception as e:
        logger.error(f"Knowledge upload error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading knowledge: {str(e)}"
        )


@router.post("/knowledge/upload/file")
async def upload_knowledge_file(
    file: UploadFile = File(...),
    source_name: Optional[str] = Form(None),
    vector_store: VectorStore = Depends(get_vector_store)
):
    """
    Upload knowledge from file (text, markdown, etc.)
    """
    
    try:
        # Read file content
        content = await file.read()
        text_content = content.decode('utf-8')
        
        # Use filename as source if not provided
        source = source_name or file.filename or f"upload_{uuid.uuid4().hex[:8]}"
        
        # Validate content
        if len(text_content.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="File content too short (minimum 50 characters)"
            )
            
        # Calculate entropy for quality assessment
        entropy_calculator = EntropyCalculator()
        entropy_metrics = await entropy_calculator.calculate_comprehensive_metrics(text_content)
        
        # Add to vector store
        success = await vector_store.add_document(
            content=text_content,
            source=source,
            metadata={
                "file_name": file.filename,
                "file_size": len(content),
                "upload_timestamp": datetime.now().isoformat(),
                "entropy_score": entropy_metrics.shannon_entropy,
                "quality_score": entropy_metrics.overall_quality
            }
        )
        
        if success:
            logger.info(f"File uploaded: {source} - Quality: {entropy_metrics.overall_quality:.2f}")
            return {
                "message": f"File '{source}' uploaded successfully",
                "source": source,
                "content_length": len(text_content),
                "quality_score": entropy_metrics.overall_quality,
                "entropy_score": entropy_metrics.shannon_entropy
            }
        else:
            raise HTTPException(
                status_code=400,
                detail="File upload failed (possible duplicate or quality issue)"
            )
            
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be valid UTF-8 text"
        )
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}"
        )


@router.post("/knowledge/search", response_model=KnowledgeSearchResponse)
async def search_knowledge(
    request: KnowledgeSearchRequest,
    vector_store: VectorStore = Depends(get_vector_store)
) -> KnowledgeSearchResponse:
    """
    Search knowledge base with entropy analysis
    """
    
    try:
        # Calculate query entropy
        entropy_calculator = EntropyCalculator()
        query_entropy = await entropy_calculator.calculate_text_entropy(request.query)
        
        # Perform similarity search
        results = await vector_store.similarity_search(
            query=request.query,
            k=request.limit,
            filter_metadata=request.filter_metadata
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "content": result.content,
                "source": result.source,
                "relevance_score": result.relevance_score,
                "document_id": result.document_id,
                "metadata": result.metadata
            })
            
        # Determine search quality based on entropy
        search_quality = await entropy_calculator.get_entropy_status(query_entropy)
        
        return KnowledgeSearchResponse(
            results=formatted_results,
            total_results=len(formatted_results),
            query_entropy=query_entropy,
            search_quality=search_quality
        )
        
    except Exception as e:
        logger.error(f"Knowledge search error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching knowledge: {str(e)}"
        )


@router.get("/knowledge/documents")
async def list_documents(
    limit: int = 20,
    offset: int = 0,
    source_filter: Optional[str] = None,
    vector_store: VectorStore = Depends(get_vector_store)
):
    """
    List documents in the knowledge base
    """
    
    try:
        # Build metadata filter if source specified
        metadata_filter = {}
        if source_filter:
            metadata_filter["source"] = source_filter
            
        # Search with metadata filter
        results = await vector_store.search_by_metadata(
            metadata_filter=metadata_filter,
            limit=limit
        )
        
        # Format results
        documents = []
        for result in results:
            documents.append({
                "document_id": result.document_id,
                "source": result.source,
                "content_preview": result.content[:200] + "..." if len(result.content) > 200 else result.content,
                "content_length": len(result.content),
                "metadata": result.metadata
            })
            
        return {
            "documents": documents,
            "total_found": len(documents),
            "limit": limit,
            "offset": offset,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"List documents error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing documents: {str(e)}"
        )


@router.get("/knowledge/document/{document_id}")
async def get_document(
    document_id: str,
    vector_store: VectorStore = Depends(get_vector_store)
):
    """
    Get specific document by ID
    """
    
    try:
        # Search for document by metadata (using document_id)
        results = await vector_store.search_by_metadata(
            metadata_filter={"document_id": document_id},
            limit=1
        )
        
        if not results:
            raise HTTPException(
                status_code=404,
                detail=f"Document {document_id} not found"
            )
            
        doc = results[0]
        
        # Calculate current entropy metrics
        entropy_calculator = EntropyCalculator()
        entropy_metrics = await entropy_calculator.calculate_comprehensive_metrics(doc.content)
        
        return {
            "document_id": doc.document_id,
            "source": doc.source,
            "content": doc.content,
            "metadata": doc.metadata,
            "entropy_metrics": {
                "shannon_entropy": entropy_metrics.shannon_entropy,
                "certainty_score": entropy_metrics.certainty_score,
                "semantic_coherence": entropy_metrics.semantic_coherence,
                "overall_quality": entropy_metrics.overall_quality
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get document error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving document: {str(e)}"
        )


@router.delete("/knowledge/document/{document_id}")
async def delete_document(
    document_id: str,
    vector_store: VectorStore = Depends(get_vector_store)
):
    """
    Delete document by ID
    """
    
    try:
        success = await vector_store.delete_document(document_id)
        
        if success:
            logger.info(f"Document deleted: {document_id}")
            return {
                "message": f"Document {document_id} deleted successfully",
                "document_id": document_id,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Document {document_id} not found or could not be deleted"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete document error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting document: {str(e)}"
        )


@router.get("/knowledge/statistics")
async def get_knowledge_statistics(
    vector_store: VectorStore = Depends(get_vector_store)
):
    """
    Get knowledge base statistics and metrics
    """
    
    try:
        # Get vector store statistics
        stats = await vector_store.get_statistics()
        
        # Add entropy-related metrics
        entropy_status = {
            "total_documents": stats.get("total_documents", 0),
            "similarity_threshold": stats.get("similarity_threshold", 0.7),
            "model_info": stats.get("model_name", "unknown"),
            "last_updated": stats.get("last_updated"),
            "entropy_optimization": "active",
            "quality_filtering": "enabled"
        }
        
        return {
            "statistics": entropy_status,
            "system_status": "optimal",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Statistics error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving statistics: {str(e)}"
        )


@router.post("/knowledge/analyze")
async def analyze_text(
    text: str = Form(...),
    include_suggestions: bool = Form(False)
):
    """
    Analyze text entropy and quality metrics
    """
    
    try:
        if len(text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Text content cannot be empty"
            )
            
        entropy_calculator = EntropyCalculator()
        
        # Calculate comprehensive metrics
        metrics = await entropy_calculator.calculate_comprehensive_metrics(text)
        
        # Get entropy status
        entropy_status = await entropy_calculator.get_entropy_status(metrics.shannon_entropy)
        
        result = {
            "entropy_metrics": {
                "shannon_entropy": metrics.shannon_entropy,
                "normalized_entropy": metrics.normalized_entropy,
                "certainty_score": metrics.certainty_score,
                "word_diversity": metrics.word_diversity,
                "semantic_coherence": metrics.semantic_coherence,
                "overall_quality": metrics.overall_quality
            },
            "entropy_status": entropy_status,
            "quality_assessment": "excellent" if metrics.overall_quality > 0.8 else 
                                "good" if metrics.overall_quality > 0.6 else
                                "acceptable" if metrics.overall_quality > 0.4 else "poor",
            "text_length": len(text),
            "word_count": len(text.split()),
            "timestamp": datetime.now().isoformat()
        }
        
        # Add improvement suggestions if requested
        if include_suggestions:
            suggestions = await entropy_calculator.suggest_improvements(text)
            result["improvement_suggestions"] = suggestions
            
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Text analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing text: {str(e)}"
        )


@router.post("/knowledge/reset")
async def reset_knowledge_base(
    confirm: bool = Form(False),
    vector_store: VectorStore = Depends(get_vector_store)
):
    """
    Reset entire knowledge base (use with extreme caution)
    """
    
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Must set confirm=true to reset knowledge base"
        )
        
    try:
        success = await vector_store.reset_collection()
        
        if success:
            logger.warning("Knowledge base reset completed")
            return {
                "message": "Knowledge base reset successfully",
                "total_documents": 0,
                "timestamp": datetime.now().isoformat(),
                "warning": "All documents have been permanently deleted"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to reset knowledge base"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Reset knowledge base error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error resetting knowledge base: {str(e)}"
        )


# Health check endpoint
@router.get("/knowledge/health")
async def knowledge_health_check():
    """Health check for knowledge management"""
    return {
        "status": "healthy",
        "service": "knowledge_controller",
        "timestamp": datetime.now().isoformat()
    }

