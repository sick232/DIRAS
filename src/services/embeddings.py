"""
Embeddings Service
Generates semantic embeddings for text using SentenceTransformers
"""

import logging
from typing import List, Union
import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """
    Generates embeddings using SentenceTransformers
    Converts text to 384-dimensional vectors
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding generator

        Args:
            model_name: HuggingFace model name (default: all-MiniLM-L6-v2)
        """
        
        try:
            from sentence_transformers import SentenceTransformer
            
            logger.info(f"Loading embedding model: {model_name}")
            self.model = SentenceTransformer(model_name)
            self.model_name = model_name
            
            logger.info(f"Model loaded successfully. Vector dimension: {self.model.get_sentence_embedding_dimension()}")
            
        except ImportError:
            raise ImportError("sentence-transformers not installed. Install with: pip install sentence-transformers")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text

        Args:
            text: Text to embed

        Returns:
            Embedding vector (384-dim)
        """
        
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for embedding")
                return [0.0] * 384  # Return zero vector for empty text
            
            # Generate embedding
            embedding = self.model.encode(text, convert_to_numpy=True)
            
            # Convert to list if numpy array or tensor
            if hasattr(embedding, 'tolist'):  # Works for numpy arrays and torch tensors
                embedding = embedding.tolist()
            elif isinstance(embedding, (list, tuple)):
                embedding = list(embedding)
            
            return embedding
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise

    def embed_batch(
        self,
        texts: List[str],
        batch_size: int = 32,
        show_progress: bool = False
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch

        Args:
            texts: List of texts to embed
            batch_size: Batch size for processing
            show_progress: Whether to show progress bar

        Returns:
            List of embedding vectors
        """
        
        try:
            logger.info(f"Generating embeddings for {len(texts)} texts with batch size {batch_size}...")
            
            # Generate embeddings in batches
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                convert_to_numpy=True,
                show_progress_bar=show_progress
            )
            
            # Convert to list of lists if numpy array
            embeddings_list = []
            if isinstance(embeddings, np.ndarray):
                embeddings_list = embeddings.tolist()
            else:
                # Handle tensor or other types
                embeddings_list = [emb.tolist() if hasattr(emb, 'tolist') else list(emb) for emb in embeddings]
            
            logger.info(f"Generated {len(embeddings_list)} embeddings")
            
            return embeddings_list
            
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise

    def embed_documents_from_db(
        self,
        db: object = None,
        batch_size: int = 32,
        limit: int = None
    ) -> List[tuple]:
        """
        Generate embeddings for unindexed documents in database

        Args:
            db: SQLAlchemy database session
            batch_size: Batch size for processing
            limit: Maximum number of chunks to process

        Returns:
            List of (chunk_id, embedding) tuples
        """
        
        try:
            from src.models.document import DocumentChunk, Embedding
            
            logger.info(f"Fetching unindexed chunks from database...")
            
            # Get unindexed chunks
            query = db.query(DocumentChunk).filter(
                ~DocumentChunk.embedding.any()
            )
            
            if limit:
                query = query.limit(limit)
            
            chunks = query.all()
            logger.info(f"Found {len(chunks)} unindexed chunks")
            
            if not chunks:
                return []
            
            # Extract texts and chunk IDs
            chunk_ids = [f"chunk_{chunk.id}" for chunk in chunks]
            texts = [chunk.chunk_text for chunk in chunks]
            
            # Generate embeddings
            embeddings = self.embed_batch(texts, batch_size=batch_size)
            
            # Store embeddings in database
            logger.info(f"Storing {len(embeddings)} embeddings in database...")
            
            results = []
            for chunk, chunk_id, embedding in zip(chunks, chunk_ids, embeddings):
                # Create embedding record
                emb = Embedding(
                    chunk_id=chunk.id,
                    vector=embedding,
                    model_name=self.model_name
                )
                
                db.add(emb)
                results.append((chunk_id, embedding))
            
            db.commit()
            logger.info(f"Stored {len(results)} embeddings in database")
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to embed documents: {e}")
            db.rollback()
            raise

    @staticmethod
    def embedding_dimension() -> int:
        """Get the dimension of embeddings (always 384 for all-MiniLM-L6-v2)"""
        return 384


# Global instance
_embedder_instance = None


def get_embedding_generator(model_name: str = "all-MiniLM-L6-v2") -> EmbeddingGenerator:
    """Get or create embedding generator instance"""
    global _embedder_instance
    
    if _embedder_instance is None:
        _embedder_instance = EmbeddingGenerator(model_name)
    
    return _embedder_instance
