#!/usr/bin/env bash
set -euo pipefail

python scripts/run_pipeline.py \
  --pdf examples/sample_paper.pdf \
  --output-dir examples/output \
  --html-preview
