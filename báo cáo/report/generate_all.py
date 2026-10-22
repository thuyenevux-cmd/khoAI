# -*- coding: utf-8 -*-
"""
Full Generator for AIA331 Report:
1. Bao_cao_AIA331.docx (Word complete with 16 chapters, tables, figures, code blocks)
2. LaTeX Package (ictu_style.sty, main.tex, references.bib, 16 chapter .tex files, appendix, cover)
3. Word COM -> Bao_cao_AIA331.pdf
4. Docs: RUBRIC_CHECKLIST.md & README_REPORT.md
"""
import os
import sys
import json
from pathlib import Path

# Paths
REPORT_ROOT = Path(r"D:\it-thesis-research-documentation-engineer-v3.0\report")
WORD_DIR = REPORT_ROOT / "Word"
LATEX_DIR = REPORT_ROOT / "LaTeX"
CH_DIR = LATEX_DIR / "chapters"
FIGS_DIR = LATEX_DIR / "figures"
IMG_DIR = REPORT_ROOT / "Images"
SHOTS_DIR = REPORT_ROOT / "Screenshots"
DOCS_FINAL = Path(r"D:\it-thesis-research-documentation-engineer-v3.0\docs\final")

WORD_DIR.mkdir(parents=True, exist_ok=True)
LATEX_DIR.mkdir(parents=True, exist_ok=True)
CH_DIR.mkdir(parents=True, exist_ok=True)
FIGS_DIR.mkdir(parents=True, exist_ok=True)
DOCS_FINAL.mkdir(parents=True, exist_ok=True)

# Copy images to LaTeX figures if not present
for src in IMG_DIR.glob("*.png"):
    dst = FIGS_DIR / src.name
    if not dst.exists():
        dst.write_bytes(src.read_bytes())
for src in SHOTS_DIR.glob("*.png"):
    dst = FIGS_DIR / src.name
    if not dst.exists():
        dst.write_bytes(src.read_bytes())

print(f"Verified {len(list(FIGS_DIR.glob('*.png')))} figures in LaTeX figures folder.")
