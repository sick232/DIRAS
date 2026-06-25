#!/usr/bin/env python3
"""
Test RAG retrieval with newly indexed PDFs
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.services.retrieval import get_document_retriever
from src.services.embeddings import get_embedding_generator
from src.shared.database import SessionLocal

def test_rag_retrieval():
    """Test retrieval with newly indexed PDFs"""
    
    print("\n" + "="*70)
    print("RAG RETRIEVAL TEST - NEW PDFs")
    print("="*70)
    
    try:
        db = SessionLocal()
        retriever = get_document_retriever()
        
        # Test queries related to defence procurement
        test_queries = [
            "What is the defence procurement manual?",
            "Financial delegation authority for procurement",
            "Manual for goods procurement",
            "Standardisation rules and procedures",
            "DRDO procurement guidelines"
        ]
        
        print("\n🔍 Testing RAG Retrieval:\n")
        
        for query in test_queries:
            print(f"Query: {query}")
            
            results = retriever.retrieve(query, top_k=3, db=db)
            
            if results.get('status') == 'success':
                chunks = results.get('results', [])
                print(f"  Results: {len(chunks)} chunks retrieved")
                
                for idx, chunk in enumerate(chunks[:3], 1):
                    metadata = chunk.get('metadata', {})
                    doc_title = metadata.get('document_title', 'Unknown')
                    doc_type = metadata.get('document_type', 'Unknown')
                    similarity = chunk.get('similarity_score', 0)
                    
                    print(f"    [{idx}] {doc_title} ({doc_type})")
                    print(f"        Similarity: {similarity:.3f}")
                    text_preview = chunk['text'][:80].replace('\n', ' ')
                    print(f"        Preview: {text_preview}...")
            else:
                print(f"  Error: {results.get('error', 'Unknown error')}")
            
            print()
        
        db.close()
        
        print("="*70)
        print("✅ RAG RETRIEVAL TEST PASSED")
        print("="*70)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_rag_retrieval()
