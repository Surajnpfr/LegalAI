import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


def ask_ollama(prompt: str) -> str:
    """
    Keep your original function for raw LLM inference testing.
    """
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    response.raise_for_status()
    return response.json()["response"]


class LegalRAGEngine:
    def __init__(self):
        self.base_url = OLLAMA_URL
        self.model = OLLAMA_MODEL

    def _build_prompt(self, query: str, contexts: List[Dict[str, Any]]) -> str:
        """
        Builds a highly constrained grounding prompt in authentic Nepali.
        """
        context_str = "\n\n".join([
            f"सङ्केत व्यवस्था (Source): {c.get('law_title', 'नेपालको संविधान')}, धारा: {c.get('section_number', 'N/A')}\n"
            f"विषय: {c.get('heading', 'N/A')}\n"
            f"नियम: {c.get('content', 'N/A')}"
            for c in contexts
        ])
        
        return f"""You are a strict, professional Nepali Legal AI Assistant. Your only job is to answer the user's query using the provided verified legal context pieces.

CRITICAL INSTRUCTIONS:
1. Answer strictly in clear, grammatical, authentic Nepali language.
2. Do NOT use Hindi words or mix Indian grammatical structures (like 'के आधार पर', 'नहीं छ', 'हुकुम') under any circumstances.
3. Base your answer ONLY on the provided Context below. Do not use your own outside assumptions or training data.
4. If the provided context does not contain the explicit answer to the user's question, reply exactly with: "प्रस्तुत सामग्रीहरूमा यस प्रश्नको जवाफ फेला पार्न सकिएन।" (The answer could not be found in the provided sources). Do not make up an answer.

Context:
{context_str}

User Question: {query}
Grounded Legal Answer (in authentic Nepali with inline citations like [नेपालको संविधान, धारा: १८]):
"""

    def generate_answer(self, query: str, contexts: List[Dict[str, Any]]) -> str:
        """
        Synthesizes a legal answer grounded on the database context.
        """
        prompt = self._build_prompt(query, contexts)
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,       # Low temp keeps it focused strictly on context
                    "repeat_penalty": 1.2,    # Prevents infinite repetition loop bugs
                    "num_predict": 400        # Safe cutoff boundary for full legal expressions
                }
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["response"]