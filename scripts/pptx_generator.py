from __future__ import annotations

from pathlib import Path

from pptx import Presentation

from models import SlidePlan


def generate_pptx(slide_plan: SlidePlan, output_path: Path) -> None:
    prs = Presentation()

    for item in slide_plan.slides:
        layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(layout)
        slide.shapes.title.text = item.title

        body = slide.shapes.placeholders[1].text_frame
        body.clear()
        for bullet in item.bullets:
            p = body.add_paragraph()
            p.text = bullet
            p.level = 0

        notes = slide.notes_slide.notes_text_frame
        notes.text = item.speaker_notes

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))
