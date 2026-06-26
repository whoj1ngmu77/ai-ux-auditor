# 🔍 AI UX Auditor

An autonomous multi-agent AI system that audits any website for UX and accessibility issues and generates a professional report — in under 2 minutes.

## 🌐 Live Demo
- **Frontend:** https://ai-ux-auditor-five.vercel.app
- **Backend:** https://ai-ux-auditor-backend-lexb.onrender.com

## 🎥 How It Works
1. Paste any website URL
2. Four AI agents autonomously analyze the site
3. Get a scored report with actionable fixes + export as PDF

## 🤖 Multi-Agent Pipeline (LangGraph)

| Agent | Role |
|---|---|
| Browser Agent | Playwright crawls the site, takes desktop + mobile screenshots |
| UX Analyst | Groq Vision (Llama 4 Scout) analyzes screenshots for UX issues |
| Accessibility Checker | Scans raw HTML against WCAG 2.1 rules |
| Report Generator | Groq (Llama 3.3 70B) synthesizes findings into actionable report |

## 🛠️ Tech Stack

**Backend**
- FastAPI + LangGraph
- Playwright (autonomous browser)
- Groq API (Llama 4 Scout vision + Llama 3.3 70B)
- BeautifulSoup4 (HTML accessibility parsing)
- Docker + Render

**Frontend**
- Next.js 15 + TypeScript
- Tailwind CSS + Framer Motion
- Recharts (score visualizations)
- jsPDF (PDF export)
- Vercel

## ✨ Features
- 🌐 Audits any public website autonomously
- 👁️ Visual UX analysis via AI vision on real screenshots
- ♿ WCAG 2.1 accessibility compliance checking
- 📊 Scored report (Overall, UX, Accessibility)
- 📋 Top 5 prioritized fixes
- 📄 Export full report as PDF
- 📱 Desktop + mobile view analysis

## 🚀 Run Locally

**Backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
uvicorn app.main:app --reload --port 8000
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

**Environment Variables**

Backend `.env`:
```
GROQ_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

Frontend `.env.local`:
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## 📁 Project Structure
```
ai-ux-auditor/
├── backend/
│   └── app/
│       ├── agents/
│       │   ├── browser_agent.py       # Playwright crawler
│       │   ├── ux_analyst.py          # Groq Vision analysis
│       │   ├── accessibility_agent.py # WCAG checker
│       │   └── report_agent.py        # Report synthesis
│       ├── graph/
│       │   └── pipeline.py            # LangGraph StateGraph
│       ├── routes/
│       │   └── audit.py               # FastAPI endpoint
│       └── models/
│           └── schemas.py             # Pydantic models
└── frontend/
    └── app/
        ├── page.tsx                   # URL input page
        ├── results/page.tsx           # Audit dashboard
        └── components/
            └── AuditReport.tsx        # PDF export
```
