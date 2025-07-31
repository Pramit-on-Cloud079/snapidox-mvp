# src/linkedin/post_generator.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_linkedin_post(prompt: str) -> str:
    style_prompt = (
        f"Write a concise and engaging LinkedIn post for this AWS project:\n\n{prompt}\n\n"
        "Style:\n"
        "- First-person tone\n"
        "- Mix of technical + personal takeaway\n"
        "- Start with a hook\n"
        "- End with a question or call to action\n"
        "- Add up to 5 relevant hashtags"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": style_prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
