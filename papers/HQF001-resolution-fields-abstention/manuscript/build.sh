#!/usr/bin/env bash
# Build the manuscript: regenerate macros from results, then run latexmk (pdflatex + bibtex).
set -euo pipefail
cd "$(dirname "$0")"
python3 ../experiments/make_numbers.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -c main.tex >/dev/null 2>&1 || true
echo "built manuscript/main.pdf"
