# -*- coding: utf-8 -*-
"""
Script xây dựng toàn bộ bộ báo cáo kỹ thuật đồ án AIA331
- Xuất tệp Word: D:\it-thesis-research-documentation-engineer-v3.0\report\Word\Bao_cao_AIA331.docx
- Xuất tệp LaTeX đầy đủ: D:\it-thesis-research-documentation-engineer-v3.0\report\LaTeX\ (main.tex, ictu_style.sty, 16 chương, phụ lục)
- Gọi PowerShell Word COM để xuất PDF chuẩn: Bao_cao_AIA331.pdf
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

# Thiết lập thư mục gốc
REPORT_ROOT = Path(r"D:\it-thesis-research-documentation-engineer-v3.0\report")
WORD_DIR = REPORT_ROOT / "Word"
LATEX_DIR = REPORT_ROOT / "LaTeX"
CHAPTERS_DIR = LATEX_DIR / "chapters"
FIGURES_DIR = LATEX_DIR / "figures"
IMAGES_DIR = REPORT_ROOT / "Images"
SHOTS_DIR = REPORT_ROOT / "Screenshots"
DOCS_FINAL = Path(r"D:\it-thesis-research-documentation-engineer-v3.0\docs\final")

WORD_DIR.mkdir(parents=True, exist_ok=True)
LATEX_DIR.mkdir(parents=True, exist_ok=True)
CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
DOCS_FINAL.mkdir(parents=True, exist_ok=True)

OUT_DOCX = WORD_DIR / "Bao_cao_AIA331.docx"
OUT_PDF = WORD_DIR / "Bao_cao_AIA331.pdf"

NAVY = "003B7A"
LIGHT = "EEF3FB"
TABLE_COUNTER = 0
FIGURE_COUNTER = 0

# --- Helper DOCX Styles ---
def set_run_font(run, name="Times New Roman", size=12, bold=False, italic=False, color=None):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)

def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)

def set_cell_margins(cell, top=70, start=80, bottom=70, end=80):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")

def repeat_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)

def cant_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    node = OxmlElement("w:cantSplit")
    node.set(qn("w:val"), "true")
    tr_pr.append(node)

def style_document(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 1.25
    normal.paragraph_format.space_after = Pt(4)
    for style_name, size in (("Heading 1", 14), ("Heading 2", 13), ("Heading 3", 12)):
        style = doc.styles[style_name]
        style.font.name = "Times New Roman"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(NAVY)
        style.paragraph_format.space_before = Pt(10)
        style.paragraph_format.space_after = Pt(5)
        style.paragraph_format.keep_with_next = True

def setup_sections(doc):
    for section in doc.sections:
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.left_margin = Cm(3.5)
        section.right_margin = Cm(2.0)
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        footer = section.footer.paragraphs[0]
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = footer.add_run()
        set_run_font(run, size=10)
        fld_begin = OxmlElement("w:fldChar")
        fld_begin.set(qn("w:fldCharType"), "begin")
        instr = OxmlElement("w:instrText")
        instr.set(qn("xml:space"), "preserve")
        instr.text = " PAGE "
        fld_sep = OxmlElement("w:fldChar")
        fld_sep.set(qn("w:fldCharType"), "separate")
        text = OxmlElement("w:t")
        text.text = "1"
        fld_end = OxmlElement("w:fldChar")
        fld_end.set(qn("w:fldCharType"), "end")
        run._r.extend([fld_begin, instr, fld_sep, text, fld_end])

def page_break(doc):
    doc.add_page_break()

def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.keep_with_next = True
    return p

def add_para(doc, text, indent=True, align=None, bold=False, italic=False, size=12):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.space_after = Pt(4)
    if indent:
        p.paragraph_format.first_line_indent = Cm(1.27)
    if align is not None:
        p.alignment = align
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic)
    return p

def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)
    set_run_font(p.add_run(text), size=11.5)
    return p

def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    set_run_font(p.add_run(text), size=10.5, italic=True)
    return p

def add_table(doc, headers, rows, caption=None, font_size=9.5, header_fill=LIGHT):
    global TABLE_COUNTER
    if caption:
        TABLE_COUNTER += 1
        add_caption(doc, f"Bảng {TABLE_COUNTER}. {caption}")
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    hdr = table.rows[0]
    repeat_header(hdr)
    cant_split(hdr)
    for cell, value in zip(hdr.cells, headers):
        set_cell_shading(cell, header_fill)
        set_cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(str(value))
        set_run_font(run, size=font_size, bold=True)
    for row_values in rows:
        row = table.add_row()
        cant_split(row)
        cells = row.cells
        for cell, value in zip(cells, row_values):
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(str(value))
            set_run_font(run, size=font_size)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return table

def add_code(doc, code, caption=None, size=8.5):
    table = doc.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_shading(cell, "F7F7F8")
    set_cell_margins(cell, top=80, start=110, bottom=80, end=110)
    p = cell.paragraphs[0]
    p.paragraph_format.left_indent = Cm(0)
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    lines = code.strip("\n").splitlines()
    for idx, line in enumerate(lines):
        run = p.add_run(line)
        set_run_font(run, name="Consolas", size=size, color="1B1B1B")
        if idx != len(lines) - 1:
            run.add_break()
    if caption:
        add_caption(doc, caption)
    return table

def add_figure(doc, img_path, caption, width=15.0):
    global FIGURE_COUNTER
    FIGURE_COUNTER += 1
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    if Path(img_path).exists():
        p.add_run().add_picture(str(img_path), width=Cm(width))
    add_caption(doc, f"Hình {FIGURE_COUNTER}. {caption}")

print("Loaded base docx styling module.")
