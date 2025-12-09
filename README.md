# 🎯 Productivity Coach App

A personal productivity application with AI-powered planning and weekly reviews.

## 🌟 Features

- 📅 **Daily Planning:** AI-generated personalized daily schedules
- 📊 **Weekly Reviews:** Progress analysis and feedback
- 📈 **Dashboard:** Visualizations and statistics
- 💾 **Local Storage:** SQLite database for data persistence
- 📤 **Export:** Save plans as Markdown/PDF

## 🎯 Goals

This app helps me achieve my personal goals:
- 🕌 **Quran:** Memorize 1 page/day + review
- 📖 **Islamic Studies:** Structured learning (Aqida, Fiqh, Hadith)
- 👶 **Family:** Quality time planning
- 💼 **Career:** Find remote job (portfolio building)

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.12
- **AI:** Groq API (Llama 3.1 70B)
- **Database:** SQLite
- **Environment:** Linux, venv

## 📋 Prerequisites

- Python 3.12+
- Git
- Groq API account (free tier)

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/productivity-coach.git
cd productivity-coach

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your Groq API key

# Run application
streamlit run app.py

