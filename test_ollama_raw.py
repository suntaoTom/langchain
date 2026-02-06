"""Manual test for raw Ollama API connection."""

import logging

import requests

logger = logging.getLogger(__name__)

def test_ollama_raw():
    """Test raw connection to local Ollama server."""
    url = "http://127.0.0.1:11434/api/generate"
    data = {
        "model": "deepseek-r1:8b",
        "prompt": "hi",
        "stream": False
    }
    try:
        logger.info("Connecting to %s...", url)
        response = requests.post(url, json=data, timeout=30, proxies={"http": None, "https": None})
        logger.info("Status Code: %s", response.status_code)
        logger.info("Response: %s", response.text)
    except Exception:
        logger.exception("Error in test_ollama_raw")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_ollama_raw()
