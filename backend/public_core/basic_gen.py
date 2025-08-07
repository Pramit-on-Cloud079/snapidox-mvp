# public_core/basic_gen.py

import os
from datetime import datetime

def generate_summary(prompt: str) -> str:
    return f"Summary for: {prompt}\n\n(This is a basic mode placeholder. Upgrade to Snapidox Pro for full summary generation.)"

def create_readme(summary: str, filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# AWS Project Report\n\n")
        f.write(summary)
        f.write("\n\n---\n\n")
        f.write("_Generated with Snapidox Basic_\n")

def handle_basic(prompt, screenshots):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    folder = os.path.join("uploads", f"basic_{timestamp}")
    os.makedirs(folder, exist_ok=True)

    summary = generate_summary(prompt)
    readme_path = os.path.join(folder, 'README.md')
    create_readme(summary, readme_path)

    return {
        "summary": summary,
        "pdf_path": None,
        "readme_path": readme_path,
        "linkedin_post": "(LinkedIn post not available in Snapidox Basic)"
    }
