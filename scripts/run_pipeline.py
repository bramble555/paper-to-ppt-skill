from __future__ import annotations

import argparse
from pathlib import Path

from html_preview import generate_html_from_detail
from paper_report import write_paper_detail_report
from pdf_parser import parse_paper
from pptx_generator import generate_pptx_from_html


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Academic PDF to HTML/PPTX pipeline")
    parser.add_argument("--pdf", type=Path, required=True, help="Path to academic PDF")
    parser.add_argument("--output-dir", type=Path, default=Path("./out"), help="Directory for artifacts")
    parser.add_argument("--approve-detail", action="store_true", help="Continue to HTML/PPT after paper-detail review")
    parser.add_argument("--html-template", type=Path, default=Path("templates/html/base.html"))
    return parser.parse_args()


def _print_review_gate(detail_path: Path) -> None:
    content = detail_path.read_text(encoding="utf-8")
    print("\n" + "=" * 80)
    print("论文详细汇报（节选）")
    print("=" * 80)
    print("\n".join(content.splitlines()[:80]))
    print("=" * 80)
    print("论文详细汇报已生成，是否同意以此内容开始生成 HTML 和 PPT？")
    print("如同意，请重新运行：python scripts/run_pipeline.py --pdf <path> --approve-detail")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    parsed = parse_paper(args.pdf)
    detail_path = args.output_dir / "paper-detail.txt"
    write_paper_detail_report(parsed, detail_path)

    if not args.approve_detail:
        _print_review_gate(detail_path)
        return

    html_path = args.output_dir / "preview.html"
    generate_html_from_detail(detail_path, html_path, template_path=args.html_template)

    pptx_path = args.output_dir / "presentation.pptx"
    generate_pptx_from_html(html_path, pptx_path)

    print(f"Generated: {detail_path}")
    print(f"Generated: {html_path}")
    print(f"Generated: {pptx_path}")


if __name__ == "__main__":
    main()
