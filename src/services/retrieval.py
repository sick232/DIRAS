"""
Retrieval Service (BM25)
Uses SQLite-stored document chunks and BM25 ranking (rank-bm25)
"""

import logging
import pickle
import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

_bm25_model = None
_bm25_chunk_metas = []
_bm25_loaded = False


def load_bm25_index(
    index_path: str = "data/bm25/bm25_index.pkl",
    chunks_path: str = "data/bm25/chunks.json"
) -> bool:
    global _bm25_model, _bm25_chunk_metas, _bm25_loaded
    try:
        index_file = Path(index_path)
        chunks_file = Path(chunks_path)

        if not index_file.exists() or not chunks_file.exists():
            logger.warning(f"BM25 index or chunks file not found: {index_file}, {chunks_file}")
            _bm25_loaded = False
            return False

        with index_file.open("rb") as f:
            _bm25_model = pickle.load(f)

        with chunks_file.open("r", encoding="utf-8") as f:
            _bm25_chunk_metas = json.load(f)

        _bm25_loaded = True
        logger.info(f"BM25 chunks loaded: {len(_bm25_chunk_metas)}")
        logger.info("BM25 index loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to load BM25 index: {e}")
        _bm25_loaded = False
        return False


def is_bm25_loaded() -> bool:
    return _bm25_loaded


def _simple_tokenize(text: str) -> List[str]:
    # Lowercase and split on non-word characters
    tokens = re.findall(r"\w+", text.lower())
    return tokens


