# paper-to-ppt-skill

A production-oriented Codex Skill repository that automates this workflow:

`Academic PDF -> parsing -> structured understanding -> graduate-level slides -> editable PPTX`

## Features
- PDF text extraction (PyMuPDF)
- Section parsing for academic structure
- LLM-driven structured slide planning
- Editable `.pptx` generation with speaker notes
- Optional HTML preview generation
- Modular, extensible pipeline

## Repository Layout
- `SKILL.md` — Codex skill trigger and behavior definition
- `agents/openai.yaml` — default orchestration and runtime settings
- `scripts/` — pipeline modules and CLI
- `references/` — prompt templates and schema
- `templates/` — style/theme configuration
- `examples/` — runnable example command(s)
- `requirements.txt` — Python dependencies

## Installation
1. Clone repository.
2. Create a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure API key:
   ```bash
   export OPENAI_API_KEY="your_key_here"
   ```

## Run
```bash
python scripts/run_pipeline.py \
  --pdf /path/to/paper.pdf \
  --output-dir ./out \
  --model gpt-5 \
  --html-preview
```

## Outputs
- `out/presentation.pptx` (fully editable)
- `out/preview.html` (optional)
- `out/parsed_paper.json`
- `out/slide_plan.json`

## Notes for open-source extension
- Add robust header/footer/reference extraction.
- Add citation-grounded slide generation checks.
- Add style template families for lab or conference branding.
