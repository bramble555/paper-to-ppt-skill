from __future__ import annotations

import re
from pathlib import Path

import fitz

from models import PaperMetadata, ParsedPaper, ParsedSection


SECTION_PATTERN = re.compile(
    r"^(abstract|introduction|background|related work|method|methods|experiments|results|discussion|conclusion|limitations)\s*$",
    re.IGNORECASE,
)


def extract_text_from_pdf(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    pages = [page.get_text("text") for page in doc]
    return "\n".join(pages)


def parse_sections(raw_text: str) -> list[ParsedSection]:
    lines = [ln.strip() for ln in raw_text.splitlines()]
    sections: list[ParsedSection] = []
    current_name = "Front Matter"
    buffer: list[str] = []

    for line in lines:
        if not line:
            continue
        if SECTION_PATTERN.match(line):
            if buffer:
                sections.append(ParsedSection(name=current_name, content="\n".join(buffer)))
            current_name = line.title()
            buffer = []
        else:
            buffer.append(line)

    if buffer:
        sections.append(ParsedSection(name=current_name, content="\n".join(buffer)))

    return sections


def parse_paper(pdf_path: Path) -> ParsedPaper:
    raw = extract_text_from_pdf(pdf_path)
    sections = parse_sections(raw)

    title = next((s for s in raw.splitlines() if s.strip()), "Untitled Paper")[:200]
    abstract = next((s.content for s in sections if s.name.lower() == "abstract"), None)
    references_count = raw.lower().count("reference")

    metadata = PaperMetadata(title=title)
    return ParsedPaper(metadata=metadata, abstract=abstract, sections=sections, references_count=references_count)
