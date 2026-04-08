# 🤖 HR AI Agent: Smart Batch CV Screener

An intelligent, agentic HR tool built to automate resume parsing, eliminate hiring bias, and optimize the recruitment pipeline. Powered by Python, Flask, and the `gemini-2.5-flash` model.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Gemini API](https://img.shields.io/badge/Google-GenAI-orange.svg)](https://ai.google.dev/)
[![Deployed on Vercel](https://img.shields.io/badge/Deployed-Vercel-black.svg)](https://vercel.com/)

**🔗 Live Demo:** [View Live Site Here](YOUR_VERCEL_LINK_HERE)
**🎥 Project Walkthrough:** [Watch the Loom Video](YOUR_LOOM_LINK_HERE)

---

## 🌟 The Problem
Recruiters spend countless hours manually parsing hundreds of resumes, often leading to fatigue, hiring bias, and a slow "time-to-hire." Furthermore, when candidates score similarly, making objective, data-driven decisions becomes difficult without deep technical expertise.

## 🚀 The Solution
This AI-driven HR Agent processes resumes in batches, scores them dynamically against a specific Job Description, and provides actionable tools to move top candidates immediately into the interview phase.

## ✨ Key Features
* **📊 Batch Processing & Leaderboard Ranking:** Upload dozens of PDF resumes at once. The AI extracts the text directly from memory, analyzes it against the JD, and generates a ranked leaderboard based on a calculated Match Score.
* **⚖️ Head-to-Head Comparison:** Select your top two candidates and run a side-by-side comparison. The AI acts as a Hiring Manager, outlining their relative strengths, weaknesses, and providing a final, data-backed recommendation.
* **🎯 Automated Interview Scripts:** Instantly turn a candidate's "Missing Skills" into a tailored 5-7 question technical interview script, allowing non-technical HR staff to conduct rigorous screening calls.
* **📥 One-Click Manager Export:** Export the top candidates into a cleanly formatted CSV file containing ranks, scores, verified skills, and skill gaps to share with engineering managers.
* **🛡️ Blind Screening Mode:** Toggle on Unbiased Mode to instruct the AI to completely ignore names, genders, geographical locations, and university prestige, evaluating candidates strictly on merit and project experience.

## 🛠️ Tech Stack
* **Backend:** Python, Flask, PyPDF (for memory-safe PDF buffering)
* **AI Integration:** Google GenAI SDK (`gemini-2.5-flash` for high-speed, large-context parsing)
* **Frontend:** Vanilla HTML5, CSS3, JavaScript (Fetch API)
* **Deployment:** Pre-configured for serverless deployment on Vercel.

---

## 💻 Local Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/thakurmayanksingh/smart-cv-screener.git](https://github.com/thakurmayanksingh/smart-cv-screener.git)
   cd smart-cv-screener
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Create the environment
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

5. **Run the Application:**
   ```bash
   python api/index.py
   ```
   The application will be available at `http://127.0.0.1:5000/`.

---

## ☁️ Vercel Deployment Guide
This project includes a `vercel.json` configuration file, making it ready for instant deployment.

1. Push this repository to your GitHub account.
2. Log into Vercel and click **Add New Project**.
3. Import your GitHub repository.
4. Go to the **Environment Variables** section in the Vercel settings and add:
   * **Key:** `GOOGLE_API_KEY`
   * **Value:** `your_actual_api_key`
5. Click **Deploy**. Vercel will automatically detect the Flask application and host it via serverless functions.

---

## 👨‍💻 Author
**Mayank Singh** *Computer Science and Engineering Student* Passionate about building AI workflows that solve real-world operational bottlenecks.