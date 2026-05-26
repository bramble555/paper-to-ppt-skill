from __future__ import annotations

import re
from pathlib import Path

import fitz

from models import PaperMetadata, ParsedPaper, ParsedSection

SECTION_PATTERN = re.compile(
    r"^(\d+\.?\s*)?(abstract|introduction|background|related work|problem statement|method|methods|approach|experiments|experimental setup|results|discussion|conclusion|limitations|future work)\s*$",
    re.IGNORECASE,
)


def extract_text_from_pdf(pdf_path: Path) -> str:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    doc = fitz.open(pdf_path)
    pages: list[str] = []
    for page in doc:
        text = page.get_text("text") or ""
        pages.append(text.strip())
    return "\n\n".join(pages)


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
            current_name = re.sub(r"^\d+\.?\s*", "", line).title()
            buffer = []
            continue
        buffer.append(line)

    if buffer:
        sections.append(ParsedSection(name=current_name, content="\n".join(buffer)))

    return sections


def _extract_title(raw_text: str) -> str:
    candidates = [ln.strip() for ln in raw_text.splitlines() if ln.strip()]
    for c in candidates[:30]:
        if len(c) > 20 and not c.lower().startswith("arxiv") and "@" not in c:
            return c[:220]
    return candidates[0][:220] if candidates else "Untitled Paper"


def parse_paper(pdf_path: Path) -> ParsedPaper:
    raw = extract_text_from_pdf(pdf_path)
    sections = parse_sections(raw)

    title = _extract_title(raw)
    abstract = next((s.content for s in sections if "abstract" in s.name.lower()), None)
    references_count = raw.lower().count("reference") + raw.lower().count("bibliography")

    metadata = PaperMetadata(title=title)
    return ParsedPaper(metadata=metadata, abstract=abstract, sections=sections, references_count=references_count)
