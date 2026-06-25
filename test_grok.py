#!/usr/bin/env python
import os
import sys

# Check environment variable
key = os.getenv('GROK_API_KEY')
print(f"Env var GROK_API_KEY set: {bool(key)}")
if key:
    print(f"Key starts with: {key[:15]}...")
    
# Check config
from src.shared.config import settings
print(f"Settings grok_api_key set: {bool(settings.grok_api_key)}")
if settings.grok_api_key:
    print(f"Settings key starts with: {settings.grok_api_key[:15]}...")

# Try to get grok client
try:
    from src.services.llm.grok_client import get_grok_client
    client = get_grok_client(api_key=settings.grok_api_key)
    print("✅ Grok client created successfully!")
    print(f"Model: {client.model}")
except Exception as e:
    print(f"❌ Failed to create Grok client: {e}")
