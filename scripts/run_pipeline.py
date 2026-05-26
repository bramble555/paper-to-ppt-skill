from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from html_preview import generate_html_preview
from llm_planner import build_agent_prompt, build_slide_plan
from paper_report import write_paper_detail_report
from pdf_parser import parse_paper
from pptx_generator import generate_pptx


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Academic PDF to editable PPTX pipeline")
    parser.add_argument("--pdf", type=Path, required=True, help="Path to academic PDF")
    parser.add_argument("--output-dir", type=Path, default=Path("./out"), help="Directory for artifacts")
    parser.add_argument("--title-override", default=None, help="Optional deck title override")
    parser.add_argument("--ppt-theme", type=Path, default=Path("templates/default_theme.json"))
    parser.add_argument("--html-template", type=Path, default=Path("templates/html/base.html"))
    parser.add_argument("--agent-slide-plan-json", type=Path, default=None, help="Agent-produced slide_plan.json")
    parser.add_argument("--emit-agent-prompt", action="store_true", help="Write prompt for Codex/Antigravity agent")
    parser.add_argument("--approve-detail", action="store_true", help="Continue to HTML/PPT after paper-detail review")
    return parser.parse_args()


def _print_review_gate(detail_path: Path) -> None:
    content = detail_path.read_text(encoding="utf-8")
    preview = "\n".join(content.splitlines()[:60])
    print("\n" + "=" * 80)
    print("论文详细汇报（节选）")
    print("=" * 80)
    print(preview)
    print("=" * 80)
    print("论文详细汇报已生成，是否同意以此内容开始生成 HTML 和 PPT？")
    print("请在确认后重新运行并追加参数：--approve-detail")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    parsed = parse_paper(args.pdf)
    detail_path = args.output_dir / "paper-detail.txt"
    write_paper_detail_report(parsed, detail_path)

    if not args.approve_detail:
        _print_review_gate(detail_path)
        return

    if args.emit_agent_prompt:
        prompt = build_agent_prompt(parsed, Path("references/prompts.yaml"))
        (args.output_dir / "agent_prompt.txt").write_text(prompt, encoding="utf-8")

    plan = build_slide_plan(parsed, Path("references/prompts.yaml"), agent_slide_plan_json=args.agent_slide_plan_json)
    if args.title_override:
        plan.deck_title = args.title_override

    shutil.copy(Path("assets/slide-theme.css"), args.output_dir / "slide-theme.css")
    generate_html_preview(plan, args.output_dir / "preview.html", template_path=args.html_template)

    pptx_path = args.output_dir / "presentation.pptx"
    generate_pptx(plan, pptx_path, theme_path=args.ppt_theme)

    (args.output_dir / "parsed_paper.json").write_text(parsed.model_dump_json(indent=2), encoding="utf-8")
    (args.output_dir / "slide_plan.json").write_text(json.dumps(plan.model_dump(), indent=2), encoding="utf-8")

    print(f"Generated: {detail_path}")
    print(f"Generated: {args.output_dir / 'preview.html'}")
    print(f"Generated: {pptx_path}")


if __name__ == "__main__":
    main()
