import re


SECTION_PATTERN = re.compile(
    r"(धारा\s+[०-९0-9]+[^\n]*:?)(.*?)(?=\nधारा\s+[०-९0-9]+|\Z)",
    re.DOTALL,
)


def split_sections(text: str):
    sections = []

    for match in SECTION_PATTERN.finditer(text):
        heading_line = match.group(1).strip()
        content = match.group(2).strip()

        number_match = re.search(r"धारा\s+([०-९0-9]+)", heading_line)
        section_number = number_match.group(1) if number_match else None

        heading = heading_line
        heading = re.sub(r"^धारा\s+[०-९0-9]+\.?", "", heading)
        heading = heading.replace(":", "").strip()

        sections.append(
            {
                "section_number": section_number,
                "heading": heading,
                "content": content,
            }
        )

    return sections