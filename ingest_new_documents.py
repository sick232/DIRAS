#!/usr/bin/env python3
"""
PDF Document Ingestion Pipeline
Scans documents folder for PDFs, detects new/modified files, and indexes them to ChromaDB
Reuses existing architecture: TextProcessor, EmbeddingGenerator, VectorStore, DocumentIndexer
"""

import logging
import json
import hashlib
import time
from pathlib import Path
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import os
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.orm import Session
from src.shared.database import SessionLocal, init_db
from src.models.document import Document, DocumentChunk, IndexingLog
from src.services.text_processor import get_text_processor
from src.services.embeddings import get_embedding_generator
from src.services.vectorstore import get_vector_store


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PDFExtractor:
    """Extract text from PDF files with multiple methods"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_text_with_pypdf(self, pdf_path: str) -> Tuple[str, bool]:
        """Extract text using PyPDF2 (simple, fast)"""
        try:
            try:
                import PyPDF2
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page_num, page in enumerate(reader.pages, 1):
                        text += f"\n--- Page {page_num} ---\n"
                        text += page.extract_text()
                    return text, len(reader.pages) > 0
            except ImportError:
                # Try pypdf as alternative (newer package)
                import pypdf
                with open(pdf_path, 'rb') as file:
                    reader = pypdf.PdfReader(file)
                    text = ""
                    for page_num, page in enumerate(reader.pages, 1):
                        text += f"\n--- Page {page_num} ---\n"
                        text += page.extract_text()
                    return text, len(reader.pages) > 0
        except Exception as e:
            self.logger.warning(f"PyPDF extraction failed for {pdf_path}: {e}")
            return None, False
    
    def extract_text_with_ocr(self, pdf_path: str) -> Tuple[str, bool]:
        """Extract text using OCR Pipeline (slower, better for scanned PDFs)"""
        try:
            import importlib
            ocr_module = importlib.import_module('src.01-data-pipeline.ocr')
            OCRPipeline = ocr_module.OCRPipeline
            
            ocr_pipeline = OCRPipeline(languages=['en', 'hi'], use_gpu=False, batch_size=4)
            result = ocr_pipeline.process_pdf(pdf_path)
            
            if result.get('success'):
                text = result.get('full_text', '')
                total_pages = result.get('total_pages', 0)
                self.logger.info(f"OCR extraction successful for {pdf_path}: {total_pages} pages")
                return text, total_pages > 0
            else:
                self.logger.warning(f"OCR extraction failed for {pdf_path}: {result.get('error')}")
                return None, False
        except Exception as e:
            self.logger.warning(f"OCR extraction failed for {pdf_path}: {e}")
            return None, False
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF using best available method"""
        self.logger.info(f"Extracting text from {pdf_path}...")
        
        # Try PyPDF first (fast)
        text, success = self.extract_text_with_pypdf(pdf_path)
        if success and text and len(text.strip()) > 100:
            self.logger.info(f"✓ PyPDF extraction successful ({len(text)} chars)")
            return text
        
        # Fall back to OCR (slower, better for scanned PDFs)
        self.logger.info(f"PyPDF insufficient, trying OCR extraction...")
        text, success = self.extract_text_with_ocr(pdf_path)
        if success and text and len(text.strip()) > 100:
            self.logger.info(f"✓ OCR extraction successful ({len(text)} chars)")
            return text
        
        # Last resort: return minimal text
        if text and len(text.strip()) > 10:
            self.logger.warning(f"Using partial extraction ({len(text)} chars)")
            return text
        
        logger.error(f"✗ Failed to extract text from {pdf_path}")
        return None


