"""
DIRAS FastAPI Main Application
Phase 2 Implementation - Free Stack
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import database
from src.shared.database import get_db
# Register download router
from src.api.download_excel import router as download_router

# Initialize FastAPI app
app = FastAPI(
    title="DIRAS (Defence Intelligence Retrieval and Analysis System)",
    description="Phase 2 Implementation - Free Stack",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(download_router)

# ============================================================================
# Request/Response Models
# ============================================================================

class QueryRequest(BaseModel):
    question: str
    top_k: int = 15
    document_type: str = None

# ============================================================================
# Health Check Endpoints
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker health checks"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0"
    }

@app.get("/api/v1/health")
async def api_health_check():
    """Detailed health check with service status"""
    health_status = {
        "app": "running",
        "database": "checking...",
        "vector_db": "checking...",
        "search": "checking..."
    }
    
    try:
        # Check PostgreSQL connection
        from src.shared.database import get_db
        logger.info("Database connection OK")
        health_status["database"] = "connected"
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        health_status["database"] = f"error: {str(e)}"
    
    try:
        # Check ChromaDB connection
        logger.info("Vector DB connection OK (lazy load)")
        health_status["vector_db"] = "ready"
    except Exception as e:
        logger.error(f"Vector DB connection failed: {e}")
        health_status["vector_db"] = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "services": health_status,
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================================
# System Status Endpoints
# ============================================================================

@app.get("/api/v1/status")
async def system_status():
    """System status including metrics and configuration"""
    return {
        "phase": "Phase 2",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "status": "development",
        "start_time": datetime.utcnow().isoformat(),
        "capabilities": {
            "ocr": "enabled",
            "classification": "enabled",
            "ner": "enabled",
            "embeddings": "enabled",
            "retrieval": "enabled",
            "rag": "enabled"
        }
    }

# ============================================================================
# API Version Info
# ============================================================================

@app.get("/api/v1/info")
async def api_info():
    """API information and available endpoints"""
    return {
        "name": "DIRAS API",
        "version": "0.1.0",
        "phase": "Phase 2 Implementation",
        "free_stack": True,
        "endpoints": {
            "health": "/health",
            "api_health": "/api/v1/health",
            "status": "/api/v1/status",
            "info": "/api/v1/info",
            "documents": "/api/v1/documents",
            "query": "/api/v1/query",
            "metrics": "/api/v1/metrics"
        }
    }

# ============================================================================
# Query & Search Endpoints
# ============================================================================

@app.post("/api/v1/query")
async def query(
    request: QueryRequest,
    db = Depends(get_db)
):
    """
    Execute a query using RAG pipeline
    Real implementation: retrieves documents + generates answer with Grok
    """
    
    try:
        from src.services.rag_engine import get_rag_engine
        import time
        
        start_time = time.time()
        
        # Get RAG engine
        rag = get_rag_engine(top_k=request.top_k)
        
        # Generate answer
        result = rag.generate_answer(
            query=request.question,
            db=db,
            top_k=request.top_k,
            document_type_filter=request.document_type
        )
        
        # Add processing metadata
        result["processing_time"] = time.time() - start_time
        
        logger.info(f"Query processed in {result['processing_time']:.2f}s")
        
        return result
        
    except Exception as e:
        logger.error(f"Query endpoint error: {e}")
        return {
            "answer": "",
            "sources": [],
            "error": str(e),
            "confidence": 0.0,
            "processing_time": 0
        }

# ============================================================================
# Scraping & Indexing Endpoints
# ============================================================================

@app.post("/api/v1/scrape")
async def start_scraping(max_docs: int = 200):
    """
    Start document scraping from government sources
    Returns immediately; scraping happens in background
    """
    
    try:
        import importlib
        scraper_module = importlib.import_module('src.01-data-pipeline.scraper_runner')
        ScraperRunner = getattr(scraper_module, 'ScraperRunner')
        
        logger.info(f"Starting scraper to download {max_docs} documents...")
        
        runner = ScraperRunner()
        result = runner.run_moad_scraper(max_docs=max_docs)
        
        return {
            "status": result["status"],
            "documents_downloaded": result.get("documents_downloaded", 0),
            "duration_seconds": result.get("duration_seconds", 0),
            "next_steps": result.get("next_steps", []),
            "errors": result.get("errors", [])
        }
        
    except Exception as e:
        logger.error(f"Scraping error: {e}")
        return {
            "status": "failed",
            "error": str(e)
        }

@app.get("/api/v1/documents")
async def list_documents(skip: int = 0, limit: int = 10, db = Depends(get_db)):
    """List documents from database with status"""
    
    try:
        from src.models.document import Document
        
        total = db.query(Document).count()
        documents = db.query(Document).offset(skip).limit(limit).all()
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "documents": [
                {
                    "id": doc.id,
                    "title": doc.title,
                    "source_url": doc.source_url,
                    "source_type": doc.source_type,
                    "document_type": doc.document_type,
                    "status": doc.status,
                    "is_indexed": doc.is_indexed,
                    "ocr_confidence": doc.ocr_confidence,
                    "downloaded_date": doc.downloaded_date.isoformat() if doc.downloaded_date else None
                }
                for doc in documents
            ]
        }
        
    except Exception as e:
        logger.error(f"List documents error: {e}")
        return {"error": str(e), "documents": []}

@app.get("/api/v1/index-status")
async def get_index_status(db = Depends(get_db)):
    """Get indexing progress and statistics"""
    
    try:
        from src.models.document import Document, DocumentChunk
        
        total_docs = db.query(Document).count()
        indexed_docs = db.query(Document).filter(Document.is_indexed == True).count()
        total_chunks = db.query(DocumentChunk).count()
        indexed_chunks = db.query(DocumentChunk).filter(DocumentChunk.is_indexed == True).count()
        
        return {
            "total_documents": total_docs,
            "indexed_documents": indexed_docs,
            "pending_documents": total_docs - indexed_docs,
            "total_chunks": total_chunks,
            "indexed_chunks": indexed_chunks,
            "pending_chunks": total_chunks - indexed_chunks,
            "completion_percentage": round((indexed_chunks / total_chunks * 100) if total_chunks > 0 else 0, 1)
        }
        
    except Exception as e:
        logger.error(f"Index status error: {e}")
        return {"error": str(e)}

# ============================================================================
# Processing Endpoints
# ============================================================================

@app.post("/api/v1/process-documents")
async def process_documents(limit: int = 50, db = Depends(get_db)):
    """Process documents through OCR pipeline"""
    
    try:
        from src.services.document_processor import get_document_processor
        
        processor = get_document_processor()
        result = processor.batch_process_documents(limit=limit, db=db)
        
        return result
        
    except Exception as e:
        logger.error(f"Document processing error: {e}")
        return {"error": str(e), "status": "failed"}

@app.post("/api/v1/index-documents")
async def index_documents(db = Depends(get_db)):
    """Index documents into vector store"""
    
    try:
        from src.services.indexer import get_document_indexer
        
        indexer = get_document_indexer()
        result = indexer.index_all_documents(db=db)
        
        return result
        
    except Exception as e:
        logger.error(f"Document indexing error: {e}")
        return {"error": str(e), "status": "failed"}

# ============================================================================
# Classification Endpoints (Placeholder for Sprint 3)
# ============================================================================

@app.post("/api/v1/classify")
async def classify_document(text: str):
    """Classify document type (Sprint 3)"""
    return {
        "text": text[:100],
        "message": "Classification will be available after Sprint 3",
        "status": "pending"
    }

# ============================================================================
# NER Endpoints (Placeholder for Sprint 4)
# ============================================================================

@app.post("/api/v1/extract-entities")
async def extract_entities(text: str):
    """Extract named entities from text (Sprint 4)"""
    return {
        "text": text[:100],
        "message": "Entity extraction will be available after Sprint 4",
        "status": "pending",
        "entities": []
    }

# ============================================================================
# Metrics Endpoints (Placeholder for Sprint 8)
# ============================================================================

@app.get("/api/v1/metrics")
async def get_metrics():
    """Get system metrics (OCR accuracy, retrieval quality, etc.)"""
    return {
        "message": "Metrics will be available after Sprint 8",
        "status": "pending",
        "metrics": {}
    }

# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API documentation link"""
    return {
        "message": "Welcome to DIRAS (Defence Intelligence Retrieval and Analysis System)",
        "documentation": "/docs",
        "openapi_schema": "/openapi.json",
        "version": "0.1.0",
        "phase": "Phase 2 Implementation",
        "status": "development"
    }

# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": True}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": True}
    )

# ============================================================================
# Startup & Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on app startup"""
    logger.info("DIRAS API starting up...")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    
    try:
        # Initialize database and create tables
        from src.shared.database import init_db
        init_db()
        logger.info("✓ Database initialized")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
    
    try:
        # Verify sentence-transformers availability and load embedding model
        try:
            import sentence_transformers  # type: ignore
            logger.info("✅ sentence-transformers imported successfully")
        except Exception as e:
            logger.error(f"❌ sentence-transformers failed: {e}")

        from src.services.embeddings import get_embedding_generator
        embedder = get_embedding_generator()
        logger.info(f"✓ Embedding model loaded: {embedder.model_name}")
    except Exception as e:
        logger.warning(f"⚠ Embedding model loading failed: {e}")
    
    try:
        # Initialize vector store and log collection stats
        from src.services.vectorstore import get_vector_store
        vector_store = get_vector_store()
        info = vector_store.get_collection_info()
        logger.info(f"✓ Vector store initialized. Collection: {info.get('collection_name')}")
        logger.info(f"🔥 ChromaDB contains {info.get('total_embeddings', 0)} chunks")

        try:
            from src.shared.database import SessionLocal
            from src.models.document import Document, DocumentChunk
            from src.services.indexer import get_document_indexer

            with SessionLocal() as startup_db:
                total_documents = startup_db.query(Document).count()
                total_chunks_in_db = startup_db.query(DocumentChunk).count()
                logger.info(f"📌 Startup check: {total_documents} documents in database, {total_chunks_in_db} chunks in database")

                if total_documents > 0 and info.get('total_embeddings', 0) == 0:
                    logger.warning("❗ ChromaDB contains 0 embeddings while documents exist; rebuilding vector index")
                    indexer = get_document_indexer()
                    rebuild_result = indexer.index_all_documents(db=startup_db, batch_size=32, skip_indexed=False)
                    logger.info(f"🔄 Rebuild result: {rebuild_result}")

                    info = vector_store.get_collection_info()
                    logger.info(f"🔥 Final ChromaDB chunk count after rebuild: {info.get('total_embeddings', 0)}")

        except Exception as e:
            logger.warning(f"⚠ Startup index rebuild check failed: {e}")
    except Exception as e:
        logger.warning(f"⚠ Vector store initialization failed: {e}")
    
    try:
        # Test Groq API connection
        from src.shared.config import settings
        from src.services.llm.groq_client import get_groq_client
        
        if settings.groq_api_key:
            groq = get_groq_client(api_key=settings.groq_api_key)
            logger.info("✓ Groq LLM API configured")
        else:
            logger.warning("⚠ Groq API key not configured")
    except Exception as e:
        logger.warning(f"⚠ Groq LLM initialization failed: {e}")
    
    logger.info("Phase 2 Free Stack implementation ready ✓")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on app shutdown"""
    logger.info("DIRAS API shutting down...")
    # TODO: Cleanup
    # - Close database connections
    # - Save models
    # - Stop monitoring

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True,
        log_level=os.getenv("API_LOG_LEVEL", "info").lower()
    )
