#!/usr/bin/env bash
# Build the manuscript: regenerate macros from results, then run latexmk.
set -euo pipefail
cd "$(dirname "$0")"
python3 ../experiments/make_numbers.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
echo "built manuscript/main.pdf"
