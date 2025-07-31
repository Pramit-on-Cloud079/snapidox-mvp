import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, send_file
from src.utils.genai import generate_summary
from fpdf import FPDF
import datetime
import os

app = Flask(__name__)

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

        # === README Generation ===
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
        with open("web/README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)

        # === LinkedIn Post Generation ===
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

        with open("web/linkedin_post.txt", "w", encoding="utf-8") as f:
            f.write(linkedin_post)

        return render_template("index.html", generated=True)

    return render_template("index.html", generated=False)


@app.route("/download/<filename>")
def download_file(filename):
    return send_file(f"web/{filename}", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
