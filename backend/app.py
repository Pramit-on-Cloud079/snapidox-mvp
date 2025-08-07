from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import shutil
from datetime import datetime
import sys

# Enable importing from root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

from src.utils.genai import generate_summary_and_title, generate_tech_features_arch
from backend.private_core.generator import generate_detailed_pdf

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)
CORS(app)

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
GENERATED_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'generated'))
ALLOWED_EXTENSIONS = {'txt', 'md', 'py'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_input = data.get('prompt', '').strip()
    github_url = data.get('repo_url') or data.get('github_url')  # support both keys

    if not user_input and not github_url:
        return jsonify({'error': 'No input provided'}), 400

    # 🔥 Clear previous files
    for folder in [UPLOAD_FOLDER, GENERATED_FOLDER]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

    content_input = github_url if github_url else user_input
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    session_dir = os.path.join(UPLOAD_FOLDER, timestamp)
    os.makedirs(session_dir, exist_ok=True)

    # 🧠 AI Content
    title, summary = generate_summary_and_title(content_input)
    tech_stack, features, architecture = generate_tech_features_arch(content_input)

    # 🧼 Remove duplicate section headers (if any) from summary text only
    section_keywords = ["Tech Stack", "Features", "Architecture", "🔧", "🚀", "🧠"]
    for word in section_keywords:
        summary = summary.replace(word, "").strip()

    # 🧾 PDF Filename
    clean_title = title.replace("📌", "").replace('"', "").strip()

    watermark = "🔗 Generated with Snapidox — https://github.com/Pramit-on-Cloud079/snapidox-mvp"

    linkedin_post = f"""📢 {title}

📝 {summary}

🔧 Tech Stack:
{tech_stack}

🚀 Features:
{features}

🧠 Architecture:
{architecture}

{watermark}"""

    # 📄 Markdown Output
    md_filename = f"report_{timestamp}.md"
    md_path = os.path.join(GENERATED_FOLDER, md_filename)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n{summary}\n\n## 🔧 Tech Stack\n{tech_stack}\n\n## 🚀 Features\n{features}\n\n## 🧠 Architecture\n{architecture}\n\n{watermark}")

    # 📄 PDF Output
    pdf_filename = f"report_{timestamp}.pdf"
    pdf_path = os.path.join(GENERATED_FOLDER, pdf_filename)
    generate_detailed_pdf(clean_title, summary, tech_stack, features, architecture, pdf_path)

    return jsonify({
        'message': 'Report generated successfully',
        'markdown_filename': md_filename,
        'pdf_filename': pdf_filename,
        'title': title,
        'summary': summary,
        'tech_stack': tech_stack,
        'features': features,
        'architecture': architecture,
        'linkedin_post': linkedin_post
    })


@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/download/pdf', methods=['GET'])
def download_pdf():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({'error': 'No PDF filename specified'}), 400
    full_path = os.path.join(GENERATED_FOLDER, filename)
    if not os.path.exists(full_path):
        return jsonify({'error': 'PDF not found'}), 404
    return send_file(full_path, as_attachment=True)

@app.route('/download/md', methods=['GET'])
def download_md():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({'error': 'No Markdown filename specified'}), 400
    full_path = os.path.join(GENERATED_FOLDER, filename)
    if not os.path.exists(full_path):
        return jsonify({'error': 'Markdown not found'}), 404
    return send_file(full_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
