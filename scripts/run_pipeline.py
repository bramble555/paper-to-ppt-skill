from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from html_preview import generate_html_preview
from llm_planner import build_slide_plan
from pdf_parser import parse_paper
from pptx_generator import generate_pptx


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Academic PDF to editable PPTX pipeline")
    parser.add_argument("--pdf", type=Path, required=True, help="Path to academic PDF")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for artifacts")
    parser.add_argument("--model", default="gpt-5", help="OpenAI model")
    parser.add_argument("--title-override", default=None, help="Optional deck title override")
    parser.add_argument("--html-preview", action="store_true", help="Generate HTML preview")
    parser.add_argument("--ppt-theme", type=Path, default=Path("templates/default_theme.json"))
    parser.add_argument("--html-template", type=Path, default=Path("templates/html/base.html"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    parsed = parse_paper(args.pdf)
    plan = build_slide_plan(parsed, Path("references/prompts.yaml"), model=args.model)

    if args.title_override:
        plan.deck_title = args.title_override

    pptx_path = args.output_dir / "presentation.pptx"
    generate_pptx(plan, pptx_path, theme_path=args.ppt_theme)

    if args.html_preview:
        assets_dir = args.output_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        shutil.copy(Path("assets/slide-theme.css"), assets_dir / "slide-theme.css")
        generate_html_preview(plan, args.output_dir / "preview.html", template_path=args.html_template)

    (args.output_dir / "parsed_paper.json").write_text(parsed.model_dump_json(indent=2), encoding="utf-8")
    (args.output_dir / "slide_plan.json").write_text(json.dumps(plan.model_dump(), indent=2), encoding="utf-8")

    print(f"Generated: {pptx_path}")


if __name__ == "__main__":
    main()
