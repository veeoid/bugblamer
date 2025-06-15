import os
from dotenv import load_dotenv
import httpx

load_dotenv()

def analyze_failure(logs: str, diffs: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You're a CI/CD debugging expert. Based on the following git diffs and CI logs, identify the commit most likely to have caused the failure. Mention the commit hash or file, and explain your reasoning clearly.

--- GIT DIFFS ---
{diffs}

--- CI LOGS ---
{logs}
"""

    payload = {
        "messages": [
            {"role": "system", "content": "You are a precise software debugging assistant."},
            {"role": "user", "content": prompt}
        ],
        "model": "llama-3.3-70b-versatile"  # ✅ Confirmed model on Groq
    }

    try:
        response = httpx.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"
