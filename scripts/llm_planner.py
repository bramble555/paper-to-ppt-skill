from __future__ import annotations

import json
from pathlib import Path

import yaml
from jinja2 import Template
from openai import OpenAI

from models import ParsedPaper, SlidePlan


def load_prompts(prompts_path: Path) -> dict:
    return yaml.safe_load(prompts_path.read_text(encoding="utf-8"))


def build_slide_plan(parsed: ParsedPaper, prompts_path: Path, model: str) -> SlidePlan:
    prompts = load_prompts(prompts_path)
    system_prompt = prompts["system_prompt"]
    user_template = Template(prompts["slide_planning_prompt"])
    user_prompt = user_template.render(parsed_paper_json=parsed.model_dump_json(indent=2))

    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    raw_text = response.output_text
    payload = json.loads(raw_text)
    return SlidePlan.model_validate(payload)
