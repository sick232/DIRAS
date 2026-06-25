"""
Vector Store Service
Manages ChromaDB for storing and retrieving document embeddings
"""

import logging
from typing import List, Dict, Optional, Tuple
import json
import os
import shutil
import asyncio
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor, TimeoutError

logger = logging.getLogger(__name__)


class VectorStore:
    """
    ChromaDB vector store wrapper
    Handles embedding storage and semantic search
    """

    def __init__(self, persist_directory: str = "data/vectorstore", collection_name: str = "diras_documents"):
        """
        Initialize ChromaDB vector store

        Args:
            persist_directory: Directory for persistent storage
            collection_name: Name of ChromaDB collection
        """
        
        try:
            import chromadb
            from chromadb.config import Settings as ChromaSettings
            
            # Disable anonymous telemetry in environments like Railway
            chroma_settings = ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True,
                is_persistent=True
            )
            
            # Initialize client using new PersistentClient API (v1.5.x+)
            self.client = chromadb.PersistentClient(path=persist_directory, settings=chroma_settings)
            self.collection_name = collection_name
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"ChromaDB vector store initialized. Collection: {collection_name}, Path: {persist_directory}")
            
            # Note: We now use SQLite for search via numpy, not ChromaDB
            # These fields kept for backward compatibility but not actively used for search
            self._embedding_cache = {}
            self._document_cache = {}
            self._cache_loaded = True  # Mark as ready since we use SQLite directly
            
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            self.collection = None
            self._embedding_cache = {}
            self._document_cache = {}
            self._cache_loaded = True
    
    def _load_cache_async(self):
        """Load embeddings into memory cache for faster searching"""
        try:
            if not self.collection:
                logger.info("No collection available for caching")
                self._cache_loaded = True
                return
            
            # Wrap ChromaDB get() in timeout to prevent hanging
            def get_all_docs():
                return self.collection.get(include=["embeddings", "documents", "metadatas"])
            
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(get_all_docs)
                try:
                    all_docs = future.result(timeout=5)
                except TimeoutError:
                    logger.warning("ChromaDB get() timed out during cache load")
                    self._cache_loaded = True
                    return
            
            if not all_docs or not all_docs.get("ids"):
                logger.info("No documents in collection for caching")
                self._cache_loaded = True
                return
            
            # Build cache
            embeddings_list = all_docs.get("embeddings") or []
            documents_list = all_docs.get("documents") or []
            metadatas_list = all_docs.get("metadatas") or []
            
            for i, doc_id in enumerate(all_docs["ids"]):
                embedding = embeddings_list[i] if i < len(embeddings_list) else None
                document = documents_list[i] if i < len(documents_list) else ""
                metadata = metadatas_list[i] if i < len(metadatas_list) else {}
                
                if embedding and len(embedding) > 0:
                    self._embedding_cache[doc_id] = np.array(embedding, dtype=np.float32)
                    self._document_cache[doc_id] = {
                        "document": document,
                        "metadata": metadata,
                        "id": doc_id
                    }
            
            logger.info(f"✓ Loaded {len(self._embedding_cache)} embeddings into memory cache")
            self._cache_loaded = True
            
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")
            self._cache_loaded = True
            
        except ImportError:
            raise ImportError("ChromaDB not installed. Install with: pip install chromadb")
        except Exception as e:
            if "no such column: collections.topic" in str(e):
                logger.warning("ChromaDB schema mismatch detected; rebuilding vector store persistence")
                shutil.rmtree(persist_directory, ignore_errors=True)
                os.makedirs(persist_directory, exist_ok=True)

                chroma_settings = ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True,
                    is_persistent=True
                )
                self.client = chromadb.PersistentClient(path=persist_directory, settings=chroma_settings)
                self.collection_name = collection_name
                self.collection = self.client.get_or_create_collection(
                    name=collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
                logger.info(f"ChromaDB vector store rebuilt and initialized. Collection: {collection_name}, Path: {persist_directory}")
            else:
                logger.error(f"Failed to initialize ChromaDB: {e}")
                raise

    def add_embeddings(
        self,
        chunk_ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[Dict] = None
    ) -> bool:
        """
        Add embeddings to vector store

        Args:
            chunk_ids: List of unique chunk IDs
            embeddings: List of embedding vectors (384-dim)
            documents: List of chunk texts
            metadatas: Optional list of metadata dicts per chunk

        Returns:
            True if successful, False otherwise
        """
        
        try:
            if metadatas is None:
                metadatas = [{} for _ in chunk_ids]
            
            logger.info(f"Adding {len(chunk_ids)} embeddings to ChromaDB...")
            
            # Add to collection
            self.collection.add(
                ids=chunk_ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            
            logger.info(f"Successfully added {len(chunk_ids)} embeddings")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add embeddings: {e}")
            return False

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filters: Dict = None
    ) -> List[Dict]:
        """
        Search for similar documents using SQLite + numpy similarity search
        Completely bypasses ChromaDB to avoid Windows hanging issues
        
        Args:
            query_embedding: Query embedding vector (384-dim)
            top_k: Number of results to return
            filters: Optional metadata filters (document_type)

        Returns:
            List of similar documents with scores and metadata
        """
        try:
            start_time = time.time()
            logger.info(f"🔍 Vector search starting (top_k={top_k})...")
            
            # Import database deps
            from src.shared.database import SessionLocal
            from src.models.document import Document, DocumentChunk, Embedding
            from sqlalchemy.orm import joinedload
            
            # Query SQLite for all embeddings
            session = SessionLocal()
            try:
                # Get all embeddings with their chunks
                embeddings_query = session.query(Embedding).join(
                    DocumentChunk
                ).join(
                    Document
                )
                
                all_embeddings = embeddings_query.all()
                
                if not all_embeddings:
                    logger.info("📭 No embeddings found in database")
                    return []
                
                logger.info(f"Found {len(all_embeddings)} embeddings in SQLite")
                
                # Convert query embedding to numpy
                query_vec = np.array(query_embedding, dtype=np.float32)
                
                # Compute similarities
                similarities = []
                for emb in all_embeddings:
                    try:
                        # Parse embedding vector from JSON
                        embedding_vec = np.array(emb.vector, dtype=np.float32)
                        
                        # Cosine similarity
                        dot_product = np.dot(query_vec, embedding_vec)
                        norm_query = np.linalg.norm(query_vec)
                        norm_doc = np.linalg.norm(embedding_vec)
                        
                        if norm_query > 0 and norm_doc > 0:
                            similarity = dot_product / (norm_query * norm_doc)
                        else:
                            similarity = 0.0
                        
                        # Get chunk and document info
                        chunk = emb.chunk
                        doc = chunk.document if chunk else None
                        
                        if doc and chunk:
                            # Apply filters if specified
                            if filters and "document_type" in filters:
                                if doc.document_type != filters["document_type"]:
                                    continue
                            
                            similarities.append({
                                "similarity": similarity,
                                "embedding_id": emb.id,
                                "chunk_id": chunk.id,
                                "doc_id": doc.id,
                                "text": chunk.chunk_text,
                                "doc_title": doc.title,
                                "doc_type": doc.document_type
                            })
                    except Exception as e:
                        logger.warning(f"Error processing embedding {emb.id}: {e}")
                        continue
                
                # Sort by similarity descending
                similarities.sort(key=lambda x: x["similarity"], reverse=True)
                
                # Get top-k results
                results = []
                for item in similarities[:top_k]:
                    results.append({
                        "id": f"chunk_{item['chunk_id']}",
                        "document": item["text"],
                        "metadata": {
                            "chunk_id": item["chunk_id"],
                            "document_id": item["doc_id"],
                            "title": item["doc_title"],
                            "document_type": item["doc_type"]
                        },
                        "distance": 1.0 - item["similarity"]  # Convert similarity to distance
                    })
                
                elapsed = time.time() - start_time
                logger.info(f"✓ SQLite + numpy search completed in {elapsed:.3f}s, found {len(results)} results")
                return results
                
            finally:
                session.close()
            
        except Exception as e:
            logger.error(f"❌ Vector search error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return []

    def delete_chunk(self, chunk_id: str) -> bool:
        """
        Delete a chunk from the vector store

        Args:
            chunk_id: ID of chunk to delete

        Returns:
            True if successful
        """
        
        try:
            self.collection.delete(ids=[chunk_id])
            logger.info(f"Deleted chunk {chunk_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete chunk {chunk_id}: {e}")
            return False

    def _count_collection(self, timeout: int = 5) -> Optional[int]:
        """Count collection embeddings with timeout protection."""
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(self.collection.count)
                return future.result(timeout=timeout)
        except TimeoutError:
            logger.warning(f"ChromaDB count timed out after {timeout} seconds")
            return None
        except Exception as e:
            logger.warning(f"Failed to count ChromaDB collection: {e}")
            return None

    def get_collection_info(self) -> Dict:
        """
        Get information about the collection

        Returns:
            Dict with collection stats
        """
        try:
            count = self._count_collection(timeout=5)
            return {
                "collection_name": self.collection_name,
                "total_embeddings": count if count is not None else 0,
                "collection_object": self.collection
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {
                "collection_name": self.collection_name,
                "total_embeddings": 0,
                "collection_object": self.collection
            }

    def persist(self):
        """Persist the collection to disk (auto-handled by PersistentClient)"""
        try:
            # PersistentClient automatically persists data, so this is a no-op
            # but we keep the method for API compatibility
            logger.info("ChromaDB data is automatically persisted")
        except Exception as e:
            logger.error(f"Error in persist: {e}")

    def clear_collection(self):
        """Clear all embeddings from collection (USE WITH CAUTION)"""
        try:
            # Get all IDs and delete
            results = self.collection.get()
            if results and results['ids']:
                self.collection.delete(ids=results['ids'])
            logger.warning(f"Cleared {len(results.get('ids', []))} embeddings from collection")
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")


# Global instance
_store_instance: Optional[VectorStore] = None


def get_vector_store(
    persist_directory: str = "data/vectorstore",
    collection_name: str = "diras_documents"
) -> VectorStore:
    """Get or create vector store instance"""
    global _store_instance
    
    if _store_instance is None:
        _store_instance = VectorStore(persist_directory, collection_name)
    
    return _store_instance
