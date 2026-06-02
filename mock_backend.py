#!/usr/bin/env python3
"""
DIRAS Mock Backend Server
Runs without Docker for frontend testing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import time
from typing import Optional, List

app = FastAPI(title="DIRAS Mock Backend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    document_type: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float
    processing_time: float
    documents_searched: int
    results_count: int
    model_used: str

# Mock data for different queries
MOCK_RESPONSES = {
    "defence": {
        "answer": "Defence is the comprehensive security architecture maintained by nations to protect their territorial integrity, sovereignty, and citizens. It encompasses military strategy, technological advancement, intelligence gathering, and international cooperation.",
        "sources": [
            "Ministry of Defence Annual Report 2025",
            "Parliamentary Standing Committee on Defence",
            "National Security Strategy Document",
            "Defence Research & Development Organisation Report",
            "Armed Forces Policy Review"
        ],
        "confidence": 0.92
    },
    "procurement": {
        "answer": "The latest defence procurement policy emphasizes indigenous manufacturing, technology transfer, and supporting Indian defence industries. Key priorities include: 1) Make in India initiatives, 2) Quality assurance mechanisms, 3) Transparent bidding processes, 4) Supporting startups and MSMEs in defence sector, 5) Accelerated capital acquisition.",
        "sources": [
            "Defence Procurement Policy 2024-25",
            "Department of Defence Production Guidelines",
            "PIB Press Release - March 2026",
            "Parliamentary Committee Report on Defence Procurement",
            "Ministry of Defence Circular"
        ],
        "confidence": 0.88
    },
    "military": {
        "answer": "Recent military developments include modernization of armed forces, induction of advanced surveillance systems, cyber warfare capabilities enhancement, and improved inter-service coordination. Budget allocations prioritize personnel welfare, equipment upgrades, and infrastructure development.",
        "sources": [
            "Armed Forces Modernization Plan",
            "Defence Budget 2026-27 Document",
            "Military Strategy Review",
            "Chief of Defence Staff Briefing",
            "Services Headquarters Reports"
        ],
        "confidence": 0.85
    },
    "expenditure": {
        "answer": "Defence expenditure for FY 2026-27 is allocated at ₹6.5 lakh crores (approximately 2.4% of GDP), up from ₹6.2 lakh crores in FY 2025-26. The allocation covers: Personnel (52%), Modernization (28%), Maintenance & Operations (20%). Major focus areas include indigenization and technology development.",
        "sources": [
            "Union Budget 2026-27 - Defence Allocation",
            "Ministry of Defence Financial Analysis",
            "Parliamentary Budget Committee Report",
            "Economic Survey 2026",
            "Defence Finance Analysis Report"
        ],
        "confidence": 0.94
    },
    "policy": {
        "answer": "Current defence policies prioritize: 1) National Security Strategy integration, 2) Regional balance maintenance, 3) Technological self-sufficiency, 4) Military modernization, 5) Strategic partnerships with allies, 6) Cyber and space domain capabilities, 7) Personnel welfare and readiness.",
        "sources": [
            "National Defence Policy 2024",
            "Strategic Defence Review",
            "Ministry of Defence Policy Circulars",
            "Defence Committee Minutes",
            "Strategic Affairs Division Report"
        ],
        "confidence": 0.89
    },
    "default": {
        "answer": "I can help you with information about defence procurement policies, military strategies, defence expenditure, and related governance matters. Please ask specific questions about these topics to get more detailed answers backed by official documents and reports.",
        "sources": [
            "Ministry of Defence Official Documentation",
            "Parliamentary Committee Reports",
            "Defence Research Organisation Publications",
            "Government of India Circulars",
            "Strategic Studies Institute Reports"
        ],
        "confidence": 0.75
    }
}

def get_mock_response(query: str) -> dict:
    """Get mock response based on query keywords"""
    query_lower = query.lower()
    
    for keyword, response in MOCK_RESPONSES.items():
        if keyword in query_lower:
            return response
    
    return MOCK_RESPONSES["default"]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/api/v1/health")
async def api_health_check():
    """Detailed health check"""
    return {
        "status": "ok",
        "components": {
            "api": "ok",
            "database": "mocked",
            "vector_db": "mocked",
            "search": "mocked"
        }
    }

@app.get("/api/v1/status")
async def status():
    """System status"""
    return {
        "phase": "Phase 2 - Data Pipeline",
        "environment": "development",
        "version": "1.0.0-mock",
        "mode": "mock_backend",
        "capabilities": [
            "document_scraping",
            "ocr_processing",
            "text_preprocessing",
            "classification",
            "ner",
            "embeddings",
            "retrieval",
            "rag"
        ]
    }

@app.post("/api/v1/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    """Main query endpoint - returns mock RAG responses"""
    
    start_time = time.time()
    
    # Get mock response based on query
    mock_data = get_mock_response(req.question)
    
    # Simulate processing time (0.5-2 seconds)
    processing_time = time.time() - start_time + 0.5
    
    return QueryResponse(
        answer=mock_data["answer"],
        sources=mock_data["sources"][:req.top_k],
        confidence=mock_data["confidence"],
        processing_time=processing_time,
        documents_searched=5000,
        results_count=req.top_k,
        model_used="Llama 3 (Mocked)"
    )

@app.get("/api/v1/documents")
async def list_documents(skip: int = 0, limit: int = 10):
    """List documents"""
    return {
        "documents": [
            {"id": 1, "title": "Defence Procurement Policy 2024-25", "type": "policy_document"},
            {"id": 2, "title": "Ministry of Defence Annual Report", "type": "report"},
            {"id": 3, "title": "Armed Forces Modernization Plan", "type": "strategic_plan"},
            {"id": 4, "title": "Parliamentary Committee Recommendations", "type": "parliamentary_report"},
            {"id": 5, "title": "Defence Budget Analysis", "type": "financial_report"},
        ],
        "total": 5000,
        "skip": skip,
        "limit": limit
    }

@app.post("/api/v1/classify")
async def classify_document(document_id: int, text: str):
    """Mock classification endpoint"""
    return {
        "document_id": document_id,
        "classification": "policy_document",
        "confidence": 0.87
    }

@app.post("/api/v1/extract-entities")
async def extract_entities(text: str):
    """Mock NER endpoint"""
    return {
        "entities": [
            {"text": "Ministry of Defence", "label": "ORGANIZATION"},
            {"text": "Defence Procurement Policy", "label": "DOCUMENT"},
            {"text": "2024-25", "label": "DATE"}
        ]
    }

@app.get("/api/v1/metrics")
async def get_metrics():
    """System metrics"""
    return {
        "requests_total": 1234,
        "requests_processed": 1200,
        "errors": 34,
        "average_latency_ms": 850,
        "model": "Llama 3",
        "uptime_hours": 24.5
    }

if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║     DIRAS Mock Backend Server Starting...             ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("\n✓ No Docker required!")
    print("✓ Frontend testing enabled!")
    print("\n📊 API Endpoints:")
    print("  • GET  http://localhost:8000/health")
    print("  • GET  http://localhost:8000/api/v1/health")
    print("  • GET  http://localhost:8000/api/v1/status")
    print("  • POST http://localhost:8000/api/v1/query")
    print("  • GET  http://localhost:8000/api/v1/documents")
    print("  • GET  http://localhost:8000/api/v1/metrics")
    print("\n🔗 Frontend: http://localhost:3000")
    print("\n✨ Press Ctrl+C to stop\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
