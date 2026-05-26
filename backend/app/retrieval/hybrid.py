# app/retrieval/hybrid.py
from sqlalchemy import or_
from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
from app.db.models import LegalSection  # <-- Clean import of your actual model
from app.retrieval.embedder import LocalEmbedder
from typing import List, Dict, Any

class HybridRetriever:
    def __init__(self, db_session: Session, qdrant_client: QdrantClient, embedder: LocalEmbedder):
        self.db = db_session
        self.qdrant = qdrant_client
        self.embedder = embedder
        self.collection_name = "nepali_laws"

    async def _keyword_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Performs a type-safe ORM query using your exact model definitions."""
        search_filter = f"%{query}%"
        
        results = (
            self.db.query(LegalSection)
            .filter(
                or_(
                    LegalSection.content.ilike(search_filter),
                    LegalSection.heading.ilike(search_filter)
                )
            )
            .limit(limit)
            .all()
        )
        
        return [
            {
                "id": section.id,
                "section_number": section.section_number,
                "heading": section.heading,
                "content": section.content,
                "chapter": section.chapter,
                "law_title": "नेपालको संविधान",
                "law_type": "constitution"
            }
            for section in results
        ]

    async def _semantic_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Queries Qdrant vector spaces using the modern client syntax."""
        query_vector = await self.embedder.get_embedding(query)
        
        search_result = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit
        ).points
        
        return [hit.payload for hit in search_result]

    async def search(self, query: str, limit: int = 4) -> List[Dict[str, Any]]:
        """Fuses results from keyword matches and vector search, stripping out duplicates."""
        keyword_res = await self._keyword_search(query, limit=limit)
        semantic_res = await self._semantic_search(query, limit=limit)
        
        seen_sections = set()
        combined_results = []
        
        for item in keyword_res + semantic_res:
            uid = f"{item.get('law_title')}_{item.get('section_number')}"
            if uid not in seen_sections:
                seen_sections.add(uid)
                combined_results.append(item)
                
        return combined_results[:limit]