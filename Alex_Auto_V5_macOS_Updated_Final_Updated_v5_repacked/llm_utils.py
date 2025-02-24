# llm_utils.py

import requests
from config import Config

cfg = Config()

base_url_sync = "http://192.168.1.101:1234/v1"

def create_chat_completion(messages, model=None, temperature=cfg.temperature, max_tokens=None) -> str:
    """Create a chat completion using the server (synchronous)"""
    response = None
    num_retries = 5
    for attempt in range(num_retries):
        try:
            url = f"{base_url_sync}/chat/completions"
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                break
            elif response.status_code == 429:
                # Handle rate limit reached
                pass
            elif response.status_code == 502:
                # Handle bad gateway
                pass
            else:
                raise RuntimeError(f"Received unexpected status code: {response.status_code}")
        except Exception as e:
            if attempt == num_retries - 1:
                raise
            else:
                # Handle other exceptions
                pass

    if response is None:
        raise RuntimeError("Failed to get response after 5 retries")

    content = response.json().get("choices", [])[0].get("message", {}).get("content", "")
    return content
