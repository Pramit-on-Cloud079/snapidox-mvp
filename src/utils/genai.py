# src/utils/genai.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(prompt: str) -> str:
    full_prompt = (
        f"Write a technical summary for this AWS project: {prompt}\n\n"
        "Structure:\n"
        "- What it does\n"
        "- AWS services used\n"
        "- How the automation works\n"
        "- Deployment flow in 4–5 steps"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
