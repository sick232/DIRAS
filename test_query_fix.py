import requests
import json

query = 'What is the maximum financial limit for lab director approval?'
response = requests.post(
    'http://127.0.0.1:8001/api/v1/query',
    json={'question': query},
    timeout=120
)

if response.status_code == 200:
    result = response.json()
    print('✓ Query successful')
    print(f'Answer: {result.get("answer", "")[:300]}...')
    print(f'Confidence: {result.get("confidence", 0)}')
    print(f'Model: {result.get("model", "")}')
else:
    print(f'✗ Error: {response.status_code}')
    print(response.text[:500])
