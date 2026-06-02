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
print(f"\nFull Response:")
print(json.dumps(result, indent=2))
