# test_groq_key.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load from .env

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

try:
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # Valid Groq model
        messages=[{"role": "user", "content": "Say hello"}],
        temperature=0.3
    )
    print("✅ API Key works! Response:", response.choices[0].message.content)
except Exception as e:
    print("❌ Error:", str(e))
