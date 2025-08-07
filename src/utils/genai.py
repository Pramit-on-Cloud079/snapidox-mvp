# src/utils/genai.py

import os
from openai import OpenAI

client = OpenAI()

EMOJI_CATEGORIES = {
    "cloud": "☁️",
    "python": "🐍",
    "frontend": "🎨",
    "backend": "🖥️",
    "database": "🗄️",
    "devops": "⚙️",
    "ai": "🧠",
    "api": "🔗",
    "auth": "🔐",
    "storage": "💾"
}


def apply_emoji_labels(text):
    labeled = ""
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        if any(e in line for e in EMOJI_CATEGORIES.values()):
            labeled += line + "\n"
            continue
        for keyword, emoji in EMOJI_CATEGORIES.items():
            if keyword.lower() in line.lower():
                line = f"{emoji} {line}"
                break
        labeled += line + "\n"
    return labeled.strip()


def generate_summary_and_title(user_input):
    prompt = f"""
You are a helpful assistant. Given the user input or project idea below, generate:
- A catchy project title (1 line)
- A detailed, professional project summary (max 4 lines)

Respond in this format only:
Title: <title here>
Summary: <summary here>

Input:
{user_input}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a skilled documentation AI."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content.strip()

    title_line = next((line for line in content.splitlines() if line.lower().startswith("title:")), "Title: Untitled")
    summary_line = next((line for line in content.splitlines() if line.lower().startswith("summary:")), "Summary: No summary available")

    title = title_line.split(":", 1)[1].strip()
    summary_raw = summary_line.split(":", 1)[1].strip()

    # ❌ Remove section-like lines from summary accidentally inserted by GPT
    forbidden_starts = ("🛠️", "🚀", "🧠", "Tech Stack", "Features", "Architecture")
    summary_lines = summary_raw.splitlines()
    filtered_summary = "\n".join(
        line for line in summary_lines if not any(line.strip().lower().startswith(fs.lower()) for fs in forbidden_starts)
    )

    return title, filtered_summary.strip()



import re

def generate_tech_features_arch(user_input):
    prompt = f"""
You are a skilled technical analyst. Given the project prompt below, return these three sections — each as 3–6 bullet points:

Tech Stack:
- tools and platforms used

Features:
- core functionalities

Architecture:
- major workflow or architecture steps

Input:
{user_input}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a structured and reliable tech breakdown assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content.strip()

    # Split lines and classify based on order
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    tech_lines, feature_lines, arch_lines = [], [], []
    section = None

    for line in lines:
        if "tech stack" in line.lower():
            section = "tech"
            continue
        elif "feature" in line.lower():
            section = "feature"
            continue
        elif "architecture" in line.lower() or "workflow" in line.lower():
            section = "arch"
            continue

        if line.startswith("-") or line.startswith("•"):
            if section == "tech":
                tech_lines.append(line)
            elif section == "feature":
                feature_lines.append(line)
            elif section == "arch":
                arch_lines.append(line)

    tech = apply_emoji_labels("\n".join(tech_lines)) if tech_lines else "❌ No Tech Stack found."
    features = apply_emoji_labels("\n".join(feature_lines)) if feature_lines else "❌ No Features found."
    architecture = apply_emoji_labels("\n".join(arch_lines)) if arch_lines else "❌ No Architecture found."

    return tech.strip(), features.strip(), architecture.strip()


