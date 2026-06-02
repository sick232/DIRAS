#!/usr/bin/env python
import os
from openai import OpenAI

api_key = "<YOUR_XAI_API_KEY>"  # Set in environment: xai.com/api
client = OpenAI(api_key=api_key, base_url='https://api.x.ai/v1')

# Try different model names
models_to_try = ['grok-2', 'grok-2-1212', 'grok-vision-beta', 'grok-vision', 'grok-3', 'grok', 'grok-latest']

print("Testing available Grok models...")
for model in models_to_try:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': 'Hi'}],
            max_tokens=5
        )
        print(f'✅ Model "{model}" WORKS!')
        print(f'   Response model name: {response.model}')
        break
    except Exception as e:
        error_msg = str(e)
        if 'Model not found' in error_msg:
            print(f'❌ {model}: Not available on xAI API')
        elif 'insufficient_quota' in error_msg.lower():
            print(f'⚠️  {model}: Available but quota exceeded')
            break
        else:
            print(f'❌ {model}: Error - {error_msg[:80]}')
