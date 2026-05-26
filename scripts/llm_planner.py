from __future__ import annotations

import json
from pathlib import Path

import yaml
from jinja2 import Template

from models import ParsedPaper, Slide, SlidePlan

REQUIRED_SECTIONS = [
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


def load_prompts(prompts_path: Path) -> dict:
    return yaml.safe_load(prompts_path.read_text(encoding="utf-8"))


def build_agent_prompt(parsed: ParsedPaper, prompts_path: Path) -> str:
    prompts = load_prompts(prompts_path)
    user_template = Template(prompts["slide_planning_prompt"])
    return user_template.render(parsed_paper_json=parsed.model_dump_json(indent=2))


def _fallback_plan(parsed: ParsedPaper) -> SlidePlan:
    title = parsed.metadata.title or "Paper Presentation"
    section_text = {s.name.lower(): s.content for s in parsed.sections}

    slides: list[Slide] = []
    for sec in REQUIRED_SECTIONS:
        key = sec.lower()
        source = section_text.get(key, parsed.abstract or "")
        lines = [ln.strip() for ln in source.splitlines() if ln.strip()][:4]
        bullets = lines if lines else [f"Summarize {sec.lower()} from source paper.", "Verify claims against paper text."]
        if len(bullets) == 1:
            bullets.append("Add one supporting technical point.")
        slides.append(
            Slide(
                section=sec,
                title=sec,
                bullets=bullets[:6],
                speaker_notes=f"Explain {sec.lower()} with focus on technical rigor and caveats.",
            )
        )

    return SlidePlan(deck_title=title, slides=slides)


def build_slide_plan(parsed: ParsedPaper, prompts_path: Path, agent_slide_plan_json: Path | None = None) -> SlidePlan:
    if agent_slide_plan_json and agent_slide_plan_json.exists():
        payload = json.loads(agent_slide_plan_json.read_text(encoding="utf-8"))
        return SlidePlan.model_validate(payload)
    return _fallback_plan(parsed)
