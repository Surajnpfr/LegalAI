
# app/retrieval/embedder.py
import os
import httpx
from typing import List

class LocalEmbedder:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

    async def get_embedding(self, text: str) -> List[float]:
        """Generates dense vectors from target text string using Ollama API."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": text},
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()["embedding"]