# 🧠 AI Knowledge Service – RAG & FastAPI

This project is a **Refactored and Production-Ready version** of the original [rizts/rag-ai-concept](https://github.com/rizts/rag-ai-concept).  
It aims to be more structured, modular, and ready for real-world deployment, with a clear separation between **Backend (FastAPI)** and **Frontend (Vite + ReactJS)**.


## 🚀 Overview

This project demonstrates a **Retrieval-Augmented Generation (RAG)** backend using:
- **FastAPI** for API endpoints
- **LangChain** for intelligent text chunking and orchestration
- **Qdrant** as the vector database
- Ready for deployment on **Railway** (backend) and **Vercel** (frontend)

The goal is to demonstrate a production-level **Retrieval-Augmented Generation (RAG)** system that can:
1. Process documents and intelligently chunk them using **LangChain**.
2. Generate embeddings and store them in **Qdrant** Vector Database.
3. Expose APIs for semantic search and knowledge retrieval.
4. Integrate with MLOps stages to showcase AI orchestration lifecycle.

## 🏗️ Project Setup

### 1. Install dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run server
```bash
uvicorn app.main:app --reload
```

### 3. Check health endpoint
Open http://localhost:8000/health


## 🐳 Run Qdrant via Docker Compose

You can run a local Qdrant vector database using docker-compose.

```bash
cd docker
docker-compose up -d
```

### **Project Structure**
```bash
rag-stack/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── logger.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── rag.py
│   ├── services/
│   │   ├── semantic.py
│   │   └── vectorstore_qdrant.py
│   └── utils/
│       └── chunking.py
├── requirements.txt
├── README.md
└── .env.example
```

🧩 Structure Overview

- `app/api` → FastAPI routers
- `app/services` → Core business logic (semantic search, vector store)
- `app/utils` → Helper utilities (LangChain chunking)
- `app/core` → Config & logging


Author: [Risdy](https://linkedin.com/in/rizts)

### **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

❤️ Happy coding!