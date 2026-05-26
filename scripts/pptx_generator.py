from __future__ import annotations

import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Pt

from models import SlidePlan


def _load_theme(theme_path: Path | None) -> dict:
    path = theme_path or Path("templates/default_theme.json")
    return json.loads(path.read_text(encoding="utf-8"))


def generate_pptx(slide_plan: SlidePlan, output_path: Path, theme_path: Path | None = None) -> None:
    """
    Template-oriented PPT generator.
    Indirectly mirrors frontend-slides style by converting structured slides
    into clean title/body/note blocks with consistent typography.
    """
    theme = _load_theme(theme_path)
    prs = Presentation()

    for item in slide_plan.slides:
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        title = slide.shapes.title
        title.text = item.title
        tp = title.text_frame.paragraphs[0]
        tp.font.name = theme.get("title_font", "Calibri")
        tp.font.size = Pt(theme.get("title_size_pt", 34))
        tp.font.bold = True
        tp.font.color.rgb = RGBColor(29, 47, 95)

        body = slide.shapes.placeholders[1].text_frame
        body.clear()
        for idx, bullet in enumerate(item.bullets):
            p = body.paragraphs[0] if idx == 0 else body.add_paragraph()
            p.text = bullet
            p.level = 0
            p.font.name = theme.get("body_font", "Calibri")
            p.font.size = Pt(theme.get("body_size_pt", 20))

        notes = slide.notes_slide.notes_text_frame
        notes.text = item.speaker_notes

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))
