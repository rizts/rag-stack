[![CI](https://github.com/rizts/rag-stack/actions/workflows/deploy.yml/badge.svg)](https://github.com/rizts/rag-stack/actions/workflows/deploy.yml)
[![Deploy to Railway](https://github.com/rizts/rag-stack/actions/workflows/deploy.yml/badge.svg)](https://github.com/rizts/rag-stack/actions/workflows/deploy.yml)
[![Deploy to Vercel](https://github.com/rizts/rag-stack/actions/workflows/deploy.yml/badge.svg)](https://github.com/rizts/rag-stack/actions/workflows/deploy.yml)


# 🧠 AI Knowledge Service – RAG & FastAPI

This project is a **Refactored and Production-Ready version** of the original [rizts/rag-ai-concept](https://github.com/rizts/rag-ai-concept).  
It aims to be more structured, modular, and ready for real-world deployment, with a clear separation between **Backend (FastAPI)** and **Frontend (Vite + ReactJS)**.


## 🚀 Overview

This project demonstrates a complete **AI pipeline** with:
- 🧩 **Backend (FastAPI)** — API layer, Gemini integration, and LangChain-based chunking.
- ⚛️ **Frontend (Vite + React + TypeScript)** — interactive RAG chat UI.
- 🧠 **AI Layer** — intelligent chunking, Gemini embeddings, semantic retrieval, and answer generation.
- 💾 **Vector Database (Qdrant)** — document storage and vector similarity search.
- 🚀 **CI/CD** — Railway (backend) + Vercel (frontend).


The goal is to demonstrate a production-level **Retrieval-Augmented Generation (RAG)** system that can:
1. Process documents and intelligently chunk them using **LangChain**.
2. Generate embeddings and store them in **Qdrant** Vector Database.
3. Expose APIs for semantic search and knowledge retrieval.
4. Integrate with MLOps stages to showcase AI orchestration lifecycle.

---

## 🏗️ Architecture Overview

```mermaid
graph TD
  A[📄 Document Upload] --> B[🔍 Intelligent Chunking (LangChain)]
  B --> C[🔢 Gemini Embeddings]
  C --> D[(🧠 Qdrant Vector DB)]
  E[💬 Query Request] --> F[Semantic Retrieval + Contextual Search]
  F --> G[🧠 Gemini Generative Response]
  G --> H[💡 Answer Output (React UI)]
  ```

## 🏗️ Project Setup

### 1. Install dependencies
```bash
# Backend
# Create virtual environment (recommended)
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Frontend
cd frontend
# Install dependencies
npm install
```

### 2 Run Vector Database (Qdrant)

```bash
cd backend/docker
docker compose up -d
```
Qdrant will run at http://localhost:6333

### 3. Run server

## Backend
```bash
# Backend
cd backend
uvicorn app.main:app --reload
```
Backend will run at http://localhost:8000


## Frontend
```bash
# Frontend
cd frontend
npm run dev
```
Frontend will run at http://localhost:5173


### 4. Check backend health endpoint
Open http://localhost:8000/health


### 5. Test the Integration

Open http://localhost:5173
Ask a question related to your indexed documents.
Answer will be generated based on Qdrant context retrieval.


### **Project Structure**
```bash
rag-stack/
├── backend
│   ├── app
│   │   ├── api
│   │   │   ├── health.py
│   │   │   └── rag.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   └── logger.py
│   │   ├── main.py
│   │   ├── services
│   │   │   ├── embeddings_huggingface.py
│   │   │   ├── semantic.py
│   │   │   └── vectorstore_qdrant.py
│   │   └── utils
│   │       └── chunking.py
│   ├── docker
│   │   └── docker-compose.yml
│   ├── Dockerfile
│   ├── Makefile
│   ├── pyproject.toml
│   ├── rag_stack.egg-info
│   │   ├── dependency_links.txt
│   │   ├── PKG-INFO
│   │   ├── requires.txt
│   │   ├── SOURCES.txt
│   │   └── top_level.txt
│   ├── requirements-dev.txt
│   ├── requirements.txt
│   └── tests
│       └── test_rag_basic.py
├── frontend
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   │   └── vite.svg
│   ├── README.md
│   ├── src
│   │   ├── api
│   │   │   └── rag.ts
│   │   ├── App.css
│   │   ├── App.tsx
│   │   ├── assets
│   │   │   └── react.svg
│   │   ├── components
│   │   │   ├── AnswerCard.tsx
│   │   │   └── QueryForm.tsx
│   │   ├── index.css
│   │   └── main.tsx
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
├── LICENSE
└── README.md
```

### 🔐 Environment Variables

Backend `.env.example`
```bash
# === FastAPI Configuration ===
APP_NAME=HuggingFace RAG API
APP_ENV=development
APP_PORT=8000

# === Google Gemini ===
GEMINI_API_KEY=your_google_gemini_api_key

# === HuggingFace ===
HF_API_KEY=your_hf_api_key
EMBEDDING_MODEL_NAME=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

# === Qdrant ===
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# === Frontend ===
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]

# === Railway ===
RAILWAY_TOKEN=your_railway_token

# === LangChain / Chunking Settings ===
CHUNK_SIZE=1000
CHUNK_OVERLAP=100

# === Deployment (Railway) ===
# Railway automatically injects PORT env var
# You can override below if running locally
PORT=8000
```

Frontend `.env.example`
```bash
# === Frontend Environment Variables ===
# Base URL of backend API (FastAPI on Railway)
VITE_API_BASE=http://localhost:8000

# Port for local development
VITE_PORT=5173
```

🧩 Structure Overview

- `app/api` → FastAPI routers
- `app/services` → Core business logic (semantic search, vector store)
- `app/utils` → Helper utilities (LangChain chunking)
- `app/core` → Config & logging


## 🧠 RAG API Endpoints

### 1️⃣ Index new content
```bash
curl -X POST "http://localhost:8000/rag/index" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "content=FastAPI is a Python framework for building APIs quickly."
```

Response:
```json
{"status": "indexed", "detail": {"chunks_indexed": 1}}
```

### 2️⃣ Query the knowledge base
```bash
curl -X POST "http://localhost:8000/rag/query" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "query=What is FastAPI used for?"
```

Response:
```json
{
  "query": "What is FastAPI used for?",
  "answer": "FastAPI is used to build APIs quickly and efficiently in Python.",
  "context_used": ["FastAPI is a Python framework for building APIs quickly."]
}
```

### 🚀 Deployment
🔹 Backend → Railway
Configured via `backend/.github/workflows/deploy-backend.yml`
```yaml
name: Deploy Backend to Railway

on:
  push:
    branches:
      - main
    paths:
      - "backend/**"

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Deploy to Railway
        uses: railwayapp/railway-action@v2
        with:
          railwayToken: ${{ secrets.RAILWAY_TOKEN }}
          projectId: ${{ secrets.RAILWAY_PROJECT_ID }}
          service: backend
          path: ./backend
```

🔹 Frontend → Vercel
Configured via `frontend/.github/workflows/deploy-frontend.yml`
```yaml
name: Deploy Frontend to Vercel

on:
  push:
    branches:
      - main
    paths:
      - "frontend/**"

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./frontend
          prod: true
```

Both deployments run automatically on push to the main branch.


### 🧠 AI Orchestration (RAG Flow)

| Stage          | Component       | Description                                              |
| -------------- | --------------- | -------------------------------------------------------- |
| 1️⃣ Chunking   | LangChain       | Intelligent text splitting (size + overlap configurable) |
| 2️⃣ Embedding  | Gemini          | Generate vector embeddings via Gemini API                |
| 3️⃣ Storage    | Qdrant          | Store embeddings and metadata                            |
| 4️⃣ Query      | Semantic Search | Retrieve contextually similar chunks                     |
| 5️⃣ Generation | Gemini          | Compose human-like, context-aware answers                |


### 🧪 CI/CD Overview

| Project  | Workflow              | Description         |
| -------- | --------------------- | ------------------- |
| Backend  | `ci-backend.yml`      | Lint + test FastAPI |
| Backend  | `deploy-backend.yml`  | Deploy to Railway   |
| Frontend | `ci-frontend.yml`     | Lint + build React  |
| Frontend | `deploy-frontend.yml` | Deploy to Vercel    |


### 👨‍💻 Author

[Risdy](https://linkedin.com/in/rizts)
Remote Software Engineer (since 2013)
AI & Fullstack Developer — FastAPI | React | LangChain | Gemini | HuggingFace | Qdrant
📍 Based in Indonesia

### 🏁 **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
Feel free to fork and build your own RAG experiments.

❤️ Happy coding!