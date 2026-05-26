from __future__ import annotations

import argparse
import json
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    parsed = parse_paper(args.pdf)
    plan = build_slide_plan(parsed, Path("references/prompts.yaml"), model=args.model)

    if args.title_override:
        plan.deck_title = args.title_override

    pptx_path = args.output_dir / "presentation.pptx"
    generate_pptx(plan, pptx_path)

    if args.html_preview:
        generate_html_preview(plan, args.output_dir / "preview.html")

    (args.output_dir / "parsed_paper.json").write_text(parsed.model_dump_json(indent=2), encoding="utf-8")
    (args.output_dir / "slide_plan.json").write_text(json.dumps(plan.model_dump(), indent=2), encoding="utf-8")

    print(f"Generated: {pptx_path}")


if __name__ == "__main__":
    main()
