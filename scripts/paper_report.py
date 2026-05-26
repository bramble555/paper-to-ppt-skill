from __future__ import annotations

from pathlib import Path

from models import ParsedPaper

SLIDE_TITLES = [
    "Title",
    "Motivation",
    "Background",
    "Problem Definition",
    "Method Overview",
    "Technical Details",
    "Experiments",
    "Results",
    "Discussion",
    "Conclusion",
]


def _clean_lines(text: str, max_lines: int = 6) -> list[str]:
    parts = [" ".join(x.split()) for x in text.splitlines() if x.strip()]
    return parts[:max_lines]


def build_paper_detail_report(parsed: ParsedPaper) -> str:
    section_map = {s.name.lower(): s.content for s in parsed.sections}
    lines: list[str] = []
    lines.append(f"Title: {parsed.metadata.title}")
    lines.append("\n# Paper Detailed Briefing\n")
    lines.append("请先审核以下内容；确认后再进入 HTML/PPT 生成阶段。")

    if parsed.abstract:
        lines.append("\n## Abstract Summary")
        lines.extend([f"- {x}" for x in _clean_lines(parsed.abstract, 8)])

    lines.append("\n## Slide Draft (10-12 pages)\n")
    for i, title in enumerate(SLIDE_TITLES, 1):
        src = section_map.get(title.lower(), parsed.abstract or "")
        bullets = _clean_lines(src, 4)
        if len(bullets) < 2:
            bullets = [f"Explain {title.lower()} based on parsed paper.", "Highlight verifiable technical points."]
        lines.append(f"[Slide {i}] {title}")
        for b in bullets[:6]:
            lines.append(f"- {b}")
        lines.append("")

    if len(parsed.sections) > 8:
        lines.append("[Slide 11] Limitations")
        lines.append("- Discuss assumptions, failure modes, and scope boundaries.")
        lines.append("- Identify reproducibility and generalization caveats.")
        lines.append("")
        lines.append("[Slide 12] Future Work")
        lines.append("- Suggest next-step experiments and practical extensions.")
        lines.append("- Prioritize high-impact research directions.")

    return "\n".join(lines)


def write_paper_detail_report(parsed: ParsedPaper, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_paper_detail_report(parsed), encoding="utf-8")
