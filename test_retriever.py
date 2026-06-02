from src.services.retrieval import DocumentRetriever, get_document_retriever
from src.shared.database import get_db
from src.shared.config import settings

# Test direct retriever
print("=== Test 1: Direct retriever instance ===")
retriever = DocumentRetriever(top_k=15)
result = retriever.retrieve("Tell me about recent military expenditure", top_k=15, db=None, document_type_filter=None)
print(f"Status: {result['status']}")
print(f"Chunks: {result.get('chunk_count', 0)}")
if result['status'] == 'failed':
    print(f"Error: {result.get('error')}")

# Test with document_type filter like API sends
print("\n=== Test 2: With document_type_filter='All Types' ===")
retriever2 = DocumentRetriever(top_k=15)
result2 = retriever2.retrieve("Tell me about recent military expenditure", top_k=15, db=None, document_type_filter="All Types")
print(f"Status: {result2['status']}")
print(f"Chunks: {result2.get('chunk_count', 0)}")
if result2['status'] == 'failed':
    print(f"Error: {result2.get('error')}")

# Test factory function
print("\n=== Test 3: Factory function ===")
retriever3 = get_document_retriever(top_k=15)
result3 = retriever3.retrieve("Tell me about recent military expenditure", top_k=15, db=None, document_type_filter=None)
print(f"Status: {result3['status']}")
print(f"Chunks: {result3.get('chunk_count', 0)}")
if result3['status'] == 'failed':
    print(f"Error: {result3.get('error')}")
