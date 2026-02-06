import requests
import json

def test_ollama_raw():
    url = "http://127.0.0.1:11434/api/generate"
    data = {
        "model": "deepseek-r1:8b",
        "prompt": "hi",
        "stream": False
    }
    try:
        print(f"Connecting to {url}...")
        response = requests.post(url, json=data, timeout=30, proxies={"http": None, "https": None})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ollama_raw()
