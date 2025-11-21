import requests
import json

class LocalLLM:
    def __init__(self, model="llama3.1:8b-instruct-fp16", base_url="http://10.10.110.25:11434"):
        self.model = model
        self.base_url = base_url

    def __call__(self, prompt: str):
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            r = requests.post(url, json=payload, timeout=200)
            data = r.json()
            return data.get("response", json.dumps(data))

        except Exception as e:
            return json.dumps({"answer": f"LLM error: {e}"})
