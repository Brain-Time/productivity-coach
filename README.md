# 🎯 Productivity Coach - AI-Powered Personal Productivity App

An intelligent productivity application designed for busy individuals balancing multiple life goals - spiritual growth, family, career, and personal development.

**Built with AI personalization** - The app learns about you during onboarding and adapts its coaching style to your unique situation.

---

## ✨ Features

### 🤖 AI-Powered Personalization
- **Smart Onboarding**: 7 questions to understand your role, goals, and challenges
- **Adaptive Coaching**: AI generates personalized system messages based on your profile
- **Multi-Language Support**: English, Deutsch, العربية (Arabic), Français
- **Context-Aware**: Remembers your time constraints, motivation style, and focus areas

### 📅 Daily Planning
- Time-blocked schedules tailored to your available hours
- Prioritization based on your stated goals
- Realistic plans that account for real-world constraints
- Islamic productivity principles (optional, based on your preference)

### 📊 Weekly Reviews
- Progress analysis and pattern identification
- Constructive feedback (celebrates wins, suggests improvements)
- Personalized recommendations for next week
- Continuous improvement tracking

### 🌍 Multi-Language AI
- UI and AI responses in your preferred language
- Proper RTL support for Arabic
- Language-specific coaching nuances

### 💾 Local-First Architecture
- All data stored locally (SQLite)
- No cloud dependency (except AI API)
- Privacy-focused design
- Export capabilities (coming soon)

---

## 🎯 Who Is This For?

This app is designed for:
- **Parents** balancing childcare with personal goals
- **Students** managing studies and spiritual growth
- **Professionals** seeking work-life-deen balance
- **Anyone** wanting AI-powered productivity coaching

**Special focus on:**
- Islamic productivity principles
- Time management with limited availability
- Multi-role balancing (family, career, spiritual)

---

## 🛠️ Tech Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| **Frontend** | Streamlit | Rapid prototyping, Python-native |
| **AI** | Groq API (LLaMA 3.3 70B) | Fast inference, excellent quality |
| **Database** | SQLite | Local-first, no setup required |
| **Language** | Python 3.12+ | Rich ecosystem, AI-friendly |
| **Deployment** | Local (Streamlit Cloud planned) | Privacy-first approach |

---

## 📋 Prerequisites

- **Python 3.10+** (3.12 recommended)
- **Git** for version control
- **Groq API Key** (free tier available)
  - Sign up: https://console.groq.com
  - Free tier: 30 requests/minute (more than enough!)

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Brain-Time/productivity-coach.git
cd productivity-coach

2. Set Up Virtual Environment
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables
# Copy example file
cp .env.example .env

# Edit .env and add your Groq API key
# Get your key from: https://console.groq.com/keys

Your .env should look like:
GROQ_API_KEY=gsk_your_actual_key_here

5. Run the App
streamlit run app.py

The app will open in your browser at http://localhost:8501

📁 Project Structure
productivity-coach/
├── app.py                      # Main Streamlit application
├── ai_config.py               # AI models, prompts, and configuration
├── onboarding.py              # User onboarding and profile generation
├── database.py                # SQLite database operations
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
└── tests/
    ├── test_groq_api.py      # API connection tests
    └── test_groq_experiments.py  # AI behavior experiments


🔧 Configuration
AI Models
The app uses different models for different tasks:
| Feature | Model | Why? |
|---------|-------|------|
| Daily Planning | llama-3.3-70b-versatile | High quality, structured output |
| Weekly Review | llama-3.1-70b-versatile | Long context (128K tokens) |
| Quick Tasks | llama-3.1-8b-instant | Fast responses |
| Onboarding | llama-3.3-70b-versatile | Profile generation quality |
Temperature Settings
| Feature | Temperature | Behavior |
|---------|------------|----------|
| Daily Planning | 0.4 | Consistent, structured |
| Weekly Review | 0.8 | Analytical + creative |
| Motivational | 1.1 | Creative, inspiring |
All configurable in ai_config.py

🌍 Language Support
Currently supported:

🇬🇧 English - Full support
🇩🇪 Deutsch - Full support
🇸🇦 العربية (Arabic) - Full support with RTL
🇫🇷 Français - Full support

The AI responds in your chosen language, and the UI adapts accordingly.

🧪 Testing
Test AI Configuration
python ai_config.py

Test Onboarding Flow
python onboarding.py

Test Groq API Connection
python tests/test_groq_api.py

Run AI Experiments
python tests/test_groq_experiments.py


🗺️ Roadmap
✅ Phase 1: Foundation (Current)

[x] AI configuration system
[x] User onboarding flow
[x] Profile generation
[x] Multi-language support
[ ] Database implementation
[ ] Streamlit UI

🔄 Phase 2: Core Features (Next)

[ ] Daily planning interface
[ ] Weekly review system
[ ] Dashboard with visualizations
[ ] Progress tracking
[ ] Goal management

🚀 Phase 3: Enhancement (Future)

[ ] Export to Markdown/PDF
[ ] Habit tracking
[ ] Calendar integration
[ ] Mobile-responsive design
[ ] Deployment to Streamlit Cloud

💡 Phase 4: Advanced (Ideas)

[ ] Voice input (Whisper API)
[ ] Pomodoro timer integration
[ ] Community features (optional)
[ ] Offline mode
[ ] Desktop app (PyQt/Electron)


🤝 Contributing
This is a personal learning project, but contributions are welcome!
How to Contribute

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'feat: Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

Commit Convention
feat: New feature
fix: Bug fix
docs: Documentation changes
refactor: Code restructuring
test: Adding tests
chore: Maintenance tasks


📄 License
MIT License - see LICENSE file for details.
TL;DR: You can use this code for anything, including commercial projects. Just give credit!

🙏 Acknowledgments

Groq for blazing-fast AI inference
Streamlit for making Python UIs easy
LLaMA (Meta) for excellent open models
The open-source community for inspiration


👤 Author
Brain-Time

GitHub: @Brain-Time
Project: productivity-coach


📞 Support

Issues: GitHub Issues
Discussions: GitHub Discussions


🌟 Star History
If this project helps you, please consider giving it a ⭐!

📊 Project Status




Current Phase: Foundation (Phase 1)
Last Updated: December 2024
Next Milestone: Complete Streamlit UI

💭 Philosophy

"The best productivity system is the one you actually use."

This app is built on these principles:

Personalization - One size does NOT fit all
Simplicity - Complex systems fail
Privacy - Your data stays yours
Adaptability - Life changes, your system should too
Balance - Productivity without burnout


🔒 Privacy & Security

✅ Local-first: All personal data stored locally
✅ No tracking: No analytics, no telemetry
✅ API only: Only AI requests sent to Groq (no personal data)
✅ Open source: Audit the code yourself
✅ No login required: No accounts, no passwords

Your API key is stored in .env and never committed to Git.

Built with ❤️ by a parent learning to code while the baby sleeps 👶💤

"Productivity is not about doing more. It's about doing what matters."
