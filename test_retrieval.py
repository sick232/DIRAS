#!/usr/bin/env python
from src.services.retrieval import get_document_retriever

retriever = get_document_retriever()
results = retriever.retrieve('Tell me about defence budget allocation', top_k=5)

print(f"Status: {results['status']}")
print(f"Chunks found: {results['chunk_count']}")

if results['results']:
    print("\nTop 3 results:")
    for i, r in enumerate(results['results'][:3], 1):
        score = r['similarity_score']
        text = r['text'][:150]
        print(f"\n{i}. Score: {score:.3f}")
        print(f"   {text}...")
else:
    print("No results found!")
