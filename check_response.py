#!/usr/bin/env python3
import json
import urllib.request
import time

url = 'http://127.0.0.1:8000/api/v1/query'
data = json.dumps({'question': 'test query'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

print('Sending query...')
try:
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode())
    print(f'Response keys: {list(result.keys())}')
    print(f'Status: {resp.status}')
    print(json.dumps(result, indent=2)[:1000])
except Exception as e:
    print(f'Error: {e}')
