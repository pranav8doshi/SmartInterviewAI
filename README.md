
# SmartInterviewAI 🧠🎤

**A Smart AI-Powered Interview System** that evaluates answers, analyzes posture, and generates detailed reports using LLMs and speech recognition.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🔍 Overview

SmartInterviewAI is a Flask-based application designed to conduct automated interviews using:
- 🤖 LLM-based Question Generation & Scoring
- 🗣️ Speech-to-Text with Google Speech API
- 🧍 Posture & Attention Analysis
- 📄 Auto-generated interview reports

---

## 🗂 Project Structure

```
SMARTINTERVIEWAI-MAIN/
├── app.py                      # Main Flask backend
├── .env                        # Environment variables (API keys, etc.)
├── static/                     # CSS, JS, media assets
│   ├── css/styles.css
│   ├── js/scripts.js
│   └── ai.mp4
├── templates/                  # HTML templates
│   ├── index.html
│   ├── interview.html
│   ├── meeting.html
│   └── result.html
├── logs/                       # Interview reports and summaries
│   ├── summary.txt
│   └── Software_Engineer/
├── interview_questions.json    # Predefined role-based questions
├── posture_analysis.log        # Log of posture detection
├── requirements.txt            # Python dependencies
├── apt.txt                     # System packages (if applicable)
└── vercel.json                 # Deployment config
```

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.10+
- `pip` (Python package manager)
- Microphone Access
- Internet Connection (for API calls)

### 🔧 Installation

```bash
git clone https://github.com/pranav8doshi/SmartInterviewAI
cd SmartInterviewAI
pip install -r requirements.txt
```

Make sure to create a `.env` file:

```bash
TOGETHER_API_KEY=your_together_api_key_here
```

---

## ▶️ Running the App

```bash
python app.py
```

Open browser at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ✨ Features

- AI-generated and scored interview questions (via Together's LLaMA API)
- Voice interaction using Google Speech-to-Text and `pyttsx3`
- Dynamic follow-up questions
- Real-time posture and attention analysis
- Log and report generation

---

## 🧪 Testing the Flow

1. Open `/` — start interface
2. Submit your name and role
3. Answer AI questions via microphone
4. See generated report after completion at `/result`

---

## ⚙️ Deployment

The app can be deployed on services like:
- [Vercel (with vercel.json)](https://vercel.com)
- [Render](https://render.com)
- [Heroku](https://heroku.com)

---

## 📜 License

MIT © 2025 Pranav Doshi

---

## 🙏 Acknowledgements

- [Together API](https://www.together.ai/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [OpenAI](https://openai.com/)
- [Flask](https://flask.palletsprojects.com/)
