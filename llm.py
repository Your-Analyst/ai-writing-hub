import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "hermes3:8b")


def generate_text(prompt: str, model: str = OLLAMA_MODEL, temperature: float = 0.8) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except requests.RequestException as exc:
        return f"Error talking to Ollama: {exc}"