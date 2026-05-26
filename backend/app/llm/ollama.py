# app/llm/ollama.py
import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


# Keep your original function for raw LLM inference testing
def ask_ollama(prompt: str) -> str:
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


# Add the class that app/main.py needs for context parsing
class LegalRAGEngine:
    def __init__(self):
        self.base_url = OLLAMA_URL
        self.model = OLLAMA_MODEL

    def _build_prompt(self, query: str, contexts: List[Dict[str, Any]]) -> str:
        context_str = ""
        for i, ctx in enumerate(contexts, 1):
            context_str += f"[{i}] दस्तावेज: {ctx.get('law_title')} | दफा/धारा: {ctx.get('section_number')} ({ctx.get('heading')})\n"
            context_str += f"विवरण: {ctx.get('content')}\n\n"

        return f"""
तपाईं एक विशेषज्ञ नेपाली कानूनी एआई सहायक हुनुहुन्छ। तल दिइएको आधिकारिक कानूनी दस्तावेजहरूको सन्दर्भ (Context) प्रयोग गरेर प्रयोगकर्ताको प्रश्नको उत्तर दिनुहोस्।

नियमहरू:
१. तपाईंको उत्तर पूर्ण रूपमा प्रदान गरिएको सन्दर्भ (Context) मा मात्र आधारित हुनुपर्दछ। आफ्नो मनबाट कुनै तथ्य थप नगर्नुहोस्।
२. उत्तर दिँदा अनिवार्य रूपमा ऐन, धारा वा दफाको नाम कोष्ठक भित्र उल्लेख (Citation) गर्नुहोस् (जस्तै: [नेपालको संविधान, धारा १८]).
३. यदि सन्दर्भमा उत्तर स्पष्ट छैन भने, "प्रदान गरिएको कानूनी दस्तावेजमा यसको जवाफ फेला परेन।" भन्नुहोस्।

सन्दर्भ दस्तावेजहरू:
{context_str}

प्रयोगकर्ताको प्रश्न: {query}

कानूनी जवाफ (Citations सहित):
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
                    "temperature": 0.1,       # Low temp keeps it focused on context
                    "repeat_penalty": 1.2,    # Prevents infinite repetition loop bugs
                    "num_predict": 300        # Cuts off text generation safely if it wanders
                }
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["response"]