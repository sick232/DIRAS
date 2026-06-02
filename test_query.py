import requests
import json

query_data = {
    "question": "Tell me about recent military expenditure",
    "top_k": 15,
    "document_type": "All Types"
}

response = requests.post(
    "http://localhost:8000/api/v1/query",
    json=query_data,
    timeout=60
)

print(f"Status: {response.status_code}")
result = response.json()
print(f"\nAnswer length: {len(result.get('answer', ''))}")
print(f"Sources: {len(result.get('sources', []))}")
print(f"Confidence: {result.get('confidence_score')}")
print(f"\nFirst 300 chars of answer:")
print(result.get('answer', '')[:300])
print(f"\nSources:")
for i, src in enumerate(result.get('sources', [])[:5]):
    print(f"  {i+1}. {src.get('title', 'Unknown')}")
