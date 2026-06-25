#!/usr/bin/env python
"""Test available Groq models"""
import os
from openai import OpenAI

api_key = "<YOUR_GROQ_API_KEY>"  # Get from groq.com
client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

# Try different model names
models_to_try = [
    'llama-3-70b-8192',
    'llama-2-70b-4096',
    'gemma-7b-it',
    'mixtral-8x7b-32768'
]

print("Testing available Groq models...")
for model in models_to_try:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': 'Hi'}],
            max_tokens=5
        )
        print(f'✅ Model "{model}" WORKS!')
        print(f'   Response model: {response.model}')
        break
    except Exception as e:
        error_msg = str(e)
        if 'decommissioned' in error_msg.lower():
            print(f'❌ {model}: Decommissioned')
        elif 'not found' in error_msg.lower():
            print(f'❌ {model}: Not available')
        else:
            print(f'⚠️  {model}: {error_msg[:100]}')
