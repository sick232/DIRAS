#!/usr/bin/env python3
import json
import urllib.request
import time

url = 'http://127.0.0.1:8000/api/v1/query'
data = json.dumps({'question': 'what is DRDO?'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

print('Sending query to backend...')
start = time.time()

try:
    resp = urllib.request.urlopen(req, timeout=90)
    elapsed = time.time() - start
    print(f'✓ Response received in {elapsed:.1f}s')
    
    result = json.loads(resp.read().decode())
    print(f'Status: {resp.status}')
    print(f'Answer length: {len(result.get("answer", ""))} chars')
    print(f'Model used: {result.get("model_used", "unknown")}')
    print(f'Answer preview: {result.get("answer", "")[:300]}...')
    
except urllib.error.URLError as e:
    elapsed = time.time() - start
    print(f'✗ URLError after {elapsed:.1f}s: {e}')
except json.JSONDecodeError as e:
    elapsed = time.time() - start
    print(f'✗ JSON error after {elapsed:.1f}s: {e}')
except Exception as e:
    elapsed = time.time() - start
    print(f'✗ Error after {elapsed:.1f}s: {type(e).__name__}: {e}')
