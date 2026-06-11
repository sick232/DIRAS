"""Download endpoint for RAG debug Excel log

Provides /api/v1/download-excel which returns the rag_debug_logs.xlsx file
"""
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).resolve().parents[2]
LOG_FILE_PATH = ROOT_DIR / "data" / "generated_answers" / "rag_debug_logs.xlsx"


@router.get("/api/v1/download-excel", summary="Download RAG debug Excel log", response_description="Excel file")
async def download_excel():
    """Return the RAG debug Excel log file.

    Returns 404 if the file does not exist.
    """
    try:
        if not LOG_FILE_PATH.exists():
            logger.warning("Excel file not found: %s", LOG_FILE_PATH)
            return JSONResponse(status_code=404, content={"error": "Excel file not found"})

        return FileResponse(
            path=str(LOG_FILE_PATH),
            filename="rag_debug_logs.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except Exception:
        logger.exception("Unexpected error while serving Excel file")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})
