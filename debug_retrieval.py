from src.services.retrieval import RetrieverService
from src.shared.config import settings

retriever = RetrieverService()
results = retriever.retrieve('Tell me about military expenditure', top_k=15)
print(f'Documents retrieved: {len(results)}')
for i, doc in enumerate(results[:3]):
    print(f'\n{i+1}. {doc.get("document_title", "Unknown")}')
    print(f'   Similarity: {doc.get("distance", 0):.3f}')
    print(f'   Content preview: {doc.get("chunk_text", "")[:100]}...')
