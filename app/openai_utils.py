import os
import requests

def get_embeddings(text):
    """
    Get embeddings for a given text from OpenAI.
    """
    endpoint = "https://api.openai.com/v1/embeddings"
    payload = {
        "input": text,
        "model": "text-embedding-ada-002",
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }

    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["data"][0]["embedding"]
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to get embeddings: {e}")

def generate_chat_response(messages, prompt, assistant_message):
    """
    Generate a chat response using OpenAI's ChatGPT.
    """
    endpoint = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4",
        "messages": messages + [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_message},
        ],
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to generate chat response: {e}")