class FileHashTracker:
    """Track file changes using content hashing"""
    
    TRACKER_FILE = "data/ingest_tracker.json"
    
    @staticmethod
    def compute_hash(file_path: str) -> str:
        """Compute SHA256 hash of file content"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    @staticmethod
    def load_tracker() -> Dict[str, Dict]:
        """Load existing file tracker"""
        tracker_path = Path(FileHashTracker.TRACKER_FILE)
        if tracker_path.exists():
            try:
                with open(tracker_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load tracker: {e}")
                return {}
        return {}
    
    @staticmethod
    def save_tracker(tracker: Dict):
        """Save file tracker to disk"""
        tracker_path = Path(FileHashTracker.TRACKER_FILE)
        tracker_path.parent.mkdir(parents=True, exist_ok=True)
        with open(tracker_path, 'w') as f:
            json.dump(tracker, f, indent=2)
    
    @staticmethod
    def has_changed(file_path: str, tracker: Dict) -> bool:
        """Check if file is new or has been modified"""
        current_hash = FileHashTracker.compute_hash(file_path)
        file_key = str(file_path)
        
        if file_key not in tracker:
            return True  # New file
        
        stored_hash = tracker[file_key].get('hash')
        return current_hash != stored_hash


class DocumentIngester:
    """Main ingestion pipeline"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.documents_dir = Path("documents")
        self.pdf_extractor = PDFExtractor()
        self.text_processor = get_text_processor(
            chunk_size=512,
            chunk_overlap=100,
            strategy="semantic"
        )
        self.embedding_generator = get_embedding_generator()
        self.vector_store = get_vector_store()
        
        # Create tables if needed
        try:
            init_db()
        except Exception as e:
            self.logger.warning(f"Database initialization may have failed: {e}")
    
    def get_document_type_from_filename(self, filename: str) -> str:
        """Infer document type from filename"""
        filename_lower = filename.lower()
        
        if 'procurement' in filename_lower or 'purchase' in filename_lower or 'rfp' in filename_lower:
            return 'procurement'
        elif 'policy' in filename_lower or 'policy' in filename_lower:
            return 'policy'
        elif 'delegation' in filename_lower or 'financial' in filename_lower:
            return 'financial_policy'
        elif 'consultant' in filename_lower or 'services' in filename_lower:
            return 'professional_services'
        elif 'manual' in filename_lower:
            return 'manual'
        elif 'standardisation' in filename_lower or 'standardization' in filename_lower:
            return 'standardization'
        elif 'drdo' in filename_lower:
            return 'drdo_procurement'
        elif 'handbook' in filename_lower:
            return 'handbook'
        elif 'guidelines' in filename_lower or 'dap' in filename_lower:
            return 'guidelines'
        elif 'approval' in filename_lower or 'committee' in filename_lower:
            return 'approval_workflow'
        elif 'contract' in filename_lower or 'vendor' in filename_lower:
            return 'contract_vendor'
        else:
            return 'policy_document'

    def extract_document_tags(self, text: str, filename: str) -> List[str]:
        """Extract key procurement and policy tags from document text and filename"""
        text_lower = text.lower()
        filename_lower = filename.lower()
        tags = set()

        keywords = [
            'procurement', 'purchase', 'rfp', 'tender', 'quotation',
            'competitive bidding', 'single-source', 'sole-source',
            'direct buy', 'approval', 'committee', 'authority',
            'delegation', 'vendor', 'consultant', 'services',
            'professional services', 'capex', 'revenue expenditure',
            'sustainable procurement', 'green procurement', 'eco-friendly',
            'budget', 'financial limit', 'purchase order', 'po',
            'price threshold', 'approval threshold', 'contract',
            'laboratory equipment', 'project alpha', 'lab director',
            'r&d', 'defence', 'mod', 'drdo'
        ]

        for keyword in keywords:
            if keyword in text_lower or keyword in filename_lower:
                tags.add(keyword.replace(' ', '_'))

        acronyms = ['drdo', 'dpsu', 'mod', 'rfp', 'aon', 'dpp', 'dac']
        for acronym in acronyms:
            if acronym in text_lower or acronym in filename_lower:
                tags.add(acronym)

        return sorted(tags)

    def scan_documents_folder(self) -> List[Path]:
        """Scan documents folder for PDF files"""
        if not self.documents_dir.exists():
            self.logger.warning(f"Documents directory not found: {self.documents_dir}")
            return []
        
        pdf_files = list(self.documents_dir.glob("*.pdf"))
        self.logger.info(f"📁 Found {len(pdf_files)} PDF files in {self.documents_dir}")
        return sorted(pdf_files)
    
    def ingest_document(
        self,
        pdf_path: Path,
        db: Session,
        tracker: Dict
    ) -> Dict:
        """Ingest a single PDF document"""
        
        result = {
            'file': str(pdf_path),
            'status': 'failed',
            'document_id': None,
            'chunks_created': 0,
            'embeddings_generated': 0,
            'error': None,
            'duration': 0
        }
        
        start_time = time.time()
        
        try:
            filename = pdf_path.name
            
            # Check if already indexed
            existing = db.query(Document).filter(
                Document.source_url == str(pdf_path)
            ).first()
            
            if existing:
                self.logger.info(f"  ⊘ {filename} already indexed (ID: {existing.id})")
                result['status'] = 'skipped'
                result['document_id'] = existing.id
                return result
            
            # Extract text from PDF
            text = self.pdf_extractor.extract_text(str(pdf_path))
            if not text:
                result['error'] = 'Failed to extract text from PDF'
                return result
            
            self.logger.info(f"  ✓ Text extracted ({len(text)} chars)")
            
            # Create Document record
            doc_type = self.get_document_type_from_filename(filename)
            tags = self.extract_document_tags(text, filename)
            document = Document(
                title=filename.replace('.pdf', ''),
                source_url=str(pdf_path),
                source_type='pdf_file',
                document_type=doc_type,
                content_raw=text,
                content_processed=text,
                status='ocr_complete',
                ocr_confidence=0.95,
                is_indexed=False,
                doc_metadata={
                    'source': 'local_pdf',
                    'filename': filename,
                    'file_size': pdf_path.stat().st_size,
                    'ingestion_source': 'ingest_new_documents.py',
                    'ingested_at': datetime.utcnow().isoformat(),
                    'tags': tags
                }
            )
            
            db.add(document)
            db.flush()
            document_id = document.id
            result['document_id'] = document_id
            
            self.logger.info(f"  ✓ Document created (ID: {document_id}, type: {doc_type}, tags: {tags})")
            
            # Chunk the document
            chunks = self.text_processor.chunk_document(
                text,
                document_id=document_id,
                db=db,
                document_type=doc_type
            )
            
            result['chunks_created'] = len(chunks)
            self.logger.info(f"  ✓ Document chunked into {len(chunks)} chunks")
            
            # Get chunks from database
            db_chunks = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document_id
            ).all()

            result['chunks_created'] = len(db_chunks)

            # NOTE: Using BM25 retrieval. We persist chunks and metadata to the DB.
            # Skip embedding generation and ChromaDB storage to reduce memory and avoid Chroma dependency.
            document.is_indexed = True
            for chunk in db_chunks:
                chunk.is_indexed = True

            db.commit()
            
            # Update tracker
            file_hash = FileHashTracker.compute_hash(str(pdf_path))
            tracker[str(pdf_path)] = {
                'hash': file_hash,
                'document_id': document_id,
                'ingested_at': datetime.utcnow().isoformat()
            }
            
            result['status'] = 'success'
            result['duration'] = time.time() - start_time
            
            self.logger.info(f"  ✅ {filename} indexed successfully in {result['duration']:.2f}s")
            
            return result
            
        except Exception as e:
            self.logger.error(f"  ✗ Error ingesting {pdf_path}: {str(e)}", exc_info=True)
            db.rollback()
            result['error'] = str(e)
            result['duration'] = time.time() - start_time
            return result
    
    def ingest_all(self):
        """Ingest all new/modified PDFs"""
        
        self.logger.info("="*70)
        self.logger.info("PDF DOCUMENT INGESTION PIPELINE")
        self.logger.info("="*70)
        
        # Load file tracker
        tracker = FileHashTracker.load_tracker()
        self.logger.info(f"📊 Loaded tracker with {len(tracker)} previously indexed files")
        
        # Scan documents folder
        pdf_files = self.scan_documents_folder()
        if not pdf_files:
            self.logger.info("No PDF files found in documents folder")
            return
        
        # Filter for new/modified files
        files_to_process = []
        for pdf_path in pdf_files:
            if FileHashTracker.has_changed(str(pdf_path), tracker):
                files_to_process.append(pdf_path)
        
        self.logger.info(f"📝 {len(files_to_process)} new/modified files to process")
        if not files_to_process:
            self.logger.info("✓ All documents already indexed")
            return
        
        # Process each file
        stats = {
            'total': len(files_to_process),
            'successful': 0,
            'skipped': 0,
            'failed': 0,
            'total_chunks': 0,
            'total_embeddings': 0,
            'duration': 0
        }
        
        start_time = time.time()
        results = []
        
        db = SessionLocal()
        try:
            for idx, pdf_path in enumerate(files_to_process, 1):
                self.logger.info(f"\n[{idx}/{len(files_to_process)}] Processing: {pdf_path.name}")
                
                result = self.ingest_document(pdf_path, db, tracker)
                results.append(result)
                
                if result['status'] == 'success':
                    stats['successful'] += 1
                    stats['total_chunks'] += result['chunks_created']
                    stats['total_embeddings'] += result['embeddings_generated']
                elif result['status'] == 'skipped':
                    stats['skipped'] += 1
                else:
                    stats['failed'] += 1
            
            # Save updated tracker
            FileHashTracker.save_tracker(tracker)
            self.logger.info(f"✓ Tracker saved with {len(tracker)} files")
            
        finally:
            db.close()
        
        stats['duration'] = time.time() - start_time
        
        # Print summary
        self.logger.info("\n" + "="*70)
        self.logger.info("INGESTION SUMMARY")
        self.logger.info("="*70)
        self.logger.info(f"📋 Files Processed:    {stats['successful']} successful, {stats['skipped']} skipped, {stats['failed']} failed")
        self.logger.info(f"✂️  Total Chunks:       {stats['total_chunks']}")
        self.logger.info(f"🧠 Total Embeddings:   {stats['total_embeddings']}")
        self.logger.info(f"⏱️  Duration:           {stats['duration']:.2f}s")
        self.logger.info("="*70)
        
        # Log individual results
        if results:
            self.logger.info("\n📑 DETAILED RESULTS:")
            for result in results:
                status_icon = "✅" if result['status'] == 'success' else "⊘" if result['status'] == 'skipped' else "✗"
                self.logger.info(f"  {status_icon} {Path(result['file']).name}")
                if result['status'] == 'success':
                    self.logger.info(f"     ID: {result['document_id']}, Chunks: {result['chunks_created']}, Duration: {result['duration']:.2f}s")
                elif result['error']:
                    self.logger.info(f"     Error: {result['error']}")
        
        return stats


