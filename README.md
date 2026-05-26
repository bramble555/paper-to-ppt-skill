# paper-to-ppt-skill

Agent-agnostic Codex Skill repository for automating:

`Academic PDF -> parsing -> structured understanding -> graduate-level slides -> editable PPTX`

## CLI Installation (Skill-first, Agent-agnostic)
Install via CLI (example):

```bash
npx skills add https://github.com/bramble555/paper-to-ppt-skill
```

This repository is designed as a reusable skill package and can be orchestrated by different agents/runtimes.

## Features
- PDF text extraction (PyMuPDF)
- Section parsing for academic structure
- LLM-driven structured slide planning
- Editable `.pptx` generation with speaker notes
- Template-based HTML preview generation
- Modular, extensible pipeline

## Repository Layout
- `SKILL.md` — Codex skill trigger and behavior definition
- `agents/openai.yaml` — optional OpenAI runtime defaults (not required by all agents)
- `scripts/` — pipeline modules and CLI
- `references/` — prompt templates and schema
- `templates/` — PPT + HTML templates
- `assets/` — HTML theme assets
- `examples/` — runnable example command(s)
- `requirements.txt` — Python dependencies

## Local Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your_key_here"
```

## Run
```bash
python scripts/run_pipeline.py \
  --pdf /path/to/paper.pdf \
  --output-dir ./out \
  --model gpt-5 \
  --ppt-theme templates/default_theme.json \
  --html-template templates/html/base.html \
  --html-preview
```

## Outputs
- `out/presentation.pptx` (fully editable)
- `out/preview.html` + `out/assets/slide-theme.css` (optional)
- `out/parsed_paper.json`
- `out/slide_plan.json`

## Template Integration Notes
This skill now includes an upgraded template-driven HTML preview and slide visual pipeline inspired by and adapted from the following projects:
- https://github.com/zarazhangrui/beautiful-html-templates
- https://github.com/zarazhangrui/frontend-slides

Use `templates/html/base.html` and `assets/slide-theme.css` as the default frontend-slide style basis, and customize per lab/conference branding.
