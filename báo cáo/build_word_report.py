# -*- coding: utf-8 -*-
"""
Script biên soạn Báo cáo Đồ án Toàn diện 16 Chương (.docx) chuẩn quy cách Bộ GD&ĐT và Đại học Thái Nguyên (ICTU)
Đề tài: HỆ THỐNG QUẢN LÝ KHO CÓ TÍCH HỢP AI
Học phần: Ứng dụng Trí tuệ Nhân tạo - AIA331 (Mã 80273)
Nhóm thực hiện: Nhóm 11 (Dương Minh Quang - DTC245200225, Vũ Ngọc Anh Thuyên - DTC245200428)
Giảng viên hướng dẫn: ThS. Nguyễn Tuấn Anh
"""
import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_OUTPUT_PATH = r"D:\khoAI\báo cáo\báo cáo dự án Kho AI nhóm 11.docx"
DOCX_COPY_PATH = r"D:\khoAI\báo cáo\Bao_cao_AIA331.docx"
DIAGRAM_DIR = r"D:\khoAI\báo cáo\diagrams"
LOGO_PATH = os.path.join(DIAGRAM_DIR, "logo_ictu.png")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="000000", sz="10", val="single"):
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def build_report(page_map=None):
    doc = Document()

    # Disable picture compression in document settings (Preserve 600 DPI quality)
    try:
        settings_part = doc.settings._element
        node = parse_xml(f'<w:defaultImageDpi {nsdecls("w")} w:val="0"/>')
        settings_part.append(node)
    except Exception:
        pass

    # Exact page numbers measured from Microsoft Word document layout engine
    pm = {
        "cover": "1", "thanks": "2", "abstract": "4", "abbr": "5",
        "toc": "6", "skills_toc": "8", "lof": "10", "lot": "12",
        "matrix": "14",
        "ch1": "17", "ch2": "17", "ch3": "20", "ch4": "21",
        "ch5": "24", "ch6": "29", "ch7": "32", "ch8": "33",
        "ch9": "36", "ch10": "38", "ch11": "40", "ch12": "41",
        "ch13": "42", "ch14": "42", "ch15": "43", "ch16": "45",
        "refs": "46", "appendix": "47",
        "fig3_1": "21", "fig4_1": "22", "fig4_2": "23",
        "fig5_1": "24", "fig5_2": "25", "fig5_3": "26", "fig5_4": "27",
        "fig6_1": "30", "fig6_2": "31", "fig6_3": "32",
        "fig8_1": "34", "fig8_2": "35", "fig9_1": "37",
        "fig15_1": "44", "fig15_2": "44", "fig15_3": "45", "fig15_4": "45",
        "tbl1_1": "3", "tbl2_1": "17", "tbl5_1": "27",
        "tbl10_1": "38", "tbl11_1": "40", "tbl12_1": "41",
        "tbl14_1": "42", "tbl_pl1": "47", "tbl_pl2": "55",
    }
    if page_map:
        pm.update(page_map)

    # Page Margins: Left 3cm, Right 2cm, Top 2cm, Bottom 2cm
    for section in doc.sections:
        section.top_margin = Inches(0.79)     # ~2.0 cm
        section.bottom_margin = Inches(0.79)  # ~2.0 cm
        section.left_margin = Inches(1.18)    # ~3.0 cm
        section.right_margin = Inches(0.79)   # ~2.0 cm
        section.page_width = Inches(8.27)     # A4
        section.page_height = Inches(11.69)
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("BÁO CÁO ĐỒ ÁN: AIA331 - HỆ THỐNG QUẢN LÝ KHO CÓ TÍCH HỢP AI | NHÓM 11")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(120, 120, 120)

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Trường Đại học Công nghệ Thông tin & Truyền thông - Đại học Thái Nguyên")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(9)
        frun.font.color.rgb = RGBColor(120, 120, 120)

    # Styles
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(13)
    style_normal.font.color.rgb = RGBColor(15, 23, 42)
    style_normal.paragraph_format.line_spacing = 1.3
    style_normal.paragraph_format.space_after = Pt(4)

    # Helper functions
    def add_p(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, pt_size=13, color=RGBColor(15, 23, 42), space_after=4):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(space_after)
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(pt_size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 58, 138) # Deep Blue
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(14.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(13.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_bullet(lead_text, body_text):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(3)
        r1 = p.add_run(lead_text)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(13)
        r1.font.bold = True
        r2 = p.add_run(body_text)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(13)

    def add_image(img_filename, caption_text, width_inches=6.2):
        path = os.path.join(DIAGRAM_DIR, img_filename)
        if os.path.exists(path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(3)
            p_img.paragraph_format.keep_with_next = True
            run = p_img.add_run()
            run.add_picture(path, width=Inches(width_inches))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(3)
            p_cap.paragraph_format.space_after = Pt(10)
            rcap = p_cap.add_run(caption_text)
            rcap.font.name = "Times New Roman"
            rcap.font.size = Pt(12)
            rcap.font.italic = True
            rcap.font.bold = True
            rcap.font.color.rgb = RGBColor(51, 65, 85)

    def add_toc_line(title, page_str, bold=False, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(1.5)
        p.paragraph_format.space_after = Pt(1.5)
        if level == 1:
            p.paragraph_format.left_indent = Inches(0)
        elif level == 2:
            p.paragraph_format.left_indent = Inches(0.22)
        elif level == 3:
            p.paragraph_format.left_indent = Inches(0.44)

        tab_stops = p.paragraph_format.tab_stops
        tab_stops.add_tab_stop(Inches(6.25), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

        r1 = p.add_run(title)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11.5 if level > 1 else 12)
        r1.font.bold = bold
        if level == 1 and bold:
            r1.font.color.rgb = RGBColor(30, 58, 138)
        else:
            r1.font.color.rgb = RGBColor(15, 23, 42)

        r2 = p.add_run(f"\t{page_str}")
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11.5 if level > 1 else 12)
        r2.font.bold = bold
        r2.font.color.rgb = RGBColor(15, 23, 42)
        return p

    # =========================================================================
    # 1. TRANG BÌA (COVER PAGE)
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("ĐẠI HỌC THÁI NGUYÊN\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    r2 = p.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(14)
    r2.font.bold = True

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_after = Pt(15)
    r_line = p_line.add_run("─────────── ★ ───────────")
    r_line.font.bold = True

    # Logo ICTU
    if os.path.exists(LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(18)
        p_logo.add_run().add_picture(LOGO_PATH, width=Inches(1.9))

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(6)
    r_sub = p_sub.add_run("BÁO CÁO DỰ ÁN HỌC PHẦN")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(15)
    r_sub.font.bold = True

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(16)
    r_c = p_course.add_run("HỌC PHẦN: ỨNG DỤNG TRÍ TUỆ NHÂN TẠO – AIA331\n(MÃ HỌC PHẦN: 80273)")
    r_c.font.name = "Times New Roman"
    r_c.font.size = Pt(13)
    r_c.font.bold = True
    r_c.font.color.rgb = RGBColor(30, 58, 138)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(22)
    r_t = p_title.add_run("ĐỀ TÀI:\nHỆ THỐNG QUẢN LÝ KHO CÓ TÍCH HỢP AI\n(AI-POWERED SAAS INVENTORY MANAGEMENT SYSTEM)")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(17)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(185, 28, 28)

    # Info table
    tbl = doc.add_table(rows=5, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    col_widths = [Inches(2.4), Inches(3.8)]
    row_data = [
        ("Giảng viên hướng dẫn:", "ThS. Nguyễn Tuấn Anh"),
        ("Nhóm sinh viên thực hiện:", "Nhóm 11"),
        ("Sinh viên 1:", "Dương Minh Quang  –  MSV: DTC245200225"),
        ("Sinh viên 2:", "Vũ Ngọc Anh Thuyên – MSV: DTC245200428"),
        ("Ngành / Lớp học:", "Công nghệ Thông tin - K24 ICTU"),
    ]
    for i, (k, v) in enumerate(row_data):
        row = tbl.rows[i]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width, c2.width = col_widths[0], col_widths[1]
        set_cell_margins(c1, top=45, bottom=45, left=70, right=70)
        set_cell_margins(c2, top=45, bottom=45, left=70, right=70)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(k)
        r1.font.name, r1.font.size, r1.font.bold = "Times New Roman", Pt(14), True
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_after = Pt(2)
        r2 = p2.add_run(v)
        r2.font.name, r2.font.size = "Times New Roman", Pt(13.5)
        r2.font.bold = (i in [0, 1, 2, 3])

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_after = Pt(30)
    p_bottom = doc.add_paragraph()
    p_bottom.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_b = p_bottom.add_run("THÁI NGUYÊN – THÁNG 09/2026")
    r_b.font.name, r_b.font.size, r_b.font.bold = "Times New Roman", Pt(13), True

    doc.add_page_break()

    # =========================================================================
    # 2. LỜI CẢM ƠN
    # =========================================================================
    add_h1("LỜI CẢM ƠN")
    add_p("Trong quá trình học tập, nghiên cứu và hoàn thành đồ án môn học 'Ứng dụng Trí tuệ Nhân tạo – AIA331', nhóm 11 đã nhận được sự quan tâm, giảng dạy tận tình và hướng dẫn chi tiết từ các thầy cô giáo trong trường.", space_after=3)
    add_p("Trước hết, chúng em xin trân trọng gửi lời cảm ơn sâu sắc nhất tới Thầy ThS. Nguyễn Tuấn Anh – Giảng viên trực tiếp giảng dạy và hướng dẫn học phần. Thầy đã trang bị cho chúng em nền tảng kiến thức vững chắc về Trí tuệ Nhân tạo, định hướng tư duy phân tích nghiệp vụ thực tế, kỹ thuật thiết kế Prompt kiểm soát dữ liệu nền tảng và phương pháp xây dựng hệ thống phần mềm có độ tin cậy cao.", space_after=3)
    add_p("Chúng em cũng xin gửi lời cảm ơn tới Ban Giám hiệu, Khoa Công nghệ Thông tin – Trường Đại học Công nghệ Thông tin và Truyền thông, Đại học Thái Nguyên đã luôn tạo điều kiện thuận lợi về môi trường học tập, cơ sở vật chất và tài liệu nghiên cứu để chúng em hoàn thành đồ án này.", space_after=3)
    add_p("Mặc dù nhóm chúng em đã rất nỗ lực, đồ án chắc chắn không tránh khỏi những thiếu sót nhất định. Chúng em rất mong nhận được những lời nhận xét, góp ý quý báu từ Thầy để hệ thống ngày càng hoàn thiện hơn. Chúng em xin chân thành cảm ơn!", italic=True, space_after=6)

    # BẢNG PHÂN CÔNG NHIỆM VỤ THÀNH VIÊN
    p_mem_h = doc.add_paragraph()
    p_mem_h.paragraph_format.space_before = Pt(8)
    p_mem_h.paragraph_format.space_after = Pt(4)
    p_mem_h.paragraph_format.keep_with_next = True
    r_mh = p_mem_h.add_run("BẢNG PHÂN CÔNG NHIỆM VỤ VÀ TỶ LỆ ĐÓNG GÓP THÀNH VIÊN NHÓM 11")
    r_mh.font.name = "Times New Roman"
    r_mh.font.size = Pt(13)
    r_mh.font.bold = True
    r_mh.font.color.rgb = RGBColor(15, 23, 42)

    tbl_mem = doc.add_table(rows=3, cols=5)
    tbl_mem.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_mem.autofit = False
    set_table_borders(tbl_mem, color="000000", sz="10")
    mem_widths = [Inches(0.55), Inches(1.75), Inches(1.2), Inches(2.2), Inches(0.6)]
    m_hdr = ["STT", "Họ và Tên", "Mã SV", "Phần việc đảm nhiệm trong dự án", "Đóng góp"]
    trPr0 = tbl_mem.rows[0]._tr.get_or_add_trPr()
    trPr0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    for i, h in enumerate(m_hdr):
        c = tbl_mem.rows[0].cells[i]
        c.width = mem_widths[i]
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=50, bottom=50, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(14.5), True
        r.font.color.rgb = RGBColor(255, 255, 255)

    members_data = [
        ("1", "Dương Minh Quang", "DTC245200225", "Trưởng nhóm: Thiết kế kiến trúc tổng thể, xây dựng Backend FastAPI, ORM 11 bảng CSDL, tích hợp Pipeline AI 2 lớp (Gemini Cloud + Rule Engine) và bộ test Pytest tự động.", "50%"),
        ("2", "Vũ Ngọc Anh Thuyên", "DTC245200428", "Thành viên: Phân tích yêu cầu nghiệp vụ, thiết kế hệ thống sơ đồ kỹ thuật (ERD, Sequence, Activity, Use Case), xây dựng Frontend React Vite SaaS UI và biên soạn báo cáo.", "50%"),
    ]
    for r_idx, m in enumerate(members_data):
        row = tbl_mem.rows[r_idx + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for c_idx, val in enumerate(m):
            c = row.cells[c_idx]
            c.width = mem_widths[c_idx]
            set_cell_margins(c, top=45, bottom=45, left=65, right=65)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2, 4] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name, r.font.size = "Times New Roman", Pt(13.5)
            if c_idx == 1:
                r.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # 3. TÓM TẮT & TỪ KHÓA (ABSTRACT & KEYWORDS)
    # =========================================================================
    add_h1("TÓM TẮT BÁO CÁO (ABSTRACT)")
    add_p("Trong kỷ nguyên thương mại điện tử và chuyển đổi số, hoạt động kho vận giữ vai trò quyết định đến vòng quay vốn lưu động và năng lực cung ứng của doanh nghiệp. Đồ án học phần AIA331 của Nhóm 11 tập trung nghiên cứu và hiện thực hóa 'Hệ thống Quản lý Kho có Tích hợp Trí tuệ Nhân tạo (AI-Powered Inventory Management System)', giải quyết triệt để các bất cập cố hữu của phương pháp ghi chép thủ công và bảng tính Excel rời rạc.")
    add_p("Hệ thống được thiết kế theo chuẩn Kiến trúc 3 tầng phân tách độc lập (Presentation Tier: React 18 Single Page Application, SaaS Dark Mode; Logic Tier: FastAPI Async Web Framework, Python 3.14; Data/Cloud Tier: SQLAlchemy ORM với 11 bảng cơ sở dữ liệu quan hệ chuẩn 3NF và dịch vụ đám mây Google Gemini 1.5 Flash). Điểm sáng tạo đột phá của dự án là việc cài đặt thành công Pipeline AI 2 lớp (Dual-layer AI Pipeline): Lớp 1 ứng dụng Mô hình Ngôn ngữ Lớn (LLM) để phân tích chuyên sâu và hỏi đáp ngôn ngữ tự nhiên; Lớp 2 là Bộ máy tính toán xác định cục bộ (Local Deterministic Rule Engine) đảm bảo hệ thống duy trì hoạt động 100% không gián đoạn cả khi mất Internet hoặc hết hạn mức API.")
    add_p("Đặc biệt, hệ thống áp dụng cơ chế Chống ảo giác số liệu tuyệt đối (Anti-Hallucination) thông qua kỹ thuật Bơm dữ liệu thực tế (Ground-Truth Context Injection) và chuẩn hóa công thức toán học tính Vận tốc tiêu thụ (Daily Burn-rate) và Số ngày cạn tồn (Depletion Days), loại bỏ hoàn toàn lỗi chia cho 0 (ZeroDivisionError). Toàn bộ 12/12 ca kiểm thử tự động Backend (Pytest Suite) đều vượt qua tuyệt đối (100% Passed), kết hợp kiểm soát bảo mật đa tầng (JWT Bearer, Argon2, RBAC 3 vai trò: Admin, Warehouse, Accountant, và vết kiểm toán Audit Trail bất biến).")

    add_h2("TỪ KHÓA (KEYWORDS)")
    add_p("Quản lý kho thông minh (Smart Inventory), Dual-layer AI Pipeline, Anti-Hallucination, Ground-Truth Context Injection, FastAPI, React Vite, SQLAlchemy ORM, RBAC, Pytest Automation, Audit Logs, SaaS Dark Mode.", italic=True)

    doc.add_page_break()

    # =========================================================================
    # DANH MỤC CÁC TỪ VIẾT TẮT
    # =========================================================================
    add_h1("DANH MỤC CÁC TỪ VIẾT TẮT")
    tbl_abbr = doc.add_table(rows=11, cols=3)
    tbl_abbr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_abbr, color="000000", sz="10")
    trPr_ab0 = tbl_abbr.rows[0]._tr.get_or_add_trPr()
    trPr_ab0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    abbr_hdr = ["Từ viết tắt", "Tên đầy đủ tiếng Anh", "Ý nghĩa / Diễn giải tiếng Việt"]
    for i, h in enumerate(abbr_hdr):
        c = tbl_abbr.rows[0].cells[i]
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=50, bottom=50, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(14.5), True
        r.font.color.rgb = RGBColor(255, 255, 255)

    abbr_data = [
        ("AI", "Artificial Intelligence", "Trí tuệ Nhân tạo"),
        ("API", "Application Programming Interface", "Giao diện lập trình ứng dụng"),
        ("JWT", "JSON Web Token", "Chuỗi mã hóa xác thực người dùng không trạng thái"),
        ("RBAC", "Role-Based Access Control", "Mô hình kiểm soát truy cập dựa trên vai trò"),
        ("ORM", "Object-Relational Mapping", "Ánh xạ cơ sở dữ liệu quan hệ sang đối tượng"),
        ("LLM", "Large Language Model", "Mô hình ngôn ngữ lớn (Google Gemini)"),
        ("NLP", "Natural Language Processing", "Xử lý ngôn ngữ tự nhiên"),
        ("SPA", "Single Page Application", "Ứng dụng web hiển thị động trên một trang"),
        ("SKU", "Stock Keeping Unit", "Mã định danh đơn vị hàng hóa lưu kho"),
        ("ERD", "Entity Relationship Diagram", "Sơ đồ thực thể liên kết cơ sở dữ liệu"),
    ]
    for r_idx, ab in enumerate(abbr_data):
        row = tbl_abbr.rows[r_idx + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for c_idx, val in enumerate(ab):
            c = row.cells[c_idx]
            set_cell_margins(c, top=45, bottom=45, left=65, right=65)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name, r.font.size = "Times New Roman", Pt(13.5)
            if c_idx == 0:
                r.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # 4. MỤC LỤC CHÍNH (16 CHƯƠNG)
    # =========================================================================
    add_h1("MỤC LỤC")
    add_p("Cấu trúc toàn bộ 16 chương kỹ thuật, tài liệu tham khảo và phụ lục của báo cáo:", italic=True, pt_size=11, space_after=6)

    chapters_toc = [
        ("LỜI CẢM ƠN", pm["thanks"], True, 1),
        ("TÓM TẮT BÁO CÁO (ABSTRACT)", pm["abstract"], True, 1),
        ("TỪ KHÓA & DANH MỤC TỪ VIẾT TẮT", pm["abbr"], True, 1),
        ("MỤC LỤC BÁO CÁO", pm["toc"], True, 1),
        ("MỤC LỤC CÁC BÀI KIỂM TRA KỸ NĂNG", pm["skills_toc"], True, 1),
        ("DANH MỤC HÌNH VẼ", pm["lof"], True, 1),
        ("DANH MỤC BẢNG BIỂU", pm["lot"], True, 1),
        ("BẢNG TRA CỨU NỘI DUNG THEO BÀI KIỂM TRA", pm["matrix"], True, 1),
        
        ("CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI", pm["ch1"], True, 1),
        ("    1.1. Bối cảnh bài toán quản lý kho tại các doanh nghiệp vừa và nhỏ", pm["ch1"], False, 2),
        ("    1.2. Mục tiêu, đối tượng và phạm vi nghiên cứu", pm["ch1"], False, 2),
        ("    1.3. Phương pháp nghiên cứu và cách tiếp cận ứng dụng Trí tuệ Nhân tạo", pm["ch1"], False, 2),

        ("CHƯƠNG 2. PHÂN TÍCH YÊU CẦU", pm["ch2"], True, 1),
        ("    2.1. Yêu cầu chức năng chi tiết (FR01 - FR09)", pm["ch2"], False, 2),
        ("    2.2. Yêu cầu phi chức năng (Bảo mật, Hiệu năng, Toàn vẹn ACID, SaaS UI)", pm["ch2"], False, 2),

        ("CHƯƠNG 3. PHÂN TÍCH ACTOR VÀ USE CASE", pm["ch3"], True, 1),
        ("    3.1. Xác định và phân quyền 3 tác nhân Actor (Admin, Warehouse, Accountant)", pm["ch3"], False, 2),
        ("    3.2. Sơ đồ Use Case tổng thể hệ thống (Hình 3.1)", pm["ch3"], False, 2),
        ("    3.3. Đặc tả các Use Case cốt lõi", pm["ch3"], False, 2),

        ("CHƯƠNG 4. THIẾT KẾ QUY TRÌNH NGHIỆP VỤ", pm["ch4"], True, 1),
        ("    4.1. Lược đồ hoạt động quy trình Nhập kho (Hình 4.1)", pm["ch4"], False, 2),
        ("    4.2. Lược đồ hoạt động quy trình Xuất kho và kiểm tra tồn khả dụng (Hình 4.2)", pm["ch4"], False, 2),
        ("    4.3. Quy trình kiểm kê định kỳ và xử lý cân bằng kho", pm["ch4"], False, 2),

        ("CHƯƠNG 5. THIẾT KẾ CƠ SỞ DỮ LIỆU", pm["ch5"], True, 1),
        ("    5.1. Sơ đồ thực thể liên kết (ERD) tổng quan 11 bảng CSDL (Hình 5.1)", pm["ch5"], False, 2),
        ("    5.2. Thiết kế chi tiết các phân hệ CSDL (Hình 5.2, 5.3, 5.4)", pm["ch5"], False, 2),
        ("    5.3. Danh mục 11 bảng cơ sở dữ liệu quan hệ (Bảng 5.1)", pm["ch5"], False, 2),
        ("    5.4. Ràng buộc toàn vẹn tham chiếu và cơ chế ACID Database Transaction", pm["ch5"], False, 2),

        ("CHƯƠNG 6. KIẾN TRÚC HỆ THỐNG", pm["ch6"], True, 1),
        ("    6.1. Thiết kế Kiến trúc 3 tầng tổng thể (Hình 6.1)", pm["ch6"], False, 2),
        ("    6.2. Sơ đồ tuần tự xử lý giao dịch an toàn (Hình 6.2)", pm["ch6"], False, 2),
        ("    6.3. Sơ đồ điều hướng giao diện người dùng (Frontend Sitemap - Hình 6.3)", pm["ch6"], False, 2),

        ("CHƯƠNG 7. THIẾT KẾ CHI TIẾT CHỨC NĂNG", pm["ch7"], True, 1),
        ("    7.1. Phân hệ Quản lý Danh mục và Sản phẩm SKU", pm["ch7"], False, 2),
        ("    7.2. Phân hệ Quản lý Giao dịch Nhập xuất kho", pm["ch7"], False, 2),
        ("    7.3. Phân hệ Vị trí lưu kho và Sơ đồ kệ chứa (Zone/Shelf)", pm["ch7"], False, 2),
        ("    7.4. Phân hệ Thống kê Dashboard và Định giá tài sản kho", pm["ch7"], False, 2),

        ("CHƯƠNG 8. THIẾT KẾ VÀ TÍCH HỢP AI", pm["ch8"], True, 1),
        ("    8.1. Định vị vai trò của AI và Kiến trúc Pipeline 2 lớp (Hình 8.1)", pm["ch8"], False, 2),
        ("    8.2. Lớp 1: Cloud LLM (Google Gemini) với phân tích sâu", pm["ch8"], False, 2),
        ("    8.3. Lớp 2: Local Deterministic Rule Engine với độ tin cậy tuyệt đối", pm["ch8"], False, 2),
        ("    8.4. Trợ lý Hỏi Đáp Kho AI Tự Nhiên (NLP Assistant - Hình 8.2)", pm["ch8"], False, 2),

        ("CHƯƠNG 9. THIẾT KẾ PROMPT VÀ THỬ NGHIỆM", pm["ch9"], True, 1),
        ("    9.1. Kỹ nghệ thiết kế Prompt có cấu trúc và Ground-Truth Context Injection", pm["ch9"], False, 2),
        ("    9.2. Cơ chế chống ảo giác số liệu (Anti-Hallucination Framework)", pm["ch9"], False, 2),
        ("    9.3. Mô hình toán học: Daily Burn-rate, Depletion Days và Z-score Anomaly (Hình 9.1)", pm["ch9"], False, 2),

        ("CHƯƠNG 10. KIỂM THỬ", pm["ch10"], True, 1),
        ("    10.1. Chiến lược kiểm thử phần mềm tự động bằng Pytest", pm["ch10"], False, 2),
        ("    10.2. Kết quả thực nghiệm bộ kiểm thử 12 ca kiểm thử tự động (Bảng 10.1)", pm["ch10"], False, 2),
        ("    10.3. Kiểm thử an toàn ngoại lệ và xử lý lỗi HTTP toàn cục", pm["ch10"], False, 2),

        ("CHƯƠNG 11. BẢO MẬT VÀ ĐẠO ĐỨC AI", pm["ch11"], True, 1),
        ("    11.1. Tuân thủ tiêu chuẩn an toàn OWASP Top 10 và bảo vệ cơ sở dữ liệu", pm["ch11"], False, 2),
        ("    11.2. Xác thực JWT, băm mật khẩu Argon2 và Ma trận phân quyền RBAC (Bảng 11.1)", pm["ch11"], False, 2),
        ("    11.3. Đạo đức AI: Quyền riêng tư dữ liệu kho, tính minh bạch và vết kiểm toán", pm["ch11"], False, 2),

        ("CHƯƠNG 12. TRIỂN KHAI HỆ THỐNG", pm["ch12"], True, 1),
        ("    12.1. Yêu cầu môi trường phần cứng và phần mềm", pm["ch12"], False, 2),
        ("    12.2. Hướng dẫn cài đặt và khởi chạy Backend FastAPI và Frontend Vite", pm["ch12"], False, 2),
        ("    12.3. Danh sách tài khoản thử nghiệm hệ thống mặc định (Bảng 12.1)", pm["ch12"], False, 2),

        ("CHƯƠNG 13. MINH CHỨNG SỬ DỤNG AI TRONG SDLC", pm["ch13"], True, 1),
        ("    13.1. Ứng dụng AI hỗ trợ phân tích yêu cầu và sinh sơ đồ kiến trúc", pm["ch13"], False, 2),
        ("    13.2. Ứng dụng AI hỗ trợ lập trình, sinh Test Case và tối ưu hóa ORM", pm["ch13"], False, 2),
        ("    13.3. Review mã nguồn tự động và giám sát chất lượng kỹ thuật", pm["ch13"], False, 2),

        ("CHƯƠNG 14. ĐÁNH GIÁ THEO RUBRIC", pm["ch14"], True, 1),
        ("    14.1. Bảng đối chiếu tự đánh giá theo 40 tiêu chí Rubric môn học AIA331 (Bảng 14.1)", pm["ch14"], False, 2),
        ("    14.2. Phân tích kết quả đáp ứng từng giai đoạn KT1, KT2, KT3 và Cuối kỳ", pm["ch14"], False, 2),

        ("CHƯƠNG 15. DEMO HỆ THỐNG", pm["ch15"], True, 1),
        ("    15.1. Kịch bản chạy demo thực tế hệ thống kho vận", pm["ch15"], False, 2),
        ("    15.2. Hình ảnh minh chứng các giao diện SaaS Dashboard, Sản phẩm và AI Hub", pm["ch15"], False, 2),

        ("CHƯƠNG 16. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", pm["ch16"], True, 1),
        ("    16.1. Tổng kết các kết quả đạt được của đề tài", pm["ch16"], False, 2),
        ("    16.2. Những hạn chế còn tồn tại", pm["ch16"], False, 2),
        ("    16.3. Hướng phát triển và mở rộng trong tương lai", pm["ch16"], False, 2),

        ("TÀI LIỆU THAM KHẢO", pm["refs"], True, 1),
        ("PHỤ LỤC CÁC BẢNG VÀ MÃ NGUỒN", pm["appendix"], True, 1),
    ]

    for title, pg, is_b, lvl in chapters_toc:
        add_toc_line(title, pg, bold=is_b, level=lvl)

    doc.add_page_break()

    # =========================================================================
    # 5. MỤC LỤC CÁC BÀI KIỂM TRA KỸ NĂNG
    # =========================================================================
    add_h1("MỤC LỤC CÁC BÀI KIỂM TRA KỸ NĂNG")
    add_p("Mục lục chuyên biệt này giúp Giảng viên đánh giá nhanh chóng việc đáp ứng toàn bộ 40 tiêu chí kiểm tra kỹ năng của học phần AIA331 theo từng giai đoạn:", italic=True, pt_size=11, space_after=6)

    skills_toc_data = [
        ("BÀI KIỂM TRA THƯỜNG XUYÊN 1 – KT1 (PHÂN TÍCH & THIẾT KẾ)", pm["ch1"], True, 1),
        ("    1. Phân tích đúng bài toán quản lý kho hàng", pm["ch1"], False, 2),
        ("    2. Xác định đầy đủ yêu cầu chức năng (FR01 - FR09)", pm["ch2"], False, 2),
        ("    3. Xác định yêu cầu phi chức năng (Bảo mật, Hiệu năng, ACID)", pm["ch2"], False, 2),
        ("    4. Thiết kế actor và sơ đồ Use Case tổng thể", pm["ch3"], False, 2),
        ("    5. Thiết kế cơ sở dữ liệu quan hệ chuẩn hóa 3NF (11 Bảng)", pm["ch5"], False, 2),
        ("    6. Thiết kế kiến trúc hệ thống 3 tầng phân tách độc lập", pm["ch6"], False, 2),
        ("    7. Xác định vị trí ứng dụng AI giải quyết bài toán cạn tồn", pm["ch8"], False, 2),
        ("    8. Thiết kế prompt và luồng gọi AI có kiểm soát dữ liệu", pm["ch9"], False, 2),
        ("    9. Minh chứng sử dụng AI hỗ trợ phân tích thiết kế", pm["ch13"], False, 2),
        ("    10. Hồ sơ tài liệu phân tích thiết kế kỹ thuật hoàn chỉnh", pm["ch14"], False, 2),

        ("BÀI KIỂM TRA THƯỜNG XUYÊN 2 – KT2 (BACKEND, CSDL & BẢO MẬT)", pm["ch6"], True, 1),
        ("    1. Cấu trúc dự án mã nguồn theo nguyên lý Clean Architecture", pm["ch6"], False, 2),
        ("    2. Đăng nhập an toàn và phân quyền RBAC 3 vai trò (Admin/Warehouse/Accountant)", pm["ch11"], False, 2),
        ("    3. CRUD nghiệp vụ quản lý sản phẩm, vị trí kệ và giao dịch", pm["ch7"], False, 2),
        ("    4. Tìm kiếm và lọc hàng hóa thông minh, hiển thị trạng thái tồn kho", pm["ch7"], False, 2),
        ("    5. Thống kê và báo cáo tài chính kho (KPIs, định giá kho)", pm["ch7"], False, 2),
        ("    6. Giao diện người dùng SaaS Dark Mode hiện đại trực quan", pm["ch7"], False, 2),
        ("    7. Kết nối CSDL quan hệ SQLAlchemy ORM 11 bảng", pm["ch5"], False, 2),
        ("    8. Xử lý lỗi toàn cục và bắt ngoại lệ HTTP an toàn", pm["ch10"], False, 2),
        ("    9. Minh chứng sử dụng AI hỗ trợ lập trình và tối ưu hóa", pm["ch13"], False, 2),
        ("    10. README và tài liệu hướng dẫn vận hành, chạy thử", pm["ch12"], False, 2),

        ("BÀI KIỂM TRA THƯỜNG XUYÊN 3 – KT3 (TÍCH HỢP TRÍ TUỆ NHÂN TẠO)", pm["ch8"], True, 1),
        ("    1. Tích hợp giải pháp AI giải quyết bài toán quản lý kho", pm["ch8"], False, 2),
        ("    2. Kết nối API Cloud LLM (Gemini) và Bộ máy Rule Engine cục bộ", pm["ch8"], False, 2),
        ("    3. Thiết kế Prompt có cấu trúc nghiêm ngặt định dạng Markdown", pm["ch9"], False, 2),
        ("    4. Tối ưu prompt và cơ chế chống ảo giác số liệu (Anti-Hallucination)", pm["ch9"], False, 2),
        ("    5. Sử dụng dữ liệu thực tế hệ thống (Ground-Truth Context Injection)", pm["ch9"], False, 2),
        ("    6. Hiển thị kết quả AI dạng Smart Component kèm bảng số liệu", pm["ch8"], False, 2),
        ("    7. Xử lý lỗi, ngắt kết nối mạng và chuyển vùng dự phòng cục bộ", pm["ch8"], False, 2),
        ("    8. Kiểm thử tự động các chức năng AI (Restock, Anomaly, NLP Chat)", pm["ch10"], False, 2),
        ("    9. Review mã nguồn tự động và giám sát chất lượng bằng AI", pm["ch13"], False, 2),
        ("    10. Tích hợp AI nâng cao trải nghiệm người vận hành kho", pm["ch15"], False, 2),

        ("THI KẾT THÚC HỌC PHẦN (HOÀN THIỆN ĐỒ ÁN & ĐÓNG GÓI)", pm["ch14"], True, 1),
        ("    1. Hoàn thiện toàn bộ chức năng nghiệp vụ hệ thống", pm["ch7"], False, 2),
        ("    2. Chất lượng kiến trúc hệ thống và tính module hóa mã nguồn", pm["ch6"], False, 2),
        ("    3. Chất lượng cơ sở dữ liệu chuẩn 3NF và tính toàn vẹn ACID", pm["ch5"], False, 2),
        ("    4. Giao diện và trải nghiệm người dùng chuyên nghiệp (SaaS UI)", pm["ch15"], False, 2),
        ("    5. Chất lượng bộ máy AI kép hoạt động ổn định và chính xác", pm["ch8"], False, 2),
        ("    6. Bảo mật OWASP, quyền riêng tư dữ liệu và đạo đức AI", pm["ch11"], False, 2),
        ("    7. Hiệu năng xử lý cao (<100ms API, <50ms AI Local)", pm["ch2"], False, 2),
        ("    8. Triển khai, đóng gói và cung cấp sẵn Seed Data thử nghiệm", pm["ch12"], False, 2),
        ("    9. Hồ sơ báo cáo kỹ thuật hoàn chỉnh (Word chuẩn Bộ & LaTeX)", pm["ch14"], False, 2),
        ("    10. Kịch bản thuyết trình và chạy thử nghiệm hệ thống (Demo)", pm["ch15"], False, 2),
    ]

    for title, pg, is_b, lvl in skills_toc_data:
        add_toc_line(title, pg, bold=is_b, level=lvl)

    doc.add_page_break()

    # =========================================================================
    # 6. DANH MỤC HÌNH VẼ & DANH MỤC BẢNG BIỂU
    # =========================================================================
    add_h2("DANH MỤC HÌNH VẼ")
    tbl_lof = doc.add_table(rows=18, cols=3)
    tbl_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_lof.autofit = False
    set_table_borders(tbl_lof, color="000000", sz="10")
    lof_widths = [Inches(1.2), Inches(4.5), Inches(0.7)]
    trPr_lf0 = tbl_lof.rows[0]._tr.get_or_add_trPr()
    trPr_lf0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    lof_hdr = ["Mã hình", "Tên sơ đồ / Bản vẽ kỹ thuật minh chứng", "Trang"]
    for i, h in enumerate(lof_hdr):
        c = tbl_lof.rows[0].cells[i]
        c.width = lof_widths[i]
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=45, bottom=45, left=65, right=65)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(14.5), True
        r.font.color.rgb = RGBColor(255, 255, 255)

    figures_list = [
        ("Hình 3.1", "Sơ đồ Use Case tổng thể hệ thống phân quyền 3 tác nhân", pm.get("fig3_1", "19")),
        ("Hình 4.1", "Lược đồ hoạt động quy trình nghiệp vụ nhập kho và gán kệ", pm.get("fig4_1", "20")),
        ("Hình 4.2", "Lược đồ hoạt động quy trình nghiệp vụ xuất kho và kiểm tra tồn khả dụng", pm.get("fig4_2", "21")),
        ("Hình 5.1", "Sơ đồ thực thể liên kết (ERD) tổng quan 11 bảng CSDL chuẩn hóa 3NF", pm.get("fig5_1", "23")),
        ("Hình 5.2", "Sơ đồ ERD phân hệ Quản trị người dùng, Phân quyền RBAC & AI Logs", pm.get("fig5_2", "24")),
        ("Hình 5.3", "Sơ đồ ERD phân hệ Danh mục Hàng hóa, Nhà cung cấp & Vị trí Kệ kho", pm.get("fig5_3", "25")),
        ("Hình 5.4", "Sơ đồ ERD phân hệ Quản lý Tồn kho & Giao dịch Xuất Nhập kho", pm.get("fig5_4", "26")),
        ("Hình 6.1", "Sơ đồ kiến trúc tổng thể hệ thống 3 tầng (Presentation - Logic - Data/AI)", pm.get("fig6_1", "28")),
        ("Hình 6.2", "Sơ đồ tuần tự xử lý giao dịch kho an toàn (Sequence Diagram)", pm.get("fig6_2", "29")),
        ("Hình 6.3", "Sơ đồ điều hướng cây giao diện người dùng (Frontend Sitemap UI)", pm.get("fig6_3", "30")),
        ("Hình 8.1", "Sơ đồ kiến trúc Pipeline AI 2 lớp (Cloud Gemini LLM + Local Fallback)", pm.get("fig8_1", "32")),
        ("Hình 8.2", "Sơ đồ tuần tự xử lý Trợ lý hỏi đáp tự nhiên NLP (AI Assistant)", pm.get("fig8_2", "34")),
        ("Hình 9.1", "Lưu đồ thuật toán phát hiện bất thường và tính vận tốc tiêu thụ", pm.get("fig9_1", "36")),
        ("Hình 15.1", "Giao diện SaaS Dashboard tổng quan và 6 thẻ chỉ số KPI kho", pm.get("fig15_1", "42")),
        ("Hình 15.2", "Giao diện Quản lý Danh mục Sản phẩm và Smart Table Renderer", pm.get("fig15_2", "42")),
        ("Hình 15.3", "Giao diện AI Analytics Hub (Dự báo cạn tồn & Phát hiện dị biệt Z-score)", pm.get("fig15_3", "43")),
        ("Hình 15.4", "Giao diện Trợ lý Hỏi Đáp Kho AI Tự Nhiên (AI Chat Console)", pm.get("fig15_4", "43")),
    ]
    for r_idx, fig in enumerate(figures_list):
        row = tbl_lof.rows[r_idx + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for c_idx, val in enumerate(fig):
            c = row.cells[c_idx]
            c.width = lof_widths[c_idx]
            set_cell_margins(c, top=40, bottom=40, left=60, right=60)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name, r.font.size = "Times New Roman", Pt(13.5)
            if c_idx == 0:
                r.font.bold = True

    p_sp_tbl = doc.add_paragraph()
    p_sp_tbl.paragraph_format.space_after = Pt(8)

    add_h2("DANH MỤC BẢNG BIỂU")
    tbl_lot = doc.add_table(rows=10, cols=3)
    tbl_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_lot.autofit = False
    set_table_borders(tbl_lot, color="000000", sz="10")
    lot_widths = [Inches(1.2), Inches(4.5), Inches(0.7)]
    trPr_lt0 = tbl_lot.rows[0]._tr.get_or_add_trPr()
    trPr_lt0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    lot_hdr = ["Mã bảng", "Tên bảng số liệu / Đặc tả kỹ thuật", "Trang"]
    for i, h in enumerate(lot_hdr):
        c = tbl_lot.rows[0].cells[i]
        c.width = lot_widths[i]
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=45, bottom=45, left=65, right=65)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(14.5), True
        r.font.color.rgb = RGBColor(255, 255, 255)

    tables_list = [
        ("Bảng 1.1", "Bảng phân công nhiệm vụ và tỷ lệ đóng góp thành viên Nhóm 11", pm.get("tbl1_1", "3")),
        ("Bảng 2.1", "Danh mục các yêu cầu chức năng cốt lõi (FR01 - FR09)", pm.get("tbl2_1", "17")),
        ("Bảng 5.1", "Danh mục 11 bảng cơ sở dữ liệu quan hệ chuẩn hóa 3NF", pm.get("tbl5_1", "27")),
        ("Bảng 10.1", "Kết quả thực nghiệm bộ kiểm thử tự động Backend (Pytest Suite 12/12 Passed)", pm.get("tbl10_1", "38")),
        ("Bảng 11.1", "Ma trận phân quyền truy cập Role-Based Access Control (RBAC 3 vai trò)", pm.get("tbl11_1", "40")),
        ("Bảng 12.1", "Danh sách tài khoản thử nghiệm hệ thống mặc định (Seed Data)", pm.get("tbl12_1", "41")),
        ("Bảng 14.1", "Bảng đối chiếu tự đánh giá theo 40 tiêu chí Rubric môn học AIA331", pm.get("tbl14_1", "42")),
        ("Bảng PL.1", "Đặc tả chi tiết 77 trường dữ liệu thuộc 11 bảng cơ sở dữ liệu quan hệ", pm.get("tbl_pl1", "47")),
        ("Bảng PL.2", "Kịch bản chi tiết 12 ca kiểm thử Pytest tự động và kết quả kỳ vọng", pm.get("tbl_pl2", "55")),
    ]
    for r_idx, tb in enumerate(tables_list):
        row = tbl_lot.rows[r_idx + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for c_idx, val in enumerate(tb):
            c = row.cells[c_idx]
            c.width = lot_widths[c_idx]
            set_cell_margins(c, top=40, bottom=40, left=60, right=60)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name, r.font.size = "Times New Roman", Pt(13.5)
            if c_idx == 0:
                r.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # 7. BẢNG TRA CỨU NỘI DUNG THEO BÀI KIỂM TRA (40 TIÊU CHÍ)
    # =========================================================================
    add_h1("BẢNG TRA CỨU NỘI DUNG THEO BÀI KIỂM TRA")
    add_p("Bảng ma trận truy xuất dưới đây giúp Giảng viên dễ dàng định vị chính xác vị trí chương mục, hình ảnh minh chứng và tệp mã nguồn tương ứng cho toàn bộ 40 tiêu chí đánh giá môn học AIA331:", italic=True, pt_size=11, space_after=8)

    matrix_40_data = [
        # (BaiKT, TieuChi, ChuongMuc, MinhChung, FileCode)
        ("KT1", "1. Phân tích bài toán", "Chương 1 (1.1 - 1.2)", "Ngữ cảnh kho SME", "docs/requirements.md"),
        ("KT1", "2. Yêu cầu chức năng", "Chương 2 (2.1)", "Bảng 2.1 (FR01-FR09)", "app/schemas/"),
        ("KT1", "3. Yêu cầu phi chức năng", "Chương 2 (2.2)", "Mục tiêu ACID, OWASP", "app/core/config.py"),
        ("KT1", "4. Thiết kế actor & Use case", "Chương 3 (3.1 - 3.2)", "Hình 3.1 Use Case", "02_so_do_usecase.drawio"),
        ("KT1", "5. Thiết kế CSDL 3NF", "Chương 5 (5.1 - 5.4)", "Hình 5.1-5.4 ERD 11 bảng", "app/models/"),
        ("KT1", "6. Kiến trúc hệ thống", "Chương 6 (6.1)", "Hình 6.1 Kiến trúc 3 tầng", "01_so_do_kien_truc.drawio"),
        ("KT1", "7. Vị trí ứng dụng AI", "Chương 8 (8.1)", "Hình 8.1 Pipeline AI", "app/services/ai_service.py"),
        ("KT1", "8. Thiết kế prompt & luồng AI", "Chương 9 (9.1 - 9.2)", "System Prompt Grounding", "app/services/ai_prompts.py"),
        ("KT1", "9. Minh chứng dùng AI SDLC", "Chương 13 (13.1)", "Nhật ký AI Assistant", "docs/ai_prompts_log.md"),
        ("KT1", "10. Tài liệu phân tích thiết kế", "Chương 1 đến Chương 6", "13 bản vẽ kỹ thuật UML", "báo cáo dự án nhóm 11.docx"),

        ("KT2", "1. Cấu trúc dự án", "Chương 6 & Chương 7", "Clean Architecture", "backend/ & frontend/"),
        ("KT2", "2. Đăng nhập & RBAC", "Chương 11 (11.2)", "Bảng 11.1 Ma trận RBAC", "app/core/security.py"),
        ("KT2", "3. CRUD nghiệp vụ", "Chương 7 (7.1 - 7.2)", "API Products & Trans", "app/routers/inventory.py"),
        ("KT2", "4. Tìm kiếm và lọc", "Chương 7 (7.3)", "Smart Table Search", "frontend/src/pages/Products"),
        ("KT2", "5. Thống kê & báo cáo", "Chương 7 (7.4)", "Hình 15.1 Thẻ 6 KPI", "app/routers/dashboard.py"),
        ("KT2", "6. Giao diện SaaS UI", "Chương 7 (7.5) & Ch.15", "HorizonX Dark Mode", "frontend/src/App.tsx"),
        ("KT2", "7. Kết nối CSDL SQLAlchemy", "Chương 5 (5.4)", "Bảng 5.1 ORM Models", "app/db/session.py"),
        ("KT2", "8. Xử lý lỗi toàn cục", "Chương 10 (10.3)", "HTTP Exception Handlers", "app/main.py"),
        ("KT2", "9. Minh chứng AI lập trình", "Chương 13 (13.2)", "Sinh Pytest & ORM query", "tests/test_api_suite.py"),
        ("KT2", "10. README & chạy thử", "Chương 12 (12.2)", "Hướng dẫn Uvicorn & npm", "README.md"),

        ("KT3", "1. Tích hợp AI bài toán kho", "Chương 8 (8.1)", "Dự báo cạn tồn & Anomaly", "app/services/ai_service.py"),
        ("KT3", "2. Kết nối Cloud & Local AI", "Chương 8 (8.2 - 8.3)", "Hình 8.1 Dual-layer", "app/services/ai_fallback.py"),
        ("KT3", "3. Thiết kế prompt có cấu trúc", "Chương 9 (9.1)", "Markdown Table Prompt", "app/services/ai_prompts.py"),
        ("KT3", "4. Tối ưu prompt chống ảo giác", "Chương 9 (9.2)", "Anti-Hallucination rules", "app/services/ai_service.py"),
        ("KT3", "5. Dữ liệu thực tế hệ thống", "Chương 9 (9.3)", "Ground-Truth Context", "app/routers/ai_hub.py"),
        ("KT3", "6. Hiển thị kết quả AI", "Chương 8 (8.4) & Ch.15", "Hình 15.3 AI Analytics", "frontend/src/pages/AIHub"),
        ("KT3", "7. Xử lý ngắt mạng / lỗi AI", "Chương 8 (8.3)", "Local Deterministic Rule", "app/services/rule_engine.py"),
        ("KT3", "8. Kiểm thử chức năng AI", "Chương 10 (10.2)", "TC10, TC11, TC12", "tests/test_api_suite.py"),
        ("KT3", "9. Review code bằng AI", "Chương 13 (13.3)", "Refactor & Static review", "docs/ai_review_log.md"),
        ("KT3", "10. Trải nghiệm người dùng AI", "Chương 15 (15.2)", "Hình 15.4 Chat Console", "frontend/src/components/AI"),

        ("CK", "1. Hoàn thiện chức năng", "Chương 7 & Chương 15", "Đủ 5 phân hệ phần mềm", "Backend + Frontend SPA"),
        ("CK", "2. Chất lượng kiến trúc", "Chương 6 (6.1)", "Hình 6.1 3-Tier chuẩn", "Clean Architecture"),
        ("CK", "3. Chất lượng CSDL 3NF", "Chương 5 & Phụ lục", "Hình 5.1 & Bảng PL.1", "11 bảng SQLAlchemy"),
        ("CK", "4. Trải nghiệm người dùng", "Chương 15 (15.1 - 15.2)", "Hình 15.1 - 15.4", "Tailwind SaaS UI"),
        ("CK", "5. Chất lượng chức năng AI", "Chương 8 & Chương 9", "Dual-layer Resilience", "Gemini + Local Engine"),
        ("CK", "6. Bảo mật & Đạo đức AI", "Chương 11 (11.1 - 11.3)", "Bảng 11.1 & Audit Log", "app/models/audit.py"),
        ("CK", "7. Hiệu năng & Ổn định", "Chương 2 (2.2) & Ch.10", "12/12 Test Passed (100%)", "Pytest TestClient"),
        ("CK", "8. Triển khai & Đóng gói", "Chương 12 & Bảng 12.1", "Seed data 3 tài khoản", "app/db/seed_data.py"),
        ("CK", "9. Báo cáo kỹ thuật", "Toàn bộ 16 Chương", "Word chuẩn Bộ & LaTeX", "báo cáo dự án nhóm 11.docx"),
        ("CK", "10. Thuyết trình & Demo", "Chương 15 (15.1 - 15.2)", "Kịch bản demo 5 bước", "Live Demo Port 3000/8000"),
    ]

    tbl_m40 = doc.add_table(rows=len(matrix_40_data) + 1, cols=5)
    tbl_m40.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_m40.autofit = False
    set_table_borders(tbl_m40, color="000000", sz="10")
    m40_widths = [Inches(0.7), Inches(1.85), Inches(1.15), Inches(1.35), Inches(1.35)]
    m40_hdrs = ["Bài KT", "Tiêu chí kiểm tra", "Chương / Mục", "Minh chứng", "File / Mã nguồn"]
    trPr_m0 = tbl_m40.rows[0]._tr.get_or_add_trPr()
    trPr_m0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    for i, h in enumerate(m40_hdrs):
        c = tbl_m40.rows[0].cells[i]
        c.width = m40_widths[i]
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=35, bottom=35, left=50, right=50)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(13.5), True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_vals in enumerate(matrix_40_data):
        row = tbl_m40.rows[r_idx + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        bg_c = "f8fafc" if r_idx % 2 == 1 else "ffffff"
        for c_idx, val in enumerate(row_vals):
            c = row.cells[c_idx]
            c.width = m40_widths[c_idx]
            set_cell_background(c, bg_c)
            set_cell_margins(c, top=30, bottom=30, left=45, right=45)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name, r.font.size = "Times New Roman", Pt(12.5)
            if c_idx == 0:
                r.font.bold = True
                if val == "KT1":
                    r.font.color.rgb = RGBColor(30, 58, 138)
                elif val == "KT2":
                    r.font.color.rgb = RGBColor(14, 116, 144)
                elif val == "KT3":
                    r.font.color.rgb = RGBColor(180, 83, 9)
                else:
                    r.font.color.rgb = RGBColor(16, 185, 129)

    doc.add_page_break()

    # =========================================================================
    # CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI
    # =========================================================================
    add_h1("CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI")
    add_h2("1.1. Bối cảnh bài toán quản lý kho tại các doanh nghiệp vừa và nhỏ")
    add_p("Trong nền kinh tế thị trường số hóa, hệ thống kho bãi giữ vai trò mạch máu luân chuyển hàng hóa. Tuy nhiên, khảo sát thực tế tại các doanh nghiệp vừa và nhỏ (SMEs) tại Việt Nam cho thấy đa số vẫn quản lý bằng sổ tay hoặc các tệp Excel phân mảnh. Phương pháp thủ công này bộc lộ các yếu điểm nghiêm trọng: độ trễ dữ liệu từ 1 đến 3 ngày, sai sót do nhập liệu trùng lặp, tình trạng chôn vốn do hàng tồn kho nằm bất động (Dead-stock) hoặc đứt gãy cung ứng do cạn hàng đột ngột (Stock-out).")
    
    add_h2("1.2. Mục tiêu, đối tượng và phạm vi nghiên cứu")
    add_bullet("Mục tiêu tổng quát: ", "Xây dựng một hệ thống phần mềm Quản lý Kho thông minh có tích hợp Trí tuệ Nhân tạo hỗ trợ tự động hóa nghiệp vụ xuất nhập tồn, phân tích vận tốc tiêu thụ hàng hóa và tương tác tự nhiên với người vận hành.")
    add_bullet("Mục tiêu cụ thể: ", "Thiết kế CSDL chuẩn hóa 3NF 11 bảng; Xây dựng Backend FastAPI hiệu năng cao; Thiết kế Frontend React Vite SaaS UI; Hiện thực hóa Pipeline AI 2 lớp (Cloud Gemini LLM + Local Deterministic Rule Engine); Kiểm thử tự động đạt tỷ lệ 100% Passed.")
    add_bullet("Đối tượng và phạm vi: ", "Áp dụng cho các nhà kho phân phối phụ kiện công nghệ, máy tính, thiết bị mạng với quy trình phân quyền 3 vai trò: Quản trị viên, Thủ kho và Kế toán.")

    add_h2("1.3. Phương pháp nghiên cứu và cách tiếp cận ứng dụng Trí tuệ Nhân tạo")
    add_p("Dự án áp dụng phương pháp luận kỹ nghệ phần mềm chuẩn mực kết hợp với nguyên tắc Chống ảo giác dữ liệu (Anti-Hallucination). Trí tuệ Nhân tạo không được tự ý suy diễn hoặc bịa đặt số liệu mà bắt buộc phải dựa trên Ảnh chụp dữ liệu kho thực tế (Ground-Truth DB Context Snapshot). Hệ thống xây dựng cơ chế dự phòng kép (Dual-layer Resilience) để đảm bảo luôn hoạt động ổn định kể cả khi mất kết nối mạng.")

    # =========================================================================
    # CHƯƠNG 2. PHÂN TÍCH YÊU CẦU
    # =========================================================================
    add_h1("CHƯƠNG 2. PHÂN TÍCH YÊU CẦU")
    add_h2("2.1. Yêu cầu chức năng chi tiết (Functional Requirements)")
    add_p("Hệ thống được thiết kế để đáp ứng toàn diện 9 nhóm yêu cầu chức năng nghiệp vụ sau (Bảng 2.1):")

    add_p("Bảng 2.1: Danh mục các yêu cầu chức năng cốt lõi của hệ thống (FR01 - FR09)", bold=True, pt_size=13.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    tbl_fr = doc.add_table(rows=10, cols=3)
    tbl_fr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_fr.autofit = False
    set_table_borders(tbl_fr, color="000000", sz="10")
    fr_widths = [Inches(1.0), Inches(2.2), Inches(3.2)]
    trPr_fr0 = tbl_fr.rows[0]._tr.get_or_add_trPr()
    trPr_fr0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    fr_hdrs = ["Mã FR", "Tên phân hệ chức năng", "Mô tả chi tiết yêu cầu nghiệp vụ"]
    for i, h in enumerate(fr_hdrs):
        c = tbl_fr.rows[0].cells[i]
        c.width = fr_widths[i]
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=50, bottom=50, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(14.5), True
        r.font.color.rgb = RGBColor(255, 255, 255)

    fr_data = [
        ("FR01", "Xác thực & Phân quyền (RBAC)", "Đăng nhập an toàn nhận Bearer JWT, băm mật khẩu Argon2, phân định 3 vai trò Admin, Warehouse, Accountant."),
        ("FR02", "Quản lý Dữ liệu nền tảng", "Quản lý danh mục nhóm hàng, danh sách nhà cung cấp, sơ đồ vị trí ô kệ (Zone/Shelf) có giới hạn sức chứa."),
        ("FR03", "Quản lý Danh mục Sản phẩm", "Quản lý mã SKU duy nhất, tên hàng, đơn vị tính, giá vốn, giá bán, định mức an toàn tối thiểu và tối đa."),
        ("FR04", "Quản lý Giao dịch Nhập kho", "Tạo phiếu nhập hàng từ nhà cung cấp, kiểm đếm thực tế, phân bổ số lượng vào từng vị trí ô kệ cụ thể."),
        ("FR05", "Quản lý Giao dịch Xuất kho", "Tạo phiếu xuất hàng, tự động kiểm tra số lượng tồn khả dụng, khóa hàng an toàn chống xung đột đồng thời."),
        ("FR06", "Dự báo Tồn kho AI (Forecast)", "Tính tốc độ tiêu thụ ngày (Burn-rate), dự đoán số ngày cạn tồn (Depletion Days) và gợi ý số lượng tái đặt hàng."),
        ("FR07", "Phát hiện Bất thường AI (Anomaly)", "Áp dụng kiểm định thống kê Z-score để gắn cờ giao dịch xuất kho đột biến hoặc cảnh báo hàng tồn kho đóng băng."),
        ("FR08", "Trợ lý Hỏi Đáp Kho AI (NLP Chat)", "Cung cấp giao diện chat thông minh nhận câu hỏi tự nhiên bằng tiếng Việt, trả lời bằng thẻ giao diện và bảng số liệu."),
        ("FR09", "Nhật ký Kiểm toán (Audit Trail)", "Tự động ghi nhận vết bất biến cho mọi thao tác C/U/D kèm User ID, địa chỉ IP, giá trị JSON trước và sau thay đổi."),
    ]
    for r_idx, fr_row in enumerate(fr_data):
        row = tbl_fr.rows[r_idx + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for c_idx, val in enumerate(fr_row):
            c = row.cells[c_idx]
            c.width = fr_widths[c_idx]
            set_cell_margins(c, top=45, bottom=45, left=65, right=65)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name, r.font.size = "Times New Roman", Pt(13.5)
            if c_idx == 0:
                r.font.bold = True

    add_h2("2.2. Yêu cầu phi chức năng (Non-Functional Requirements)")
    add_bullet("Tính bảo mật (Security): ", "Tuân thủ tiêu chuẩn an toàn OWASP Top 10, phòng chống SQL Injection bằng tham số hóa ORM, chống XSS và kiểm soát CORS nghiêm ngặt.")
    add_bullet("Hiệu năng xử lý (Performance): ", "Thời gian đáp ứng của các API CRUD cơ bản < 100ms; bộ máy AI cục bộ phản hồi < 50ms; API đám mây Cloud LLM phản hồi < 1.5s.")
    add_bullet("Tính toàn vẹn dữ liệu (Data Integrity): ", "Thực thi toàn bộ các giao dịch xuất nhập hàng trong Transaction ACID của CSDL, đảm bảo nếu có lỗi bất kỳ thì Rollback hoàn toàn.")
    add_bullet("Giao diện và trải nghiệm (Usability): ", "Thiết kế SaaS Dark Mode hiện đại lấy cảm hứng từ HorizonX và 21st.dev, hỗ trợ hiển thị tối ưu trên máy tính và máy tính bảng nhà kho.")

    # =========================================================================
    # CHƯƠNG 3. PHÂN TÍCH ACTOR VÀ USE CASE
    # =========================================================================
    add_h1("CHƯƠNG 3. PHÂN TÍCH ACTOR VÀ USE CASE")
    add_h2("3.1. Xác định và phân quyền 3 tác nhân Actor")
    add_bullet("1. Quản trị viên (Admin): ", "Người chịu trách nhiệm cao nhất về hệ thống. Có quyền tạo mới tài khoản nhân viên, cấu hình thông số kho, quản lý danh mục SKU và xem toàn bộ vết kiểm toán Audit Log.")
    add_bullet("2. Thủ kho (Warehouse Staff): ", "Người trực tiếp kiểm đếm hàng hóa tại kho. Có quyền lập phiếu nhập hàng, xếp hàng vào kệ, tạo phiếu xuất kho giao hàng và sử dụng AI Hub để tra cứu tồn.")
    add_bullet("3. Kế toán kho (Accountant): ", "Người theo dõi giá trị tài sản và dòng tiền. Có quyền xem báo cáo tồn kho tổng hợp, định giá tài sản kho theo VNĐ, kiểm tra doanh thu xuất và chi phí nhập.")

    add_h2("3.2. Sơ đồ Use Case tổng thể hệ thống")
    add_p("Sơ đồ Use Case tổng thể được thiết kế phân định ranh giới chức năng rõ ràng giữa 3 tác nhân thông qua Hình 3.1 dưới đây:")
    add_image("02_so_do_usecase_tong_the.png", "Hình 3.1: Sơ đồ Use Case tổng thể hệ thống phân quyền 3 tác nhân (Nhóm 11)")

    add_h2("3.3. Đặc tả các Use Case cốt lõi")
    add_p("Các Use Case trọng yếu như 'Tạo phiếu nhập kho', 'Tạo phiếu xuất kho', 'Tra cứu tồn kho thông minh' và 'Hỏi đáp AI' đều được thiết kế chặt chẽ với điều kiện tiên quyết (Pre-condition), luồng sự kiện chính (Main flow) và luồng rẽ nhánh xử lý ngoại lệ (Exception flow).")

    # =========================================================================
    # CHƯƠNG 4. THIẾT KẾ QUY TRÌNH NGHIỆP VỤ
    # =========================================================================
    add_h1("CHƯƠNG 4. THIẾT KẾ QUY TRÌNH NGHIỆP VỤ")
    add_h2("4.1. Lược đồ hoạt động quy trình Nhập kho")
    add_p("Quy trình nhập kho bắt đầu khi hàng hóa từ nhà cung cấp cập bến. Thủ kho bắt buộc phải thực hiện bước kiểm tra quy cách thực tế trước khi xác nhận lưu kho (Hình 4.1):")
    add_image("04_luoc_do_hoat_dong_nhap_kho.png", "Hình 4.1: Lược đồ hoạt động quy trình nhập hàng và phân bổ vị trí kệ kho (Nhóm 11)")

    add_h2("4.2. Lược đồ hoạt động quy trình Xuất kho và kiểm tra tồn khả dụng")
    add_p("Tại quy trình xuất kho, hệ thống áp dụng cơ chế khóa an toàn và kiểm tra tồn khả dụng (Available Stock) để ngăn chặn hoàn toàn tình trạng xuất âm (Hình 4.2):")
    add_image("05_luoc_do_hoat_dong_xuat_kho.png", "Hình 4.2: Lược đồ hoạt động quy trình xuất kho và kiểm tra tồn khả dụng (Nhóm 11)")

    add_h2("4.3. Quy trình kiểm kê định kỳ và xử lý cân bằng kho")
    add_p("Định kỳ hàng tháng, thủ kho tiến hành kiểm đếm thực tế và đối chiếu với số liệu trên phần mềm. Nếu phát hiện chênh lệch do hao hụt vật lý, hệ thống hỗ trợ tạo phiếu điều chỉnh (Adjustment Slip) và ghi nhận rõ ràng vào nhật ký kiểm toán.")

    # =========================================================================
    # CHƯƠNG 5. THIẾT KẾ CƠ SỞ DỮ LIỆU
    # =========================================================================
    add_h1("CHƯƠNG 5. THIẾT KẾ CƠ SỞ DỮ LIỆU")
    add_h2("5.1. Sơ đồ thực thể liên kết (ERD) tổng quan 11 bảng CSDL chuẩn hóa 3NF")
    add_p("Cơ sở dữ liệu của hệ thống được thiết kế theo mô hình quan hệ (RDBMS) và chuẩn hóa ở dạng chuẩn 3 (3NF), đảm bảo loại bỏ hoàn toàn các dị thường thêm, sửa, xóa (Anomalies) và tối ưu hóa hiệu năng truy vấn. Sơ đồ ERD tổng quan 11 bảng được bố cục theo 3 phân hệ kiến trúc độc lập (Hình 5.1):")
    add_image("03_so_do_erd_11_bang.png", "Hình 5.1: Sơ đồ Thực thể Liên kết (ERD) tổng quan 11 bảng CSDL chuẩn hóa 3NF (Nhóm 11)", width_inches=6.3)

    add_h2("5.2. Thiết kế chi tiết các phân hệ cơ sở dữ liệu")
    add_p("Để thuận tiện cho công tác kiểm tra, phát triển và bảo trì hệ thống, cấu trúc 11 bảng CSDL được phân rã chi tiết thành 3 phân hệ nghiệp vụ độc lập:")

    add_h3("5.2.1. Phân hệ Quản trị người dùng, Phân quyền RBAC & Nhật ký AI")
    add_p("Phân hệ quản lý toàn bộ định danh người dùng, kiểm soát phân quyền 3 vai trò (ADMIN, WAREHOUSE, ACCOUNTANT), lưu vết kiểm toán bất biến (Audit Trail) và lịch sử truy vấn trí tuệ nhân tạo (Hình 5.2):")
    add_image("03a_erd_nhom_nguoi_dung_ai.png", "Hình 5.2: Sơ đồ ERD phân hệ Quản trị người dùng, Phân quyền RBAC & AI Logs (Nhóm 11)", width_inches=6.2)

    add_h3("5.2.2. Phân hệ Danh mục Hàng hóa, Nhà cung cấp & Sơ đồ Vị trí Kệ kho")
    add_p("Phân hệ quản lý các thực thể dữ liệu nền tảng (Master Data), quy tắc định danh mã SKU duy nhất, thông tin đối tác cung ứng và tọa độ vật lý ô kệ kho (Zone, Shelf, Level, Sức chứa tối đa) (Hình 5.3):")
    add_image("03b_erd_nhom_danh_muc_kho.png", "Hình 5.3: Sơ đồ ERD phân hệ Danh mục Hàng hóa, Nhà cung cấp & Vị trí Kệ kho (Nhóm 11)", width_inches=6.2)

    add_h3("5.2.3. Phân hệ Quản lý Tồn kho Khả dụng & Giao dịch Nhập / Xuất kho")
    add_p("Phân hệ trung tâm quản lý số lượng tồn kho thực tế, số lô sản xuất, hạn sử dụng, cơ chế khóa dòng tạm thời (Row-level Locking) và nhật ký chứng từ giao dịch xuất nhập kho an toàn (Hình 5.4):")
    add_image("03c_erd_nhom_ton_kho_giao_dich.png", "Hình 5.4: Sơ đồ ERD phân hệ Quản lý Tồn kho & Giao dịch Xuất Nhập kho (Nhóm 11)", width_inches=6.2)

    add_h2("5.3. Danh mục 11 bảng cơ sở dữ liệu quan hệ")
    add_p("Bảng 5.1 tóm lược danh mục 11 bảng CSDL quan hệ được cài đặt thông qua SQLAlchemy ORM:")

    add_p("Bảng 5.1: Danh mục 11 bảng cơ sở dữ liệu quan hệ chuẩn hóa 3NF của hệ thống", bold=True, pt_size=13.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    tbl_db_cat = doc.add_table(rows=12, cols=3)
    tbl_db_cat.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_db_cat.autofit = False
    set_table_borders(tbl_db_cat, color="000000", sz="10")
    db_cat_widths = [Inches(0.6), Inches(2.0), Inches(3.8)]
    trPr_cat0 = tbl_db_cat.rows[0]._tr.get_or_add_trPr()
    trPr_cat0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    for i, h in enumerate(["STT", "Tên bảng trong CSDL", "Vai trò và chức năng lưu trữ nghiệp vụ"]):
        c = tbl_db_cat.rows[0].cells[i]
        c.width = db_cat_widths[i]
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=50, bottom=50, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(14.5), True
        r.font.color.rgb = RGBColor(255, 255, 255)

    db_cat_data = [
        ("1", "roles", "Lưu trữ danh sách vai trò phân quyền: ADMIN, WAREHOUSE, ACCOUNTANT."),
        ("2", "users", "Lưu trữ tài khoản người dùng, mật khẩu băm Argon2, họ tên, email và khóa ngoại role_id."),
        ("3", "categories", "Danh mục nhóm sản phẩm: Thiết bị mạng, Bàn phím cơ, Màn hình máy tính, Phụ kiện..."),
        ("4", "suppliers", "Thông tin đối tác cung cấp hàng hóa: Tên pháp nhân, người liên hệ, số điện thoại, địa chỉ."),
        ("5", "locations", "Vị trí ô kệ vật lý trong nhà kho: Mã vị trí (A1-01), Khu vực (Zone A/B), Tầng kệ, Sức chứa."),
        ("6", "products", "Bảng trung tâm quản lý sản phẩm: Mã SKU duy nhất, tên hàng, đơn vị, giá vốn, giá bán, min/max."),
        ("7", "inventory_items", "Quản lý tồn kho thực tế tại từng vị trí kệ, theo dõi số lô (Batch) và hạn sử dụng."),
        ("8", "inventory_transactions", "Phiếu giao dịch xuất nhập kho: Mã phiếu chứng từ, loại giao dịch (IMP/EXP), người lập, tổng tiền."),
        ("9", "inventory_transaction_items", "Dòng chi tiết các mặt hàng xuất nhập trong phiếu: SKU, vị trí lấy hàng, số lượng, đơn giá."),
        ("10", "audit_logs", "Vết kiểm toán bất biến: Ghi nhận User ID, thao tác C/U/D, bảng bị tác động, giá trị cũ/mới JSON, IP."),
        ("11", "ai_query_logs", "Nhật ký AI: Lưu câu hỏi người dùng, phân loại truy vấn, ảnh chụp dữ liệu, thời gian thực thi ms."),
    ]
    for r_idx, cat in enumerate(db_cat_data):
        row = tbl_db_cat.rows[r_idx + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for c_idx, val in enumerate(cat):
            c = row.cells[c_idx]
            c.width = db_cat_widths[c_idx]
            set_cell_margins(c, top=45, bottom=45, left=65, right=65)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name, r.font.size = "Times New Roman", Pt(13.5)
            if c_idx in [0, 1]:
                r.font.bold = True

    add_h2("5.4. Ràng buộc toàn vẹn tham chiếu và cơ chế ACID Database Transaction")
    add_p("Hệ thống cài đặt đầy đủ các ràng buộc khóa ngoại (Foreign Keys) có thiết lập cơ chế kiểm soát xóa (ON DELETE RESTRICT) để bảo vệ tính toàn vẹn dữ liệu. Khi thực hiện giao dịch nhập xuất gồm nhiều mặt hàng, SQLAlchemy Session kích hoạt Transaction đảm bảo trọn vẹn 4 tính chất ACID (Atomicity, Consistency, Isolation, Durability).")

    # =========================================================================
    # CHƯƠNG 6. KIẾN TRÚC HỆ THỐNG
    # =========================================================================
    add_h1("CHƯƠNG 6. KIẾN TRÚC HỆ THỐNG")
    add_h2("6.1. Thiết kế Kiến trúc 3 tầng tổng thể")
    add_p("Hệ thống được thiết kế theo mô hình Kiến trúc 3 tầng phân tách độc lập các trách nhiệm (Hình 6.1):")
    add_image("01_so_do_kien_truc_he_thong.png", "Hình 6.1: Sơ đồ Kiến trúc tổng thể 3 tầng của hệ thống Quản lý Kho AI (Nhóm 11)")
    add_bullet("1. Tầng Trình diễn (Presentation Tier): ", "Xây dựng trên nền React 18 SPA với trình đóng gói Vite siêu tốc, giao diện Tailwind CSS và bộ biểu tượng Lucide React.")
    add_bullet("2. Tầng Nghiệp vụ (Application Tier): ", "Xây dựng bằng FastAPI Async Web Framework (Python 3.14) theo nguyên lý Clean Architecture (tách riêng routers, models, schemas, services).")
    add_bullet("3. Tầng Dữ liệu & Đám mây (Data Tier): ", "Hệ quản trị CSDL quan hệ (SQLite cho dev, PostgreSQL cho production) và dịch vụ AI đám mây Google Gemini 1.5 Flash.")

    add_h2("6.2. Sơ đồ tuần tự xử lý giao dịch an toàn")
    add_p("Sơ đồ tuần tự tại Hình 6.2 mô tả chi tiết quy trình xử lý giao dịch kho từ khi Client gửi yêu cầu, qua lớp xác thực Bearer Token, kiểm tra tồn kho, cập nhật CSDL và ghi vết kiểm toán:")
    add_image("06_so_do_tuan_tu_nhap_xuat.png", "Hình 6.2: Sơ đồ tuần tự giao dịch nhập xuất kho an toàn (Nhóm 11)")

    add_h2("6.3. Sơ đồ điều hướng giao diện người dùng (Frontend Sitemap)")
    add_p("Cây điều hướng giao diện tại Hình 6.3 mô tả cấu trúc menu và luồng di chuyển của các phân hệ trên giao diện người dùng:")
    add_image("10_so_do_sitemap_giao_dien.png", "Hình 6.3: Sơ đồ cấu trúc điều hướng cây giao diện người dùng (Nhóm 11)")

    # =========================================================================
    # CHƯƠNG 7. THIẾT KẾ CHI TIẾT CHỨC NĂNG
    # =========================================================================
    add_h1("CHƯƠNG 7. THIẾT KẾ CHI TIẾT CHỨC NĂNG")
    add_h2("7.1. Phân hệ Quản lý Danh mục và Sản phẩm SKU")
    add_p("Cho phép Quản trị viên thêm mới, sửa đổi thông tin sản phẩm SKU, thiết lập giá vốn, giá niêm yết bán lẻ và định mức cảnh báo tồn tối thiểu/tối đa. Giao diện trang bị bộ lọc tức thì (Instant Filter) theo tên, mã SKU hoặc nhóm ngành hàng.")

    add_h2("7.2. Phân hệ Quản lý Giao dịch Nhập xuất kho")
    add_p("Cung cấp biểu mẫu tạo phiếu nhập hàng từ nhà cung cấp và phiếu xuất hàng giao khách. Hệ thống tự động tính thành tiền từng mặt hàng, kiểm tra sức chứa ô kệ và cập nhật số lượng tồn kho khả dụng theo thời gian thực.")

    add_h2("7.3. Phân hệ Vị trí lưu kho và Sơ đồ kệ chứa (Zone/Shelf)")
    add_p("Mô phỏng sơ đồ vật lý của nhà kho theo từng phân khu (Zone A: Đồ điện tử giá trị cao, Zone B: Phụ kiện) và dãy kệ (Shelf 01 - 05). Hỗ trợ thủ kho định vị nhanh vị trí mặt hàng cần lấy.")

    add_h2("7.4. Phân hệ Thống kê Dashboard và Định giá tài sản kho")
    add_p("Hiển thị 6 thẻ chỉ số KPI tổng hợp: Tổng số SKU, Tổng sản lượng hàng tồn, Số mặt hàng đang báo động đỏ dưới định mức an toàn, Tổng giá trị tài sản kho theo VNĐ, Doanh thu xuất và Chi phí nhập.")

    # =========================================================================
    # CHƯƠNG 8. THIẾT KẾ VÀ TÍCH HỢP AI
    # =========================================================================
    add_h1("CHƯƠNG 8. THIẾT KẾ VÀ TÍCH HỢP AI")
    add_h2("8.1. Định vị vai trò của AI và Kiến trúc Pipeline 2 lớp")
    add_p("Trí tuệ Nhân tạo đóng vai trò là 'Bộ não phân tích chuyên sâu'. Để đảm bảo hệ thống có độ sẵn sàng cao nhất (High Availability), nhóm 11 đã thiết kế thành công Pipeline AI 2 lớp (Hình 8.1):")
    add_image("07_so_do_pipeline_ai_fallback.png", "Hình 8.1: Sơ đồ kiến trúc Pipeline AI 2 lớp linh hoạt (Nhóm 11)")

    add_h2("8.2. Lớp 1: Cloud LLM (Google Gemini) với phân tích sâu")
    add_p("Sử dụng mô hình gemini-1.5-flash tiếp nhận ảnh chụp dữ liệu kho thực tế để sinh ra báo cáo phân tích nhận định bằng văn bản tự nhiên, kèm bảng Markdown trực quan và gợi ý chiến lược quản trị.")

    add_h2("8.3. Lớp 2: Local Deterministic Rule Engine với độ tin cậy tuyệt đối")
    add_p("Xây dựng bằng thuật toán thống kê Python nội tại. Khi mất kết nối internet hoặc tài khoản Cloud AI hết hạn mức, hệ thống tự động chuyển vùng sang bộ máy tính toán cục bộ trong 20ms, đảm bảo các tính năng dự báo tồn và cảnh báo bất thường không bao giờ bị gián đoạn.")

    add_h2("8.4. Trợ lý Hỏi Đáp Kho AI Tự Nhiên (NLP Assistant)")
    add_p("Endpoint chuyên biệt POST /api/ai/ask cho phép người dùng hỏi đáp bằng tiếng Việt tự nhiên ('Kho còn bao nhiêu bàn phím cơ AKKO?'). Sơ đồ tuần tự xử lý được mô tả tại Hình 8.2:")
    add_image("08_so_do_tuan_tu_hoi_dap_ai.png", "Hình 8.2: Sơ đồ tuần tự Trợ lý hỏi đáp kho bằng ngôn ngữ tự nhiên (Nhóm 11)")

    # =========================================================================
    # CHƯƠNG 9. THIẾT KẾ PROMPT VÀ THỬ NGHIỆM
    # =========================================================================
    add_h1("CHƯƠNG 9. THIẾT KẾ PROMPT VÀ THỬ NGHIỆM")
    add_h2("9.1. Kỹ nghệ thiết kế Prompt có cấu trúc và Ground-Truth Context Injection")
    add_p("Để AI đưa ra câu trả lời chính xác, hệ thống áp dụng kỹ thuật Ground-Truth Context Injection: Truy vấn số liệu tồn kho thực tế từ CSDL, đóng gói thành cấu trúc JSON và bơm trực tiếp vào System Prompt trước khi gửi đến mô hình AI.")

    add_h2("9.2. Cơ chế chống ảo giác số liệu (Anti-Hallucination Framework)")
    add_p("System Prompt quy định nghiêm ngặt: (1) Chỉ sử dụng dữ liệu được cung cấp trong snapshot; (2) Tuyệt đối không tự bịa đặt số lượng tồn hoặc giá bán; (3) Nếu sản phẩm chưa có lịch sử xuất, ghi rõ 'Tồn ổn định / Chưa phát sinh xuất', không được báo lỗi.")

    add_h2("9.3. Mô hình toán học: Daily Burn-rate, Depletion Days và Z-score Anomaly")
    add_p("Hệ thống ứng dụng các công thức thống kê toán học cụ thể (Lưu đồ thuật toán tại Hình 9.1):")
    add_bullet("1. Tốc độ xuất kho bình quân ngày (Daily Burn Rate - V): ", "V = (Tổng lượng xuất 30 ngày) / 30.")
    add_bullet("2. Số ngày cạn tồn dự kiến (Depletion Days - D): ", "D = Tồn kho hiện tại / V (Nếu V > 0); Nếu V = 0 thì D = Vô hạn ngày (Tồn an toàn). Nhờ đó loại bỏ hoàn toàn lỗi chia cho 0.")
    add_bullet("3. Đề xuất số lượng cần tái nhập (Reorder Quantity - Q): ", "Q = max(0, max_threshold - Tồn kho hiện tại).")
    add_bullet("4. Phát hiện bất thường qua độ lệch chuẩn (Z-score): ", "Z = (X - μ) / σ. Nếu |Z| > 2.5 hoặc lượng xuất vượt 300% mức bình quân, hệ thống gắn cờ Cảnh báo Bất thường.")
    add_image("09_so_do_phan_tich_bat_thuong.png", "Hình 9.1: Lưu đồ thuật toán kiểm tra số ngày cạn tồn và phát hiện bất thường (Nhóm 11)")

    # =========================================================================
    # CHƯƠNG 10. KIỂM THỬ
    # =========================================================================
    add_h1("CHƯƠNG 10. KIỂM THỬ")
    add_h2("10.1. Chiến lược kiểm thử phần mềm tự động bằng Pytest")
    add_p("Nhóm 11 áp dụng phương pháp kiểm thử tự động hóa toàn diện (Automated Testing) với thư viện Pytest và FastAPI TestClient, kiểm thử từ các API xác thực, CRUD sản phẩm, giao dịch xuất nhập cho đến bộ máy AI.")

    add_h2("10.2. Kết quả thực nghiệm bộ kiểm thử 12 ca kiểm thử tự động")
    add_p("Bảng 10.1 tổng hợp kết quả chạy thực nghiệm toàn bộ 12 ca kiểm thử tự động của hệ thống:")

    add_p("Bảng 10.1: Bảng tổng hợp kết quả chạy bộ kiểm thử tự động Backend (Pytest Suite 12/12 Passed)", bold=True, pt_size=13.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    tbl_tc = doc.add_table(rows=13, cols=4)
    tbl_tc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_tc.autofit = False
    set_table_borders(tbl_tc, color="000000", sz="10")
    tc_widths = [Inches(0.7), Inches(2.2), Inches(2.3), Inches(1.2)]
    trPr_tc0 = tbl_tc.rows[0]._tr.get_or_add_trPr()
    trPr_tc0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    for i, h in enumerate(["Mã", "Tên hàm kiểm thử (Test Function)", "Kịch bản và hành vi kiểm thử", "Kết quả"]):
        c = tbl_tc.rows[0].cells[i]
        c.width = tc_widths[i]
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=45, bottom=45, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(14.5), True
        r.font.color.rgb = RGBColor(255, 255, 255)

    tc_data = [
        ("TC01", "test_health_check", "Kiểm tra trạng thái máy chủ FastAPI khởi động sẵn sàng", "100% PASSED"),
        ("TC02", "test_login_success", "Đăng nhập tài khoản hợp lệ admin nhận Bearer JWT Token", "100% PASSED"),
        ("TC03", "test_login_invalid_password", "Đăng nhập sai mật khẩu trả về HTTP 401 Unauthorized", "100% PASSED"),
        ("TC04", "test_get_products_list", "Lấy danh sách sản phẩm với Header Bearer Token", "100% PASSED"),
        ("TC05", "test_create_product_admin", "Admin tạo mới sản phẩm với đầy đủ mã SKU và định mức", "100% PASSED"),
        ("TC06", "test_create_product_forbidden", "Tài khoản nhân viên kho bị chặn khi cố tạo SKU (HTTP 403)", "100% PASSED"),
        ("TC07", "test_inventory_import_flow", "Quy trình tạo phiếu nhập kho và cộng dồn số lượng tồn", "100% PASSED"),
        ("TC08", "test_inventory_export_insufficient", "Xuất hàng vượt quá tồn kho thực tế bị chặn an toàn (HTTP 400)", "100% PASSED"),
        ("TC09", "test_dashboard_kpis", "Kiểm tra 6 chỉ số KPI kho và giá trị tài sản tính đúng VNĐ", "100% PASSED"),
        ("TC10", "test_ai_restock_forecast", "Dự báo nhu cầu nhập kho và tính toán Depletion Days không lỗi", "100% PASSED"),
        ("TC11", "test_ai_anomaly_detection", "Phát hiện biến động xuất kho đột biến qua độ lệch chuẩn", "100% PASSED"),
        ("TC12", "test_ai_assistant_ask", "Trợ lý hỏi đáp tự nhiên NLP trả về bảng Markdown và JSON snapshot", "100% PASSED"),
    ]
    for r_idx, tc in enumerate(tc_data):
        row = tbl_tc.rows[r_idx + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for c_idx, val in enumerate(tc):
            c = row.cells[c_idx]
            c.width = tc_widths[c_idx]
            set_cell_margins(c, top=40, bottom=40, left=55, right=55)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name, r.font.size = "Times New Roman", Pt(13.5)
            if c_idx == 3:
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129)

    add_h2("10.3. Kiểm thử an toàn ngoại lệ và xử lý lỗi HTTP toàn cục")
    add_p("Hệ thống cài đặt các Global Exception Handler nhằm bắt trọn vẹn các mã lỗi HTTP tiêu chuẩn: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found và 422 Unprocessable Entity, không bao giờ để lộ lỗi 500 Internal Server Error ra phía người dùng.")

    # =========================================================================
    # CHƯƠNG 11. BẢO MẬT VÀ ĐẠO ĐỨC AI
    # =========================================================================
    add_h1("CHƯƠNG 11. BẢO MẬT VÀ ĐẠO ĐỨC AI")
    add_h2("11.1. Tuân thủ tiêu chuẩn an toàn OWASP Top 10 và bảo vệ cơ sở dữ liệu")
    add_p("Bảo vệ hệ thống trước các nguy cơ tấn công mạng phổ biến: Chống SQL Injection nhờ cơ chế Parameterized Query của SQLAlchemy; Chống Cross-Site Scripting (XSS) nhờ React tự động escape HTML; Cấu hình CORS chặt chẽ giới hạn domain tin cậy.")

    add_h2("11.2. Xác thực JWT, băm mật khẩu Argon2 và Ma trận phân quyền RBAC")
    add_p("Bảng 11.1 thể hiện ma trận phân quyền truy cập Role-Based Access Control (RBAC) chi tiết giữa 3 vai trò người dùng:")

    add_p("Bảng 11.1: Ma trận phân quyền truy cập Role-Based Access Control (RBAC 3 vai trò)", bold=True, pt_size=13.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    tbl_rb = doc.add_table(rows=7, cols=5)
    tbl_rb.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_rb.autofit = False
    set_table_borders(tbl_rb, color="000000", sz="10")
    rb_widths = [Inches(1.8), Inches(1.5), Inches(1.0), Inches(1.1), Inches(1.0)]
    trPr_rb0 = tbl_rb.rows[0]._tr.get_or_add_trPr()
    trPr_rb0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    for i, h in enumerate(["Phân hệ chức năng", "Endpoint API", "ADMIN", "WAREHOUSE", "ACCOUNTANT"]):
        c = tbl_rb.rows[0].cells[i]
        c.width = rb_widths[i]
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=45, bottom=45, left=55, right=55)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(14.0), True
        r.font.color.rgb = RGBColor(255, 255, 255)

    rb_data = [
        ("Quản lý tài khoản & Quyền", "/api/users/*", "✓ Toàn quyền", "✗ Bị cấm (403)", "✗ Bị cấm (403)"),
        ("Xem Audit Trail Logs", "/api/audit-logs", "✓ Toàn quyền", "✗ Bị cấm (403)", "✗ Bị cấm (403)"),
        ("Tạo / Sửa / Xóa Sản phẩm", "/api/products", "✓ Cho phép", "✗ Bị cấm (403)", "✗ Bị cấm (403)"),
        ("Tạo phiếu Nhập / Xuất kho", "/api/inventory/trans", "✓ Cho phép", "✓ Phụ trách chính", "✗ Bị cấm (403)"),
        ("Xem Tồn kho & Tra cứu AI", "/api/inventory/stock", "✓ Cho phép", "✓ Cho phép", "✓ Cho phép"),
        ("Xem Định giá tài sản kho", "/api/reports/financial", "✓ Cho phép", "✗ Giới hạn", "✓ Phụ trách chính"),
    ]
    for r_idx, r_vals in enumerate(rb_data):
        row = tbl_rb.rows[r_idx + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for c_idx, val in enumerate(r_vals):
            c = row.cells[c_idx]
            c.width = rb_widths[c_idx]
            set_cell_margins(c, top=40, bottom=40, left=50, right=50)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name, r.font.size = "Times New Roman", Pt(13.0)
            if c_idx in [2, 3, 4]:
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129) if "✓" in val else RGBColor(239, 68, 68)

    add_h2("11.3. Đạo đức AI: Quyền riêng tư dữ liệu kho, tính minh bạch và vết kiểm toán")
    add_p("Hệ thống cam kết: (1) Tuyệt đối không gửi dữ liệu nhạy cảm của khách hàng hay thông tin giá trị tài sản riêng tư lên các API AI bên thứ ba nếu không được mã hóa; (2) AI luôn giải thích căn cứ số liệu minh bạch; (3) Mọi khuyến nghị của AI chỉ đóng vai trò tham vấn hỗ trợ, quyết định cuối cùng thuộc về người quản lý kho.")

    # =========================================================================
    # CHƯƠNG 12. TRIỂN KHAI HỆ THỐNG
    # =========================================================================
    add_h1("CHƯƠNG 12. TRIỂN KHAI HỆ THỐNG")
    add_h2("12.1. Yêu cầu môi trường phần cứng và phần mềm")
    add_bullet("Môi trường Phần mềm: ", "Hệ điều hành Windows 10/11 hoặc Linux Ubuntu 22.04; Python 3.10+ (Đã thử nghiệm tốt trên Python 3.14); Node.js v18+ và npm.")
    add_bullet("Môi trường Phần cứng: ", "Tối thiểu 4GB RAM, 2 CPU Cores, 2GB dung lượng ổ cứng trống.")

    add_h2("12.2. Hướng dẫn cài đặt và khởi chạy Backend FastAPI và Frontend Vite")
    add_bullet("Khởi chạy Backend: ", "Di chuyển vào thư mục backend: python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")
    add_bullet("Khởi chạy Frontend: ", "Di chuyển vào thư mục frontend: npm install && npm run dev (Truy cập tại http://localhost:3000)")

    add_h2("12.3. Danh sách tài khoản thử nghiệm hệ thống mặc định (Seed Data)")
    add_p("Bảng 12.1 cung cấp thông tin 3 tài khoản mẫu đã được khởi tạo sẵn trong cơ sở dữ liệu để phục vụ kiểm thử phân quyền:")

    add_p("Bảng 12.1: Danh sách tài khoản thử nghiệm hệ thống mặc định phân quyền 3 vai trò", bold=True, pt_size=13.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    tbl_ac = doc.add_table(rows=4, cols=4)
    tbl_ac.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_ac.autofit = False
    set_table_borders(tbl_ac, color="000000", sz="10")
    ac_widths = [Inches(1.2), Inches(1.3), Inches(1.2), Inches(2.7)]
    trPr_ac0 = tbl_ac.rows[0]._tr.get_or_add_trPr()
    trPr_ac0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    for i, h in enumerate(["Tên đăng nhập (Username)", "Mật khẩu mặc định", "Vai trò (Role)", "Quyền hạn chính"]):
        c = tbl_ac.rows[0].cells[i]
        c.width = ac_widths[i]
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=50, bottom=50, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(14.5), True
        r.font.color.rgb = RGBColor(255, 255, 255)

    ac_data = [
        ("admin", "Admin@123", "ADMIN", "Toàn quyền quản trị hệ thống, quản lý người dùng, xem Audit Log."),
        ("warehouse", "Warehouse@123", "WAREHOUSE", "Tạo phiếu nhập/xuất kho, quản lý sản phẩm, sử dụng AI Hub."),
        ("accountant", "Accountant@123", "ACCOUNTANT", "Xem báo cáo tài chính, định giá tài sản kho, tra cứu tồn kho."),
    ]
    for r_idx, ac in enumerate(ac_data):
        row = tbl_ac.rows[r_idx + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for c_idx, val in enumerate(ac):
            c = row.cells[c_idx]
            c.width = ac_widths[c_idx]
            set_cell_margins(c, top=45, bottom=45, left=65, right=65)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name, r.font.size = "Times New Roman", Pt(13.5)
            if c_idx in [0, 2]:
                r.font.bold = True

    # =========================================================================
    # CHƯƠNG 13. MINH CHỨNG SỬ DỤNG AI TRONG SDLC
    # =========================================================================
    add_h1("CHƯƠNG 13. MINH CHỨNG SỬ DỤNG AI TRONG SDLC")
    add_h2("13.1. Ứng dụng AI hỗ trợ phân tích yêu cầu và sinh sơ đồ kiến trúc")
    add_p("Trong giai đoạn khởi đầu dự án, nhóm sinh viên đã sử dụng các công cụ AI hỗ trợ (Antigravity Assistant) để gợi ý các ca sử dụng biên (Edge Use Cases), hỗ trợ phác thảo sơ đồ ERD chuẩn 3NF và sinh mã nguồn Draw.io XML tự động cho 10 bản vẽ kỹ thuật.")

    add_h2("13.2. Ứng dụng AI hỗ trợ lập trình, sinh Test Case và tối ưu hóa ORM")
    add_p("Trong giai đoạn lập trình Backend, AI được ứng dụng để sinh tự động khung kiểm thử Pytest TestClient, rà soát các câu truy vấn SQLAlchemy ORM tránh lỗi N+1 Query và gợi ý cơ chế băm mật khẩu Argon2 an toàn.")

    add_h2("13.3. Review mã nguồn tự động và giám sát chất lượng kỹ thuật")
    add_p("Nhóm áp dụng quy trình kiểm duyệt code tự động bằng AI trước khi tích hợp vào nhánh chính, đảm bảo tuân thủ chuẩn Clean Architecture, xử lý trọn vẹn ngoại lệ HTTP và đạt điểm tối đa trong Rubric đánh giá.")

    # =========================================================================
    # CHƯƠNG 14. ĐÁNH GIÁ THEO RUBRIC
    # =========================================================================
    add_h1("CHƯƠNG 14. ĐÁNH GIÁ THEO RUBRIC")
    add_h2("14.1. Bảng đối chiếu tự đánh giá theo 40 tiêu chí Rubric môn học AIA331")
    add_p("Bảng 14.1 tổng hợp kết quả tự đánh giá và đối chiếu sản phẩm với 40 tiêu chuẩn thuộc Rubric môn học AIA331 do Bộ môn ban hành:")

    rubric_summary_4 = [
        ("Giai đoạn KT1 (Phân tích bài toán, Actor, Use-case, ERD, Kiến trúc):", "Hoàn thành 10/10 tiêu chí (Đạt 2.5 / 2.5 điểm). Đầy đủ hồ sơ đặc tả, sơ đồ UML và ERD 11 bảng chuẩn 3NF."),
        ("Giai đoạn KT2 (Mã nguồn Backend, API, Database, Bảo mật):", "Hoàn thành 10/10 tiêu chí (Đạt 2.5 / 2.5 điểm). FastAPI Async, SQLAlchemy ORM, JWT, RBAC 3 vai trò, Audit Logs."),
        ("Giai đoạn KT3 (Tích hợp AI, Prompt Engineering, Thử nghiệm mô hình):", "Hoàn thành 10/10 tiêu chí (Đạt 2.5 / 2.5 điểm). Pipeline AI 2 lớp, Burn-rate & Depletion Days, Z-score, không chia 0."),
        ("Giai đoạn Đồ án Cuối kỳ (Giao diện hoàn chỉnh, Báo cáo Word & LaTeX, Demo):", "Hoàn thành 10/10 tiêu chí (Đạt 2.5 / 2.5 điểm). SaaS Dark Mode UI, Pytest 100% Passed, Báo cáo 16 chương hoàn chỉnh."),
    ]
    for r_title, r_desc in rubric_summary_4:
        add_bullet(r_title, " " + r_desc)

    add_p("Tổng kết điểm tự đánh giá toàn khóa: 10.0 / 10.0 điểm.", bold=True, pt_size=12, color=RGBColor(30, 58, 138), space_after=10)

    # =========================================================================
    # CHƯƠNG 15. DEMO HỆ THỐNG
    # =========================================================================
    add_h1("CHƯƠNG 15. DEMO HỆ THỐNG")
    add_h2("15.1. Kịch bản chạy demo thực tế hệ thống kho vận")
    add_bullet("Bước 1: ", "Đăng nhập với tài khoản admin, xem Dashboard tổng quan với 6 chỉ số KPI và biểu đồ tồn kho.")
    add_bullet("Bước 2: ", "Đăng nhập với tài khoản warehouse, tạo mới một phiếu nhập kho gồm 50 chiếc Bàn phím cơ AKKO vào vị trí kệ A1-01.")
    add_bullet("Bước 3: ", "Kiểm tra số lượng tồn tăng từ 15 lên 65 chiếc; sau đó tạo phiếu xuất kho 60 chiếc giao đại lý.")
    add_bullet("Bước 4: ", "Sau khi xuất, tồn kho chỉ còn 5 chiếc (dưới min_threshold = 10) -> Hệ thống lập tức bật đèn LED đỏ cảnh báo.")
    add_bullet("Bước 5: ", "Mở AI Analytics Hub -> Tab Hỏi đáp AI, gõ câu hỏi: 'Kho còn bao nhiêu bàn phím AKKO và có cần nhập thêm không?' -> AI phân tích chính xác và đưa ra bảng gợi ý nhập hàng.")

    add_h2("15.2. Hình ảnh minh chứng các giao diện SaaS Dashboard, Sản phẩm và AI Hub")
    add_p("Dưới đây là hình ảnh chụp màn hình thực tế các giao diện chức năng chính của hệ thống đang vận hành trực tiếp trên trình duyệt web tại cổng kết nối localhost:3000 (giữ nguyên trạng thái màu sắc thực tế làm minh chứng kỹ thuật):")
    add_image("11_screenshot_dashboard.png", "Hình 15.1: Giao diện SaaS Dashboard tổng quan và 6 thẻ chỉ số KPI kho", width_inches=6.2)
    add_image("12_screenshot_products.png", "Hình 15.2: Giao diện Quản lý Danh mục Sản phẩm và Smart Table Renderer", width_inches=6.2)
    add_image("13_screenshot_ai_report.png", "Hình 15.3: Giao diện AI Analytics Hub (Dự báo cạn tồn & Phát hiện dị biệt Z-score)", width_inches=6.2)
    add_image("14_screenshot_ai_assistant.png", "Hình 15.4: Giao diện Trợ lý Hỏi Đáp Kho AI Tự Nhiên (AI Chat Console)", width_inches=6.2)

    # =========================================================================
    # CHƯƠNG 16. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
    # =========================================================================
    add_h1("CHƯƠNG 16. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")
    add_h2("16.1. Tổng kết các kết quả đạt được của đề tài")
    add_p("Sau một học kỳ nỗ lực nghiên cứu và lập trình nghiêm túc, Nhóm 11 đã hoàn thành trọn vẹn toàn bộ mục tiêu đề ra cho đồ án môn học AIA331: Xây dựng thành công hệ thống Quản lý Kho hoàn chỉnh, vận hành thực tế ổn định, giao diện SaaS hiện đại, bảo mật đa tầng, Pipeline AI 2 lớp chống ảo giác số liệu và đạt tỷ lệ 100% ca kiểm thử tự động.")

    add_h2("16.2. Những hạn chế còn tồn tại")
    add_bullet("• ", "Chưa tích hợp trực tiếp với các thiết bị phần cứng kiểm kho chuyên dụng như máy quét mã vạch cầm tay PDA hay chip RFID qua giao thức IoT.")
    add_bullet("• ", "Mô hình dự báo nhu cầu hiện mới dựa trên tốc độ tiêu thụ bình quân 30 ngày và độ lệch chuẩn tĩnh, chưa xét đến yếu tố mùa vụ dài hạn (Seasonality).")

    add_h2("16.3. Hướng phát triển và mở rộng trong tương lai")
    add_bullet("• ", "Nghiên cứu ứng dụng các mô hình chuỗi thời gian học sâu (Deep Learning Time-Series như LSTM, Prophet) để dự báo nhu cầu nhập kho theo mùa vụ chính xác hơn.")
    add_bullet("• ", "Phát triển ứng dụng di động (Mobile App) quét mã QR Code nhận diện vị trí kệ hàng tức thời dành riêng cho nhân viên kho.")
    add_bullet("• ", "Mở rộng hệ thống hỗ trợ quản lý chuỗi kho đa chi nhánh (Multi-warehouse) và tự động gợi ý điều chuyển hàng hóa nội bộ.")

    # =========================================================================
    # TÀI LIỆU THAM KHẢO
    # =========================================================================
    add_h1("TÀI LIỆU THAM KHẢO")
    refs = [
        "[1] Nguyễn Tuấn Anh (2025), Giáo trình và bài giảng học phần Ứng dụng Trí tuệ Nhân tạo (AIA331), Trường ĐH Công nghệ Thông tin & Truyền thông - ĐH Thái Nguyên.",
        "[2] Tiêu Thị Hoa (2024), Bài giảng Phân tích và Thiết kế Hệ thống Thông tin, Nhà xuất bản Đại học Thái Nguyên.",
        "[3] FastAPI Framework Documentation (2026), 'Modern, fast (high-performance), web framework for building APIs with Python', https://fastapi.tiangolo.com/.",
        "[4] Google DeepMind (2025), 'Gemini API Developer Documentation: Structured Outputs and Grounding', https://ai.google.dev/docs.",
        "[5] SQLAlchemy Authors (2025), 'SQLAlchemy 2.0 Unified Documentation and ORM Best Practices', https://docs.sqlalchemy.org/.",
        "[6] React Team (2025), 'React 18 Architecture and State Management Patterns', https://react.dev/.",
        "[7] OWASP Foundation (2024), 'OWASP Top 10 Web Application Security Risks', https://owasp.org/www-project-top-ten/.",
    ]
    for ref in refs:
        add_p(ref, pt_size=11, space_after=4)

    # =========================================================================
    # PHỤ LỤC CÁC BẢNG VÀ MÃ NGUỒN
    # =========================================================================
    doc.add_page_break()
    add_h1("PHỤ LỤC CÁC BẢNG VÀ MÃ NGUỒN")
    add_p("Phụ lục này cung cấp toàn bộ các bảng đặc tả kỹ thuật chi tiết của hệ thống nhằm phục vụ công tác rà soát mã nguồn, kiểm chứng cơ sở dữ liệu và đánh giá đồ án.")

    # BẢNG PL.1: ĐẶC TẢ CHI TIẾT 11 BẢNG CSDL
    add_h2("Phụ lục Bảng PL.1: Đặc tả cấu trúc chi tiết 11 bảng cơ sở dữ liệu quan hệ chuẩn 3NF")
    db_schema_rows = [
        ("1", "roles", "id", "INTEGER", "PK, AUTO", "Khóa chính định danh vai trò người dùng"),
        ("2", "roles", "role_name", "VARCHAR(30)", "UNIQUE, NOT NULL", "Tên vai trò: ADMIN, WAREHOUSE, ACCOUNTANT"),
        ("3", "roles", "description", "VARCHAR(255)", "NULL", "Mô tả phạm vi quyền hạn của vai trò"),
        ("4", "roles", "created_at", "DATETIME", "DEFAULT NOW", "Thời điểm khởi tạo bản ghi vai trò"),

        ("5", "users", "id", "INTEGER", "PK, AUTO", "Khóa chính định danh tài khoản người dùng"),
        ("6", "users", "username", "VARCHAR(50)", "UNIQUE, NOT NULL", "Tên tài khoản đăng nhập vào hệ thống"),
        ("7", "users", "password_hash", "VARCHAR(255)", "NOT NULL", "Mật khẩu băm an toàn theo thuật toán Argon2/Bcrypt"),
        ("8", "users", "full_name", "VARCHAR(100)", "NOT NULL", "Họ và tên đầy đủ của cán bộ nhân viên"),
        ("9", "users", "email", "VARCHAR(100)", "NULL", "Địa chỉ email liên hệ nhận thông báo"),
        ("10", "users", "role_id", "INTEGER", "FK -> roles.id", "Khóa ngoại liên kết vai trò phân quyền"),
        ("11", "users", "is_active", "BOOLEAN", "DEFAULT TRUE", "Trạng thái hoạt động của tài khoản"),
        ("12", "users", "created_at", "DATETIME", "DEFAULT NOW", "Thời điểm tạo tài khoản người dùng"),

        ("13", "categories", "id", "INTEGER", "PK, AUTO", "Khóa chính danh mục sản phẩm"),
        ("14", "categories", "category_code", "VARCHAR(30)", "UNIQUE, NOT NULL", "Mã danh mục hàng hóa (CAT-KB, CAT-NET...)"),
        ("15", "categories", "category_name", "VARCHAR(100)", "NOT NULL", "Tên phân loại (Bàn phím, Màn hình, Thiết bị mạng)"),
        ("16", "categories", "description", "TEXT", "NULL", "Mô tả chi tiết nhóm ngành hàng"),

        ("17", "suppliers", "id", "INTEGER", "PK, AUTO", "Khóa chính đối tác nhà cung cấp"),
        ("18", "suppliers", "supplier_name", "VARCHAR(150)", "NOT NULL", "Tên pháp nhân công ty cung ứng hàng"),
        ("19", "suppliers", "contact_person", "VARCHAR(100)", "NULL", "Người đại diện phụ trách giao dịch"),
        ("20", "suppliers", "phone", "VARCHAR(20)", "NULL", "Số điện thoại liên hệ đặt hàng"),
        ("21", "suppliers", "email", "VARCHAR(100)", "NULL", "Hòm thư điện tử tiếp nhận đơn PO"),
        ("22", "suppliers", "address", "VARCHAR(255)", "NULL", "Địa chỉ trụ sở kho nhà cung cấp"),

        ("23", "locations", "id", "INTEGER", "PK, AUTO", "Khóa chính vị trí kệ lưu kho vật lý"),
        ("24", "locations", "location_code", "VARCHAR(30)", "UNIQUE, NOT NULL", "Mã định danh ô kệ (A1-01, B2-03)"),
        ("25", "locations", "zone_name", "VARCHAR(50)", "NOT NULL", "Khu vực kho (Zone A: Điện tử, Zone B: Phụ kiện)"),
        ("26", "locations", "shelf_number", "VARCHAR(30)", "NOT NULL", "Số hiệu tầng kệ lưu trữ"),
        ("27", "locations", "max_capacity", "INTEGER", "DEFAULT 500", "Sức chứa tối đa (đơn vị sản phẩm)"),
        ("28", "locations", "is_active", "BOOLEAN", "DEFAULT TRUE", "Trạng thái khả dụng tiếp nhận hàng"),

        ("29", "products", "id", "INTEGER", "PK, AUTO", "Khóa chính danh mục sản phẩm kho"),
        ("30", "products", "category_id", "INTEGER", "FK -> categories.id", "Khóa ngoại nhóm phân loại sản phẩm"),
        ("31", "products", "sku", "VARCHAR(50)", "UNIQUE, NOT NULL", "Mã SKU quản lý kho duy nhất (VD: AKKO-3087)"),
        ("32", "products", "name", "VARCHAR(150)", "NOT NULL", "Tên thương mại chi tiết của sản phẩm"),
        ("33", "products", "unit", "VARCHAR(20)", "DEFAULT 'Cái'", "Đơn vị tính quy chuẩn (Cái, Chiếc, Bộ, Thùng)"),
        ("34", "products", "cost_price", "DECIMAL(12,2)", "DEFAULT 0", "Giá vốn bình quân nhập kho (VNĐ)"),
        ("35", "products", "selling_price", "DECIMAL(12,2)", "DEFAULT 0", "Giá niêm yết bán lẻ / phân phối (VNĐ)"),
        ("36", "products", "min_threshold", "INTEGER", "DEFAULT 10", "Định mức tồn tối thiểu an toàn (Safety Stock)"),
        ("37", "products", "max_threshold", "INTEGER", "DEFAULT 100", "Định mức tồn tối đa ngăn ứ đọng vốn"),
        ("38", "products", "is_active", "BOOLEAN", "DEFAULT TRUE", "Trạng thái kinh doanh của mặt hàng"),

        ("39", "inventory_items", "id", "INTEGER", "PK, AUTO", "Khóa chính lô hàng tồn kho vật lý"),
        ("40", "inventory_items", "product_id", "INTEGER", "FK -> products.id", "Khóa ngoại liên kết sản phẩm"),
        ("41", "inventory_items", "location_id", "INTEGER", "FK -> locations.id", "Khóa ngoại vị trí ô kệ lưu trữ thực tế"),
        ("42", "inventory_items", "current_stock", "INTEGER", "NOT NULL, >= 0", "Số lượng tồn kho thực tế khả dụng"),
        ("43", "inventory_items", "batch_number", "VARCHAR(50)", "NULL", "Mã số lô sản xuất (Batch/Lot number)"),
        ("44", "inventory_items", "expiry_date", "DATE", "NULL", "Hạn sử dụng khuyến cáo của lô hàng"),
        ("45", "inventory_items", "last_audited_at", "DATETIME", "NULL", "Thời điểm kiểm đếm vật lý gần nhất"),

        ("46", "inventory_transactions", "id", "INTEGER", "PK, AUTO", "Khóa chính phiếu giao dịch kho"),
        ("47", "inventory_transactions", "transaction_code", "VARCHAR(50)", "UNIQUE, NOT NULL", "Mã chứng từ kế toán kho (IMP-20260901-01)"),
        ("48", "inventory_transactions", "transaction_type", "VARCHAR(20)", "NOT NULL", "Loại giao dịch: IMPORT (Nhập), EXPORT (Xuất)"),
        ("49", "inventory_transactions", "supplier_id", "INTEGER", "FK -> suppliers.id", "Khóa ngoại nhà cung cấp (nếu nhập kho)"),
        ("50", "inventory_transactions", "created_by", "INTEGER", "FK -> users.id", "Khóa ngoại người lập phiếu giao dịch"),
        ("51", "inventory_transactions", "total_amount", "DECIMAL(15,2)", "DEFAULT 0", "Tổng giá trị tài chính của phiếu (VNĐ)"),
        ("52", "inventory_transactions", "note", "TEXT", "NULL", "Ghi chú lý do xuất nhập hoặc số hợp đồng"),
        ("53", "inventory_transactions", "created_at", "DATETIME", "DEFAULT NOW", "Thời điểm giao dịch được xác nhận"),

        ("54", "inventory_transaction_items", "id", "INTEGER", "PK, AUTO", "Khóa chính dòng chi tiết mặt hàng trong phiếu"),
        ("55", "inventory_transaction_items", "transaction_id", "INTEGER", "FK -> trans.id", "Khóa ngoại liên kết phiếu giao dịch mẹ"),
        ("56", "inventory_transaction_items", "product_id", "INTEGER", "FK -> products.id", "Khóa ngoại sản phẩm được xuất hoặc nhập"),
        ("57", "inventory_transaction_items", "location_id", "INTEGER", "FK -> locations.id", "Khóa ngoại vị trí kệ kho thực hiện bốc dỡ"),
        ("58", "inventory_transaction_items", "quantity", "INTEGER", "NOT NULL, > 0", "Số lượng hàng hóa giao dịch"),
        ("59", "inventory_transaction_items", "unit_price", "DECIMAL(12,2)", "NOT NULL", "Đơn giá giao dịch tại thời điểm tạo phiếu"),
        ("60", "inventory_transaction_items", "subtotal", "DECIMAL(15,2)", "NOT NULL", "Thành tiền của dòng mặt hàng (qty * price)"),

        ("61", "audit_logs", "id", "INTEGER", "PK, AUTO", "Khóa chính bản ghi vết kiểm toán bất biến"),
        ("62", "audit_logs", "user_id", "INTEGER", "FK -> users.id", "Khóa ngoại người dùng thực hiện thao tác"),
        ("63", "audit_logs", "action_type", "VARCHAR(30)", "NOT NULL", "Thao tác: CREATE, UPDATE, DELETE, EXPORT"),
        ("64", "audit_logs", "entity_name", "VARCHAR(50)", "NOT NULL", "Bảng dữ liệu bị tác động (products, items...)"),
        ("65", "audit_logs", "entity_id", "INTEGER", "NULL", "ID của bản ghi bị tác động"),
        ("66", "audit_logs", "old_value", "TEXT (JSON)", "NULL", "Trạng thái dữ liệu trước khi thay đổi"),
        ("67", "audit_logs", "new_value", "TEXT (JSON)", "NULL", "Trạng thái dữ liệu sau khi hoàn tất thay đổi"),
        ("68", "audit_logs", "ip_address", "VARCHAR(45)", "NULL", "Địa chỉ IPv4/IPv6 gửi yêu cầu API"),
        ("69", "audit_logs", "created_at", "DATETIME", "DEFAULT NOW", "Thời điểm ghi nhận hành động kiểm toán"),

        ("70", "ai_query_logs", "id", "INTEGER", "PK, AUTO", "Khóa chính nhật ký phân tích Trí tuệ Nhân tạo"),
        ("71", "ai_query_logs", "user_id", "INTEGER", "FK -> users.id", "Khóa ngoại người gửi yêu cầu phân tích"),
        ("72", "ai_query_logs", "query_type", "VARCHAR(30)", "NOT NULL", "Phân loại: ASK_NLP, ANOMALY, RESTOCK_FORECAST"),
        ("73", "ai_query_logs", "prompt_text", "TEXT", "NOT NULL", "Nội dung câu hỏi hoặc Prompt gửi cho AI"),
        ("74", "ai_query_logs", "context_snapshot", "TEXT (JSON)", "NOT NULL", "Ảnh chụp Ground-Truth DB cung cấp cho AI"),
        ("75", "ai_query_logs", "response_text", "TEXT", "NOT NULL", "Kết quả phân tích trả về từ LLM hoặc Rule Engine"),
        ("76", "ai_query_logs", "execution_time_ms", "INTEGER", "DEFAULT 0", "Thời gian xử lý của bộ máy AI (mili-giây)"),
        ("77", "ai_query_logs", "created_at", "DATETIME", "DEFAULT NOW", "Thời điểm sinh nhật ký phân tích AI"),
    ]

    tbl_db = doc.add_table(rows=len(db_schema_rows) + 1, cols=6)
    tbl_db.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_db.autofit = False
    set_table_borders(tbl_db, color="000000", sz="10")
    db_widths = [Inches(0.45), Inches(1.15), Inches(1.3), Inches(0.95), Inches(1.05), Inches(1.5)]
    db_hdrs = ["STT", "Tên bảng", "Tên trường", "Kiểu DL", "Ràng buộc", "Diễn giải nghiệp vụ"]
    trPr_db0 = tbl_db.rows[0]._tr.get_or_add_trPr()
    trPr_db0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    for i, h in enumerate(db_hdrs):
        c = tbl_db.rows[0].cells[i]
        c.width = db_widths[i]
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=35, bottom=35, left=45, right=45)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(13.5), True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_vals in enumerate(db_schema_rows):
        row = tbl_db.rows[r_idx + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        bg_color = "f8fafc" if r_idx % 2 == 1 else "ffffff"
        for c_idx, val in enumerate(row_vals):
            c = row.cells[c_idx]
            c.width = db_widths[c_idx]
            set_cell_background(c, bg_color)
            set_cell_margins(c, top=30, bottom=30, left=40, right=40)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name, r.font.size = "Times New Roman", Pt(12.5)
            if c_idx in [1, 2]:
                r.font.bold = True

    # BẢNG PL.2: KỊCH BẢN CHI TIẾT 12 CA KIỂM THỬ PYTEST
    p_sp_pl2 = doc.add_paragraph()
    p_sp_pl2.paragraph_format.space_after = Pt(12)
    add_h2("Phụ lục Bảng PL.2: Kịch bản chi tiết 12 ca kiểm thử Pytest tự động và kết quả kỳ vọng")
    pl2_data = [
        ("TC01", "test_health_check", "GET /api/health", "Gửi request kiểm tra trạng thái máy chủ", "HTTP 200 OK, {'status': 'healthy'}", "100% PASSED"),
        ("TC02", "test_login_success", "POST /api/auth/login", "Đăng nhập với username=admin, password đúng", "HTTP 200 OK, trả về access_token JWT hợp lệ", "100% PASSED"),
        ("TC03", "test_login_invalid_password", "POST /api/auth/login", "Đăng nhập với mật khẩu sai 'WrongPass'", "HTTP 401 Unauthorized, thông báo lỗi xác thực", "100% PASSED"),
        ("TC04", "test_get_products_list", "GET /api/products", "Lấy danh sách sản phẩm kèm Header Bearer Token", "HTTP 200 OK, danh sách mảng JSON > 0 phần tử", "100% PASSED"),
        ("TC05", "test_create_product_admin", "POST /api/products", "Admin tạo mới SKU 'TEST-SKU-01', min=5, max=50", "HTTP 201 Created, bản ghi được ghi vào DB", "100% PASSED"),
        ("TC06", "test_create_product_forbidden", "POST /api/products", "Tài khoản Warehouse gửi yêu cầu tạo SKU mới", "HTTP 403 Forbidden, chặn quyền truy cập trái phép", "100% PASSED"),
        ("TC07", "test_inventory_import_flow", "POST /api/inventory/trans", "Tạo phiếu nhập IMP 50 cái SKU vào vị trí A1-01", "HTTP 200 OK, tồn kho tăng chính xác +50 cái", "100% PASSED"),
        ("TC08", "test_inventory_export_insufficient", "POST /api/inventory/trans", "Xuất hàng 999 cái (vượt quá tồn thực tế 50)", "HTTP 400 Bad Request, Rollback giao dịch an toàn", "100% PASSED"),
        ("TC09", "test_dashboard_kpis", "GET /api/dashboard/kpi", "Truy vấn 6 thẻ chỉ số KPI và định giá tổng tài sản", "HTTP 200 OK, số liệu khớp chính xác dữ liệu kho", "100% PASSED"),
        ("TC10", "test_ai_restock_forecast", "GET /api/ai/forecast", "Chạy mô hình dự báo cạn tồn Depletion Days", "HTTP 200 OK, trả về mảng phân tích burn-rate", "100% PASSED"),
        ("TC11", "test_ai_anomaly_detection", "GET /api/ai/anomalies", "Kiểm định Z-score phát hiện biến động xuất đột biến", "HTTP 200 OK, gắn cờ đúng giao dịch ngoại lai", "100% PASSED"),
        ("TC12", "test_ai_assistant_ask", "POST /api/ai/ask", "Hỏi đáp tự nhiên: 'Sản phẩm nào sắp hết hàng?'", "HTTP 200 OK, câu trả lời Markdown + Snapshot JSON", "100% PASSED"),
    ]
    tbl_pl2 = doc.add_table(rows=len(pl2_data) + 1, cols=6)
    tbl_pl2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_pl2.autofit = False
    set_table_borders(tbl_pl2, color="000000", sz="10")
    pl2_widths = [Inches(0.55), Inches(1.3), Inches(1.1), Inches(1.4), Inches(1.3), Inches(0.75)]
    pl2_hdrs = ["Mã", "Tên hàm test", "Endpoint API", "Kịch bản thực thi", "Kết quả mong đợi", "Trạng thái"]
    trPr_pl2_0 = tbl_pl2.rows[0]._tr.get_or_add_trPr()
    trPr_pl2_0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    for i, h in enumerate(pl2_hdrs):
        c = tbl_pl2.rows[0].cells[i]
        c.width = pl2_widths[i]
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=35, bottom=35, left=45, right=45)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name, r.font.size, r.font.bold = "Times New Roman", Pt(13.5), True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_vals in enumerate(pl2_data):
        row = tbl_pl2.rows[r_idx + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        bg_c = "f8fafc" if r_idx % 2 == 1 else "ffffff"
        for c_idx, val in enumerate(row_vals):
            c = row.cells[c_idx]
            c.width = pl2_widths[c_idx]
            set_cell_background(c, bg_c)
            set_cell_margins(c, top=30, bottom=30, left=40, right=40)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 5] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name, r.font.size = "Times New Roman", Pt(12.5)
            if c_idx == 0:
                r.font.bold = True
            elif c_idx == 5:
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129)

    # Save documents
    doc.save(DOCX_OUTPUT_PATH)
    doc.save(DOCX_COPY_PATH)
    print(f"Report DOCX successfully created at: {DOCX_OUTPUT_PATH}")
    print(f"Report DOCX copy successfully created at: {DOCX_COPY_PATH}")

if __name__ == "__main__":
    build_report()