def verify_ingestion():
    """Verify ingestion by building/loading BM25 index and performing a sample query."""
    logger.info("\n" + "="*70)
    logger.info("VERIFICATION: Building/Checking BM25 index")
    logger.info("="*70)

    try:
        # Build BM25 index from DB and run a sample query
        from rank_bm25 import BM25Okapi
        import pickle
        import json

        from src.shared.database import SessionLocal
        from src.models.document import DocumentChunk, Document

        session = SessionLocal()
        try:
            chunks = session.query(DocumentChunk).join(Document).all()
            if not chunks:
                logger.warning("No chunks found in database to build BM25 index")
                return

            corpus = [c.chunk_text for c in chunks]
            tokenized = [re.findall(r"\w+", t.lower()) for t in corpus]

            bm25 = BM25Okapi(tokenized)

            # Persist BM25 and metadata
            bm25_dir = Path("data/bm25")
            bm25_dir.mkdir(parents=True, exist_ok=True)

            with open(bm25_dir / "bm25_index.pkl", "wb") as f:
                pickle.dump(bm25, f)

            # Save chunk metadata (ids and texts)
            chunks_meta = [
                {
                    "chunk_id": c.id,
                    "document_id": c.document_id,
                    "title": c.document.title if c.document else None,
                    "document_type": c.document.document_type if c.document else None,
                    "text": c.chunk_text,
                    "source_url": c.document.source_url if c.document else None
                }
                for c in chunks
            ]
            with open(bm25_dir / "chunks.json", "w", encoding="utf-8") as f:
                json.dump(chunks_meta, f, ensure_ascii=False, indent=2)

            logger.info(f"✓ BM25 index built and saved ({len(corpus)} chunks)")

            # Sample query
            sample_query = "defence procurement manual"
            q_tokens = re.findall(r"\w+", sample_query.lower())
            scores = bm25.get_scores(q_tokens)
            top_idxs = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:3]

            logger.info("Sample BM25 results:")
            for i in top_idxs:
                meta = chunks_meta[i]
                logger.info(f"  - Chunk {meta['chunk_id']} (doc {meta['document_id']}): {meta['text'][:150]}...")

        finally:
            session.close()

    except Exception as e:
        logger.error(f"Verification (BM25) failed: {e}", exc_info=True)


def main():
    """Main entry point"""
    try:
        ingester = DocumentIngester()
        ingester.ingest_all()
        
        # Verify ingestion
        verify_ingestion()
        
        logger.info("\n✅ Ingestion pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
