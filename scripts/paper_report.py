from __future__ import annotations

from pathlib import Path

from models import ParsedPaper

SLIDE_TITLES = [
    "标题页",
    "研究动机",
    "研究背景",
    "问题定义",
    "方法总览",
    "技术细节",
    "实验设计",
    "实验结果",
    "讨论与分析",
    "结论",
]

SECTION_ALIASES = {
    "研究动机": ["introduction", "motivation", "front matter"],
    "研究背景": ["background", "related work"],
    "问题定义": ["problem statement", "introduction"],
    "方法总览": ["method", "methods", "approach"],
    "技术细节": ["method", "methods", "approach"],
    "实验设计": ["experiments", "experimental setup"],
    "实验结果": ["results", "experiments"],
    "讨论与分析": ["discussion", "limitations"],
    "结论": ["conclusion", "future work"],
}


def _clean_lines(text: str, max_lines: int = 20, min_len: int = 20) -> list[str]:
    parts = [" ".join(x.split()) for x in text.splitlines() if x.strip()]
    parts = [p for p in parts if len(p) >= min_len]
    return parts[:max_lines]


def _pick_section_text(section_map: dict[str, str], slide_title: str, abstract: str | None) -> str:
    if slide_title in section_map:
        return section_map[slide_title]
    for alias in SECTION_ALIASES.get(slide_title, []):
        if alias in section_map:
            return section_map[alias]
    return abstract or ""


def build_paper_detail_report(parsed: ParsedPaper) -> str:
    section_map = {s.name.lower(): s.content for s in parsed.sections}
    lines: list[str] = []
    lines.append(f"论文标题：{parsed.metadata.title}")
    lines.append("\n# 面向导师汇报的论文详细解读\n")
    lines.append("以下内容用于组会/周会汇报，请先审核并补充关键结论后再生成 HTML/PPT。")
    lines.append(
        f"\n## 解析质量诊断\n- 识别章节数：{len(parsed.sections)}\n- 参考文献相关词频：{parsed.references_count}\n- 是否检测到摘要：{'是' if parsed.abstract else '否'}"
    )

    if parsed.abstract:
        lines.append("\n## 摘要深度解读（建议口述 2-3 分钟）")
        for idx, x in enumerate(_clean_lines(parsed.abstract, 24, 10), 1):
            lines.append(f"{idx}. {x}")

    lines.append("\n## 全文章节级证据提炼（用于答辩问答）")
    for sec in parsed.sections[:30]:
        lines.append(f"\n### 章节：{sec.name}")
        dense = _clean_lines(sec.content, 12, 18)
        if not dense:
            lines.append("- 未提取到足够长句，建议人工核对 PDF 原文。")
            continue
        lines.append("- 关键信息摘录：")
        for d in dense[:8]:
            lines.append(f"  - {d}")
        lines.append("- 汇报建议：")
        lines.append("  - 先讲该章节的核心目标，再讲方法/结论，最后给出你的评价。")
        lines.append("  - 若有公式或实验设置，建议在 PPT 中配图并解释变量含义。")

    lines.append("\n## 导师汇报版幻灯片草案（10-12 页）\n")
    for i, title in enumerate(SLIDE_TITLES, 1):
        src = _pick_section_text(section_map, title, parsed.abstract)
        bullets = _clean_lines(src, 12, 16)
        lines.append(f"[Slide {i}] {title}")
        if title == "标题页":
            lines.append(f"- 论文题目：{parsed.metadata.title}")
            lines.append("- 汇报人：请填写姓名与日期")
            lines.append("- 汇报目标：解释论文问题、方法、实验、结论与局限")
            lines.append("")
            continue

        if len(bullets) < 4:
            bullets.extend(
                [
                    f"请从论文原文中补充“{title}”的关键论点与证据。",
                    "优先保留可量化信息（例如准确率、提升幅度、样本规模、消融结果）。",
                    "标记不确定点，汇报前与导师重点确认。",
                    "准备 1-2 个可视化图示以增强表达。",
                ]
            )

        for b in bullets[:8]:
            lines.append(f"- {b}")
        lines.append("- 讲解提示：先结论后细节，控制每页讲解在 60-90 秒。")
        lines.append("")

    if len(parsed.sections) > 8:
        lines.append("[Slide 11] 局限性")
        lines.append("- 假设条件、边界场景与失败案例是否充分讨论？")
        lines.append("- 结果的泛化性、可复现性是否存在风险？")
        lines.append("- 若数据集或算力受限，对结论会造成什么影响？")
        lines.append("")
        lines.append("[Slide 12] 未来工作")
        lines.append("- 后续可从哪些方向提升方法性能或稳定性？")
        lines.append("- 你所在课题组可以如何复现/扩展这项工作？")
        lines.append("- 请给出 2-3 个可执行的下一步实验计划。")

    lines.append("\n## 汇报准备清单（建议打印）")
    lines.append("- 是否能用 30 秒讲清问题定义与研究意义？")
    lines.append("- 是否能用 2 分钟讲清方法流程与创新点？")
    lines.append("- 是否能准确回答实验设置、评价指标与对比基线？")
    lines.append("- 是否已准备对局限性和未来工作的个人观点？")
    return "\n".join(lines)


def write_paper_detail_report(parsed: ParsedPaper, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_paper_detail_report(parsed), encoding="utf-8")
