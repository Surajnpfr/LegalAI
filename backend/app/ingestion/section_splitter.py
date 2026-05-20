import re


SECTION_PATTERN = re.compile(
    r"(धारा\s+[०-९0-9]+[^\n]*:?)(.*?)(?=\n\s*धारा\s+[०-९0-9]+|\Z)",
    re.DOTALL,
)

PART_PATTERN = re.compile(r"भाग\s+[०-९0-9]+.*")


def split_sections(text: str):
    sections = []
    current_part = None

    lines = text.splitlines()
    rebuilt_text = []

    for line in lines:
        line = line.strip()

        if not line:
            rebuilt_text.append("")
            continue

        if PART_PATTERN.match(line):
            current_part = line
            continue

        rebuilt_text.append(line)

    normalized_text = "\n".join(rebuilt_text)

    for match in SECTION_PATTERN.finditer(normalized_text):
        heading_line = match.group(1).strip()
        content = match.group(2).strip()

        number_match = re.search(r"धारा\s+([०-९0-9]+)", heading_line)
        section_number = number_match.group(1) if number_match else None

        heading = re.sub(r"^धारा\s+[०-९0-9]+\.?", "", heading_line)
        heading = heading.replace(":", "").strip()

        sections.append(
            {
                "section_number": section_number,
                "chapter": current_part,
                "heading": heading,
                "content": content,
            }
        )

    return sections