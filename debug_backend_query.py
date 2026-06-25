import requests

BASE = "http://127.0.0.1:8000"

try:
    health = requests.get(f"{BASE}/api/v1/health", timeout=10)
    print("HEALTH", health.status_code, health.text)
except Exception as e:
    print("HEALTH ERROR", e)

try:
    payload = {
        "question": "What is the latest defence procurement policy?",
        "top_k": 5
    }
    resp = requests.post(f"{BASE}/api/v1/query", json=payload, timeout=60)
    print("QUERY STATUS", resp.status_code)
    print(resp.text)
except Exception as e:
    print("QUERY ERROR", e)
