import requests, os

from dotenv import load_dotenv

load_dotenv()

EURIAI_API_KEY = os.getenv("EURON_API_KEY")

url = "https://api.euron.one/api/v1/euri/alpha/chat/completions"

def euri_chat_completion(messages, model="gpt-4.1-nano", temperature=0.7, max_tokens=1000):
    try:
        headers = {
            "Authorization": f"Bearer {EURIAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR calling EURI API]: {e}"
