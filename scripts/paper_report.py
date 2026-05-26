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

SECTION_ALIASES = {
    "motivation": ["introduction", "motivation", "front matter"],
    "background": ["background", "related work"],
    "problem definition": ["problem statement", "introduction"],
    "method overview": ["method", "methods", "approach"],
    "technical details": ["method", "methods", "approach"],
    "experiments": ["experiments", "experimental setup"],
    "results": ["results", "experiments"],
    "discussion": ["discussion", "limitations"],
    "conclusion": ["conclusion", "future work"],
}


def _clean_lines(text: str, max_lines: int = 12, min_len: int = 25) -> list[str]:
    parts = [" ".join(x.split()) for x in text.splitlines() if x.strip()]
    parts = [p for p in parts if len(p) >= min_len]
    return parts[:max_lines]


def _pick_section_text(section_map: dict[str, str], slide_title: str, abstract: str | None) -> str:
    key = slide_title.lower()
    if key in section_map:
        return section_map[key]
    for alias in SECTION_ALIASES.get(key, []):
        if alias in section_map:
            return section_map[alias]
    return abstract or ""


def build_paper_detail_report(parsed: ParsedPaper) -> str:
    section_map = {s.name.lower(): s.content for s in parsed.sections}
    lines: list[str] = []
    lines.append(f"Title: {parsed.metadata.title}")
    lines.append("\n# Paper Detailed Briefing\n")
    lines.append("请先审核以下内容；确认后再进入 HTML/PPT 生成阶段。")
    lines.append(f"\n## Parse Diagnostics\n- Parsed sections: {len(parsed.sections)}\n- Reference-like mentions: {parsed.references_count}")

    if parsed.abstract:
        lines.append("\n## Abstract Deep Summary")
        for x in _clean_lines(parsed.abstract, 16, 10):
            lines.append(f"- {x}")

    lines.append("\n## Section-level Evidence Snapshot")
    for sec in parsed.sections[:20]:
        excerpt = _clean_lines(sec.content, 3)
        lines.append(f"\n### {sec.name}")
        if excerpt:
            lines.extend([f"- {e}" for e in excerpt])
        else:
            lines.append("- (No dense sentence extracted)")

    lines.append("\n## Slide Draft (10-12 pages)\n")
    for i, title in enumerate(SLIDE_TITLES, 1):
        src = _pick_section_text(section_map, title, parsed.abstract)
        bullets = _clean_lines(src, 8, 18)
        if len(bullets) < 3:
            bullets.extend(
                [
                    f"Extract core claims for {title.lower()} from parsed sections.",
                    "Retain quantitative statements and assumptions.",
                    "Mark uncertain points for presenter verification.",
                ]
            )
        lines.append(f"[Slide {i}] {title}")
        for b in bullets[:6]:
            lines.append(f"- {b}")
        lines.append("")

    if len(parsed.sections) > 8:
        lines.append("[Slide 11] Limitations")
        lines.append("- Discuss assumptions, failure modes, and scope boundaries.")
        lines.append("- Identify reproducibility and generalization caveats.")
        lines.append("- Clarify where empirical evidence is weak or missing.")
        lines.append("")
        lines.append("[Slide 12] Future Work")
        lines.append("- Suggest next-step experiments and practical extensions.")
        lines.append("- Prioritize high-impact research directions.")
        lines.append("- Propose milestones for near-term replication.")

    return "\n".join(lines)


def write_paper_detail_report(parsed: ParsedPaper, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_paper_detail_report(parsed), encoding="utf-8")
