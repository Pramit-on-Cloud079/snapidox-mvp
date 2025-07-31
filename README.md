# 🚀 Snapidox – AI-Powered AWS Project Documentation Generator

Snapidox is a lightweight AI-powered tool that automates project documentation for AWS use cases — including:

✅ GitHub README  
✅ PDF reports  
✅ LinkedIn posts  
✅ Screenshot ZIPs  
✅ Invoice (optional)


## 🌐 Try it Live

🔗 https://snapidox-mvp.onrender.com   

## 🧠 How It Works

1. User submits their AWS project summary
2. OpenAI API generates the README, LinkedIn post, PDF, and report assets
3. Flask app serves the downloadable content instantly
4. All artifacts are generated locally – no project data is stored


## 📦 Tech Stack

- **Python + Flask** (web interface)  
- **OpenAI GPT** (document generation)  
- **fpdf2** (PDF generation)  
- **Jinja2 + HTML Templates** (rendering output)  
- **Render** (deployment)


## 📁 Folder Structure

snapidox-mvp/
├── src/ # Core AI logic and file writers
├── web/ # Flask app
├── reports/ # PDF + generated assets
├── screenshots/ # Screenshot ZIPs (optional)
├── assets/ # Static images/logos
├── README.md # You're here
└── requirements.txt


## ✍️ Author

Made by **Pramit Dasgupta**  

## 🚧 Status

✅ MVP Deployed  
🟡 Early user feedback ongoing  
🔜 Public beta with login and credits model


## ⭐️ Star the Repo if you like it!

git clone https://github.com/Pramit-on-Cloud079/snapidox-mvp


## License

MIT