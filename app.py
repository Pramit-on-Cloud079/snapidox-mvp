from flask import Flask, render_template, request, send_file
import os
from datetime import datetime
from src.utils.genai import create_linkedin_post, create_readme, generate_summary
from src.utils.genai import create_pdf


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    screenshots = request.files.getlist('screenshots')

    # ✅ Step 1: Clear all previous uploads
    for folder in os.listdir(UPLOAD_FOLDER):
        folder_path = os.path.join(UPLOAD_FOLDER, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                os.remove(os.path.join(folder_path, file))
            os.rmdir(folder_path)

    # Step 2: Create new timestamped folder
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    folder_name = os.path.join(UPLOAD_FOLDER, timestamp)
    os.makedirs(folder_name, exist_ok=True)

    # Step 3: Save screenshots
    screenshot_paths = []
    for file in screenshots:
        if file and file.filename:
            filepath = os.path.join(folder_name, file.filename)
            file.save(filepath)
            screenshot_paths.append(filepath)

    # Step 4: Generate content
    summary_text = generate_summary(prompt)
    pdf_path = os.path.join(folder_name, 'project_report.pdf')
    create_pdf(summary_text, screenshot_paths, pdf_path)

    readme_path = os.path.join(folder_name, 'README.md')
    create_readme(summary_text, readme_path)

    linkedin_post = create_linkedin_post(summary_text)

    return render_template(
        'result.html',
        summary=summary_text,
        pdf_path=pdf_path,
        readme_path=readme_path,
        linkedin_post=linkedin_post
    )

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
