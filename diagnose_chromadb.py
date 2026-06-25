"""
Diagnostic helper for ChromaDB collection
Run: python diagnose_chromadb.py
"""

import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from src.services.vectorstore import get_vector_store
    from src.services.embeddings import get_embedding_generator
except Exception as e:
    logger.error(f"Failed importing services: {e}")
    sys.exit(2)


def run():
    try:
        vs = get_vector_store()
        logger.info(f"Collection name: {vs.collection_name}")

        # Try count
        try:
            count = None
            try:
                count = vs._count_collection(timeout=5)
            except Exception:
                count = None
            logger.info(f"Collection count (best-effort): {count}")
        except Exception as e:
            logger.warning(f"Failed getting collection count: {e}")

        # Try get sample
        try:
            results = vs.collection.get()
            ids = results.get('ids', [])
            docs = results.get('documents', [])
            metas = results.get('metadatas', [])
            logger.info(f"Collection.get() returned ids length: {len(ids)}")
            if ids:
                sample_id = ids[0]
                logger.info(f"Sample id: {sample_id}")
                if docs:
                    logger.info(f"Sample document (truncated): {docs[0][:200]}")
                if metas:
                    logger.info(f"Sample metadata: {metas[0]}")
        except Exception as e:
            logger.warning(f"collection.get() failed: {e}")

        # Run a small query test using embedder
        try:
            embedder = get_embedding_generator()
            emb = embedder.embed_text('test')
            logger.info(f"Generated test embedding length: {len(emb)}")

            res = None
            try:
                # Use the vectorstore search wrapper so it benefits from timeout
                res = vs.search(emb, top_k=1)
            except Exception as e:
                logger.warning(f"vs.search() failed: {e}")

            logger.info(f"vs.search() returned {len(res) if res is not None else 'None'} results")
            if res:
                logger.info(f"First search result metadata: {res[0].get('metadata')}")
        except Exception as e:
            logger.warning(f"Embedding/test query failed: {e}")

    except Exception as e:
        logger.error(f"Diagnostic failed: {e}")


if __name__ == '__main__':
    run()
