from app.ingestion.preeti_converter import preeti_to_unicode
import argparse
from pathlib import Path

from app.db.database import SessionLocal
from app.db.models import Document, LegalSection
from app.ingestion.pdf_extractor import extract_text_from_pdf
from app.ingestion.text_cleaner import clean_text
from app.ingestion.section_splitter import split_sections


def import_pdf_law(
    file_path: str,
    title: str,
    document_type: str = "law",
    language: str = "ne",
    source_url: str = "local_pdf",
):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    raw_text = extract_text_from_pdf(str(path))
    unicode_text = preeti_to_unicode(raw_text)
    cleaned_text = clean_text(unicode_text)
    sections = split_sections(cleaned_text)

    if not sections:
        preview = cleaned_text[:1000]
        raise ValueError(f"No sections found. Text preview:\n{preview}")

    db = SessionLocal()

    existing = db.query(Document).filter(Document.title == title).first()

    if existing:
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
                chapter=None,
                content=section["content"],
            )
        )

    db.add_all(legal_sections)
    db.commit()
    db.close()

    print(f"Imported PDF document: {title}")
    print(f"Sections imported: {len(legal_sections)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--type", default="law")
    parser.add_argument("--language", default="ne")
    parser.add_argument("--source-url", default="local_pdf")

    args = parser.parse_args()

    import_pdf_law(
        file_path=args.file,
        title=args.title,
        document_type=args.type,
        language=args.language,
        source_url=args.source_url,
    )