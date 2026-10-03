#!/usr/bin/env bash
# Build the manuscript: regenerate macros from results, then run latexmk.
set -euo pipefail
cd "$(dirname "$0")"
python3 ../experiments/make_numbers.py
python3 ../experiments/make_knn_numbers.py   # v0.4: macros of theory/knn_localisation_results.json (frozen SHA-256)
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -c main.tex >/dev/null 2>&1 || true
echo "built manuscript/main.pdf"
