from __future__ import annotations

from pathlib import Path

from models import SlidePlan


def generate_html_preview(slide_plan: SlidePlan, output_path: Path) -> None:
    slides_html = []
    for s in slide_plan.slides:
        bullets = "".join(f"<li>{b}</li>" for b in s.bullets)
        slides_html.append(
            f"<section><h2>{s.title}</h2><ul>{bullets}</ul><p><em>{s.speaker_notes}</em></p></section>"
        )

    html = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>{slide_plan.deck_title}</title></head>
<body><h1>{slide_plan.deck_title}</h1>{''.join(slides_html)}</body></html>"""
    output_path.write_text(html, encoding="utf-8")
