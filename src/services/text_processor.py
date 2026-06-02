"""
Text Processing Service
Handles text chunking, preprocessing, and normalization
"""

import logging
from typing import List, Tuple
import re
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class TextProcessor:
    """
    Processes text: chunking, cleaning, normalization
    Prepares text for embedding generation
    """

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 100, strategy: str = "semantic"):
        """
        Initialize text processor

        Args:
            chunk_size: Number of tokens per chunk (approximately)
            chunk_overlap: Number of overlapping tokens between chunks
            strategy: Chunking strategy - "simple", "semantic", or "paragraph"
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.strategy = strategy
        
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load spaCy model: {e}. Will use regex tokenization.")
            self.nlp = None
        
        # Semantic keywords for document analysis
        self.semantic_keywords = {
            'budget', 'allocation', 'expenditure', 'strategy', 'policy',
            'framework', 'deployment', 'modernization', 'capability'
        }
        
        logger.info(f"TextProcessor initialized (chunk_size={chunk_size}, overlap={chunk_overlap}, strategy={strategy})")

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text

        Args:
            text: Raw text to clean

        Returns:
            Cleaned text
        """
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters but keep sentences intact
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([.!?,;:])', r'\1', text)
        
        return text

    def tokenize_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences

        Args:
            text: Text to tokenize

        Returns:
            List of sentences
        """
        
        if self.nlp:
            doc = self.nlp(text[:1000000])  # Limit to avoid memory issues
            return [sent.text.strip() for sent in doc.sents]
        else:
            # Fallback: regex-based sentence splitting
            sentences = re.split(r'[.!?]+', text)
            return [s.strip() for s in sentences if s.strip()]

    def chunk_document(
        self,
        text: str,
        document_id: int = None,
        db: Session = None,
        document_type: str = None
    ) -> List[Tuple[str, int]]:
        """
        Split document into chunks for embedding with semantic awareness

        Args:
            text: Document text to chunk
            document_id: ID of document being chunked
            db: SQLAlchemy session for storing chunks
            document_type: Type of document (affects chunking strategy)

        Returns:
            List of (chunk_text, chunk_index) tuples
        """
        
        try:
            # Clean text
            text = self.clean_text(text)
            
            # Adapt chunk size based on document type
            chunk_size = self.chunk_size
            chunk_overlap = self.chunk_overlap
            
            if document_type == "policy" or document_type == "report":
                chunk_size = min(self.chunk_size + 256, 1024)
                chunk_overlap = self.chunk_overlap + 50
            elif document_type == "faq" or document_type == "summary":
                chunk_size = max(self.chunk_size - 200, 200)
                chunk_overlap = max(self.chunk_overlap - 50, 20)
            
            # Split into sentences
            sentences = self.tokenize_sentences(text)
            
            logger.info(f"Text split into {len(sentences)} sentences")
            
            # Split by paragraphs for semantic awareness
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            logger.debug(f"Text has {len(paragraphs)} semantic paragraphs")
            
            # Combine sentences into chunks with paragraph awareness
            chunks = []
            current_chunk = []
            current_length = 0
            chunk_index = 0
            
            for para in paragraphs:
                # Split paragraph into sentences
                para_sentences = self.tokenize_sentences(para)
                
                for sentence in para_sentences:
                    sentence_tokens = len(sentence.split()) * 1.3
                    
                    # Check if adding sentence exceeds chunk size
                    if current_length + sentence_tokens > chunk_size and current_chunk:
                        # Save current chunk
                        chunk_text = " ".join(current_chunk)
                        
                        # Verify minimum chunk size
                        min_size = max(50, chunk_size // 4)
                        if len(chunk_text.split()) >= min_size:
                            chunks.append((chunk_text, chunk_index))
                            
                            # Start new chunk with overlap
                            overlap_sentences = []
                            overlap_tokens = 0
                            for s in reversed(current_chunk):
                                s_tokens = len(s.split()) * 1.3
                                if overlap_tokens + s_tokens <= chunk_overlap:
                                    overlap_sentences.insert(0, s)
                                    overlap_tokens += s_tokens
                                else:
                                    break
                            
                            current_chunk = overlap_sentences
                            current_length = overlap_tokens
                            chunk_index += 1
                    
                    # Add sentence to current chunk
                    current_chunk.append(sentence)
                    current_length += sentence_tokens
                
                # After paragraph: prefer to break (preserve paragraph boundaries)
                if current_chunk and current_length > chunk_size * 0.6:
                    chunk_text = " ".join(current_chunk)
                    min_size = max(50, chunk_size // 4)
                    if len(chunk_text.split()) >= min_size:
                        chunks.append((chunk_text, chunk_index))
                        current_chunk = []
                        current_length = 0
                        chunk_index += 1
            
            # Add final chunk
            if current_chunk:
                chunk_text = " ".join(current_chunk)
                min_size = max(50, chunk_size // 4)
                if len(chunk_text.split()) >= min_size:
                    chunks.append((chunk_text, chunk_index))
            
            logger.info(f"Document chunked into {len(chunks)} chunks using {self.strategy} strategy")
            
            # Store chunks in database if session provided
            if db and document_id:
                self._store_chunks_in_db(document_id, chunks, db)
            
            return chunks
            
        except Exception as e:
            logger.error(f"Failed to chunk document: {e}")
            raise

    def _store_chunks_in_db(
        self,
        document_id: int,
        chunks: List[Tuple[str, int]],
        db: Session
    ) -> int:
        """
        Store chunks in database

        Args:
            document_id: ID of parent document
            chunks: List of (chunk_text, chunk_index) tuples
            db: SQLAlchemy session

        Returns:
            Count of stored chunks
        """
        
        try:
            from src.models.document import DocumentChunk
            
            stored_count = 0
            for chunk_text, chunk_index in chunks:
                # Check if chunk already exists
                existing = db.query(DocumentChunk).filter(
                    DocumentChunk.document_id == document_id,
                    DocumentChunk.chunk_index == chunk_index
                ).first()
                
                if existing:
                    continue
                
                # Create new chunk
                chunk = DocumentChunk(
                    document_id=document_id,
                    chunk_text=chunk_text,
                    chunk_index=chunk_index,
                    token_count=len(chunk_text.split())
                )
                
                db.add(chunk)
                stored_count += 1
            
            db.commit()
            logger.info(f"Stored {stored_count} chunks for document {document_id}")
            
            return stored_count
            
        except Exception as e:
            logger.error(f"Failed to store chunks: {e}")
            db.rollback()
            raise

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Estimate token count (roughly: words * 1.3)"""
        return int(len(text.split()) * 1.3)


# Global instance
_processor_instance = None


def get_text_processor(chunk_size: int = 512, chunk_overlap: int = 100, strategy: str = "semantic") -> TextProcessor:
    """Get text processor instance with specified parameters"""
    return TextProcessor(chunk_size, chunk_overlap, strategy)
