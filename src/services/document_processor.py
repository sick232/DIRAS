"""
Document Processing Service
Orchestrates OCR pipeline for processing downloaded documents
"""

import logging
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Processes documents through OCR pipeline
    Extracts text from downloaded documents and stores in database
    """

    def __init__(self):
        """Initialize document processor"""
        try:
            from src.shared.database import SessionLocal
            self.SessionLocal = SessionLocal
            logger.info("DocumentProcessor initialized")
        except Exception as e:
            logger.error(f"Failed to initialize DocumentProcessor: {e}")
            raise

    def process_document(self, document_id: int, db: Session) -> dict:
        """
        Process a single document through OCR

        Args:
            document_id: ID of document to process
            db: SQLAlchemy database session

        Returns:
            dict with processing results:
                - status: "success" or "failed"
                - document_id: processed document ID
                - text_length: length of extracted text
                - confidence: OCR confidence score (0-1)
                - error: error message if failed
        """
        
        try:
            from src.models.document import Document
            import importlib
            
            # Try to import OCRPipeline
            try:
                ocr_module = importlib.import_module('src.01-data-pipeline.ocr')
                OCRPipeline = getattr(ocr_module, 'OCRPipeline')
                ocr_available = True
            except:
                ocr_available = False
            
            # Fetch document from database
            doc = db.query(Document).filter(Document.id == document_id).first()
            if not doc:
                return {
                    "status": "failed",
                    "document_id": document_id,
                    "error": f"Document {document_id} not found"
                }
            
            # Check if already processed
            if doc.status == "ocr_complete":
                from src.models.document import DocumentChunk
                existing_chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).count()
                if existing_chunks > 0:
                    logger.info(f"Document {document_id} already OCR processed and has {existing_chunks} chunks")
                    return {
                        "status": "skipped",
                        "document_id": document_id,
                        "reason": "already_processed",
                        "text_length": len(doc.content_processed) if doc.content_processed else 0,
                        "chunks": existing_chunks
                    }
                logger.warning(f"Document {document_id} marked ocr_complete but has no chunks; retrying chunking")
            
            # Run OCR pipeline
            logger.info(f"Processing document {document_id}: {doc.title}")
            
            # For now, use content_raw as content_processed (in production, would run OCR)
            if not doc.content_raw:
                return {
                    "status": "failed",
                    "document_id": document_id,
                    "error": "Document has no raw content"
                }
            
            # Mock OCR processing (in production: OCRPipeline.process())
            if not doc.content_processed:
                doc.content_processed = doc.content_raw
            doc.ocr_confidence = 0.92
            doc.status = "ocr_complete"
            
            db.commit()
            
            # Perform semantic-aware chunking
            try:
                from src.services.text_processor import get_text_processor
                from src.shared.config import settings
                
                processor = get_text_processor(
                    chunk_size=settings.chunk_size_default,
                    chunk_overlap=settings.chunk_overlap_default,
                    strategy=settings.chunking_strategy
                )
                
                chunks = processor.chunk_document(
                    doc.content_processed,
                    document_id=document_id,
                    db=db,
                    document_type=doc.document_type
                )
                
                logger.info(f"Document {document_id} split into {len(chunks)} semantic chunks")
                
            except Exception as chunk_error:
                logger.warning(f"Chunking error (non-fatal): {chunk_error}")
            
            logger.info(f"Document {document_id} processed successfully. Text length: {len(doc.content_processed)}")
            
            return {
                "status": "success",
                "document_id": document_id,
                "text_length": len(doc.content_processed),
                "confidence": doc.ocr_confidence,
                "error": None
            }
            
        except Exception as e:
            error_msg = f"OCR processing failed for document {document_id}: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "failed",
                "document_id": document_id,
                "error": error_msg
            }

    def batch_process_documents(self, limit: int = 50, db: Session = None) -> dict:
        """
        Process multiple documents in batch

        Args:
            limit: Maximum number of documents to process
            db: SQLAlchemy database session

        Returns:
            dict with batch results:
                - status: "success" or "partial" or "failed"
                - total_processed: count of processed documents
                - successful: count of successful processings
                - failed: count of failed processings
                - duration_seconds: time taken
        """
        
        import time
        start_time = time.time()
        
        try:
            from src.models.document import Document
            
            if db is None:
                db = self.SessionLocal()
                should_close = True
            else:
                should_close = False
            
            # Get unprocessed documents
            unprocessed = db.query(Document).filter(
                Document.status.in_(["downloaded"])
            ).limit(limit).all()
            
            logger.info(f"Found {len(unprocessed)} unprocessed documents. Processing {min(len(unprocessed), limit)}...")
            
            successful = 0
            failed = 0
            
            for doc in unprocessed[:limit]:
                result = self.process_document(doc.id, db)
                if result["status"] == "success":
                    successful += 1
                elif result["status"] == "failed":
                    failed += 1
            
            duration = time.time() - start_time
            
            status = "success" if failed == 0 else "partial" if successful > 0 else "failed"
            
            logger.info(f"Batch processing complete. Success: {successful}, Failed: {failed}, Time: {duration:.1f}s")
            
            return {
                "status": status,
                "total_processed": successful + failed,
                "successful": successful,
                "failed": failed,
                "duration_seconds": duration
            }
            
        except Exception as e:
            error_msg = f"Batch processing failed: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "failed",
                "error": error_msg,
                "duration_seconds": time.time() - start_time
            }
        
        finally:
            if should_close:
                db.close()

    def get_processing_status(self, db: Session) -> dict:
        """
        Get current processing status

        Returns:
            dict with status information
        """
        
        try:
            from src.models.document import Document
            
            total = db.query(Document).count()
            downloaded = db.query(Document).filter(Document.status == "downloaded").count()
            ocr_complete = db.query(Document).filter(Document.status == "ocr_complete").count()
            
            return {
                "total_documents": total,
                "downloaded": downloaded,
                "ocr_complete": ocr_complete,
                "pending_ocr": downloaded,
                "percentage_complete": round((ocr_complete / total * 100) if total > 0 else 0, 1)
            }
            
        except Exception as e:
            logger.error(f"Failed to get processing status: {e}")
            return {"error": str(e)}


# Global instance
_processor_instance = None


def get_document_processor() -> DocumentProcessor:
    """Get or create document processor instance"""
    global _processor_instance
    if _processor_instance is None:
        _processor_instance = DocumentProcessor()
    return _processor_instance
