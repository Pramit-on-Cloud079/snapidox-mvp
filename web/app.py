import sys
import os
# Allow importing from root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import threading
import datetime
from flask import Flask, render_template, request, send_file
from fpdf import FPDF
from src.utils.genai import generate_summary

app = Flask(__name__)

# ✅ Auto-delete helper (15 minutes)
def schedule_file_cleanup(file_path, delay_seconds=900):
    def delete_file():
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"[Cleanup] Deleted {file_path}")
        except Exception as e:
            print(f"[Cleanup Error] Failed to delete {file_path}: {e}")
    threading.Timer(delay_seconds, delete_file).start()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        summary = generate_summary(prompt)

        # Metadata
        project_title = prompt.strip().capitalize()
        author = "Pramit Dasgupta"
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        # === PDF Generation ===
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="Snapidox Project Report", ln=True, align="C")
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Project Title: {project_title}", ln=True)
        pdf.cell(200, 10, txt=f"Author: {author}", ln=True)
        pdf.cell(200, 10, txt=f"Date: {date}", ln=True)
        pdf.ln(5)
        pdf.multi_cell(0, 10, f"Summary:\n{summary}")
        os.makedirs("web/reports", exist_ok=True)
        pdf_path = "web/reports/project_report.pdf"
        pdf.output(pdf_path)
        schedule_file_cleanup(pdf_path)

        # === README Generation ===
        readme_path = "web/README.md"
        readme_content = f"""# {project_title}

**Author:** {author}  
**Date:** {date}  

## Summary
{summary.strip()}

## Features
- Automated deployment using AWS tools
- Based on prompt: “{prompt}”

## Output Files
- PDF Report: `project_report.pdf`
"""
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        schedule_file_cleanup(readme_path)

        # === LinkedIn Post Generation ===
        linkedin_path = "web/linkedin_post.txt"
        linkedin_post = f"""🚀 Just documented a new AWS project using Snapidox!

🛠️ **{project_title}**  
📅 {date}

🔍 Summary:  
{summary.strip()}

📎 Generated:  
✅ PDF Report  
✅ GitHub README  
✅ LinkedIn Post Caption

Try it yourself and automate your AWS documentation!"""
        with open(linkedin_path, "w", encoding="utf-8") as f:
            f.write(linkedin_post)
        schedule_file_cleanup(linkedin_path)

        return render_template("index.html", generated=True)

    return render_template("index.html", generated=False)

@app.route("/download/<filename>")
def download_file(filename):
    return send_file(f"web/{filename}", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
