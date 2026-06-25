#!/usr/bin/env python
"""Test more Groq models"""
import os
from openai import OpenAI

api_key = "<YOUR_GROQ_API_KEY>"  # Get from groq.com
client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

# Try different model names based on potential patterns
models_to_try = [
    'llama3-8b',
    'llama3-70b',
    'mixtral-8x7b',
    'gemma-7b',
    'llama-3.1-70b-versatile',
    'llama-3.2-70b',
    'mixtral-8x7b-32768-instant',
    'deepseek-r1'
]

print("Testing potential Groq models...")
for model in models_to_try:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': 'Hi'}],
            max_tokens=5,
            timeout=5
        )
        print(f'✅ Model "{model}" WORKS!')
        print(f'   Response model: {response.model}')
        break
    except Exception as e:
        error_msg = str(e)
        if 'does not exist' in error_msg.lower() or '404' in error_msg:
            print(f'❌ {model}: Not found')
        elif 'decommissioned' in error_msg.lower():
            print(f'⚠️  {model}: Decommissioned')
        elif 'timeout' in error_msg.lower():
            print(f'❌ {model}: Timeout')
        else:
            print(f'❌ {model}: {error_msg[:80]}')
