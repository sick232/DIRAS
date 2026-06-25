from src.services.rag_engine import RAGEngine
from src.services.retrieval import DocumentRetriever
from src.services.embeddings import get_embedding_generator
from src.services.vectorstore import get_vector_store

print("=== Testing Retrieval ===")
retriever = DocumentRetriever(top_k=15)
retrieval_result = retriever.retrieve("Tell me about military expenditure", top_k=15)
print(f"Retrieval status: {retrieval_result['status']}")
print(f"Chunks retrieved: {retrieval_result.get('chunk_count', 0)}")
if retrieval_result['status'] == 'failed':
    print(f"Error: {retrieval_result.get('error', 'Unknown')}")
else:
    for i, result in enumerate(retrieval_result.get('results', [])[:2]):
        print(f"\n{i+1}. Score: {result.get('similarity_score', 0):.3f}")
        print(f"   Text: {result.get('text', '')[:100]}...")

print("\n=== Testing RAG Engine ===")
rag = RAGEngine()
print("RAGEngine initialized")

# Try to analyze complexity
complexity = rag._analyze_query_complexity("Tell me about recent military expenditure")
print(f"Query complexity: {complexity}")

print("\nCalling generate_answer...")
try:
    answer_result = rag.generate_answer(
        question="Tell me about military expenditure",
        top_k=15
    )
    print(f"Answer result keys: {answer_result.keys()}")
    print(f"Answer: {answer_result.get('answer', '')[:200] if answer_result.get('answer') else 'EMPTY'}")
    print(f"Sources: {len(answer_result.get('sources', []))}")
    print(f"Confidence: {answer_result.get('confidence_score')}")
except Exception as e:
    print(f"Error generating answer: {e}")
    import traceback
    traceback.print_exc()
