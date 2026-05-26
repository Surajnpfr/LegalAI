# app/ingestion/section_splitter.py
import re
from typing import List, Dict, Any

# Matches line indicators like: "भाग–१: प्रारम्भिक" or "भाग–२: नागरिकता"
PART_PATTERN = re.compile(r"^भाग[-–]\s*[०-९0-9]+.*")

# Captures heading starts like: "१. संविधान मूल कानून :" or "धारा १६. सम्मानपूर्वक बाँच्न पाउने हक :"
# Group 1: Number, Group 2: The rest of the heading line before the colon
SECTION_HEADER_PATTERN = re.compile(r"^(?:धारा|दफा)?\s*([०-९0-9]+)\.\s*([^:]+):")

def split_sections(text: str) -> List[Dict[str, Any]]:
    sections = []
    current_part = None
    
    current_section = None
    section_content_lines = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # 1. Track and update the current legal Part/Chapter context
        if PART_PATTERN.match(line):
            current_part = line
            continue

        # 2. Check if the line marks the start of a brand new legal section
        header_match = SECTION_HEADER_PATTERN.match(line)
        if header_match:
            # If we were already building an older section, save it before moving to the new one
            if current_section:
                current_section["content"] = "\n".join(section_content_lines).strip()
                sections.append(current_section)
            
            section_number = header_match.group(1).strip()
            heading = header_match.group(2).strip()
            
            # Extract any immediate text written on the same line after the colon marker
            line_remainder = line[header_match.end():].strip()
            
            current_section = {
                "section_number": section_number,
                "chapter": current_part,
                "heading": heading,
                "content": ""  # Will be populated below
            }
            section_content_lines = [line_remainder] if line_remainder else []
        else:
            # 3. If it's not a new section header, accumulate the text into the current section content buffer
            if current_section:
                # Avoid capturing standalone visual separator divider lines
                if not re.match(r'^[-–_=+*]{3,}$', line):
                    section_content_lines.append(line)

    # Don't forget to commit the final remaining parsed section block from the buffer loops
    if current_section:
        current_section["content"] = "\n".join(section_content_lines).strip()
        sections.append(current_section)

    return sections