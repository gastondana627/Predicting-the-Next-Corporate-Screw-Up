# Zero-Dollar Production Architecture ($0.00 Stack)

> **Predicting the Next Corporate Screw-Up**  
> *Architected and developed by Gaston Dana*

[![Master Project Page](https://img.shields.io/badge/Live-Vercel%20App-teal?style=for-the-badge)](https://predicting-the-next-corporate-screw-mauve.vercel.app/)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge)](https://github.com/gastondana627/Predicting-the-Next-Corporate-Screw-Up)

---

## 🚀 Executive Summary

This document outlines how the entire ecosystem—spanning an executive frontend interface, an asynchronous serverless FastAPI backend, multi-provider API failovers, and heavy data science pipelines—was engineered and deployed to production with **zero financial capital ($0.00)**. 

By leveraging modern cloud free tiers, serverless edge runtimes, and programmatic resiliency design, this architecture proves that enterprise-grade AI applications can be launched at zero cost without sacrificing performance or reliability.

---

## 🏗️ The Zero-Dollar Stack Breakdown

| Layer | Technology | Role & Zero-Cost Strategy |
| :--- | :--- | :--- |
| **Frontend UI** | HTML5, Tailwind CSS, Vanilla JS | High-performance, responsive executive dark-mode landing page designed via Design Arena with embedded asynchronous chat interface (`RiskBot`). |
| **Backend API** | FastAPI (Python) + Mangum | Asynchronous web framework adapted for serverless execution using Mangum adapters. |
| **Serverless Host** | Vercel Serverless Functions | Instant global deployments with zero monthly maintenance overhead. |
| **AI Resiliency** | Multi-Provider Failover | Python-based rotation engine switching across free-tier quotas (`Groq`, `Gemini`, `OpenRouter`) to bypass rate limits (`429`) seamlessly. |
| **Data Science Core**| Pandas, NetworkX, Kaggle API | Processes 150 structured logs across 15 frontier models to execute the Family-Weighted Power Ranking consensus algorithm. |
| **Dev Environment** | GitHub Codespaces | Cloud-native development container running Python, Git, and Uvicorn natively in the browser. |

---

## 🔄 Resiliency & Multi-Provider Key Rotation

To prevent single-provider rate-limiting (`HTTP 429`) and guarantee 100% uptime on free tiers, the backend utilizes a dynamic failover client (`groq_rotation_client.py`). If the primary model or API key hits exhaustion, the engine automatically cycles through configured provider tokens (`GROQ_API_KEY`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`) in real time.

---

## 📂 Repository File Structure

```text
Predicting-the-Next-Corporate-Screw-Up/
├── ARCHITECTURE.md             # Zero-dollar production architecture guide
├── main.py                     # FastAPI backend app & static/chat routes
├── groq_rotation_client.py     # Multi-provider key rotation & failover engine
├── index.html                  # Executive frontend landing page & RiskBot UI
├── requirements.txt            # Python dependencies (fastapi, uvicorn, mangum, etc.)
├── vercel.json                 # Vercel serverless routing configuration
└── .gitignore                  # Security barrier protecting local .env secrets




⚙️ Local Development Setup
To spin up this ecosystem locally using GitHub Codespaces or a local terminal:

Clone the repository:

Bash
git clone [https://github.com/gastondana627/Predicting-the-Next-Corporate-Screw-Up.git](https://github.com/gastondana627/Predicting-the-Next-Corporate-Screw-Up.git)
cd Predicting-the-Next-Corporate-Screw-Up
Install dependencies:

Bash
pip install -r requirements.txt
Configure your local environment (.env):
Create a .env file in the root directory (ignored automatically by Git):

Code snippet
GROQ_API_KEY=gsk_your_primary_key_here
GEMINI_API_KEY=AIza_your_gemini_key_here
OPENROUTER_API_KEY=sk-or_your_openrouter_key_here
Run the server locally:

Bash
uvicorn main:app --reload --port 8000
☁️ Zero-Cost Vercel Deployment
Push your code repository to GitHub (ensuring .env is listed in .gitignore).

Log in to Vercel and click Import Project from your GitHub repository.

In the project build settings, expand Environment Variables and add your live keys:

GROQ_API_KEY

GEMINI_API_KEY

OPENROUTER_API_KEY

Click Deploy. Vercel will automatically compile the FastAPI application via vercel.json and provision your production URL.

📜 License & Acknowledgments
Created and maintained by Gaston Dana. All rights reserved © 2026.