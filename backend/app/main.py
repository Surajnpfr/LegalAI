from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Document, LegalSection
from app.llm.ollama import ask_ollama

app = FastAPI(title="Nepali Legal AI")


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
    answer = ask_ollama(request.question)

    return {
        "question": request.question,
        "answer": answer,
    }


@app.get("/search")
def search_sections(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    results = (
        db.query(LegalSection)
        .join(Document)
        .filter(
            or_(
                LegalSection.content.ilike(f"%{q}%"),
                LegalSection.heading.ilike(f"%{q}%"),
                LegalSection.chapter.ilike(f"%{q}%"),
                LegalSection.section_number.ilike(f"%{q}%"),
                Document.title.ilike(f"%{q}%"),
            )
        )
        .limit(20)
        .all()
    )

    return {
        "query": q,
        "count": len(results),
        "results": [
            {
                "id": section.id,
                "document": section.document.title,
                "document_type": section.document.document_type,
                "section_number": section.section_number,
                "chapter": section.chapter,
                "heading": section.heading,
                "content": section.content,
                "source_url": section.document.source_url,
            }
            for section in results
        ],
    }