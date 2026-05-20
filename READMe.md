# Nepali Legal AI

Nepali Legal AI is an open-source legal research and retrieval system focused on Nepali laws, constitutional documents, and legal knowledge.

The project is designed to support:

* legal search
* semantic retrieval
* retrieval-augmented generation (RAG)
* bilingual Nepali/English legal workflows
* local LLM inference

---

# Project Status

Current progress:

* ✅ FastAPI backend
* ✅ PostgreSQL integration
* ✅ Qdrant vector database setup
* ✅ Ollama local LLM integration
* ✅ Unicode Nepali legal text ingestion
* ✅ Legal section parsing
* ✅ Search API
* 🚧 Embeddings + semantic search
* 🚧 Hybrid retrieval
* 🚧 Citation-aware legal RAG
* 🚧 Judgment ingestion

---

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* Qdrant

## AI / NLP

* Ollama
* Llama 3.2 3B
* Future embedding models:

  * bge-m3
  * multilingual-e5

## Frontend

* Next.js
* TailwindCSS

## Infrastructure

* Docker
* Docker Compose

---

# Architecture

```txt
Frontend (Next.js)
        ↓
FastAPI Backend
        ↓
Hybrid Retrieval Layer
    ├── PostgreSQL Keyword Search
    └── Qdrant Semantic Search
        ↓
Retrieved Legal Sections
        ↓
Local LLM (Ollama)
        ↓
Legal Response with Citations
```

---

# Current Features

## Legal Text Ingestion

Supports:

* Unicode Nepali legal text
* Section splitting
* Legal metadata extraction

Example:

```txt
धारा १६. सम्मानपूर्वक बाँच्न पाउने हक:
...
```

is parsed into:

```json
{
  "section_number": "१६",
  "heading": "सम्मानपूर्वक बाँच्न पाउने हक",
  "content": "..."
}
```

---

# Search API

Example:

```http
GET /search?q=न्याय
```

Response:

```json
{
  "query": "न्याय",
  "count": 1,
  "results": [...]
}
```

---

# Project Structure

```txt
nepali-legal-ai/
│
├── backend/
│   ├── app/
│   │   ├── db/
│   │   ├── ingestion/
│   │   ├── llm/
│   │   ├── retrieval/
│   │   └── main.py
│   │
│   └── venv/
│
├── frontend/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── unicode_laws/
│
├── docker-compose.yml
└── README.md
```

---

# Setup

## 1. Clone repository

```bash
git clone <repo-url>
cd nepali-legal-ai
```

---

# 2. Backend Setup

```bash
cd backend

python -m venv venv
```

### Windows

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv qdrant-client requests pymupdf
```

---

# 3. Docker Services

Run PostgreSQL + Qdrant:

```bash
docker compose up -d
```

Check:

```bash
docker ps
```

---

# 4. Ollama Setup

Install Ollama:

https://ollama.com/

Pull model:

```bash
ollama pull llama3.2:3b
```

Run:

```bash
ollama run llama3.2:3b
```

---

# 5. Environment Variables

Create:

```txt
backend/.env
```

```env
DATABASE_URL=postgresql://legal_user:legal_password@localhost:5432/nepali_legal_ai

OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

QDRANT_URL=http://localhost:6333
```

---

# 6. Initialize Database

```bash
python -m app.db.init_db
```

---

# 7. Run Backend

```bash
python -m uvicorn app.main:app --reload
```

Open:

```txt
http://127.0.0.1:8000/docs
```

---

# Unicode Legal Text Ingestion

Place Unicode legal text files inside:

```txt
data/raw/unicode_laws/
```

Example format:

```txt
धारा १. संविधान मूल कानून:
...
```

Import:

```bash
python -m app.ingestion.import_text_law \
  --file "../data/raw/unicode_laws/constitution_unicode.txt" \
  --title "नेपालको संविधान" \
  --type "constitution"
```

---

# PDF Ingestion Status

PDF ingestion is experimental.

Current challenge:

* Many Nepali legal PDFs use Preeti encoding
* Direct PDF extraction often produces corrupted text

Example:

```txt
g]kfnsf] ;+ljwfg
```

instead of:

```txt
नेपालको संविधान
```

Future improvements:

* Preeti → Unicode conversion
* OCR pipeline
* HTML ingestion
* PDF normalization

---

# Roadmap

## Phase 1

* Unicode law ingestion
* Search API
* Database structure

## Phase 2

* Embeddings
* Qdrant indexing
* Semantic retrieval

## Phase 3

* Hybrid retrieval
* Citation-aware RAG
* Legal answer generation

## Phase 4

* Judgment ingestion
* Lawyer review workflow
* Fine-tuning
* Production deployment

---

# Important Notes

This project is intended for:

* legal research
* educational purposes
* retrieval assistance

It is NOT legal advice.

Always verify legal outputs with authoritative legal sources and qualified professionals.

---

# License

MIT License

---

# Author

Built by Suraj Nepal
