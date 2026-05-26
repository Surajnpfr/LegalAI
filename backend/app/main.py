import os
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session
from qdrant_client import QdrantClient

# Database Infrastructure & Models
from app.db.database import get_db
from app.db.models import Document, LegalSection

# LLM & Retrieval Modules
from app.llm.ollama import ask_ollama, LegalRAGEngine
from app.retrieval.embedder import LocalEmbedder
from app.retrieval.hybrid import HybridRetriever

app = FastAPI(title="Nepali Legal AI")

# Cross-Origin Resource Sharing (CORS) Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Singleton Clients for Performance Efficiency
qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
embedder = LocalEmbedder()
llm_engine = LegalRAGEngine()


class AskRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Nepali Legal AI backend running",
    }


@app.post("/test-llm")
def test_llm(request: AskRequest):
    """Your legacy ungrounded prompt endpoint for testing raw Ollama output."""
    answer = ask_ollama(request.question)
    return {
        "question": request.question,
        "answer": answer,
    }


@app.get("/search")
async def search_sections(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    """
    Upgraded Search Route: Performs automated Hybrid Search.
    Fuses your original SQL ILIKE database lookup with Qdrant vector proximity.
    """
    retriever = HybridRetriever(db_session=db, qdrant_client=qdrant_client, embedder=embedder)
    results = await retriever.search(query=q, limit=15)
    
    return {
        "query": q,
        "count": len(results),
        "results": results,
    }
@app.post("/ask-legal")
async def ask_legal_rag(
    request: AskRequest,
    db: Session = Depends(get_db),
):
    """
    Advanced RAG Endpoint: Pulls relevant context pieces from Hybrid Search
    and feeds them to local Ollama to generate a grounded answer with citations.
    """
    retriever = HybridRetriever(db_session=db, qdrant_client=qdrant_client, embedder=embedder)
    contexts = await retriever.search(query=request.question, limit=4)
    
    if not contexts:
        return {
            "question": request.question,
            "answer": "तपाईंको प्रश्नसँग सम्बन्धित कुनै पनि कानूनी व्यवस्था फेला पार्न सकिएन।",
            "citations": []
        }
        
    answer = llm_engine.generate_answer(query=request.question, contexts=contexts)
    
    return {
        "question": request.question,
        "answer": answer,
        "citations": contexts
    }