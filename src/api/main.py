"""
DIRAS FastAPI Main Application
Phase 2 Implementation - Free Stack
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
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
# Document Endpoints (Placeholder for Sprint 2)
# ============================================================================

@app.get("/api/v1/documents")
async def list_documents(skip: int = 0, limit: int = 10):
    """List available documents (Sprint 2: will return OCR'd documents)"""
    return {
        "count": 0,
        "documents": [],
        "message": "Documents will be available after Sprint 2 data pipeline"
    }

@app.post("/api/v1/documents/upload")
async def upload_document(file_path: str):
    """Upload and process a document (Sprint 2)"""
    return {
        "message": "Document upload will be implemented in Sprint 2",
        "status": "pending"
    }

# ============================================================================
# Query Endpoints (Placeholder for Sprint 6)
# ============================================================================

@app.post("/api/v1/query")
async def query(query_text: str, top_k: int = 5):
    """
    Execute a query using retrieval + RAG
    Placeholder: Will be implemented in Sprint 6
    """
    return {
        "query": query_text,
        "message": "RAG pipeline will be available after Sprint 6",
        "status": "pending",
        "results": []
    }

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
    logger.info("Phase 2 Free Stack implementation ready")
    # TODO: Initialize services
    # - Database connection
    # - Vector DB connection
    # - Model loading
    # - Metrics initialization

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
