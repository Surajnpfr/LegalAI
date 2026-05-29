# ⚖️ Nepali Legal AI

Nepali Legal AI is an open-source, production-grade legal research and retrieval ecosystem focused on Nepali laws, constitutional frameworks, and legal knowledge. It utilizes a state-of-the-art **Hybrid Retrieval-Augmented Generation (RAG)** pipeline to deliver high-fidelity, citation-grounded legal answers natively in the Nepali language, eliminating hallucinations and ensuring real-world traceability.

### Key Capabilities:

* **Bilingual Hybrid Search:** Marries ultra-fast PostgreSQL keyword matching with deep semantic vector search via Qdrant.
* **Strict RAG Grounding Constraint:** Programmed logic layer that restricts local LLMs from fabricating legal text or slipping into linguistic cross-drift (e.g., Hindi phrases).
* **Real-time Citation Sidecar:** Interactive multi-panel user interface tracking exact source metadata blocks down to explicit section levels.
* **100% Local Deployment:** Complete privacy compliance using local databases and native local hardware GPU-accelerated inference models.

---

# 🚀 Project Status

```txt
Phase 1: Foundation (Unicode Ingestion & Relational Schema)  │  ██████████████████ 100% (Complete)
Phase 2: Vector Space (Semantic Vector Indexing Maps)        │  ██████████████████ 100% (Complete)
Phase 3: Cognitive Integration (Citation-Aware RAG Pipeline) │  ██████████████████ 100% (Complete)
Phase 4: Ecosystem & Packaging (Full Stack Containerization) │  ██████████████████ 100% (Complete)

```

* ✅ **FastAPI Backend Core Engine** (Asynchronous endpoints with complete CORS validation layout)
* ✅ **PostgreSQL Storage Layer** (Type-safe SQLAlchemy ORM relational mapping schemas)
* ✅ **Qdrant Vector Database Mapping** (Configured collections optimized for multilingual embeddings)
* ✅ **Ollama Local LLM Orchestration** (Custom prompt containment constraints utilizing Llama 3.2 3B)
* ✅ **Modern Next.js Dashboard Client** (Dark-mode responsive split-pane panel layout with dynamic context rendering)
* ✅ **Unified Multi-Stage Docker Containerization** (One-click complete network stack deployment)

---

# 🛠️ Tech Stack

### 📂 Backend Tier

* **FastAPI:** Asynchronous Python web framework for microservice routing.
* **SQLAlchemy 2.0:** Modern, type-safe Object Relational Mapper.
* **PostgreSQL 16:** Industrial-strength relational database engine.

### 🧠 Vector & AI Tier

* **Qdrant:** High-performance vector database optimizing high-dimensional text distance operations.
* **Ollama Pipeline:** Native localized machine architecture managing execution weights for **Llama 3.2 3B**.
* **Embedding Matrix Roadmaps:** Engineered to natively support `bge-m3` and `multilingual-e5` models.

### 💻 Frontend Client

* **Next.js 15+ (App Router):** Stateful modern React framework with optimized engine components.
* **TailwindCSS:** High-fidelity utility styling for strict layout compliance.

### 🐳 DevOps & Infra

* **Docker & Docker Compose:** Container abstraction wrapping application context uniformly.

---

# 🏗️ System Architecture

```txt
              ┌─────────────────────────────────────────┐
              │          Frontend (Next.js 15)          │
              └────────────────────┬────────────────────┘
                                   │  (POST /ask-legal)
                                   ▼
              ┌─────────────────────────────────────────┐
              │             FastAPI Backend             │
              └────────────────────┬────────────────────┘
                                   ▼
                   ┌───────────────────────────────┐
                   │    Hybrid Retrieval Layer     │
                   └───────┬───────────────┬───────┘
                           │               │
            (Sparse Match) ▼               ▼ (Dense Vector Match)
              ┌─────────────────┐     ┌─────────────────┐
              │  PostgreSQL DB  │     │ Qdrant Vector   │
              └─────────────────┘     └─────────────────┐
                           │               │
                           └───────┬───────┘
                                   ▼
              ┌─────────────────────────────────────────┐
              │    Retrieved Context (Top 4 Chunks)     │
              └────────────────────┬────────────────────┘
                                   ▼
              ┌─────────────────────────────────────────┐
              │    Ollama Inference (Llama 3.2 3B)      │
              │  *Strict Grounding & Language Locks* │
              └────────────────────┬────────────────────┘
                                   ▼
              ┌─────────────────────────────────────────┐
              │  Grounded Nepali Answer with Citations   │
              └─────────────────────────────────────────┘

```

---

# 📦 Project Directory Layout

```txt
nepali-legal-ai/
├── backend/
│   ├── app/
│   │   ├── api/             # Routed Endpoint Controllers
│   │   ├── db/              # SQLAlchemy Schemas, Migration Links & Seed Builders
│   │   ├── ingestion/       # Clean Unicode Text Segment Splitting Utilities
│   │   ├── llm/             # Ollama Connection Clamping & Constraint Prompt Logic
│   │   ├── retrieval/       # Hybrid Sparse/Dense Search Aggregation Frameworks
│   │   └── main.py          # Application Entrypoint & Middleware Setup
│   ├── Dockerfile           # Multi-Stage Python Runner Blueprint
│   └── requirements.txt     # Python Application Package Blueprint
├── frontend/
│   ├── app/
│   │   ├── layout.tsx       # Next.js Application Core Layout Root
│   │   ├── globals.css      # Custom Structural Tailwind Layer Bindings
│   │   └── page.tsx         # Stateful Split-Screen AI Workspace Controller
│   ├── Dockerfile           # Multi-Stage Node Node.js Build Image Manifest
│   └── package.json         # Node Client Package Map
├── data/
│   └── raw/
│       └── unicode_laws/    # Clean Source Plain-text Legal Materials (.txt)
└── docker-compose.yml       # Production-grade Orchestration Blueprint

```

