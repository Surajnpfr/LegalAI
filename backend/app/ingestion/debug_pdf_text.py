import argparse
from pathlib import Path

from app.ingestion.pdf_extractor import extract_text_from_pdf
from app.ingestion.text_cleaner import clean_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()

    text = extract_text_from_pdf(args.file)
    text = clean_text(text)

    output_dir = Path("../data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "pdf_debug.txt"
    output_file.write_text(text, encoding="utf-8")

    print(text[:2000])
    print(f"\nSaved to {output_file}")