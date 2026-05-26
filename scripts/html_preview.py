from __future__ import annotations

from pathlib import Path

from jinja2 import Template

from models import SlidePlan


def generate_html_preview(slide_plan: SlidePlan, output_path: Path, template_path: Path | None = None) -> None:
    tpl_path = template_path or Path("templates/html/base.html")
    template = Template(tpl_path.read_text(encoding="utf-8"))
    html = template.render(deck_title=slide_plan.deck_title, slides=[s.model_dump() for s in slide_plan.slides])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