class DocumentRetriever:
    """BM25-based document retriever using `document_chunks` table."""

    def __init__(self, top_k: int = 5):
        self.top_k = top_k
        logger.info(f"BM25 DocumentRetriever initialized (top_k={top_k})")

    def retrieve(
        self,
        query: str,
        top_k: int = None,
        db: Session = None,
        document_type_filter: Optional[str] = None,
        document_type_filters: Optional[List[str]] = None,
        boost_terms: Optional[List[str]] = None
    ) -> dict:
        try:
            if top_k is None:
                top_k = self.top_k

            if db is None:
                error_msg = "Database session `db` is required for BM25 retrieval"
                logger.error(error_msg)
                return {"status": "failed", "query": query, "error": error_msg, "results": []}

            def _apply_boost(score: float, text: str, title: str, terms: Optional[List[str]]) -> float:
                if not terms:
                    return score
                boost = 0.0
                text_lower = (text or "").lower()
                title_lower = (title or "").lower()
                for term in terms:
                    if term in text_lower or term in title_lower:
                        boost += 0.25
                return score + boost

            # Load chunks from database
            from src.models.document import DocumentChunk, Document

            # Optionally filter by document type or document type list
            query_filter = db.query(DocumentChunk).join(Document)
            if document_type_filters:
                query_filter = query_filter.filter(Document.document_type.in_(document_type_filters))
            elif document_type_filter and document_type_filter != "All Types":
                query_filter = query_filter.filter(Document.document_type == document_type_filter)

            chunks = query_filter.all()

            if not chunks:
                logger.info("No document chunks available for BM25 retrieval")
                return {"status": "success", "query": query, "results": [], "chunk_count": 0, "documents": []}

            tokenized_query = _simple_tokenize(query)

            if _bm25_loaded and _bm25_model is not None:
                # Use preloaded BM25 index from disk
                try:
                    scores = _bm25_model.get_scores(tokenized_query)
                    if document_type_filters:
                        filtered_indices = [
                            i for i, meta in enumerate(_bm25_chunk_metas)
                            if meta.get("document_type") in document_type_filters
                        ]
                    elif document_type_filter and document_type_filter != "All Types":
                        filtered_indices = [
                            i for i, meta in enumerate(_bm25_chunk_metas)
                            if meta.get("document_type") == document_type_filter
                        ]
                    else:
                        filtered_indices = list(range(len(scores)))

                    scored_indices = []
                    for idx in filtered_indices:
                        self_meta = _bm25_chunk_metas[idx]
                        score = float(scores[idx])
                        boosted = _apply_boost(score, self_meta.get("text", ""), self_meta.get("title", ""), boost_terms)
                        scored_indices.append((boosted, idx))
                    scored_indices.sort(key=lambda item: item[0], reverse=True)
                    scored_indices = [idx for _, idx in scored_indices]

                    results = []
                    unique_docs = set()
                    for idx in scored_indices[:top_k]:
                        self_meta = _bm25_chunk_metas[idx]
                        score = float(scores[idx])
                        unique_docs.add(self_meta.get("document_id"))
                        distance = 1.0 / (1.0 + score) if score > 0 else 1.0
                        results.append({
                            "chunk_id": f"chunk_{self_meta.get('chunk_id')}",
                            "text": self_meta.get("text", "")[:500],
                            "full_text": self_meta.get("text", ""),
                            "similarity_score": score,
                            "metadata": {
                                "document_id": self_meta.get("document_id"),
                                "title": self_meta.get("title"),
                                "document_title": self_meta.get("title"),
                                "document_type": self_meta.get("document_type"),
                                "chunk_id": self_meta.get("chunk_id")
                            },
                            "raw_distance": distance
                        })

                    logger.info(f"BM25 retrieved {len(results)} chunks from {len(unique_docs)} documents")
                    return {
                        "status": "success",
                        "query": query,
                        "results": results,
                        "chunk_count": len(results),
                        "document_count": len(unique_docs),
                        "documents": list(unique_docs)
                    }
                except Exception as e:
                    logger.warning(f"Loaded BM25 index retrieval failed, fallback to DB: {e}")

            # Prepare corpus and metadata from DB
            corpus = [chunk.chunk_text for chunk in chunks]
            tokenized_corpus = [_simple_tokenize(c) for c in corpus]

            # Build BM25 index
            try:
                from rank_bm25 import BM25Okapi
            except Exception as e:
                error_msg = f"rank_bm25 is required but not installed: {e}"
                logger.error(error_msg)
                return {"status": "failed", "query": query, "error": error_msg, "results": []}

            bm25 = BM25Okapi(tokenized_corpus)
            scores = bm25.get_scores(tokenized_query)

            scored_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

            boosted_scores = []
            for idx in scored_indices:
                chunk = chunks[idx]
                title = chunk.document.title if chunk.document else ""
                text = chunk.chunk_text
                score = float(scores[idx])
                boosted_score = _apply_boost(score, text, title, boost_terms)
                boosted_scores.append((boosted_score, idx))
            boosted_scores.sort(key=lambda item: item[0], reverse=True)
            scored_indices = [idx for _, idx in boosted_scores]

            results = []
            unique_docs = set()

            for idx in scored_indices[:top_k]:
                score = float(scores[idx])
                chunk = chunks[idx]
                doc = chunk.document

                if doc and chunk:
                    unique_docs.add(doc.id)
                    # Map BM25 score to a pseudo-distance (lower better)
                    distance = 1.0 / (1.0 + score) if score > 0 else 1.0

                    results.append({
                        "chunk_id": f"chunk_{chunk.id}",
                        "text": chunk.chunk_text[:500],
                        "full_text": chunk.chunk_text,
                        "similarity_score": score,
                        "metadata": {
                            "document_id": doc.id,
                            "title": doc.title,
                            "document_title": doc.title,
                            "document_type": doc.document_type,
                            "chunk_id": chunk.id
                        },
                        # Keep compatibility with earlier structure
                        "raw_distance": distance
                    })

            logger.info(f"BM25 retrieved {len(results)} chunks from {len(unique_docs)} documents")

            # Convert to same return shape used elsewhere
            formatted_results = []
            for r in results:
                formatted_results.append({
                    "chunk_id": r["chunk_id"],
                    "text": r["text"],
                    "full_text": r["full_text"],
                    "similarity_score": r["similarity_score"],
                    "metadata": r["metadata"],
                })

            return {
                "status": "success",
                "query": query,
                "results": formatted_results,
                "chunk_count": len(formatted_results),
                "document_count": len(unique_docs),
                "documents": list(unique_docs)
            }

        except Exception as e:
            logger.error(f"BM25 retrieval failed: {e}")
            return {"status": "failed", "query": query, "error": str(e), "results": []}

    def retrieve_by_document(self, document_id: int, db: Session, top_k: int = None) -> dict:
        try:
            if top_k is None:
                top_k = self.top_k

            from src.models.document import DocumentChunk, Document

            chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).limit(top_k).all()
            return {
                "status": "success",
                "document_id": document_id,
                "document_title": db.query(Document).filter(Document.id == document_id).first().title,
                "chunks": [
                    {"chunk_id": chunk.id, "text": chunk.chunk_text, "chunk_index": chunk.chunk_index}
                    for chunk in chunks
                ]
            }
        except Exception as e:
            logger.error(f"Failed to retrieve document by id: {e}")
            return {"status": "failed", "error": str(e)}

    def set_top_k(self, top_k: int):
        self.top_k = top_k
        logger.info(f"Updated default top_k to {top_k}")


# Global instance
_retriever_instance = None


def get_document_retriever(top_k: int = 5) -> DocumentRetriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = DocumentRetriever(top_k)
    return _retriever_instance
