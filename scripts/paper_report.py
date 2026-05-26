from __future__ import annotations

from pathlib import Path

from models import ParsedPaper


def _take_preview(text: str, limit: int = 2000) -> str:
    cleaned = " ".join(text.split())
    return cleaned[:limit] + ("..." if len(cleaned) > limit else "")


def build_paper_detail_report(parsed: ParsedPaper) -> str:
    lines: list[str] = []
    lines.append(f"Title: {parsed.metadata.title}")
    lines.append("")
    lines.append("论文详细汇报（用于生成 HTML/PPT 之前的人审）")
    lines.append("=" * 80)

    if parsed.abstract:
        lines.append("\n[Abstract 深度解析]\n")
        lines.append(_take_preview(parsed.abstract, 2500))

    lines.append("\n[章节化技术汇报]\n")
    for idx, sec in enumerate(parsed.sections, start=1):
        lines.append(f"{idx}. {sec.name}")
        lines.append("   - 核心摘要：")
        lines.append(f"     {_take_preview(sec.content, 1500)}")
        lines.append("   - 技术解读建议：")
        lines.append("     提炼问题定义、方法关键步骤、实验设置、结果结论、局限性与未来方向。")

    lines.append("\n[结构化汇报提纲建议（10-12页）]\n")
    lines.append("1) Title 2) Motivation 3) Background 4) Problem Definition 5) Method Overview")
    lines.append("6) Technical Details 7) Experiments 8) Results 9) Discussion 10) Conclusion")
    lines.append("11) Limitations (optional) 12) Future Work (optional)")
    return "\n".join(lines)


def write_paper_detail_report(parsed: ParsedPaper, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_paper_detail_report(parsed), encoding="utf-8")
