# -*- coding: utf-8 -*-
"""
Script khởi tạo toàn bộ 11 sơ đồ kỹ thuật (Draw.io XML + PNG độ nét cao)
Hệ thống Quản lý Kho có Tích hợp AI - Học phần AIA331 (Mã số 80273)
"""
import os
import shutil
import math
from PIL import Image, ImageDraw, ImageFont

REPORT_ROOT = r"D:\it-thesis-research-documentation-engineer-v3.0\report"
DRAWIO_DIR = os.path.join(REPORT_ROOT, "DrawIO")
IMAGES_DIR = os.path.join(REPORT_ROOT, "Images")
LATEX_FIGS = os.path.join(REPORT_ROOT, "LaTeX", "figures")
os.makedirs(DRAWIO_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(LATEX_FIGS, exist_ok=True)

# Helper for Draw.io XML
def write_drawio(filename, diag_id, diag_name, cells_xml):
    content = f"""<mxfile host="app.diagrams.net" modified="2026-09-19T09:00:00.000Z" agent="Antigravity" version="21.0.0" type="device">
  <diagram id="{diag_id}" name="{diag_name}">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{cells_xml}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    filepath = os.path.join(DRAWIO_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())

# Fonts
FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 26)
FONT_SUBTITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 16)
FONT_BOX_HEADER = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 18)
FONT_TEXT = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14)
FONT_TEXT_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 14)
FONT_SMALL = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 12)
FONT_CODE = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 13)

# Palette
BG_COLOR = (248, 250, 252)
TEXT_MAIN = (15, 23, 42)
TEXT_MUTED = (100, 116, 139)
NAVY_HEADER = (0, 43, 102)     # ICTU Navy

BLUE_BG = (239, 246, 255)
BLUE_BORDER = (59, 130, 246)
BLUE_TEXT = (29, 78, 216)

EMERALD_BG = (236, 253, 245)
EMERALD_BORDER = (16, 185, 129)
EMERALD_TEXT = (4, 120, 87)

PURPLE_BG = (250, 245, 255)
PURPLE_BORDER = (168, 85, 247)
PURPLE_TEXT = (107, 33, 168)

AMBER_BG = (254, 243, 199)
AMBER_BORDER = (245, 158, 11)
AMBER_TEXT = (180, 83, 9)

ROSE_BG = (255, 241, 242)
ROSE_BORDER = (244, 63, 94)
ROSE_TEXT = (190, 18, 60)

CYAN_BG = (236, 254, 255)
CYAN_BORDER = (6, 182, 212)
CYAN_TEXT = (14, 116, 144)

def draw_header(draw, width, title, subtitle):
    draw.rectangle([0, 0, width, 85], fill=NAVY_HEADER)
    draw.text((30, 18), title, fill=(255, 255, 255), font=FONT_TITLE)
    draw.text((30, 52), subtitle, fill=(203, 213, 225), font=FONT_SUBTITLE)
    draw.line([(0, 85), (width, 85)], fill=(30, 58, 138), width=2)

def draw_footer(draw, width, height, note="Đề tài: Hệ thống Quản lý Kho có Tích hợp AI - AIA331 | Nhóm 11 - ICTU 2026"):
    draw.line([(0, height - 35), (width, height - 35)], fill=(226, 232, 240), width=1)
    draw.text((30, height - 25), note, fill=TEXT_MUTED, font=FONT_SMALL)

def draw_rounded_box(draw, bbox, fill, outline, width=2, radius=8):
    x1, y1, x2, y2 = bbox
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, start, end, color=(71, 85, 105), width=2, label=""):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 10
    arrow_angle = 0.5
    px1 = x2 - arrow_len * math.cos(angle - arrow_angle)
    py1 = y2 - arrow_len * math.sin(angle - arrow_angle)
    px2 = x2 - arrow_len * math.cos(angle + arrow_angle)
    py2 = y2 - arrow_len * math.sin(angle + arrow_angle)
    draw.polygon([(x2, y2), (px1, py1), (px2, py2)], fill=color)
    if label:
        mx = (x1 + x2) / 2 + 6
        my = (y1 + y2) / 2 - 10
        draw.text((mx, my), label, fill=TEXT_MUTED, font=FONT_SMALL)

def save_image_both(im, filename):
    p1 = os.path.join(IMAGES_DIR, filename)
    p2 = os.path.join(LATEX_FIGS, filename)
    im.save(p1)
    im.save(p2)

# =========================================================================
# 1. USE CASE DIAGRAM (usecase.drawio & usecase.png)
# =========================================================================
def gen_usecase():
    W, H = 1400, 920
    im = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "HÌNH 3.1. BIỂU ĐỒ USE CASE TỔNG QUÁT CỦA HỆ THỐNG",
                "Phân quyền 4 tác nhân: Quản trị viên (Admin), Thủ kho, Kế toán và Dịch vụ AI (AI Service)")

    draw_rounded_box(draw, (320, 110, 1080, 860), (255, 255, 255), (71, 85, 105), 2)
    draw.text((340, 125), "Hệ Thống Quản Lý Kho Tích Hợp AI", fill=(71, 85, 105), font=FONT_BOX_HEADER)

    # Actors
    # Admin
    draw_rounded_box(draw, (50, 160, 250, 310), BLUE_BG, BLUE_BORDER, 2)
    draw.ellipse([130, 180, 170, 220], outline=BLUE_BORDER, width=2)
    draw.line([(150, 220), (150, 260)], fill=BLUE_BORDER, width=2)
    draw.line([(120, 235), (180, 235)], fill=BLUE_BORDER, width=2)
    draw.line([(150, 260), (130, 290)], fill=BLUE_BORDER, width=2)
    draw.line([(150, 260), (170, 290)], fill=BLUE_BORDER, width=2)
    draw.text((85, 295), "QUẢN TRỊ VIÊN (ADMIN)", fill=BLUE_TEXT, font=FONT_TEXT_BOLD)

    # Warehouse Staff
    draw_rounded_box(draw, (50, 420, 250, 570), EMERALD_BG, EMERALD_BORDER, 2)
    draw.ellipse([130, 440, 170, 480], outline=EMERALD_BORDER, width=2)
    draw.line([(150, 480), (150, 520)], fill=EMERALD_BORDER, width=2)
    draw.line([(120, 495), (180, 495)], fill=EMERALD_BORDER, width=2)
    draw.line([(150, 520), (130, 550)], fill=EMERALD_BORDER, width=2)
    draw.line([(150, 520), (170, 550)], fill=EMERALD_BORDER, width=2)
    draw.text((95, 555), "THỦ KHO (WAREHOUSE)", fill=EMERALD_TEXT, font=FONT_TEXT_BOLD)

    # Accountant
    draw_rounded_box(draw, (1150, 220, 1350, 370), AMBER_BG, AMBER_BORDER, 2)
    draw.ellipse([1230, 240, 1270, 280], outline=AMBER_BORDER, width=2)
    draw.line([(1250, 280), (1250, 320)], fill=AMBER_BORDER, width=2)
    draw.line([(1220, 295), (1280, 295)], fill=AMBER_BORDER, width=2)
    draw.line([(1250, 320), (1230, 350)], fill=AMBER_BORDER, width=2)
    draw.line([(1250, 320), (1270, 350)], fill=AMBER_BORDER, width=2)
    draw.text((1180, 355), "KẾ TOÁN (ACCOUNTANT)", fill=AMBER_TEXT, font=FONT_TEXT_BOLD)

    # AI Service
    draw_rounded_box(draw, (1150, 560, 1350, 710), PURPLE_BG, PURPLE_BORDER, 2)
    draw.ellipse([1230, 580, 1270, 620], outline=PURPLE_BORDER, width=2)
    draw.line([(1250, 620), (1250, 660)], fill=PURPLE_BORDER, width=2)
    draw.line([(1220, 635), (1280, 635)], fill=PURPLE_BORDER, width=2)
    draw.line([(1250, 660), (1230, 690)], fill=PURPLE_BORDER, width=2)
    draw.line([(1250, 660), (1270, 690)], fill=PURPLE_BORDER, width=2)
    draw.text((1190, 695), "AI SERVICE (AGENT)", fill=PURPLE_TEXT, font=FONT_TEXT_BOLD)

    usecases = [
        ("UC01: Đăng nhập & Xác thực JWT", (400, 160, 680, 210), BLUE_BG, BLUE_BORDER),
        ("UC02: Quản lý Người dùng & Phân quyền", (400, 230, 720, 280), BLUE_BG, BLUE_BORDER),
        ("UC03: Xem Nhật ký Kiểm toán (Audit Logs)", (400, 300, 720, 350), BLUE_BG, BLUE_BORDER),
        ("UC04: Quản lý Danh mục, NCC, Vị trí kho", (400, 370, 720, 420), EMERALD_BG, EMERALD_BORDER),
        ("UC05: Quản lý Sản phẩm & Định mức tồn", (400, 440, 720, 490), EMERALD_BG, EMERALD_BORDER),
        ("UC06: Tạo Phiếu Nhập kho & Phê duyệt", (400, 510, 720, 560), EMERALD_BG, EMERALD_BORDER),
        ("UC07: Tạo Phiếu Xuất kho & Kiểm tra tồn", (400, 580, 720, 630), EMERALD_BG, EMERALD_BORDER),
        ("UC08: Báo cáo Doanh thu, Chi phí, Định giá", (740, 240, 1050, 290), AMBER_BG, AMBER_BORDER),
        ("UC09: Phân tích Tồn kho & Cảnh báo Thiếu hụt (AI)", (740, 480, 1060, 530), PURPLE_BG, PURPLE_BORDER),
        ("UC10: Trợ lý Hỏi Đáp Kho AI Thông Minh (NLP)", (740, 560, 1060, 610), PURPLE_BG, PURPLE_BORDER),
        ("UC11: Phát hiện Bất thường Biến động Kho (AI)", (740, 640, 1060, 690), PURPLE_BG, PURPLE_BORDER),
        ("UC12: Xem Dashboard KPI Kho Real-time", (550, 730, 900, 780), CYAN_BG, CYAN_BORDER),
    ]

    for name, bbox, bg, bd in usecases:
        draw_rounded_box(draw, bbox, bg, bd, 2, radius=25)
        draw.text((bbox[0] + 20, bbox[1] + 15), name, fill=TEXT_MAIN, font=FONT_TEXT_BOLD)

    # Connections
    for y in [185, 255, 325, 755]:
        draw.line([(250, 235), (400, y)], fill=BLUE_BORDER, width=1)

    for y in [185, 395, 465, 535, 605, 755]:
        draw.line([(250, 495), (400, y)], fill=EMERALD_BORDER, width=1)
    draw.line([(250, 495), (740, 505)], fill=PURPLE_BORDER, width=1)
    draw.line([(250, 495), (740, 585)], fill=PURPLE_BORDER, width=1)

    for y in [185, 265, 755]:
        draw.line([(1150, 295), (740 if y == 265 else 400, y)], fill=AMBER_BORDER, width=1)
    draw.line([(1150, 295), (1060, 505)], fill=PURPLE_BORDER, width=1)

    # AI Service connects to AI UCs
    for y in [505, 585, 665]:
        draw.line([(1150, 635), (1060, y)], fill=PURPLE_BORDER, width=2)

    draw_footer(draw, W, H)
    save_image_both(im, "usecase.png")

    xml = """
        <mxCell id="boundary" value="&lt;b&gt;Hệ Thống Quản Lý Kho Tích Hợp AI&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#475569;strokeWidth=2;align=center;verticalAlign=top;spacingTop=10;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="260" y="90" width="760" height="650" as="geometry" />
        </mxCell>
        <mxCell id="act_admin" value="Quản Trị Viên (Admin)" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;" vertex="1" parent="1">
          <mxGeometry x="80" y="150" width="60" height="120" as="geometry" />
        </mxCell>
        <mxCell id="act_warehouse" value="Thủ Kho (Warehouse)" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fillColor=#ecfdf5;strokeColor=#10b981;" vertex="1" parent="1">
          <mxGeometry x="80" y="380" width="60" height="120" as="geometry" />
        </mxCell>
        <mxCell id="act_accountant" value="Kế Toán (Accountant)" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fillColor=#fef3c7;strokeColor=#f59e0b;" vertex="1" parent="1">
          <mxGeometry x="1100" y="220" width="60" height="120" as="geometry" />
        </mxCell>
        <mxCell id="act_ai" value="Dịch vụ AI (AI Service)" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fillColor=#faf5ff;strokeColor=#a855f7;" vertex="1" parent="1">
          <mxGeometry x="1100" y="500" width="60" height="120" as="geometry" />
        </mxCell>
        <mxCell id="uc1" value="UC01: Đăng nhập &amp;amp; Xác thực JWT" style="ellipse;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="320" y="140" width="220" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc2" value="UC05: Quản lý Sản phẩm &amp;amp; Định mức" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ecfdf5;strokeColor=#10b981;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="320" y="360" width="240" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc3" value="UC06: Tạo Phiếu Nhập &amp;amp; Cập nhật tồn" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ecfdf5;strokeColor=#10b981;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="320" y="430" width="240" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc4" value="UC07: Tạo Phiếu Xuất &amp;amp; Trừ tồn" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ecfdf5;strokeColor=#10b981;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="320" y="500" width="240" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc5" value="UC09: Dự báo Tồn kho AI" style="ellipse;whiteSpace=wrap;html=1;fillColor=#faf5ff;strokeColor=#a855f7;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="680" y="440" width="240" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc6" value="UC10: Trợ lý Hỏi Đáp Kho AI NLP" style="ellipse;whiteSpace=wrap;html=1;fillColor=#faf5ff;strokeColor=#a855f7;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="680" y="520" width="240" height="50" as="geometry" />
        </mxCell>
        <mxCell id="l1" style="endArrow=none;html=1;strokeColor=#3b82f6;" edge="1" parent="1" source="act_admin" target="uc1" />
        <mxCell id="l2" style="endArrow=none;html=1;strokeColor=#10b981;" edge="1" parent="1" source="act_warehouse" target="uc2" />
        <mxCell id="l3" style="endArrow=none;html=1;strokeColor=#10b981;" edge="1" parent="1" source="act_warehouse" target="uc3" />
        <mxCell id="l4" style="endArrow=none;html=1;strokeColor=#10b981;" edge="1" parent="1" source="act_warehouse" target="uc4" />
        <mxCell id="l5" style="endArrow=none;html=1;strokeColor=#a855f7;" edge="1" parent="1" source="act_warehouse" target="uc5" />
        <mxCell id="l6" style="endArrow=none;html=1;strokeColor=#a855f7;" edge="1" parent="1" source="act_ai" target="uc5" />
        <mxCell id="l7" style="endArrow=none;html=1;strokeColor=#a855f7;" edge="1" parent="1" source="act_ai" target="uc6" />
    """
    write_drawio("usecase.drawio", "diag_usecase", "UseCase Diagram", xml)
    print("Generated: usecase.drawio & usecase.png")

# =========================================================================
# 2. ERD (erd.drawio & erd.png)
# =========================================================================
def gen_erd():
    W, H = 1600, 1100
    im = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "HÌNH 5.1. SƠ ĐỒ THỰC THỂ LIÊN KẾT (ERD) TOÀN BỘ HỆ THỐNG",
                "11 Bảng CSDL quan hệ chuẩn 3NF: Người dùng, Sản phẩm, Tồn kho theo vị trí, Giao dịch, Kiểm toán & Nhật ký AI")

    tables = [
        ("roles", (40, 110, 290, 240), [
            (True, False, "id", "INTEGER (PK)"),
            (False, False, "name", "VARCHAR(50) UNIQUE"),
            (False, False, "description", "VARCHAR(255)"),
        ]),
        ("users", (40, 290, 310, 520), [
            (True, False, "id", "INTEGER (PK)"),
            (False, True, "role_id", "INTEGER (FK)"),
            (False, False, "username", "VARCHAR(50) UNIQUE"),
            (False, False, "password_hash", "VARCHAR(255)"),
            (False, False, "full_name", "VARCHAR(100)"),
            (False, False, "is_active", "BOOLEAN"),
            (False, False, "created_at", "DATETIME"),
        ]),
        ("categories", (360, 110, 610, 260), [
            (True, False, "id", "INTEGER (PK)"),
            (False, False, "name", "VARCHAR(100)"),
            (False, False, "code", "VARCHAR(50) UNIQUE"),
            (False, False, "description", "TEXT"),
        ]),
        ("suppliers", (660, 110, 930, 280), [
            (True, False, "id", "INTEGER (PK)"),
            (False, False, "name", "VARCHAR(150)"),
            (False, False, "contact_name", "VARCHAR(100)"),
            (False, False, "phone", "VARCHAR(20)"),
            (False, False, "email", "VARCHAR(100)"),
        ]),
        ("locations", (980, 110, 1260, 280), [
            (True, False, "id", "INTEGER (PK)"),
            (False, False, "code", "VARCHAR(50) UNIQUE"),
            (False, False, "zone", "VARCHAR(20)"),
            (False, False, "shelf", "VARCHAR(20)"),
            (False, False, "capacity", "INTEGER"),
        ]),
        ("products", (360, 330, 670, 660), [
            (True, False, "id", "INTEGER (PK)"),
            (False, True, "category_id", "INTEGER (FK)"),
            (False, True, "supplier_id", "INTEGER (FK)"),
            (False, False, "sku", "VARCHAR(50) UNIQUE"),
            (False, False, "name", "VARCHAR(200)"),
            (False, False, "unit", "VARCHAR(20)"),
            (False, False, "cost_price", "DECIMAL(12,2)"),
            (False, False, "selling_price", "DECIMAL(12,2)"),
            (False, False, "min_threshold", "INTEGER"),
            (False, False, "max_threshold", "INTEGER"),
            (False, False, "status", "VARCHAR(20)"),
        ]),
        ("inventory_items", (730, 340, 1050, 560), [
            (True, False, "id", "INTEGER (PK)"),
            (False, True, "product_id", "INTEGER (FK)"),
            (False, True, "location_id", "INTEGER (FK)"),
            (False, False, "quantity", "INTEGER"),
            (False, False, "batch_number", "VARCHAR(50)"),
            (False, False, "expiry_date", "DATE"),
            (False, False, "updated_at", "DATETIME"),
        ]),
        ("inventory_transactions", (1100, 340, 1550, 620), [
            (True, False, "id", "INTEGER (PK)"),
            (False, False, "code", "VARCHAR(50) UNIQUE"),
            (False, False, "type", "VARCHAR(20) (IMPORT/EXPORT)"),
            (False, True, "created_by", "INTEGER (FK users)"),
            (False, True, "supplier_id", "INTEGER (FK suppliers)"),
            (False, False, "status", "VARCHAR(20) (DRAFT/APPROVED)"),
            (False, False, "total_value", "DECIMAL(14,2)"),
            (False, False, "notes", "TEXT"),
            (False, False, "created_at", "DATETIME"),
        ]),
        ("inventory_transaction_items", (1100, 670, 1550, 930), [
            (True, False, "id", "INTEGER (PK)"),
            (False, True, "transaction_id", "INTEGER (FK)"),
            (False, True, "product_id", "INTEGER (FK)"),
            (False, True, "location_id", "INTEGER (FK)"),
            (False, False, "quantity", "INTEGER"),
            (False, False, "unit_price", "DECIMAL(12,2)"),
            (False, False, "subtotal", "DECIMAL(14,2)"),
            (False, False, "batch_number", "VARCHAR(50)"),
        ]),
        ("audit_logs", (40, 600, 330, 830), [
            (True, False, "id", "INTEGER (PK)"),
            (False, True, "user_id", "INTEGER (FK users)"),
            (False, False, "action", "VARCHAR(50)"),
            (False, False, "entity_name", "VARCHAR(50)"),
            (False, False, "entity_id", "INTEGER"),
            (False, False, "old_values", "JSON"),
            (False, False, "new_values", "JSON"),
            (False, False, "created_at", "DATETIME"),
        ]),
        ("ai_query_logs", (400, 730, 720, 950), [
            (True, False, "id", "INTEGER (PK)"),
            (False, True, "user_id", "INTEGER (FK users)"),
            (False, False, "query_type", "VARCHAR(50) (ASK/ANOMALY/RESTOCK)"),
            (False, False, "prompt", "TEXT"),
            (False, False, "response_summary", "TEXT"),
            (False, False, "execution_time_ms", "INTEGER"),
            (False, False, "created_at", "DATETIME"),
        ]),
    ]

    for name, bbox, fields in tables:
        x1, y1, x2, y2 = bbox
        draw_rounded_box(draw, bbox, (255, 255, 255), (71, 85, 105), 2)
        draw.rectangle([x1, y1, x2, y1 + 32], fill=(0, 43, 102))
        draw.text((x1 + 12, y1 + 6), f"TABLE: {name.upper()}", fill=(255, 255, 255), font=FONT_TEXT_BOLD)
        curr_y = y1 + 40
        for is_pk, is_fk, fname, ftype in fields:
            prefix = "PK " if is_pk else ("FK " if is_fk else "   ")
            color = (185, 28, 28) if is_pk else ((29, 78, 216) if is_fk else TEXT_MAIN)
            draw.text((x1 + 10, curr_y), prefix, fill=color, font=FONT_CODE)
            draw.text((x1 + 40, curr_y), fname, fill=TEXT_MAIN, font=FONT_CODE)
            draw.text((x2 - 170, curr_y), ftype, fill=TEXT_MUTED, font=FONT_SMALL)
            curr_y += 24

    draw_arrow(draw, (175, 240), (175, 290), BLUE_BORDER, 2, "1 : N")
    draw_arrow(draw, (485, 260), (485, 330), BLUE_BORDER, 2, "1 : N")
    draw_arrow(draw, (660, 200), (600, 330), BLUE_BORDER, 2, "1 : N")
    draw_arrow(draw, (670, 440), (730, 440), EMERALD_BORDER, 2, "1 : N")
    draw_arrow(draw, (1080, 280), (950, 340), EMERALD_BORDER, 2, "1 : N")
    draw_arrow(draw, (1325, 620), (1325, 670), AMBER_BORDER, 2, "1 : N")
    draw_arrow(draw, (175, 520), (175, 600), ROSE_BORDER, 2, "1 : N")
    draw_arrow(draw, (310, 480), (400, 750), PURPLE_BORDER, 2, "1 : N")

    draw_footer(draw, W, H)
    save_image_both(im, "erd.png")

    xml = """
        <mxCell id="tbl_users" value="&lt;b&gt;users&lt;/b&gt;&lt;hr&gt;+ id (PK)&lt;br&gt;+ role_id (FK)&lt;br&gt;+ username&lt;br&gt;+ password_hash" style="swimlane;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;" vertex="1" parent="1">
          <mxGeometry x="60" y="80" width="180" height="130" as="geometry" />
        </mxCell>
        <mxCell id="tbl_products" value="&lt;b&gt;products&lt;/b&gt;&lt;hr&gt;+ id (PK)&lt;br&gt;+ sku (UNIQUE)&lt;br&gt;+ name&lt;br&gt;+ category_id (FK)&lt;br&gt;+ min_threshold" style="swimlane;whiteSpace=wrap;html=1;fillColor=#eff6ff;strokeColor=#3b82f6;" vertex="1" parent="1">
          <mxGeometry x="320" y="80" width="180" height="150" as="geometry" />
        </mxCell>
        <mxCell id="tbl_inventory" value="&lt;b&gt;inventory_items&lt;/b&gt;&lt;hr&gt;+ id (PK)&lt;br&gt;+ product_id (FK)&lt;br&gt;+ location_id (FK)&lt;br&gt;+ quantity" style="swimlane;whiteSpace=wrap;html=1;fillColor=#ecfdf5;strokeColor=#10b981;" vertex="1" parent="1">
          <mxGeometry x="580" y="80" width="180" height="130" as="geometry" />
        </mxCell>
        <mxCell id="tbl_trans" value="&lt;b&gt;inventory_transactions&lt;/b&gt;&lt;hr&gt;+ id (PK)&lt;br&gt;+ code (UNIQUE)&lt;br&gt;+ type (IMPORT/EXPORT)&lt;br&gt;+ created_by (FK)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#f59e0b;" vertex="1" parent="1">
          <mxGeometry x="840" y="80" width="200" height="140" as="geometry" />
        </mxCell>
        <mxCell id="rel1" style="edgeStyle=orthogonalEdgeStyle;html=1;strokeColor=#3b82f6;" edge="1" parent="1" source="tbl_products" target="tbl_inventory">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
    """
    write_drawio("erd.drawio", "diag_erd", "ERD", xml)
    print("Generated: erd.drawio & erd.png")

# =========================================================================
# 3. ARCHITECTURE (architecture.drawio & architecture.png)
# =========================================================================
def gen_architecture():
    W, H = 1400, 950
    im = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "HÌNH 6.1. SƠ ĐỒ KIẾN TRÚC TỔNG THỂ HỆ THỐNG 3 TẦNG",
                "Phân tách 3 tầng: Presentation Layer (React Vite) -> Application Logic Layer (FastAPI) -> Data & Cloud AI Layer")

    draw_rounded_box(draw, (50, 110, 1350, 310), (255, 255, 255), (203, 213, 225), 2)
    draw.rectangle([50, 110, 1350, 150], fill=(241, 245, 249))
    draw.text((70, 120), "TẦNG TRÌNH DIỄN (PRESENTATION TIER) - SINGLE PAGE APPLICATION (REACT VITE)", fill=(15, 23, 42), font=FONT_BOX_HEADER)

    t1_boxes = [
        ("Dashboard & KPI Hub", "Tổng quan tồn kho, giá trị tài sản,\ncảnh báo thiếu hụt, biểu đồ nhập/xuất", (70, 170, 350, 290), BLUE_BG, BLUE_BORDER, BLUE_TEXT),
        ("Kho & Nghiệp Vụ", "Quản lý SP, nhập/xuất hàng,\nkiểm soát tồn vị trí kệ, barcode", (370, 170, 650, 290), BLUE_BG, BLUE_BORDER, BLUE_TEXT),
        ("AI Analytics Hub", "Tồn kho thông minh, dự báo thiếu hụt,\nphát hiện bất thường, trợ lý hỏi đáp", (670, 170, 950, 290), PURPLE_BG, PURPLE_BORDER, PURPLE_TEXT),
        ("Bảo Mật & Quản Trị", "Đăng nhập JWT, phân quyền 3 vai trò,\nnhật ký kiểm toán (Audit Logs)", (970, 170, 1330, 290), EMERALD_BG, EMERALD_BORDER, EMERALD_TEXT),
    ]
    for title, desc, bbox, bg, bd, tx in t1_boxes:
        draw_rounded_box(draw, bbox, bg, bd, 2)
        draw.text((bbox[0]+15, bbox[1]+15), title, fill=tx, font=FONT_TEXT_BOLD)
        draw.text((bbox[0]+15, bbox[1]+45), desc, fill=TEXT_MAIN, font=FONT_SMALL)

    for x in [210, 510, 810, 1150]:
        draw_arrow(draw, (x, 310), (x, 380), (100, 116, 139), 2, "REST / JSON API")

    draw_rounded_box(draw, (50, 380, 1350, 640), (255, 255, 255), (203, 213, 225), 2)
    draw.rectangle([50, 380, 1350, 420], fill=(241, 245, 249))
    draw.text((70, 390), "TẦNG NGHIỆP VỤ (APPLICATION & LOGIC TIER) - FASTAPI ASYNC BACKEND (PYTHON)", fill=(15, 23, 42), font=FONT_BOX_HEADER)

    t2_boxes = [
        ("API Gateway / Routers", "FastAPI APIRouter, OAuth2 Bearer,\nCORS Middleware, Rate Limiting", (70, 440, 360, 610), CYAN_BG, CYAN_BORDER, CYAN_TEXT),
        ("Nghiệp Vụ Kho (Services)", "InventoryService, ProductService,\nStock Validation, Audit Logging", (380, 440, 680, 610), CYAN_BG, CYAN_BORDER, CYAN_TEXT),
        ("AI Dual-Layer Engine", "Lớp 1: Google Gemini API (LLM)\nLớp 2: Local Rule-Engine (Fallback)\nTính toán tốc độ tiêu thụ & bất thường", (700, 440, 1020, 610), PURPLE_BG, PURPLE_BORDER, PURPLE_TEXT),
        ("Bảo Mật & Audit Engine", "Argon2/Bcrypt password hash,\nRole-Based Access Control (RBAC),\nBảo vệ SQLi qua SQLAlchemy ORM", (1040, 440, 1330, 610), ROSE_BG, ROSE_BORDER, ROSE_TEXT),
    ]
    for title, desc, bbox, bg, bd, tx in t2_boxes:
        draw_rounded_box(draw, bbox, bg, bd, 2)
        draw.text((bbox[0]+15, bbox[1]+15), title, fill=tx, font=FONT_TEXT_BOLD)
        draw.text((bbox[0]+15, bbox[1]+45), desc, fill=TEXT_MAIN, font=FONT_SMALL)

    for x in [215, 530, 860, 1185]:
        draw_arrow(draw, (x, 640), (x, 700), (100, 116, 139), 2, "SQLAlchemy / ORM")

    draw_rounded_box(draw, (50, 700, 1350, 900), (255, 255, 255), (203, 213, 225), 2)
    draw.rectangle([50, 700, 1350, 740], fill=(241, 245, 249))
    draw.text((70, 710), "TẦNG DỮ LIỆU & DỊCH VỤ THÔNG MINH (DATA PERSISTENCE & EXTERNAL AI LAYER)", fill=(15, 23, 42), font=FONT_BOX_HEADER)

    t3_boxes = [
        ("Cơ sở dữ liệu Quan hệ", "SQLite / PostgreSQL\n11 bảng chuẩn hóa 3NF, Index tối ưu,\nAlembic Database Migrations", (70, 755, 480, 880), AMBER_BG, AMBER_BORDER, AMBER_TEXT),
        ("Snapshot & Audit Logs", "Snapshot dữ liệu kho chuẩn xác,\nAudit Trail bất biến (immutable),\nLịch sử truy vấn AI (ai_query_logs)", (500, 755, 910, 880), AMBER_BG, AMBER_BORDER, AMBER_TEXT),
        ("Google Gemini AI Cloud", "gemini-1.5-flash / gemini-2.0\nZero-shot, Few-shot Prompting,\nGround-Truth Context Injection", (930, 755, 1330, 880), PURPLE_BG, PURPLE_BORDER, PURPLE_TEXT),
    ]
    for title, desc, bbox, bg, bd, tx in t3_boxes:
        draw_rounded_box(draw, bbox, bg, bd, 2)
        draw.text((bbox[0]+15, bbox[1]+15), title, fill=tx, font=FONT_TEXT_BOLD)
        draw.text((bbox[0]+15, bbox[1]+45), desc, fill=TEXT_MAIN, font=FONT_SMALL)

    draw_footer(draw, W, H)
    save_image_both(im, "architecture.png")

    xml = """
        <mxCell id="t1" value="&lt;b&gt;Tầng Trình Diễn (React Vite SPA)&lt;/b&gt;" style="rounded=1;fillColor=#eff6ff;strokeColor=#3b82f6;" vertex="1" parent="1">
          <mxGeometry x="100" y="80" width="600" height="80" as="geometry" />
        </mxCell>
        <mxCell id="t2" value="&lt;b&gt;Tầng Nghiệp Vụ (FastAPI Async Backend)&lt;/b&gt;" style="rounded=1;fillColor=#ecfeff;strokeColor=#06b6d4;" vertex="1" parent="1">
          <mxGeometry x="100" y="240" width="600" height="80" as="geometry" />
        </mxCell>
        <mxCell id="t3" value="&lt;b&gt;Tầng Dữ Liệu &amp;amp; AI (SQLite / Postgres + Gemini Cloud)&lt;/b&gt;" style="rounded=1;fillColor=#fef3c7;strokeColor=#f59e0b;" vertex="1" parent="1">
          <mxGeometry x="100" y="400" width="600" height="80" as="geometry" />
        </mxCell>
        <mxCell id="e1" value="REST JSON API" style="edgeStyle=orthogonalEdgeStyle;strokeColor=#475569;" edge="1" parent="1" source="t1" target="t2" />
        <mxCell id="e2" value="SQLAlchemy ORM &amp;amp; AI Requests" style="edgeStyle=orthogonalEdgeStyle;strokeColor=#475569;" edge="1" parent="1" source="t2" target="t3" />
    """
    write_drawio("architecture.drawio", "diag_arch", "System Architecture", xml)
    print("Generated: architecture.drawio & architecture.png")

# =========================================================================
# 4. ACTIVITY DIAGRAM - LOGIN (activity_login.drawio & activity_login.png)
# =========================================================================
def gen_activity_login():
    W, H = 1000, 800
    im = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "HÌNH 4.1. LƯỢC ĐỒ HOẠT ĐỘNG QUY TRÌNH ĐĂNG NHẬP",
                "Xác thực danh tính người dùng bằng hàm băm mật khẩu Argon2/Bcrypt và cấp phát JWT Bearer Token")

    steps = [
        ("Người dùng nhập username & password", (350, 110, 650, 160), BLUE_BG, BLUE_BORDER),
        ("Gửi POST /api/auth/login", (360, 190, 640, 240), BLUE_BG, BLUE_BORDER),
        ("Tìm kiếm user trong CSDL theo username", (330, 270, 670, 320), CYAN_BG, CYAN_BORDER),
        ("Người dùng tồn tại & verify_password() đúng?", (320, 350, 680, 410), AMBER_BG, AMBER_BORDER),
        ("Tạo access_token (JWT mã hóa vai trò)", (350, 460, 650, 510), EMERALD_BG, EMERALD_BORDER),
        ("Ghi log đăng nhập thành công vào audit_logs", (330, 540, 670, 590), EMERALD_BG, EMERALD_BORDER),
        ("Trả HTTP 200 OK kèm Bearer Token & UserInfo", (320, 620, 680, 670), EMERALD_BG, EMERALD_BORDER),
        ("Chuyển hướng vào Dashboard tương ứng vai trò", (330, 700, 670, 750), BLUE_BG, BLUE_BORDER),
    ]

    for title, bbox, bg, bd in steps:
        draw_rounded_box(draw, bbox, bg, bd, 2, radius=12)
        draw.text((bbox[0] + 16, bbox[1] + 15), title, fill=TEXT_MAIN, font=FONT_TEXT_BOLD)

    # Fail box
    fail_box = ("Trả HTTP 401 Unauthorized (Sai thông tin)", (740, 355, 960, 405))
    draw_rounded_box(draw, fail_box[1], ROSE_BG, ROSE_BORDER, 2, radius=12)
    draw.text((fail_box[1][0]+10, fail_box[1][1]+15), fail_box[0], fill=ROSE_TEXT, font=FONT_SMALL)

    draw_arrow(draw, (500, 160), (500, 190), BLUE_BORDER, 2)
    draw_arrow(draw, (500, 240), (500, 270), BLUE_BORDER, 2)
    draw_arrow(draw, (500, 320), (500, 350), BLUE_BORDER, 2)
    draw_arrow(draw, (500, 410), (500, 460), EMERALD_BORDER, 2, "Hợp lệ [Yes]")
    draw_arrow(draw, (680, 380), (740, 380), ROSE_BORDER, 2, "Sai [No]")
    draw_arrow(draw, (500, 510), (500, 540), EMERALD_BORDER, 2)
    draw_arrow(draw, (500, 590), (500, 620), EMERALD_BORDER, 2)
    draw_arrow(draw, (500, 670), (500, 700), BLUE_BORDER, 2)

    draw_footer(draw, W, H)
    save_image_both(im, "activity_login.png")

    xml = """
        <mxCell id="s1" value="Người dùng nhập thông tin" style="rounded=1;fillColor=#eff6ff;" vertex="1" parent="1"><mxGeometry x="100" y="80" width="200" height="60" as="geometry"/></mxCell>
        <mxCell id="s2" value="Kiểm tra mật khẩu băm" style="rhombus;fillColor=#fef3c7;" vertex="1" parent="1"><mxGeometry x="120" y="180" width="160" height="80" as="geometry"/></mxCell>
        <mxCell id="s3" value="Cấp JWT Bearer Token" style="rounded=1;fillColor=#ecfdf5;" vertex="1" parent="1"><mxGeometry x="100" y="300" width="200" height="60" as="geometry"/></mxCell>
        <mxCell id="s4" value="Báo lỗi 401" style="rounded=1;fillColor=#fff1f2;" vertex="1" parent="1"><mxGeometry x="340" y="190" width="140" height="60" as="geometry"/></mxCell>
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="s1" target="s2"/>
        <mxCell id="e2" value="Đúng" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="s2" target="s3"/>
        <mxCell id="e3" value="Sai" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="s2" target="s4"/>
    """
    write_drawio("activity_login.drawio", "diag_act_login", "Activity Login", xml)
    print("Generated: activity_login.drawio & activity_login.png")

# =========================================================================
# 5. ACTIVITY DIAGRAM - IMPORT (activity_import.drawio & activity_import.png)
# =========================================================================
def gen_activity_import():
    W, H = 1200, 950
    im = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "HÌNH 4.2. LƯỢC ĐỒ HOẠT ĐỘNG QUY TRÌNH NHẬP KHO",
                "Luồng nghiệp vụ từ tạo đơn, kiểm đếm thực tế, chỉ định vị trí kệ kho và cập nhật tồn kho an toàn")

    steps = [
        ("Khởi đầu: Thủ kho lập phiếu nhập hàng", (430, 110, 770, 160), BLUE_BG, BLUE_BORDER),
        ("Chọn Nhà Cung Cấp & Nhập thông tin phiếu", (420, 190, 780, 240), BLUE_BG, BLUE_BORDER),
        ("Thêm danh sách sản phẩm, số lượng, đơn giá", (410, 270, 790, 320), BLUE_BG, BLUE_BORDER),
        ("Kiểm đếm thực tế & quy cách hàng giao nhận", (410, 350, 790, 400), AMBER_BG, AMBER_BORDER),
        ("Hàng hóa đạt tiêu chuẩn và đúng quy cách?", (420, 430, 780, 490), AMBER_BG, AMBER_BORDER),
        ("Chỉ định vị trí kệ kho (Location: Zone/Shelf)", (420, 530, 780, 580), EMERALD_BG, EMERALD_BORDER),
        ("Hệ thống tạo Transaction (Status: APPROVED)", (410, 610, 790, 660), EMERALD_BG, EMERALD_BORDER),
        ("Cộng dồn số lượng vào inventory_items", (420, 690, 780, 740), EMERALD_BG, EMERALD_BORDER),
        ("Ghi nhận Audit Log & Cập nhật Dashboard Realtime", (400, 770, 800, 820), CYAN_BG, CYAN_BORDER),
        ("Kết thúc: Phiếu nhập hoàn tất & in phiếu", (440, 850, 760, 900), BLUE_BG, BLUE_BORDER),
    ]

    for title, bbox, bg, bd in steps:
        draw_rounded_box(draw, bbox, bg, bd, 2, radius=12)
        draw.text((bbox[0] + 18, bbox[1] + 15), title, fill=TEXT_MAIN, font=FONT_TEXT_BOLD)

    reject_box = ("Từ chối nhận hàng, lập biên bản sự cố", (860, 435, 1160, 485))
    draw_rounded_box(draw, reject_box[1], ROSE_BG, ROSE_BORDER, 2, radius=12)
    draw.text((reject_box[1][0]+15, reject_box[1][1]+15), reject_box[0], fill=ROSE_TEXT, font=FONT_TEXT_BOLD)

    draw_arrow(draw, (600, 160), (600, 190), BLUE_BORDER, 2)
    draw_arrow(draw, (600, 240), (600, 270), BLUE_BORDER, 2)
    draw_arrow(draw, (600, 320), (600, 350), BLUE_BORDER, 2)
    draw_arrow(draw, (600, 400), (600, 430), BLUE_BORDER, 2)
    draw_arrow(draw, (600, 490), (600, 530), EMERALD_BORDER, 2, "Hợp lệ [Yes]")
    draw_arrow(draw, (780, 460), (860, 460), ROSE_BORDER, 2, "Lỗi/Hỏng [No]")
    draw_arrow(draw, (1010, 485), (600, 850), ROSE_BORDER, 2, "Đóng giao dịch lỗi")

    draw_arrow(draw, (600, 580), (600, 610), EMERALD_BORDER, 2)
    draw_arrow(draw, (600, 660), (600, 690), EMERALD_BORDER, 2)
    draw_arrow(draw, (600, 740), (600, 770), EMERALD_BORDER, 2)
    draw_arrow(draw, (600, 820), (600, 850), BLUE_BORDER, 2)

    draw_footer(draw, W, H)
    save_image_both(im, "activity_import.png")

    xml = """
        <mxCell id="s1" value="Lập phiếu nhập kho" style="rounded=1;fillColor=#eff6ff;" vertex="1" parent="1"><mxGeometry x="100" y="80" width="200" height="60" as="geometry"/></mxCell>
        <mxCell id="s2" value="Kiểm tra quy cách hàng" style="rhombus;fillColor=#fef3c7;" vertex="1" parent="1"><mxGeometry x="110" y="180" width="180" height="80" as="geometry"/></mxCell>
        <mxCell id="s3" value="Chỉ định vị trí kệ kho" style="rounded=1;fillColor=#ecfdf5;" vertex="1" parent="1"><mxGeometry x="100" y="300" width="200" height="60" as="geometry"/></mxCell>
        <mxCell id="s4" value="Từ chối nhận hàng" style="rounded=1;fillColor=#fff1f2;" vertex="1" parent="1"><mxGeometry x="360" y="190" width="160" height="60" as="geometry"/></mxCell>
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="s1" target="s2"/>
        <mxCell id="e2" value="Đạt" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="s2" target="s3"/>
        <mxCell id="e3" value="Hỏng" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="s2" target="s4"/>
    """
    write_drawio("activity_import.drawio", "diag_act_imp", "Activity Import", xml)
    print("Generated: activity_import.drawio & activity_import.png")

# =========================================================================
# 6. ACTIVITY DIAGRAM - EXPORT (activity_export.drawio & activity_export.png)
# =========================================================================
def gen_activity_export():
    W, H = 1200, 950
    im = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "HÌNH 4.3. LƯỢC ĐỒ HOẠT ĐỘNG QUY TRÌNH XUẤT KHO",
                "Kiểm tra số lượng tồn khả dụng, khóa dòng chống tranh chấp, trừ kho và cảnh báo tồn tối thiểu")

    steps = [
        ("Khởi đầu: Yêu cầu xuất kho đơn hàng", (440, 110, 760, 160), BLUE_BG, BLUE_BORDER),
        ("Chọn khách hàng / lý do xuất & thông tin phiếu", (410, 190, 790, 240), BLUE_BG, BLUE_BORDER),
        ("Thêm danh mục hàng xuất & số lượng cần xuất", (410, 270, 790, 320), BLUE_BG, BLUE_BORDER),
        ("Kiểm tra tồn kho: Số lượng xuất <= Số lượng tồn?", (400, 350, 800, 410), AMBER_BG, AMBER_BORDER),
        ("Khóa tạm thời bản ghi tồn kho (Row Locking)", (410, 460, 790, 510), EMERALD_BG, EMERALD_BORDER),
        ("Trừ số lượng thực tế trong inventory_items", (410, 540, 790, 590), EMERALD_BG, EMERALD_BORDER),
        ("Kiểm tra ngưỡng tối thiểu: Stock < min_threshold?", (400, 620, 800, 680), PURPLE_BG, PURPLE_BORDER),
        ("Kích hoạt AI Alert: Cảnh báo cần tái nhập hàng", (410, 720, 790, 770), ROSE_BG, ROSE_BORDER),
        ("Ghi nhận Audit Log & Kết thúc hoàn tất xuất kho", (410, 820, 790, 870), CYAN_BG, CYAN_BORDER),
    ]

    for title, bbox, bg, bd in steps:
        draw_rounded_box(draw, bbox, bg, bd, 2, radius=12)
        draw.text((bbox[0] + 18, bbox[1] + 15), title, fill=TEXT_MAIN, font=FONT_TEXT_BOLD)

    out_of_stock = ("Báo lỗi: Kho không đủ số lượng tồn", (860, 355, 1160, 405))
    draw_rounded_box(draw, out_of_stock[1], ROSE_BG, ROSE_BORDER, 2, radius=12)
    draw.text((out_of_stock[1][0]+15, out_of_stock[1][1]+15), out_of_stock[0], fill=ROSE_TEXT, font=FONT_TEXT_BOLD)

    draw_arrow(draw, (600, 160), (600, 190), BLUE_BORDER, 2)
    draw_arrow(draw, (600, 240), (600, 270), BLUE_BORDER, 2)
    draw_arrow(draw, (600, 320), (600, 350), BLUE_BORDER, 2)
    draw_arrow(draw, (600, 410), (600, 460), EMERALD_BORDER, 2, "Đủ hàng [Yes]")
    draw_arrow(draw, (800, 380), (860, 380), ROSE_BORDER, 2, "Thiếu [No]")
    draw_arrow(draw, (600, 510), (600, 540), EMERALD_BORDER, 2)
    draw_arrow(draw, (600, 590), (600, 620), EMERALD_BORDER, 2)
    draw_arrow(draw, (600, 680), (600, 720), ROSE_BORDER, 2, "Dưới ngưỡng [Yes]")
    draw_arrow(draw, (600, 770), (600, 820), CYAN_BORDER, 2)

    draw.line([(400, 650), (330, 650)], fill=EMERALD_BORDER, width=2)
    draw.line([(330, 650), (330, 845)], fill=EMERALD_BORDER, width=2)
    draw_arrow(draw, (330, 845), (410, 845), EMERALD_BORDER, 2, "Tồn an toàn")

    draw_footer(draw, W, H)
    save_image_both(im, "activity_export.png")

    xml = """
        <mxCell id="s1" value="Lập phiếu xuất kho" style="rounded=1;fillColor=#eff6ff;" vertex="1" parent="1"><mxGeometry x="100" y="80" width="200" height="60" as="geometry"/></mxCell>
        <mxCell id="s2" value="Kiểm tra tồn kho đủ?" style="rhombus;fillColor=#fef3c7;" vertex="1" parent="1"><mxGeometry x="110" y="180" width="180" height="80" as="geometry"/></mxCell>
        <mxCell id="s3" value="Khóa dòng &amp;amp; Trừ kho" style="rounded=1;fillColor=#ecfdf5;" vertex="1" parent="1"><mxGeometry x="100" y="300" width="200" height="60" as="geometry"/></mxCell>
        <mxCell id="s4" value="Từ chối: Báo lỗi thiếu tồn" style="rounded=1;fillColor=#fff1f2;" vertex="1" parent="1"><mxGeometry x="360" y="190" width="180" height="60" as="geometry"/></mxCell>
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="s1" target="s2"/>
        <mxCell id="e2" value="Đủ" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="s2" target="s3"/>
        <mxCell id="e3" value="Thiếu" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="s2" target="s4"/>
    """
    write_drawio("activity_export.drawio", "diag_act_exp", "Activity Export", xml)
    print("Generated: activity_export.drawio & activity_export.png")

# =========================================================================
# 7. ACTIVITY DIAGRAM - AI ANALYSIS (ai_flow.drawio & ai_flow.png)
# =========================================================================
def gen_activity_ai_flow():
    W, H = 1200, 950
    im = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "HÌNH 4.4. LƯỢC ĐỒ HOẠT ĐỘNG LUỒNG PHÂN TÍCH AI",
                "Quy trình bóc tách dữ liệu kho thật, bơm ngữ cảnh Ground-Truth, gọi mô hình và hiển thị thẻ Smart UI")

    steps = [
        ("Người dùng chọn chức năng AI (Dự báo / Bất thường / NLP)", (380, 110, 820, 160), BLUE_BG, BLUE_BORDER),
        ("FastAPI Backend tiếp nhận Request", (420, 190, 780, 240), BLUE_BG, BLUE_BORDER),
        ("Lấy dữ liệu thực tế từ CSDL: Tồn kho, Vận tốc 30 ngày", (390, 270, 810, 320), CYAN_BG, CYAN_BORDER),
        ("Tổng hợp JSON Snapshot (Ground-Truth Context)", (400, 350, 800, 400), CYAN_BG, CYAN_BORDER),
        ("Dựng Prompt Template & Kiểm tra kết nối AI Cloud", (400, 430, 800, 480), AMBER_BG, AMBER_BORDER),
        ("Gọi Google Gemini API (Hoặc chuyển Fallback Local)", (390, 520, 810, 570), PURPLE_BG, PURPLE_BORDER),
        ("Kiểm tra kết quả: Output schema, bảng Markdown, số liệu", (380, 610, 820, 660), EMERALD_BG, EMERALD_BORDER),
        ("Ghi nhật ký truy vấn vào ai_query_logs", (420, 700, 780, 750), EMERALD_BG, EMERALD_BORDER),
        ("Hiển thị giao diện Smart UI Component (LED, Badges, Nút)", (370, 790, 830, 840), CYAN_BG, CYAN_BORDER),
    ]

    for title, bbox, bg, bd in steps:
        draw_rounded_box(draw, bbox, bg, bd, 2, radius=12)
        draw.text((bbox[0] + 16, bbox[1] + 15), title, fill=TEXT_MAIN, font=FONT_TEXT_BOLD)

    for i in range(len(steps) - 1):
        draw_arrow(draw, (600, steps[i][1][3]), (600, steps[i+1][1][1]), BLUE_BORDER, 2)

    draw_footer(draw, W, H)
    save_image_both(im, "ai_flow.png")

    xml = """
        <mxCell id="s1" value="Người dùng chọn chức năng AI" style="rounded=1;fillColor=#eff6ff;" vertex="1" parent="1"><mxGeometry x="100" y="80" width="220" height="60" as="geometry"/></mxCell>
        <mxCell id="s2" value="Lấy Snapshot dữ liệu CSDL" style="rounded=1;fillColor=#ecfeff;" vertex="1" parent="1"><mxGeometry x="100" y="180" width="220" height="60" as="geometry"/></mxCell>
        <mxCell id="s3" value="Bơm Ground-Truth vào Prompt" style="rounded=1;fillColor=#faf5ff;" vertex="1" parent="1"><mxGeometry x="100" y="280" width="220" height="60" as="geometry"/></mxCell>
        <mxCell id="s4" value="Gọi Gemini / Rule Engine" style="rounded=1;fillColor=#faf5ff;" vertex="1" parent="1"><mxGeometry x="100" y="380" width="220" height="60" as="geometry"/></mxCell>
        <mxCell id="s5" value="Kiểm tra schema &amp;amp; Render Smart UI" style="rounded=1;fillColor=#ecfdf5;" vertex="1" parent="1"><mxGeometry x="100" y="480" width="220" height="60" as="geometry"/></mxCell>
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="s1" target="s2"/>
        <mxCell id="e2" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="s2" target="s3"/>
        <mxCell id="e3" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="s3" target="s4"/>
        <mxCell id="e4" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="s4" target="s5"/>
    """
    write_drawio("ai_flow.drawio", "diag_ai_flow", "AI Flow", xml)
    print("Generated: ai_flow.drawio & ai_flow.png")

# =========================================================================
# 8. SEQUENCE DIAGRAM - IMPORT (sequence_import.drawio & sequence_import.png)
# =========================================================================
def gen_sequence_import():
    W, H = 1400, 920
    im = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "HÌNH 7.1. SƠ ĐỒ TUẦN TỰ QUY TRÌNH NHẬP KHO (IMPORT SEQUENCE)",
                "Tương tác đối tượng: Thủ kho -> Frontend UI -> FastAPI Router -> Inventory Service -> Database -> Audit Log")

    lifelines = [
        ("Thủ kho (User)", 120, BLUE_BG, BLUE_BORDER),
        ("React Frontend", 380, BLUE_BG, BLUE_BORDER),
        ("FastAPI APIRouter", 640, CYAN_BG, CYAN_BORDER),
        ("InventoryService", 890, CYAN_BG, CYAN_BORDER),
        ("SQL Database", 1120, AMBER_BG, AMBER_BORDER),
        ("AuditLog Service", 1310, ROSE_BG, ROSE_BORDER),
    ]

    for title, x, bg, bd in lifelines:
        draw_rounded_box(draw, (x - 70, 110, x + 70, 155), bg, bd, 2)
        draw.text((x - 60, 125), title, fill=TEXT_MAIN, font=FONT_TEXT_BOLD)
        for y in range(160, 860, 15):
            draw.line([(x, y), (x, y + 8)], fill=(148, 163, 184), width=1)

    msgs = [
        (120, 380, 190, "1. Chọn NCC, nhập SP, số lượng & bấm 'Tạo phiếu nhập'"),
        (380, 640, 240, "2. POST /api/transactions/import (Bearer JWT, Payload)"),
        (640, 890, 290, "3. validate_import_payload() & check_permission()"),
        (890, 1120, 350, "4. INSERT INTO inventory_transactions (type=IMPORT)"),
        (1120, 890, 400, "5. Trả về transaction_id mới tạo"),
        (890, 1120, 460, "6. INSERT INTO inventory_transaction_items"),
        (890, 1120, 520, "7. UPDATE inventory_items SET quantity = quantity + N"),
        (890, 1310, 580, "8. log_audit_event('IMPORT_CREATED', details)"),
        (1310, 890, 630, "9. Ghi log kiểm toán thành công"),
        (890, 640, 690, "10. Commit DB Transaction an toàn"),
        (640, 380, 750, "11. HTTP 201 Created (JSON Transaction data)"),
        (380, 120, 810, "12. Hiển thị Toast thông báo thành công & cập nhật KPI"),
    ]

    for x1, x2, y, text in msgs:
        draw_arrow(draw, (x1, y), (x2, y), (30, 41, 59), 2)
        mx = min(x1, x2) + 15
        draw.text((mx, y - 18), text, fill=(30, 41, 59), font=FONT_SMALL)

    draw_footer(draw, W, H)
    save_image_both(im, "sequence_import.png")

    xml = """
        <mxCell id="u" value="Thủ kho" style="shape=umlLifeline;participant=umlActor;" vertex="1" parent="1"><mxGeometry x="80" y="80" width="80" height="400" as="geometry"/></mxCell>
        <mxCell id="f" value="Frontend" style="shape=umlLifeline;" vertex="1" parent="1"><mxGeometry x="240" y="80" width="100" height="400" as="geometry"/></mxCell>
        <mxCell id="b" value="FastAPI" style="shape=umlLifeline;" vertex="1" parent="1"><mxGeometry x="420" y="80" width="100" height="400" as="geometry"/></mxCell>
        <mxCell id="d" value="Database" style="shape=umlLifeline;" vertex="1" parent="1"><mxGeometry x="600" y="80" width="100" height="400" as="geometry"/></mxCell>
        <mxCell id="m1" value="Nhập phiếu" style="html=1;verticalAlign=bottom;endArrow=block;" edge="1" parent="1" source="u" target="f"><mxGeometry relative="1" as="geometry"><mxPoint y="140" as="offset"/></mxGeometry></mxCell>
        <mxCell id="m2" value="POST /api/transactions" style="html=1;verticalAlign=bottom;endArrow=block;" edge="1" parent="1" source="f" target="b"><mxGeometry relative="1" as="geometry"><mxPoint y="180" as="offset"/></mxGeometry></mxCell>
        <mxCell id="m3" value="INSERT &amp;amp; UPDATE" style="html=1;verticalAlign=bottom;endArrow=block;" edge="1" parent="1" source="b" target="d"><mxGeometry relative="1" as="geometry"><mxPoint y="240" as="offset"/></mxGeometry></mxCell>
    """
    write_drawio("sequence_import.drawio", "diag_seq_imp", "Sequence Import", xml)
    print("Generated: sequence_import.drawio & sequence_import.png")

# =========================================================================
# 9. SEQUENCE DIAGRAM - EXPORT (sequence_export.drawio & sequence_export.png)
# =========================================================================
def gen_sequence_export():
    W, H = 1400, 920
    im = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "HÌNH 7.2. SƠ ĐỒ TUẦN TỰ QUY TRÌNH XUẤT KHO (EXPORT SEQUENCE)",
                "Kiểm tra tồn khả dụng, khóa dòng, trừ kho, kiểm tra ngưỡng tối thiểu và ghi nhật ký kiểm toán")

    lifelines = [
        ("Thủ kho (User)", 120, BLUE_BG, BLUE_BORDER),
        ("React Frontend", 380, BLUE_BG, BLUE_BORDER),
        ("FastAPI APIRouter", 640, CYAN_BG, CYAN_BORDER),
        ("InventoryService", 890, CYAN_BG, CYAN_BORDER),
        ("SQL Database", 1120, AMBER_BG, AMBER_BORDER),
        ("AuditLog Service", 1310, ROSE_BG, ROSE_BORDER),
    ]

    for title, x, bg, bd in lifelines:
        draw_rounded_box(draw, (x - 70, 110, x + 70, 155), bg, bd, 2)
        draw.text((x - 60, 125), title, fill=TEXT_MAIN, font=FONT_TEXT_BOLD)
        for y in range(160, 860, 15):
            draw.line([(x, y), (x, y + 8)], fill=(148, 163, 184), width=1)

    msgs = [
        (120, 380, 190, "1. Chọn mặt hàng, số lượng xuất & bấm 'Xuất kho'"),
        (380, 640, 240, "2. POST /api/transactions/export (Bearer JWT, Payload)"),
        (640, 890, 290, "3. validate_export_payload()"),
        (890, 1120, 350, "4. SELECT current_stock FROM inventory_items FOR UPDATE"),
        (1120, 890, 400, "5. Trả về kết quả tồn kho (Nếu thiếu: Ném lỗi HTTP 400 Insufficient)"),
        (890, 1120, 460, "6. [Đủ hàng]: INSERT INTO inventory_transactions (type=EXPORT)"),
        (890, 1120, 520, "7. UPDATE inventory_items SET quantity = quantity - N"),
        (890, 1310, 580, "8. log_audit_event('EXPORT_CREATED', details)"),
        (1310, 890, 630, "9. Ghi nhận nhật ký kiểm toán thành công"),
        (890, 640, 690, "10. Commit DB Transaction & kiểm tra ngưỡng an toàn"),
        (640, 380, 750, "11. HTTP 201 Created (JSON Response)"),
        (380, 120, 810, "12. Cập nhật Dashboard & bật LED cảnh báo nếu tồn < min_threshold"),
    ]

    for x1, x2, y, text in msgs:
        draw_arrow(draw, (x1, y), (x2, y), (30, 41, 59), 2)
        mx = min(x1, x2) + 15
        draw.text((mx, y - 18), text, fill=(30, 41, 59), font=FONT_SMALL)

    draw_footer(draw, W, H)
    save_image_both(im, "sequence_export.png")

    xml = """
        <mxCell id="u" value="Thủ kho" style="shape=umlLifeline;participant=umlActor;" vertex="1" parent="1"><mxGeometry x="80" y="80" width="80" height="400" as="geometry"/></mxCell>
        <mxCell id="f" value="Frontend" style="shape=umlLifeline;" vertex="1" parent="1"><mxGeometry x="240" y="80" width="100" height="400" as="geometry"/></mxCell>
        <mxCell id="b" value="FastAPI" style="shape=umlLifeline;" vertex="1" parent="1"><mxGeometry x="420" y="80" width="100" height="400" as="geometry"/></mxCell>
        <mxCell id="d" value="Database" style="shape=umlLifeline;" vertex="1" parent="1"><mxGeometry x="600" y="80" width="100" height="400" as="geometry"/></mxCell>
        <mxCell id="m1" value="Xuất kho" style="html=1;verticalAlign=bottom;endArrow=block;" edge="1" parent="1" source="u" target="f"><mxGeometry relative="1" as="geometry"><mxPoint y="140" as="offset"/></mxGeometry></mxCell>
        <mxCell id="m2" value="Kiểm tra tồn" style="html=1;verticalAlign=bottom;endArrow=block;" edge="1" parent="1" source="b" target="d"><mxGeometry relative="1" as="geometry"><mxPoint y="200" as="offset"/></mxGeometry></mxCell>
        <mxCell id="m3" value="Trừ kho (Nếu đủ)" style="html=1;verticalAlign=bottom;endArrow=block;" edge="1" parent="1" source="b" target="d"><mxGeometry relative="1" as="geometry"><mxPoint y="260" as="offset"/></mxGeometry></mxCell>
    """
    write_drawio("sequence_export.drawio", "diag_seq_exp", "Sequence Export", xml)
    print("Generated: sequence_export.drawio & sequence_export.png")

# =========================================================================
# 10. SEQUENCE DIAGRAM - AI REPORT (sequence_ai_report.drawio & sequence_ai_report.png)
# =========================================================================
def gen_sequence_ai_report():
    W, H = 1400, 920
    im = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "HÌNH 8.1. SƠ ĐỒ TUẦN TỰ TRỢ LÝ HỎI ĐÁP & BÁO CÁO KHO AI",
                "Quy trình xử lý câu hỏi tự nhiên: Thu thập Ground Truth CSDL, suy luận ngữ cảnh và render Smart UI")

    lifelines = [
        ("Người dùng", 120, BLUE_BG, BLUE_BORDER),
        ("AI Chat Console (UI)", 370, BLUE_BG, BLUE_BORDER),
        ("POST /api/ai/ask", 620, CYAN_BG, CYAN_BORDER),
        ("Data Aggregator (DB)", 870, AMBER_BG, AMBER_BORDER),
        ("AI Service / Gemini", 1120, PURPLE_BG, PURPLE_BORDER),
        ("Smart Table Renderer", 1310, EMERALD_BG, EMERALD_BORDER),
    ]

    for title, x, bg, bd in lifelines:
        draw_rounded_box(draw, (x - 70, 110, x + 70, 155), bg, bd, 2)
        draw.text((x - 60, 125), title, fill=TEXT_MAIN, font=FONT_TEXT_BOLD)
        for y in range(160, 860, 15):
            draw.line([(x, y), (x, y + 8)], fill=(148, 163, 184), width=1)

    msgs = [
        (120, 370, 190, "1. Nhập câu hỏi: 'Kho còn bao nhiêu bàn phím cơ AKKO?'"),
        (370, 620, 240, "2. Gửi request: { question: '...', user_token: '...' }"),
        (620, 870, 300, "3. Lấy snapshot CSDL: products, inventory_items, 30-day velocity"),
        (870, 620, 360, "4. Trả về JSON snapshot thực tế (Ground-Truth Context)"),
        (620, 1120, 420, "5. answer_user_question(question, data_context)"),
        (1120, 1120, 470, "6. [Gemini/Rule-Engine]: Khớp SKU, tính tồn, định dạng bảng"),
        (1120, 620, 530, "7. Trả về câu trả lời Markdown + data_snapshot JSON"),
        (620, 370, 590, "8. Trả HTTP 200 OK với kết quả phân tích chuẩn xác"),
        (370, 1310, 650, "9. SmartMarkdownViewer parse bảng Markdown thành React Component"),
        (1310, 370, 710, "10. Render giao diện đẹp mắt (Badges, LED, Nút bấm nhanh)"),
        (370, 120, 770, "11. Người dùng nhận câu trả lời trực quan & xem số liệu chứng minh"),
    ]

    for x1, x2, y, text in msgs:
        draw_arrow(draw, (x1, y), (x2, y), (30, 41, 59), 2)
        mx = min(x1, x2) + 15
        draw.text((mx, y - 18), text, fill=(30, 41, 59), font=FONT_SMALL)

    draw_footer(draw, W, H)
    save_image_both(im, "sequence_ai_report.png")

    xml = """
        <mxCell id="u" value="Thủ kho" style="shape=umlLifeline;participant=umlActor;" vertex="1" parent="1"><mxGeometry x="80" y="80" width="80" height="400" as="geometry"/></mxCell>
        <mxCell id="f" value="AI Console" style="shape=umlLifeline;" vertex="1" parent="1"><mxGeometry x="240" y="80" width="100" height="400" as="geometry"/></mxCell>
        <mxCell id="b" value="FastAPI" style="shape=umlLifeline;" vertex="1" parent="1"><mxGeometry x="420" y="80" width="100" height="400" as="geometry"/></mxCell>
        <mxCell id="ai" value="Gemini Cloud" style="shape=umlLifeline;" vertex="1" parent="1"><mxGeometry x="600" y="80" width="100" height="400" as="geometry"/></mxCell>
        <mxCell id="m1" value="Hỏi đáp kho" style="html=1;verticalAlign=bottom;endArrow=block;" edge="1" parent="1" source="u" target="f"><mxGeometry relative="1" as="geometry"><mxPoint y="140" as="offset"/></mxGeometry></mxCell>
        <mxCell id="m2" value="POST /api/ai/ask" style="html=1;verticalAlign=bottom;endArrow=block;" edge="1" parent="1" source="f" target="b"><mxGeometry relative="1" as="geometry"><mxPoint y="180" as="offset"/></mxGeometry></mxCell>
        <mxCell id="m3" value="Ground-Truth Context + Prompt" style="html=1;verticalAlign=bottom;endArrow=block;" edge="1" parent="1" source="b" target="ai"><mxGeometry relative="1" as="geometry"><mxPoint y="240" as="offset"/></mxGeometry></mxCell>
    """
    write_drawio("sequence_ai_report.drawio", "diag_seq_ai", "Sequence AI Report", xml)
    print("Generated: sequence_ai_report.drawio & sequence_ai_report.png")

# =========================================================================
# 11. DATA FLOW DIAGRAM (data_flow.drawio & data_flow.png)
# =========================================================================
def gen_data_flow():
    W, H = 1400, 920
    im = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "HÌNH 6.2. SƠ ĐỒ LUỒNG DỮ LIỆU CỦA HỆ THỐNG (DATA FLOW DIAGRAM)",
                "Luồng dịch chuyển thông tin giữa Tác nhân bên ngoài, Tiến trình xử lý, Kho lưu trữ và Bộ máy AI")

    # Entities
    draw_rounded_box(draw, (60, 200, 240, 290), BLUE_BG, BLUE_BORDER, 2)
    draw.text((95, 230), "THỦ KHO / ADMIN", fill=BLUE_TEXT, font=FONT_TEXT_BOLD)

    draw_rounded_box(draw, (60, 520, 240, 610), AMBER_BG, AMBER_BORDER, 2)
    draw.text((85, 550), "NHÀ CUNG CẤP / KHÁCH", fill=AMBER_TEXT, font=FONT_TEXT_BOLD)

    # Processes
    draw_rounded_box(draw, (380, 160, 650, 250), CYAN_BG, CYAN_BORDER, 2, radius=20)
    draw.text((410, 185), "P1: Xác thực & Phân quyền", fill=CYAN_TEXT, font=FONT_TEXT_BOLD)
    draw.text((410, 215), "Kiểm tra JWT & quyền theo vai trò", fill=TEXT_MAIN, font=FONT_SMALL)

    draw_rounded_box(draw, (380, 340, 650, 440), CYAN_BG, CYAN_BORDER, 2, radius=20)
    draw.text((400, 365), "P2: Xử lý Giao dịch Nhập/Xuất", fill=CYAN_TEXT, font=FONT_TEXT_BOLD)
    draw.text((400, 395), "Kiểm tra số lượng tồn, khóa dòng", fill=TEXT_MAIN, font=FONT_SMALL)

    draw_rounded_box(draw, (380, 540, 650, 640), PURPLE_BG, PURPLE_BORDER, 2, radius=20)
    draw.text((400, 565), "P3: Phân tích Dữ liệu AI", fill=PURPLE_TEXT, font=FONT_TEXT_BOLD)
    draw.text((400, 595), "Tính Burn-rate, Outlier & Chat NLP", fill=TEXT_MAIN, font=FONT_SMALL)

    # Data Stores (Open-ended rects)
    stores = [
        ("D1: Bảng Người dùng & Phân quyền (users, roles)", (800, 160, 1300, 240), BLUE_BG, BLUE_BORDER),
        ("D2: Bảng Hàng hóa & Vị trí kệ (products, locations, inventory)", (800, 340, 1300, 420), EMERALD_BG, EMERALD_BORDER),
        ("D3: Bảng Phiếu giao dịch (transactions, items)", (800, 520, 1300, 600), AMBER_BG, AMBER_BORDER),
        ("D4: Bảng Nhật ký kiểm toán & AI (audit_logs, ai_query_logs)", (800, 700, 1300, 780), ROSE_BG, ROSE_BORDER),
    ]
    for s_title, bbox, bg, bd in stores:
        draw_rounded_box(draw, bbox, bg, bd, 2)
        draw.text((bbox[0]+20, bbox[1]+30), s_title, fill=TEXT_MAIN, font=FONT_TEXT_BOLD)

    # Connecting arrows
    draw_arrow(draw, (240, 245), (380, 205), BLUE_BORDER, 2, "Credentials")
    draw_arrow(draw, (650, 205), (800, 200), BLUE_BORDER, 2, "Read / Validate")
    draw_arrow(draw, (240, 260), (380, 390), EMERALD_BORDER, 2, "Phiếu giao dịch")
    draw_arrow(draw, (650, 390), (800, 380), EMERALD_BORDER, 2, "Update Stock")
    draw_arrow(draw, (650, 410), (800, 560), AMBER_BORDER, 2, "Insert Transaction")
    draw_arrow(draw, (800, 400), (650, 590), PURPLE_BORDER, 2, "Read Stock Snapshot")
    draw_arrow(draw, (650, 610), (800, 740), ROSE_BORDER, 2, "Log AI Query")

    draw_footer(draw, W, H)
    save_image_both(im, "data_flow.png")

    xml = """
        <mxCell id="ent1" value="Thủ kho / Admin" style="rounded=0;fillColor=#eff6ff;" vertex="1" parent="1"><mxGeometry x="80" y="120" width="140" height="60" as="geometry"/></mxCell>
        <mxCell id="proc1" value="P1: Xử lý Giao dịch" style="ellipse;fillColor=#ecfeff;" vertex="1" parent="1"><mxGeometry x="320" y="110" width="160" height="80" as="geometry"/></mxCell>
        <mxCell id="store1" value="D1: Kho Dữ Liệu Tồn Kho" style="shape=partialRectangle;fillColor=#ecfdf5;" vertex="1" parent="1"><mxGeometry x="600" y="120" width="200" height="60" as="geometry"/></mxCell>
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="ent1" target="proc1"/>
        <mxCell id="e2" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="proc1" target="store1"/>
    """
    write_drawio("data_flow.drawio", "diag_dfd", "Data Flow Diagram", xml)
    print("Generated: data_flow.drawio & data_flow.png")

# Run all 11
if __name__ == "__main__":
    gen_usecase()
    gen_erd()
    gen_architecture()
    gen_activity_login()
    gen_activity_import()
    gen_activity_export()
    gen_activity_ai_flow()
    gen_sequence_import()
    gen_sequence_export()
    gen_sequence_ai_report()
    gen_data_flow()
    print("Successfully generated all 11 Draw.io and PNG diagrams!")