---

# ⚡ Rapid Containerized Deployment (Recommended)

The entire application ecosystem—including web services, APIs, configurations, and internal database bridges—spins up instantly on any local environment using standard container orchestration.

### 1. Launch the Multi-Service Environment

Run this at the root workspace directory containing your `docker-compose.yml`:

```bash
docker compose up -d --build

```

*This fetches specialized base images, provisions isolated bridge spaces, hooks Next.js up to Node 20, and runs your app components cleanly in the background.*

### 2. Prepare the Database Architecture

Run your relational table and vector index creation scripts securely directly inside the live container sandbox:

```bash
# Provision PostgreSQL Tables
docker compose exec backend python -m app.db.init_db

# Provision Qdrant Vector Collections
docker compose exec backend python -m app.db.init_qdrant

```

### 3. Load Your Grounding Data Assets

Pass your clean text files directly into the active vector ingestion routing matrix:

```bash
# Copy host plain text into container storage space
docker cp data/raw/unicode_laws/constitution_unicode.txt legal_backend:/tmp/constitution_unicode.txt

# Execute data ingestion matrix
docker compose exec backend python -m app.ingestion.import_text_law \
  --file "/tmp/constitution_unicode.txt" \
  --title "नेपालको संविधान" \
  --type "constitution"

```

### 4. Access the Interface

Open your browser window and navigate to your fully containerized workspace:
👉 **Client Interface:** `http://localhost:3000`
👉 **API Interactive Specs:** `http://localhost:8000/docs`

---

# ⚙️ Manual Local Developer Environment Setup

If you wish to run the microservices locally outside of containers for direct workspace development loops:

### 1. Provision Your Environment Variables

Create a file named `backend/.env`:

```env
DATABASE_URL=postgresql://legal_user:legal_password@localhost:5432/nepali_legal_ai
QDRANT_URL=http://localhost:6333
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

```

### 2. Spin Up Local Databases Only

Modify your root orchestration configuration to isolate your database assets, then execute:

```bash
docker compose up -d postgres qdrant

```

### 3. Initialize Python Environment

```bash
cd backend
python -m venv venv

# Windows Activation
.\venv\Scripts\activate

# Installation
pip install -r requirements.txt

# Run Microservice Worker Local Dev Instance
uvicorn app.main:app --reload

```

### 4. Initialize Next.js Client

```bash
cd frontend
npm install
npm run dev

```

---

# 🎯 Data Grounding & Ingestion Standards

To enforce 100% reliable system responses, this architecture completely deprecates legacy font formats (e.g., Preeti encoded PDFs) to eliminate parsing garbage strings like `g]kfnsf] ;+ljwfg`. All documents enter the system as clean **UTF-8 Unicode plain text** mapped under standard structural formatting rules.

### Document Parsing Pattern Example:

```txt
धारा १८. समानताको हक: (१) सबै नागरिक कानूनको दृष्टिमा समान हुनेछन्। कसैलाई पनि कानूनको समान संरक्षणबाट वञ्चित गरिने छैन।

```

During execution loops, this string block is dynamically segmented, processed through embedding models, and mapped across both storage levels into clean structured metadata models:

```json
{
  "law_title": "नेपालको संविधान",
  "section_number": "१८",
  "heading": "समानताको हक",
  "content": "(१) सबै नागरिक कानूनको दृष्टिमा समान हुनेछन्..."
}

```

---

# 🗺️ Strategic Roadmap

### Done (Completed Milestones)

* **Phase 1:** Complete asynchronous relational model parsing and metadata structures.
* **Phase 2:** Multi-stage Docker Compose design with persistent local data volumes.
* **Phase 3:** Indentation and alignment updates inside `ollama.py` creating low-temperature prompt locks.
* **Phase 4:** Unified state tracking panels showing answers side-by-side with verified database points.

### Next (Upcoming Roadmap)

* **Multi-Document Expansion:** Bulk upload mechanics for the Civil Code (मुलुकी देवानी संहिता) and Criminal Code (मुलुकी अपराध संहिता).
* **Sub-Section Deep Chunking:** Upgraded regex parsers to prevent token spillover inside crowded clauses.
* **Dynamic Document Ingestor Dashboard:** Simple admin page allowing verified legal professionals to drop text laws onto the active collection index using a UI.

---

# ⚖️ Disclaimers & Regulatory Warning

This software ecosystem is engineered as an automated decision-support system to streamline legal document indexing, search execution, and educational verification workflows.
This tool ia solely for education purposes only.
**It does not constitute authentic legal advice.** All generative output layers are context-constrained approximations and must be verified against authoritative official government publications (*Nepal Gazette / नेपाल राजपत्र*) or audited by a licensed attorney before use in formal judicial procedures.

---

### 📄 License & Attribution

Distributed under the **MIT Open-Source License**.

Developed and engineered with passion by **Suraj Nepal**.