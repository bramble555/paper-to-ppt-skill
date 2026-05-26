# Paper-to-PPT Skill

## When this skill should trigger
Use this skill when a user wants to automatically convert an academic PDF into a graduate-level, editable presentation package (PPTX + optional HTML preview + speaker notes), rather than manually summarizing the paper.

## What this skill does
This skill runs a modular pipeline:
1. Ingest an academic PDF.
2. Extract paper text and basic metadata.
3. Parse paper sections into structured content.
4. Use an LLM to produce a normalized slide plan.
5. Render an editable `.pptx` deck with speaker notes.
6. Optionally render an HTML slide preview.

## Repository components
- `agents/openai.yaml`: Codex/OpenAI agent configuration for orchestration defaults.
- `scripts/`: Pipeline implementation and CLI entrypoints.
- `references/`: Prompt specs and JSON schemas.
- `templates/`: Slide and style templates.
- `examples/`: Example run commands and sample outputs.

## Usage examples
```bash
python scripts/run_pipeline.py \
  --pdf examples/sample_paper.pdf \
  --output-dir examples/output \
  --title-override "Seminar Deck" \
  --html-preview
```

```bash
python scripts/run_pipeline.py \
  --pdf /path/to/paper.pdf \
  --output-dir /tmp/paper_deck \
  --model gpt-5
```

## Implementation notes
- The default slide sequence targets research-group and seminar delivery:
  Title, Motivation, Background, Problem Definition, Method Overview, Technical Details, Experiments, Results, Discussion, Conclusion.
- The generated PPTX is fully editable and includes speaker notes for each slide.
- Prompts are externalized in `references/prompts.yaml` to keep behavior tunable without code changes.
- The pipeline supports arbitrary academic papers and does not hardcode domain assumptions.
