# 🔬 Research Agent — IBM Granite

An AI-powered academic research assistant that uses **IBM Watson Machine Learning** 
with the **IBM Granite 13B Instruct** foundation model to help researchers:

- 🔍 Search and retrieve academic papers (Semantic Scholar + arXiv)
- 🤖 Summarize papers using IBM Granite AI
- 🧠 Generate novel research hypotheses
- 📄 Draft full research reports section by section
- 📚 Format citations in APA, MLA, and IEEE

---

## 🏗 Architecture

```
research-agent/
├── backend/                    # FastAPI + IBM Granite
│   ├── app.py                  # Main API application
│   ├── services/
│   │   ├── granite_service.py  # IBM WML / Granite integration
│   │   ├── search_service.py   # Semantic Scholar + arXiv
│   │   ├── citation_service.py # APA / MLA / IEEE formatting
│   │   └── report_service.py   # Report generation via Granite
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                   # React SPA
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── Sidebar.jsx
│   │   │   ├── SearchPanel.jsx
│   │   │   ├── ResultsPanel.jsx
│   │   │   ├── ReportPanel.jsx
│   │   │   └── CitationPanel.jsx
│   │   └── styles/App.css
│   ├── public/index.html
│   ├── package.json
│   └── Dockerfile
│
├── tests/
│   └── test_services.py
├── docs/
│   └── IBM_SETUP.md
├── docker-compose.yml
└── README.md
```

---

## ⚙️ IBM Cloud Setup (Required)

Follow **`docs/IBM_SETUP.md`** for a complete walkthrough. Quick summary:

1. Create a free IBM Cloud account: https://cloud.ibm.com/registration
2. Provision **Watson Studio** (Lite plan, free)
3. Provision **Watson Machine Learning** (Lite plan, free)
4. Create a **Project** in Watson Studio and copy the Project ID
5. Generate an **API Key** from IAM → Service credentials
6. Copy `backend/.env.example` → `backend/.env` and fill in your credentials

---

## 🚀 Running Locally

### Option A — Docker Compose (recommended)

```bash
# 1. Clone and enter the project
cd research-agent

# 2. Set up credentials
cp backend/.env.example backend/.env
# Fill in IBM_API_KEY and IBM_PROJECT_ID in .env

# 3. Build and run
docker-compose up --build
```

Open http://localhost:3000

### Option B — Manual

**Backend**
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # fill in your IBM credentials
uvicorn app:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm start
```

---

## 🔌 API Endpoints

| Method | Endpoint          | Description                              |
|--------|-------------------|------------------------------------------|
| POST   | `/api/research`   | Search papers + Granite AI summaries     |
| POST   | `/api/summarize`  | Summarize any text with Granite          |
| POST   | `/api/hypotheses` | Generate research hypotheses             |
| POST   | `/api/citation`   | Format a citation (APA / MLA / IEEE)     |
| POST   | `/api/report`     | Generate a full report draft             |
| GET    | `/api/health`     | Health check                             |

**Example — Search request:**
```json
POST /api/research
{
  "query": "transformer models in genomics",
  "max_results": 8,
  "output_format": "summary"
}
```

---

## 🧪 Running Tests

```bash
cd research-agent
pip install pytest pytest-asyncio
pytest tests/ -v
```

---

## 📋 IBM Granite Model Used

| Property    | Value                             |
|-------------|-----------------------------------|
| Model ID    | `ibm/granite-13b-instruct-v2`     |
| Provider    | IBM Watson Machine Learning (WML) |
| Plan        | Lite (free tier)                  |
| Region      | us-south (default)                |

---

## 🛠 Tech Stack

- **AI**: IBM Granite 13B Instruct via IBM Watson ML
- **Backend**: Python 3.11, FastAPI, httpx
- **Frontend**: React 18, Axios, react-markdown
- **Literature APIs**: Semantic Scholar, arXiv
- **Deployment**: Docker Compose
