[![CI/CD Pipeline](https://github.com/rizts/rag-stack/actions/workflows/deploy.yml/badge.svg)](https://github.com/rizts/rag-stack/actions/workflows/deploy.yml)

# 🧠 AI Knowledge Service — RAG & FastAPI

This project is a **Refactored and Production-Ready version** of the original [rizts/rag-ai-concept](https://github.com/rizts/rag-ai-concept).  
It aims to be more structured, modular, and ready for real-world deployment, with a clear separation between **Backend (FastAPI)** and **Frontend (Vite + ReactJS)**.

**🔗 Live Demo:**
- Frontend: [Deployed on Vercel](https://your-app.vercel.app)
- Backend API: [Deployed on Railway](https://rag-stack-production.up.railway.app)

---

## 🚀 Overview

This project demonstrates a complete **AI pipeline** with:
- 🧩 **Backend (FastAPI)** — API layer, Gemini integration, and LangChain-based chunking.
- ⚛️ **Frontend (Vite + React + TypeScript)** — interactive RAG chat UI.
- 🧠 **AI Layer** — intelligent chunking, HuggingFace embeddings, semantic retrieval, and Gemini answer generation.
- 💾 **Vector Database (Qdrant Cloud)** — document storage and vector similarity search.
- 🚀 **CI/CD** — Automated deployment via GitHub Actions to Railway (backend) + Vercel (frontend).

The goal is to demonstrate a production-level **Retrieval-Augmented Generation (RAG)** system that can:
1. Process documents and intelligently chunk them using **LangChain**.
2. Generate embeddings using **HuggingFace models** and store them in **Qdrant** Vector Database.
3. Expose APIs for semantic search and knowledge retrieval.
4. Integrate with modern DevOps practices to showcase AI orchestration lifecycle.

---

## 🏗️ Architecture Overview

```mermaid
graph TD
  A[📄 Document Upload] --> B[🔍 Intelligent Chunking LangChain]
  B --> C[🔢 HuggingFace Embeddings]
  C --> D[(🧠 Qdrant Vector DB)]
  E[💬 Query Request] --> F[Semantic Retrieval + Contextual Search]
  F --> G[🧠 Gemini Generative Response]
  G --> H[💡 Answer Output React UI]
```

---

## 🗂️ Project Structure

```
rag-stack/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD configuration
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── health.py       # Health check endpoint
│   │   │   └── rag.py          # RAG endpoints (index, query)
│   │   ├── core/
│   │   │   ├── config.py       # Centralized configuration
│   │   │   └── logger.py       # Logging setup
│   │   ├── services/
│   │   │   ├── embeddings_huggingface.py  # HuggingFace embeddings
│   │   │   ├── semantic.py     # Semantic search logic
│   │   │   └── vectorstore_qdrant.py      # Qdrant integration
│   │   ├── utils/
│   │   │   └── chunking.py     # LangChain text chunking
│   │   └── main.py             # FastAPI application
│   ├── tests/
│   │   └── test_rag_basic.py   # Unit tests
│   ├── Dockerfile
│   ├── requirements.txt
│   └── requirements-dev.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── rag.ts          # API client
│   │   ├── components/
│   │   │   ├── AnswerCard.tsx  # Answer display
│   │   │   └── QueryForm.tsx   # Query input form
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── vercel.json             # Vercel configuration
└── README.md
```

---

## 🛠️ Local Development Setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker (for local Qdrant)
- Git

### 1. Clone Repository

```bash
git clone https://github.com/rizts/rag-stack.git
cd rag-stack
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and add your API keys:
# - GEMINI_API_KEY
# - HF_API_KEY
# - QDRANT_URL (use localhost for local dev)
```

### 3. Run Qdrant (Local Development)

```bash
cd backend/docker
docker compose up -d
```

Qdrant will run at `http://localhost:6333`

### 4. Run Backend

```bash
cd backend
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`

Check health: `http://localhost:8000/health`

### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Edit .env:
# VITE_API_BASE=http://localhost:8000
```

### 6. Run Frontend

```bash
npm run dev
```

Frontend runs at `http://localhost:5173`

---

## 🌐 Production Deployment

### CI/CD Pipeline

This project uses **GitHub Actions** for automated deployment:

#### Workflow Overview

```yaml
Trigger: Push to main or Pull Request
├── 1. Detect Changes (backend/frontend/both)
├── 2. Run Tests
│   ├── Backend: pytest
│   └── Frontend: lint + build
├── 3. Deploy Backend (if backend changed)
│   └── Railway auto-deploys via GitHub integration
└── 4. Deploy Frontend (if frontend changed)
    └── Vercel deployment via CLI
```

#### Setup Instructions

**1. Railway Setup (Backend)**

- Sign up at [railway.app](https://railway.app)
- Create new project → Connect GitHub repo
- Configure:
  - Root Directory: `backend`
  - Builder: `Dockerfile`
  - Add environment variables (see below)
- Generate domain in Settings → Networking

**2. Vercel Setup (Frontend)**

```bash
cd frontend
vercel login
vercel link
```

Get credentials from `.vercel/project.json`:
- `orgId` → `VERCEL_ORG_ID`
- `projectId` → `VERCEL_PROJECT_ID`

Generate token: [vercel.com/account/tokens](https://vercel.com/account/tokens)

**3. GitHub Secrets**

Add these secrets in **Settings → Secrets and variables → Actions**:

```
VERCEL_TOKEN=xxx
VERCEL_ORG_ID=team_xxx
VERCEL_PROJECT_ID=prj_xxx
```

**4. Environment Variables**

**Railway (Backend):**
```bash
GEMINI_API_KEY=your_key
HF_API_KEY=your_key
QDRANT_URL=https://your-cluster.cloud.qdrant.io:6333
QDRANT_API_KEY=your_key
CORS_ORIGINS=https://your-app.vercel.app
ENVIRONMENT=production
```

**Vercel (Frontend):**
```bash
VITE_API_BASE=https://rag-stack-production.up.railway.app
```

---

## 📝 Environment Variables

### Backend (`.env`)

```bash
# FastAPI Configuration
APP_NAME=RAG AI Backend
ENVIRONMENT=development
APP_PORT=8000

# Google Gemini
GEMINI_API_KEY=your_gemini_api_key

# HuggingFace
HF_API_KEY=your_hf_api_key
EMBEDDING_MODEL_NAME=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Chunking
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
```

### Frontend (`.env`)

```bash
# API Configuration
VITE_API_BASE=http://localhost:8000

# Port
VITE_PORT=5173
```

---

## 🧠 RAG API Endpoints

### 1️⃣ Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "ok"}
```

### 2️⃣ Index Content

```bash
curl -X POST "http://localhost:8000/rag/index" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "content=FastAPI is a modern Python web framework for building APIs."
```

Response:
```json
{
  "status": "indexed",
  "detail": {
    "chunks_indexed": 1
  }
}
```

### 3️⃣ Query Knowledge Base

```bash
curl -X POST "http://localhost:8000/rag/query" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "query=What is FastAPI?"
```

Response:
```json
{
  "query": "What is FastAPI?",
  "answer": "FastAPI is a modern Python web framework designed for building APIs quickly and efficiently...",
  "context_used": ["FastAPI is a modern Python web framework..."]
}
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm run lint
npm run build
```

---

## 🎯 Key Features

### Smart Path-Based Deployment

The CI/CD pipeline intelligently detects changes:

- **Backend changes** → Tests + Railway auto-deploy
- **Frontend changes** → Tests + Vercel deploy
- **Root changes** → Run all tests

This saves GitHub Actions minutes and speeds up deployment!

### Preview Deployments

Pull requests automatically get preview deployments:
- Frontend preview on Vercel
- Comments in PR with preview URL

---

## 🧩 Tech Stack

| Layer          | Technology                    |
| -------------- | ----------------------------- |
| Backend        | FastAPI, Python 3.11          |
| Frontend       | React 18, TypeScript, Vite    |
| AI/ML          | LangChain, Google Gemini      |
| Embeddings     | HuggingFace Transformers      |
| Vector DB      | Qdrant Cloud                  |
| Deployment     | Railway (backend), Vercel     |
| CI/CD          | GitHub Actions                |
| Containerization | Docker                      |

---

## 🔄 RAG Pipeline Flow

| Stage          | Component       | Description                                              |
| -------------- | --------------- | -------------------------------------------------------- |
| 1️⃣ Chunking   | LangChain       | Intelligent text splitting (size + overlap configurable) |
| 2️⃣ Embedding  | HuggingFace     | Generate vector embeddings                               |
| 3️⃣ Storage    | Qdrant Cloud    | Store embeddings and metadata                            |
| 4️⃣ Query      | Semantic Search | Retrieve contextually similar chunks                     |
| 5️⃣ Generation | Gemini          | Compose human-like, context-aware answers                |

---

## 🚀 Deployment Checklist

- [ ] Set up Railway account & project
- [ ] Configure Railway environment variables
- [ ] Set up Vercel account & link project
- [ ] Add GitHub secrets (Vercel tokens)
- [ ] Update `BACKEND_URL` in workflow
- [ ] Update `VITE_API_BASE` in Vercel settings
- [ ] Test local development
- [ ] Push to main → Verify deployments
- [ ] Create PR → Test preview deployment

---

## 📊 Monitoring

- **Railway:** Built-in logs and metrics dashboard
- **Vercel:** Analytics and deployment logs
- **GitHub Actions:** Workflow runs and job details

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**[Risdy](https://linkedin.com/in/rizts)**  
Remote Software Engineer (since 2013)  
AI & Fullstack Developer — FastAPI | React | LangChain | Gemini | HuggingFace | Qdrant  
📍 Based in Indonesia

---

## 🙏 Acknowledgments

- Original concept: [rag-ai-concept](https://github.com/rizts/rag-ai-concept)
- Built with modern AI/ML frameworks
- Deployed with cloud-native infrastructure

---

**⭐ If you find this project useful, please give it a star!**

❤️ Happy coding!