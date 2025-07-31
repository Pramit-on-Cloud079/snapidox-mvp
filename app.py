# app.py

from fpdf import FPDF
import datetime
from src.utils.genai import generate_summary  # NEW IMPORT
from src.linkedin.post_generator import generate_linkedin_post

# Dummy input
project_title = "AWS CI/CD Pipeline for Lambda"
author = "Pramit Dasgupta"
date = datetime.datetime.now().strftime("%Y-%m-%d")

user_prompt = "A pipeline that deploys Lambda functions using CodePipeline and GitHub"
summary = generate_summary(user_prompt)



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
pdf.output("reports/project_report.pdf")

# === README Generation ===
readme_content = f"""# {project_title}

**Author:** {author}  
**Date:** {date}  

## Summary
{summary.strip()}

## Features
- Automated deployment using CodePipeline & CodeBuild
- Lambda function deployment from GitHub commits
- Artifacts stored in S3

## Folder Structure
snapidox-mvp/
├── src/
├── reports/
├── screenshots/
├── assets/

bash
Copy
Edit

## Output Files
- PDF Report: `/reports/project_report.pdf`
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("✅ Snapidox MVP bootstrap complete. Report and README generated.")

#===LinkedIn post Generator===

linkedin_content = generate_linkedin_post(user_prompt)

# Save to txt file
with open("linkedin_posts/post.txt", "w", encoding="utf-8") as f:
    f.write(linkedin_content)

print("📢 LinkedIn post saved to linkedin_posts/post.txt")
