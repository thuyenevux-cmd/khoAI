# -*- coding: utf-8 -*-
"""
Pipeline tạo toàn bộ tài liệu Báo cáo Đồ án AIA331:
1. File Word DOCX chuẩn ICTU (Bao_cao_AIA331.docx)
2. File LaTeX đầy đủ chuẩn ICTU (main.tex, ictu_style.sty, 16 chapters .tex, references.bib, appendix.tex)
3. Xuất Word sang PDF thông qua PowerShell Word COM (Bao_cao_AIA331.pdf)
4. Tạo RUBRIC_CHECKLIST.md và README_REPORT.md
"""
import os
import sys
import subprocess
from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

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

OUT_DOCX = WORD_DIR / "Bao_cao_AIA331.docx"
OUT_PDF = WORD_DIR / "Bao_cao_AIA331.pdf"
NAVY = "003B7A"
LIGHT = "EEF3FB"

# Import metadata from build_thesis_content
from build_thesis_content import METADATA, ABBREVIATIONS, RUBRIC_CRITERIA

print("Loaded base pipeline definitions.")
