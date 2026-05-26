# app/ingestion/import_text_law.py
import argparse
import asyncio
import os
from pathlib import Path
from qdrant_client import QdrantClient

from app.db.database import SessionLocal
from app.db.models import Document, LegalSection
from app.ingestion.text_cleaner import clean_text
from app.ingestion.section_splitter import split_sections
from app.retrieval.embedder import LocalEmbedder


async def sync_to_qdrant(legal_sections, title, document_type):
    """Generates embeddings using Ollama and pushes them to Qdrant in background."""
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    q_client = QdrantClient(url=qdrant_url)
    embedder = LocalEmbedder()
    
    print("\nStarting Qdrant vector embedding indexing...")
    
    for idx, sec in enumerate(legal_sections, 1):
        try:
            # Create a rich contextual string for dense vector search matching
            text_payload = f"दस्तावेज: {title} | प्रकार: {document_type} | दफा/धारा: {sec.section_number} | शीर्षक: {sec.heading} | विवरण: {sec.content}"
            
            # Generate the embedding vectors using local Ollama model
            vector_data = await embedder.get_embedding(text_payload)
            
            q_client.upsert(
                collection_name="nepali_laws",
                points=[
                    {
                        "id": sec.id,  # Maps directly to the generated Postgres primary key
                        "vector": vector_data,
                        "payload": {
                            "law_title": title,
                            "section_number": sec.section_number,
                            "heading": sec.heading,
                            "content": sec.content,
                            "law_type": document_type
                        }
                    }
                ]
            )
            if idx % 10 == 0 or idx == len(legal_sections):
                print(f"Indexed {idx}/{len(legal_sections)} sections to Qdrant...")
        except Exception as e:
            print(f"[Warning] Failed to index section {sec.section_number} to Qdrant: {e}")


def import_text_law(
    file_path: str,
    title: str,
    document_type: str = "law",
    language: str = "ne",
    source_url: str = "local_file",
):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    raw_text = path.read_text(encoding="utf-8")
    cleaned_text = clean_text(raw_text)
    sections = split_sections(cleaned_text)

    if not sections:
        raise ValueError("No sections found. Check section format.")

    db = SessionLocal()

    existing = db.query(Document).filter(Document.title == title).first()

    if existing:
        # Note: Depending on your Cascade rules, you might want to ensure 
        # that associated LegalSections are deleted when a document is dropped.
        db.delete(existing)
        db.commit()

    document = Document(
        title=title,
        document_type=document_type,
        language=language,
        source_url=source_url,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    legal_sections = []

    for section in sections:
        legal_sections.append(
            LegalSection(
                document_id=document.id,
                section_number=section["section_number"],
                heading=section["heading"],
                chapter=section.get("chapter"),
                content=section["content"],
            )
        )

    # Bulk save to relational database
    db.add_all(legal_sections)
    db.commit()
    
    # Refresh items to guarantee SQLAlchemy pulls back the newly created autoincrement ID keys
    for sec in legal_sections:
        db.refresh(sec)

    print(f"Imported document: {title}")
    print(f"Sections imported to Postgres: {len(legal_sections)}")

    # Trigger asynchronous Qdrant sync worker safely inside our synchronous module runtime
    asyncio.run(sync_to_qdrant(legal_sections, title, document_type))

    db.close()
    print("Ingestion sequence successfully executed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--type", default="law")
    parser.add_argument("--language", default="ne")
    parser.add_argument("--source-url", default="local_file")

    args = parser.parse_args()

    import_text_law(
        file_path=args.file,
        title=args.title,
        document_type=args.type,
        language=args.language,
        source_url=args.source_url,
    )