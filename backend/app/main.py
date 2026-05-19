from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.llm.ollama import ask_ollama

app = FastAPI(title="Nepali Legal AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"status": "ok", "message": "Nepali Legal AI backend running"}


@app.post("/test-llm")
def test_llm(request: AskRequest):
    answer = ask_ollama(request.question)
    return {"question": request.question, "answer": answer}