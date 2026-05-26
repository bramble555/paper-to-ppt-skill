from __future__ import annotations

import re
from pathlib import Path

from jinja2 import Template


def parse_paper_detail_to_slides(detail_text: str) -> list[dict]:
    slides: list[dict] = []
    current: dict | None = None
    for line in detail_text.splitlines():
        s = line.strip()
        m = re.match(r"^\[Slide\s+(\d+)\]\s+(.+)$", s)
        if m:
            if current:
                slides.append(current)
            current = {"index": int(m.group(1)), "title": m.group(2), "bullets": []}
            continue
        if s.startswith("- ") and current is not None:
            current["bullets"].append(s[2:].strip())
    if current:
        slides.append(current)
    return slides[:12]


def generate_html_from_detail(detail_path: Path, output_path: Path, template_path: Path | None = None) -> None:
    tpl_path = template_path or Path("templates/html/base.html")
    template = Template(tpl_path.read_text(encoding="utf-8"))
    detail_text = detail_path.read_text(encoding="utf-8")
    slides = parse_paper_detail_to_slides(detail_text)
    deck_title = next((ln.replace("Title:", "").strip() for ln in detail_text.splitlines() if ln.startswith("Title:")), "Paper Briefing")
    html = template.render(deck_title=deck_title, slides=slides)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
