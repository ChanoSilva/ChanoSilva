#!/usr/bin/env bash
# Build the manuscript: regenerate macros from results, then run latexmk (pdflatex + bibtex).
set -euo pipefail
cd "$(dirname "$0")"
python3 ../experiments/make_numbers.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
if grep -qi "undefined" main.log; then echo "WARNING: undefined references or citations remain (see main.log)"; grep -i "undefined" main.log | head; else echo "no undefined references or citations"; fi
echo "overfull boxes: $(grep -c Overfull main.log)"
latexmk -c main.tex >/dev/null 2>&1 || true
echo "built manuscript/main.pdf"
