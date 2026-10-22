# -*- coding: utf-8 -*-
"""
Script tạo 10 sơ đồ bản vẽ kỹ thuật CHUẨN ĐỒ HỌA ĐEN TRẮNG CỠ LỚN (300 DPI)
Hệ thống Quản lý Kho có Tích hợp AI - Nhóm 11 (AIA331)

Thiết kế tối ưu hóa độ đọc:
- Phông chữ Times New Roman cỡ lớn (32px - 48px trên canvas), tương đương 13pt - 16pt thực tế trên trang in.
- Nền trắng tinh khiết (#FFFFFF), đường viền và mũi tên màu đen đậm (#000000, nét dày 3px - 4px).
- Tuyệt đối không dùng màu nhạt, không dùng gradient.
- Bố cục mở rộng theo chiều dọc (Spacious Vertical Grid) giúp các bảng CSDL và hộp chức năng không bị chèn ép.
- Xuất song song PNG 300 DPI và SVG vector.
"""
import os
import math
import shutil
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIAGRAM_DIR = os.path.join(BASE_DIR, "diagrams")
SVG_DIR = os.path.join(DIAGRAM_DIR, "svg")
PDF_DIR = os.path.join(DIAGRAM_DIR, "pdf")
LATEX_IMG_DIR = os.path.join(BASE_DIR, "latex", "images")
os.makedirs(DIAGRAM_DIR, exist_ok=True)
os.makedirs(SVG_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(LATEX_IMG_DIR, exist_ok=True)

# Font configurations (Times New Roman)
FONT_PATH_REG = r"C:\Windows\Fonts\times.ttf"
FONT_PATH_BOLD = r"C:\Windows\Fonts\timesbd.ttf"
FONT_PATH_ITALIC = r"C:\Windows\Fonts\timesi.ttf"
FONT_PATH_CODE = r"C:\Windows\Fonts\consola.ttf"

F_TITLE = ImageFont.truetype(FONT_PATH_BOLD, 46)
F_SUBTITLE = ImageFont.truetype(FONT_PATH_REG, 28)
F_HEADER = ImageFont.truetype(FONT_PATH_BOLD, 36)
F_SUBHEADER = ImageFont.truetype(FONT_PATH_BOLD, 32)
F_TEXT_BOLD = ImageFont.truetype(FONT_PATH_BOLD, 30)
F_TEXT = ImageFont.truetype(FONT_PATH_REG, 28)
F_LABEL = ImageFont.truetype(FONT_PATH_BOLD, 26)
F_CODE_BOLD = ImageFont.truetype(FONT_PATH_BOLD, 26)
F_CODE = ImageFont.truetype(FONT_PATH_CODE, 25)
F_FOOTER = ImageFont.truetype(FONT_PATH_ITALIC, 22)

# Colors
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_DARK = (30, 30, 30)
C_GRAY_LIGHT = (245, 245, 245)

def draw_header(draw, width, title, subtitle):
    draw.rectangle([0, 0, width, 140], fill=C_WHITE)
    draw.text((40, 24), title, fill=C_BLACK, font=F_TITLE)
    draw.text((40, 84), subtitle, fill=C_DARK, font=F_SUBTITLE)
    draw.line([(0, 138), (width, 138)], fill=C_BLACK, width=4)
    draw.line([(0, 144), (width, 144)], fill=C_BLACK, width=2)

def draw_footer(draw, width, height, note="Nhóm 11 - AIA331 | Trường Đại học Công nghệ Thông tin & Truyền thông - ĐHTN"):
    draw.line([(0, height - 55), (width, height - 55)], fill=C_BLACK, width=2)
    draw.text((40, height - 42), note, fill=C_DARK, font=F_FOOTER)

def draw_dashed_line(draw, start, end, fill=C_BLACK, width=3, dash_len=16, gap_len=10):
    x1, y1 = start
    x2, y2 = end
    dist = math.hypot(x2 - x1, y2 - y1)
    if dist == 0:
        return
    dx = (x2 - x1) / dist
    dy = (y2 - y1) / dist
    curr = 0.0
    while curr < dist:
        seg_end = min(curr + dash_len, dist)
        draw.line([(x1 + dx * curr, y1 + dy * curr), (x1 + dx * seg_end, y1 + dy * seg_end)], fill=fill, width=width)
        curr += dash_len + gap_len

def draw_arrow(draw, start, end, fill=C_BLACK, width=3, label="", is_dashed=False, label_offset=(10, -20)):
    draw_polyline_arrow(draw, [start, end], fill=fill, width=width, is_dashed=is_dashed, 
                        label=label, label_pos=((start[0] + end[0])/2 + label_offset[0], (start[1] + end[1])/2 + label_offset[1]) if label else None)

def draw_polyline_arrow(draw, points, fill=C_BLACK, width=3, is_dashed=False, label="", label_pos=None):
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i+1]
        if is_dashed:
            draw_dashed_line(draw, p1, p2, fill=fill, width=width)
        else:
            draw.line([p1, p2], fill=fill, width=width)
    
    # Arrowhead at last segment
    p_prev, p_last = points[-2], points[-1]
    x1, y1 = p_prev
    x2, y2 = p_last
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 22
    arrow_angle = 0.45
    px1 = x2 - arrow_len * math.cos(angle - arrow_angle)
    py1 = y2 - arrow_len * math.sin(angle - arrow_angle)
    px2 = x2 - arrow_len * math.cos(angle + arrow_angle)
    py2 = y2 - arrow_len * math.sin(angle + arrow_angle)
    draw.polygon([(x2, y2), (px1, py1), (px2, py2)], fill=fill)

    if label and label_pos:
        lx, ly = label_pos
        bbox = draw.textbbox((lx, ly), label, font=F_LABEL)
        draw.rectangle([bbox[0] - 6, bbox[1] - 4, bbox[2] + 6, bbox[3] + 4], fill=C_WHITE, outline=C_BLACK, width=1)
        draw.text((lx, ly), label, fill=fill, font=F_LABEL)

def draw_box(draw, bbox, fill=C_WHITE, outline=C_BLACK, width=3, radius=10):
    x1, y1, x2, y2 = bbox
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

# =========================================================================
# 1. SƠ ĐỒ KIẾN TRÚC 3 TẦNG
# =========================================================================
def make_arch_diagram():
    W, H = 1600, 2050
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ KIẾN TRÚC TỔNG THỂ HỆ THỐNG 3 TẦNG (3-TIER ARCHITECTURE)",
                "Dự án Hệ thống Quản lý Kho có Tích hợp AI - AIA331 | Nhóm 11")

    # Tier 1
    draw_box(draw, (40, 170, 1560, 680), fill=C_WHITE, outline=C_BLACK, width=4, radius=12)
    draw.rectangle([40, 170, 1560, 235], fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
    draw.text((60, 185), "TẦNG 1: TRÌNH DIỄN (PRESENTATION TIER) - REACT VITE SPA", fill=C_BLACK, font=F_HEADER)

    t1_boxes = [
        ("Dashboard & KPI Hub", [
            "• 6 thẻ chỉ số kho thời gian thực",
            "• Biểu đồ Nhập/Xuất 30 ngày",
            "• Cảnh báo thiếu hụt cạn kho",
        ], (70, 260, 780, 440)),
        ("Quản Lý Nghiệp Vụ Kho", [
            "• Quản lý Sản phẩm & SKU",
            "• Quản lý vị trí kệ (Zone/Shelf)",
            "• Lập phiếu Nhập / Xuất kho",
        ], (820, 260, 1530, 440)),
        ("AI Analytics & NLP Hub", [
            "• Trợ lý hỏi đáp tự nhiên NLP",
            "• Dự báo số ngày cạn tồn kho",
            "• Phát hiện bất thường Z-score",
        ], (70, 470, 780, 650)),
        ("Bảo Mật & Quản Trị", [
            "• Đăng nhập Bearer JWT an toàn",
            "• Phân quyền RBAC (3 Vai trò)",
            "• Nhật ký kiểm toán Audit Logs",
        ], (820, 470, 1530, 650)),
    ]
    for title, items, bbox in t1_boxes:
        draw_box(draw, bbox, fill=C_WHITE, outline=C_BLACK, width=3, radius=8)
        draw.text((bbox[0] + 20, bbox[1] + 16), title, fill=C_BLACK, font=F_TEXT_BOLD)
        draw.line([(bbox[0], bbox[1] + 55), (bbox[2], bbox[1] + 55)], fill=C_BLACK, width=2)
        y = bbox[1] + 68
        for it in items:
            draw.text((bbox[0] + 20, y), it, fill=C_DARK, font=F_TEXT)
            y += 42

    # Communication Arrows T1 -> T2
    draw_arrow(draw, (450, 680), (450, 770), fill=C_BLACK, width=4, label="REST / JSON API (Bearer Token)", label_offset=(15, -22))
    draw_arrow(draw, (1150, 680), (1150, 770), fill=C_BLACK, width=4, label="Async Requests / CORS Handlers", label_offset=(15, -22))

    # Tier 2
    draw_box(draw, (40, 770, 1560, 1280), fill=C_WHITE, outline=C_BLACK, width=4, radius=12)
    draw.rectangle([40, 770, 1560, 835], fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
    draw.text((60, 785), "TẦNG 2: NGHIỆP VỤ (APPLICATION LOGIC TIER) - FASTAPI ASYNC BACKEND", fill=C_BLACK, font=F_HEADER)

    t2_boxes = [
        ("API Gateway & Routers", [
            "• FastAPI APIRouter phân tách",
            "• OAuth2PasswordBearer JWT",
            "• Global Exception Handlers",
        ], (70, 860, 780, 1040)),
        ("Nghiệp Vụ Kho (Services)", [
            "• InventoryService (Nhập/Xuất)",
            "• Row-level Locking chống race",
            "• Tính tồn khả dụng an toàn",
        ], (820, 860, 1530, 1040)),
        ("AI Dual-Layer Engine", [
            "• Lớp 1: Gemini 1.5 Flash Cloud",
            "• Lớp 2: Local Rule Engine",
            "• Ground-Truth Context Injection",
        ], (70, 1070, 780, 1250)),
        ("Bảo Mật & RBAC Engine", [
            "• Băm mật khẩu Argon2 an toàn",
            "• Phân quyền Decorator 3 vai trò",
            "• Chống SQLi qua SQLAlchemy",
        ], (820, 1070, 1530, 1250)),
    ]
    for title, items, bbox in t2_boxes:
        draw_box(draw, bbox, fill=C_WHITE, outline=C_BLACK, width=3, radius=8)
        draw.text((bbox[0] + 20, bbox[1] + 16), title, fill=C_BLACK, font=F_TEXT_BOLD)
        draw.line([(bbox[0], bbox[1] + 55), (bbox[2], bbox[1] + 55)], fill=C_BLACK, width=2)
        y = bbox[1] + 68
        for it in items:
            draw.text((bbox[0] + 20, y), it, fill=C_DARK, font=F_TEXT)
            y += 42

    # Communication Arrows T2 -> T3
    draw_arrow(draw, (450, 1280), (450, 1370), fill=C_BLACK, width=4, label="SQLAlchemy ORM (ACID Transactions)", label_offset=(15, -22))
    draw_arrow(draw, (1150, 1280), (1150, 1370), fill=C_BLACK, width=4, label="Prompt Calls / Audit Trail Logging", label_offset=(15, -22))

    # Tier 3
    draw_box(draw, (40, 1370, 1560, 1960), fill=C_WHITE, outline=C_BLACK, width=4, radius=12)
    draw.rectangle([40, 1370, 1560, 1435], fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
    draw.text((60, 1385), "TẦNG 3: DỮ LIỆU & AI CLOUD (DATA PERSISTENCE & AI LAYER)", fill=C_BLACK, font=F_HEADER)

    t3_boxes = [
        ("Cơ Sở Dữ Liệu Quan Hệ (11 Bảng 3NF)", [
            "• 11 bảng chuẩn hóa 3NF không dư thừa",
            "• Hỗ trợ SQLite (phát triển) và PostgreSQL (triển khai)",
            "• Toàn vẹn tham chiếu qua Khóa chính (PK) và Khóa ngoại (FK)",
        ], (70, 1460, 1530, 1600)),
        ("Snapshot Dữ Liệu & Audit Trail Bất Biến", [
            "• Bảng audit_logs lưu vết mọi thay đổi dữ liệu kèm old_values / new_values",
            "• Bảng ai_query_logs ghi nhận toàn bộ prompt và phản hồi AI",
            "• Trích xuất Snapshot CSDL đảm bảo số liệu minh bạch, chống ảo giác",
        ], (70, 1630, 1530, 1770)),
        ("Google Gemini AI Cloud (External LLM Service)", [
            "• Mô hình gemini-1.5-flash / gemini-2.0 phân tích ngữ nghĩa",
            "• Định dạng bảng Markdown tự động chuyển đổi sang UI Component",
            "• Cơ chế Fallback tức thời sang Local Rule Engine khi ngắt mạng",
        ], (70, 1800, 1530, 1940)),
    ]
    for title, items, bbox in t3_boxes:
        draw_box(draw, bbox, fill=C_WHITE, outline=C_BLACK, width=3, radius=8)
        draw.text((bbox[0] + 20, bbox[1] + 14), title, fill=C_BLACK, font=F_TEXT_BOLD)
        draw.line([(bbox[0], bbox[1] + 50), (bbox[2], bbox[1] + 50)], fill=C_BLACK, width=2)
        y = bbox[1] + 60
        for it in items:
            draw.text((bbox[0] + 20, y), it, fill=C_DARK, font=F_TEXT)
            y += 38

    draw_footer(draw, W, H)
    out_png = os.path.join(DIAGRAM_DIR, "01_so_do_kien_truc_he_thong.png")
    im.save(out_png, dpi=(300, 300))
    shutil.copy2(out_png, os.path.join(LATEX_IMG_DIR, "01_so_do_kien_truc_he_thong.png"))
    print("Generated (B&W Large 300 DPI): 01_so_do_kien_truc_he_thong.png")

# =========================================================================
# 2. SƠ ĐỒ USE CASE TỔNG THỂ
# =========================================================================
def make_usecase_diagram():
    W, H = 1600, 1950
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ USE CASE TỔNG THỂ HỆ THỐNG QUẢN LÝ KHO AI",
                "Phân quyền 3 Tác nhân: Quản trị viên (ADMIN), Thủ kho (WAREHOUSE), Kế toán (ACCOUNTANT)")

    # System boundary box
    draw_box(draw, (380, 170, 1560, 1880), fill=C_WHITE, outline=C_BLACK, width=4, radius=12)
    draw.rectangle([380, 170, 1560, 235], fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
    draw.text((410, 185), "HỆ THỐNG QUẢN LÝ KHO CÓ TÍCH HỢP AI", fill=C_BLACK, font=F_HEADER)

    # Function to draw UML Actor
    def draw_actor(cx, cy, label_role, label_code):
        draw.ellipse([cx - 30, cy - 80, cx + 30, cy - 20], outline=C_BLACK, width=4)
        draw.line([(cx, cy - 20), (cx, cy + 50)], fill=C_BLACK, width=4)
        draw.line([(cx - 50, cy), (cx + 50, cy)], fill=C_BLACK, width=4)
        draw.line([(cx, cy + 50), (cx - 35, cy + 115)], fill=C_BLACK, width=4)
        draw.line([(cx, cy + 50), (cx + 35, cy + 115)], fill=C_BLACK, width=4)
        
        bbox = (cx - 155, cy + 125, cx + 155, cy + 205)
        draw_box(draw, bbox, fill=C_WHITE, outline=C_BLACK, width=3, radius=8)
        draw.text((cx - 135, cy + 135), label_role, fill=C_BLACK, font=F_TEXT_BOLD)
        draw.text((cx - 135, cy + 170), label_code, fill=C_DARK, font=F_SUBTITLE)

    draw_actor(190, 480, "QUẢN TRỊ VIÊN", "Vai trò: ADMIN")
    draw_actor(190, 1150, "THỦ KHO", "Vai trò: WAREHOUSE")
    draw_actor(190, 1680, "KẾ TOÁN", "Vai trò: ACCOUNTANT")

    usecases = [
        ("UC01: Đăng nhập & Xác thực JWT", (430, 260, 1020, 345)),
        ("UC02: Quản lý Người dùng & Phân quyền", (430, 375, 1020, 460)),
        ("UC03: Xem Nhật ký Kiểm toán (Audit Logs)", (430, 490, 1020, 575)),
        ("UC04: Quản lý Danh mục, NCC, Vị trí kệ", (430, 620, 1020, 705)),
        ("UC05: Quản lý Sản phẩm & Định mức tồn", (430, 735, 1020, 820)),
        ("UC06: Tạo Phiếu Nhập Kho & Phê duyệt", (430, 850, 1020, 935)),
        ("UC07: Tạo Phiếu Xuất Kho & Trừ tồn kho", (430, 965, 1020, 1050)),
        ("UC08: Báo cáo Tài chính & Định giá kho", (1050, 1150, 1530, 1235)),
        ("UC09: Dự báo cạn tồn & Tái đặt hàng (AI)", (1050, 1290, 1530, 1375)),
        ("UC10: Phát hiện Bất thường Tồn kho (AI)", (1050, 1430, 1530, 1515)),
        ("UC11: Trợ lý Hỏi Đáp Kho Tự Nhiên (NLP)", (1050, 1570, 1530, 1655)),
        ("UC12: Xem Dashboard Realtime 6 Thẻ KPI", (550, 1730, 1450, 1825)),
    ]

    for name, bbox in usecases:
        draw.ellipse(bbox, fill=C_WHITE, outline=C_BLACK, width=3)
        draw.text((bbox[0] + 35, bbox[1] + 25), name, fill=C_BLACK, font=F_TEXT_BOLD)

    # Admin connections (cx=190, cy=480)
    for uc_y in [302, 417, 532]:
        draw.line([(190, 480), (430, uc_y)], fill=C_BLACK, width=3)
    draw.line([(190, 480), (550, 1777)], fill=C_BLACK, width=2) # Dashboard

    # Warehouse connections (cx=190, cy=1150)
    for uc_y in [302, 662, 777, 892, 1007]:
        draw.line([(190, 1150), (430, uc_y)], fill=C_BLACK, width=3)
    draw.line([(190, 1150), (1050, 1332)], fill=C_BLACK, width=3) # AI Restock
    draw.line([(190, 1150), (1050, 1612)], fill=C_BLACK, width=3) # AI NLP Chat
    draw.line([(190, 1150), (550, 1777)], fill=C_BLACK, width=2) # Dashboard

    # Accountant connections (cx=190, cy=1680)
    draw.line([(190, 1680), (430, 302)], fill=C_BLACK, width=2)   # Login
    draw.line([(190, 1680), (1050, 1192)], fill=C_BLACK, width=3) # Financial
    draw.line([(190, 1680), (1050, 1332)], fill=C_BLACK, width=3) # AI Restock
    draw.line([(190, 1680), (1050, 1472)], fill=C_BLACK, width=3) # AI Anomaly
    draw.line([(190, 1680), (550, 1777)], fill=C_BLACK, width=3)  # Dashboard

    draw_footer(draw, W, H)
    out_png = os.path.join(DIAGRAM_DIR, "02_so_do_usecase_tong_the.png")
    im.save(out_png, dpi=(300, 300))
    shutil.copy2(out_png, os.path.join(LATEX_IMG_DIR, "02_so_do_usecase_tong_the.png"))
    print("Generated (B&W Large 300 DPI): 02_so_do_usecase_tong_the.png")

# =========================================================================
# 3. SƠ ĐỒ THỰC THỂ LIÊN KẾT (ERD) 11 BẢNG CHUẨN 3NF (CỠ LỚN, RÕ TỪNG CỘT)
# =========================================================================
def make_erd_diagram():
    W, H = 1800, 2550
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ THỰC THỂ LIÊN KẾT (ERD) - 11 BẢNG CSDL CHUẨN 3NF",
                "Thiết kế Cơ sở Dữ liệu Quan hệ: Sản phẩm, Kệ kho, Giao dịch Nhập/Xuất, Kiểm toán & AI Logs")

    # 11 Tables arranged in 2 wide vertical columns
    # Column 1: x from 50 to 880 (width 830px)
    # Column 2: x from 920 to 1750 (width 830px)
    tables_col1 = [
        ("roles", 180, [
            (True, False, "id", "INTEGER (PK)"),
            (False, False, "name", "VARCHAR(50) UNIQUE"),
            (False, False, "description", "VARCHAR(255)"),
            (False, False, "created_at", "DATETIME"),
        ]),
        ("users", 470, [
            (True, False, "id", "INTEGER (PK)"),
            (False, True, "role_id", "INTEGER (FK -> roles.id)"),
            (False, False, "username", "VARCHAR(50) UNIQUE"),
            (False, False, "password_hash", "VARCHAR(255)"),
            (False, False, "full_name", "VARCHAR(100)"),
            (False, False, "is_active", "BOOLEAN"),
            (False, False, "created_at", "DATETIME"),
        ]),
        ("categories", 880, [
            (True, False, "id", "INTEGER (PK)"),
            (False, False, "code", "VARCHAR(50) UNIQUE"),
            (False, False, "name", "VARCHAR(100)"),
            (False, False, "description", "TEXT"),
        ]),
        ("suppliers", 1170, [
            (True, False, "id", "INTEGER (PK)"),
            (False, False, "name", "VARCHAR(150)"),
            (False, False, "contact_name", "VARCHAR(100)"),
            (False, False, "phone", "VARCHAR(20)"),
            (False, False, "email", "VARCHAR(100)"),
        ]),
        ("audit_logs", 1510, [
            (True, False, "id", "INTEGER (PK)"),
            (False, True, "user_id", "INTEGER (FK -> users.id)"),
            (False, False, "action", "VARCHAR(50)"),
            (False, False, "entity_name", "VARCHAR(50)"),
            (False, False, "entity_id", "INTEGER"),
            (False, False, "old_values", "JSON"),
            (False, False, "new_values", "JSON"),
            (False, False, "created_at", "DATETIME"),
        ]),
        ("ai_query_logs", 1990, [
            (True, False, "id", "INTEGER (PK)"),
            (False, True, "user_id", "INTEGER (FK -> users.id)"),
            (False, False, "query_type", "VARCHAR(50)"),
            (False, False, "prompt", "TEXT"),
            (False, False, "response_summary", "TEXT"),
            (False, False, "execution_time_ms", "INTEGER"),
            (False, False, "created_at", "DATETIME"),
        ]),
    ]

    tables_col2 = [
        ("locations", 180, [
            (True, False, "id", "INTEGER (PK)"),
            (False, False, "code", "VARCHAR(50) UNIQUE"),
            (False, False, "zone", "VARCHAR(20)"),
            (False, False, "shelf", "VARCHAR(20)"),
            (False, False, "capacity", "INTEGER"),
        ]),
        ("products", 500, [
            (True, False, "id", "INTEGER (PK)"),
            (False, True, "category_id", "INTEGER (FK -> categories.id)"),
            (False, True, "supplier_id", "INTEGER (FK -> suppliers.id)"),
            (False, False, "sku", "VARCHAR(50) UNIQUE"),
            (False, False, "name", "VARCHAR(200)"),
            (False, False, "unit", "VARCHAR(20)"),
            (False, False, "cost_price", "DECIMAL(12,2)"),
            (False, False, "selling_price", "DECIMAL(12,2)"),
            (False, False, "min_threshold", "INTEGER"),
            (False, False, "max_threshold", "INTEGER"),
            (False, False, "status", "VARCHAR(20)"),
        ]),
        ("inventory_items", 1120, [
            (True, False, "id", "INTEGER (PK)"),
            (False, True, "product_id", "INTEGER (FK -> products.id)"),
            (False, True, "location_id", "INTEGER (FK -> locations.id)"),
            (False, False, "quantity", "INTEGER"),
            (False, False, "batch_number", "VARCHAR(50)"),
            (False, False, "expiry_date", "DATE"),
            (False, False, "updated_at", "DATETIME"),
        ]),
        ("inventory_transactions", 1540, [
            (True, False, "id", "INTEGER (PK)"),
            (False, False, "code", "VARCHAR(50) UNIQUE"),
            (False, False, "type", "VARCHAR(20) (IMPORT / EXPORT)"),
            (False, True, "created_by", "INTEGER (FK -> users.id)"),
            (False, True, "supplier_id", "INTEGER (FK -> suppliers.id)"),
            (False, False, "status", "VARCHAR(20) (APPROVED)"),
            (False, False, "total_value", "DECIMAL(14,2)"),
            (False, False, "created_at", "DATETIME"),
        ]),
        ("inventory_transaction_items", 2000, [
            (True, False, "id", "INTEGER (PK)"),
            (False, True, "transaction_id", "INTEGER (FK -> trans.id)"),
            (False, True, "product_id", "INTEGER (FK -> products.id)"),
            (False, True, "location_id", "INTEGER (FK -> locations.id)"),
            (False, False, "quantity", "INTEGER"),
            (False, False, "unit_price", "DECIMAL(12,2)"),
            (False, False, "subtotal", "DECIMAL(14,2)"),
            (False, False, "batch_number", "VARCHAR(50)"),
        ]),
    ]

    def render_table_box(x1, y1, width, tname, fields):
        x2 = x1 + width
        row_height = 44
        y2 = y1 + 65 + len(fields) * row_height + 15
        bbox = (x1, y1, x2, y2)
        draw_box(draw, bbox, fill=C_WHITE, outline=C_BLACK, width=3, radius=8)
        
        # Header banner
        draw.rectangle([x1, y1, x2, y1 + 58], fill=C_GRAY_LIGHT, outline=C_BLACK, width=2)
        draw.text((x1 + 20, y1 + 12), f"BẢNG CSDL: {tname.upper()}", fill=C_BLACK, font=F_HEADER)
        
        curr_y = y1 + 72
        for is_pk, is_fk, fname, ftype in fields:
            # Indicator
            if is_pk:
                draw.text((x1 + 18, curr_y), "[PK]", fill=C_BLACK, font=F_CODE_BOLD)
            elif is_fk:
                draw.text((x1 + 18, curr_y), "[FK]", fill=C_BLACK, font=F_CODE_BOLD)
            else:
                draw.text((x1 + 18, curr_y), "    ", fill=C_BLACK, font=F_CODE)
            
            # Field name
            draw.text((x1 + 90, curr_y), fname, fill=C_BLACK, font=F_TEXT_BOLD if (is_pk or is_fk) else F_TEXT)
            # Field type
            draw.text((x2 - 320, curr_y), ftype, fill=C_DARK, font=F_CODE)
            curr_y += row_height
        return bbox

    # Render Col 1
    for tname, y1, fields in tables_col1:
        render_table_box(50, y1, 830, tname, fields)

    # Render Col 2
    for tname, y1, fields in tables_col2:
        render_table_box(920, y1, 830, tname, fields)

    # Cardinality Connections with thick solid arrows
    draw_arrow(draw, (465, 410), (465, 470), fill=C_BLACK, width=3, label="1 : N") # roles -> users
    draw_arrow(draw, (880, 950), (920, 620), fill=C_BLACK, width=3, label="1 : N") # categories -> products
    draw_arrow(draw, (880, 1250), (920, 720), fill=C_BLACK, width=3, label="1 : N") # suppliers -> products
    draw_arrow(draw, (1335, 1040), (1335, 1120), fill=C_BLACK, width=3, label="1 : N") # products -> inventory_items
    draw_arrow(draw, (1335, 430), (1335, 1120), fill=C_BLACK, width=3, label="1 : N") # locations -> inventory_items
    draw_arrow(draw, (1335, 1920), (1335, 2000), fill=C_BLACK, width=3, label="1 : N") # trans -> trans_items
    draw_arrow(draw, (465, 810), (465, 1510), fill=C_BLACK, width=3, label="1 : N") # users -> audit_logs
    draw_arrow(draw, (465, 1890), (465, 1990), fill=C_BLACK, width=3, label="1 : N") # users -> ai_query_logs

    draw_footer(draw, W, H)
    out_png = os.path.join(DIAGRAM_DIR, "03_so_do_erd_11_bang.png")
    im.save(out_png, dpi=(300, 300))
    shutil.copy2(out_png, os.path.join(LATEX_IMG_DIR, "03_so_do_erd_11_bang.png"))
    print("Generated (B&W Large 300 DPI): 03_so_do_erd_11_bang.png")

# =========================================================================
# 4. LƯỢC ĐỒ HOẠT ĐỘNG NHẬP KHO
# =========================================================================
def make_activity_import_diagram():
    W, H = 1600, 2050
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "LƯỢC ĐỒ HOẠT ĐỘNG QUY TRÌNH NHẬP KHO (IMPORT ACTIVITY)",
                "Quy trình nghiệp vụ: Lập phiếu, kiểm đếm thực tế, gán vị trí kệ, cập nhật tồn kho và ghi kiểm toán")

    steps = [
        ("Khởi đầu: Thủ kho yêu cầu nhập hàng từ Nhà Cung Cấp", (350, 180, 1250, 275), False),
        ("Chọn Nhà Cung Cấp và điền thông tin phiếu nhập", (350, 330, 1250, 425), False),
        ("Thêm danh sách sản phẩm, số lượng và đơn giá nhập", (350, 480, 1250, 575), False),
        ("Kiểm tra hàng hóa thực tế và đối chiếu đơn giao hàng", (350, 630, 1250, 725), False),
        ("Hàng hóa đạt tiêu chuẩn quy cách và nguyên vẹn?", (320, 780, 1280, 910), True),  # Decision Diamond
        ("Chỉ định vị trí kệ kho tiếp nhận (Location: Zone / Shelf)", (350, 980, 1250, 1075), False),
        ("Hệ thống tạo Transaction (Trạng thái: APPROVED)", (350, 1130, 1250, 1225), False),
        ("Cộng dồn số lượng thực tế vào bảng inventory_items", (350, 1280, 1250, 1375), False),
        ("Ghi nhận nhật ký kiểm toán Audit Log & Cập nhật Realtime KPI", (300, 1430, 1300, 1525), False),
        ("Kết thúc: Phiếu nhập hoàn tất thành công và in biên bản", (350, 1580, 1250, 1675), False),
    ]

    for title, bbox, is_decision in steps:
        if is_decision:
            cx = (bbox[0] + bbox[2]) // 2
            cy = (bbox[1] + bbox[3]) // 2
            w2 = (bbox[2] - bbox[0]) // 2
            h2 = (bbox[3] - bbox[1]) // 2
            draw.polygon([(cx, cy - h2), (cx + w2, cy), (cx, cy + h2), (cx - w2, cy)], fill=C_WHITE, outline=C_BLACK, width=3)
            draw.text((bbox[0] + 60, cy - 18), title, fill=C_BLACK, font=F_TEXT_BOLD)
        else:
            draw_box(draw, bbox, fill=C_WHITE, outline=C_BLACK, width=3, radius=10)
            draw.text((bbox[0] + 30, bbox[1] + 30), title, fill=C_BLACK, font=F_TEXT_BOLD)

    # Reject box (alternative flow)
    reject_box = (1330, 800, 1580, 890)
    draw_box(draw, reject_box, fill=C_WHITE, outline=C_BLACK, width=3, radius=8)
    draw.text((reject_box[0] + 16, reject_box[1] + 16), "Từ chối nhận hàng,\nlập biên bản sự cố", fill=C_BLACK, font=F_TEXT_BOLD)

    # Connections
    draw_arrow(draw, (800, 275), (800, 330), fill=C_BLACK, width=3)
    draw_arrow(draw, (800, 425), (800, 480), fill=C_BLACK, width=3)
    draw_arrow(draw, (800, 575), (800, 630), fill=C_BLACK, width=3)
    draw_arrow(draw, (800, 725), (800, 780), fill=C_BLACK, width=3)

    # Decision paths
    draw_arrow(draw, (800, 910), (800, 980), fill=C_BLACK, width=3, label="Đạt chuẩn [Yes]", label_offset=(15, -20))
    draw_arrow(draw, (1280, 845), (1330, 845), fill=C_BLACK, width=3, label="Lỗi [No]", is_dashed=True, label_offset=(10, -22))
    draw_dashed_line(draw, (1455, 890), (1455, 1627), fill=C_BLACK, width=3)
    draw_arrow(draw, (1455, 1627), (1250, 1627), fill=C_BLACK, width=3, label="Đóng giao dịch lỗi", is_dashed=True)

    draw_arrow(draw, (800, 1075), (800, 1130), fill=C_BLACK, width=3)
    draw_arrow(draw, (800, 1225), (800, 1280), fill=C_BLACK, width=3)
    draw_arrow(draw, (800, 1375), (800, 1430), fill=C_BLACK, width=3)
    draw_arrow(draw, (800, 1525), (800, 1580), fill=C_BLACK, width=3)

    draw_footer(draw, W, H)
    out_png = os.path.join(DIAGRAM_DIR, "04_luoc_do_hoat_dong_nhap_kho.png")
    im.save(out_png, dpi=(300, 300))
    shutil.copy2(out_png, os.path.join(LATEX_IMG_DIR, "04_luoc_do_hoat_dong_nhap_kho.png"))
    print("Generated (B&W Large 300 DPI): 04_luoc_do_hoat_dong_nhap_kho.png")

# =========================================================================
# 5. LƯỢC ĐỒ HOẠT ĐỘNG XUẤT KHO
# =========================================================================
def make_activity_export_diagram():
    W, H = 1600, 2050
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "LƯỢC ĐỒ HOẠT ĐỘNG QUY TRÌNH XUẤT KHO (EXPORT ACTIVITY)",
                "Kiểm tra số lượng khả dụng, khóa tạm hàng hóa, trừ kho và kích hoạt cảnh báo tái nhập tự động")

    steps = [
        ("Khởi đầu: Yêu cầu xuất kho cho khách hàng / đại lý", (350, 180, 1250, 275), False),
        ("Chọn khách hàng / mục đích xuất và điền thông tin phiếu", (350, 330, 1250, 425), False),
        ("Thêm danh mục sản phẩm và số lượng yêu cầu xuất", (350, 480, 1250, 575), False),
        ("Kiểm tra tồn kho: Số lượng xuất <= Số lượng khả dụng?", (320, 630, 1280, 760), True), # Decision 1
        ("Khóa bản ghi tồn kho tạm thời (Row-level Locking)", (350, 830, 1250, 925), False),
        ("Trừ số lượng thực tế trong bảng inventory_items", (350, 980, 1250, 1075), False),
        ("Kiểm tra ngưỡng an toàn: Stock < min_threshold?", (320, 1130, 1280, 1260), True), # Decision 2
        ("Kích hoạt cảnh báo AI Alert: Đề xuất lập phiếu tái nhập", (350, 1330, 1250, 1425), False),
        ("Ghi nhận nhật ký kiểm toán Audit Log và hoàn tất xuất kho", (300, 1480, 1300, 1575), False),
        ("Kết thúc: Bàn giao hàng hóa và in phiếu xuất kho", (350, 1630, 1250, 1725), False),
    ]

    for title, bbox, is_decision in steps:
        if is_decision:
            cx = (bbox[0] + bbox[2]) // 2
            cy = (bbox[1] + bbox[3]) // 2
            w2 = (bbox[2] - bbox[0]) // 2
            h2 = (bbox[3] - bbox[1]) // 2
            draw.polygon([(cx, cy - h2), (cx + w2, cy), (cx, cy + h2), (cx - w2, cy)], fill=C_WHITE, outline=C_BLACK, width=3)
            draw.text((bbox[0] + 50, cy - 18), title, fill=C_BLACK, font=F_TEXT_BOLD)
        else:
            draw_box(draw, bbox, fill=C_WHITE, outline=C_BLACK, width=3, radius=10)
            draw.text((bbox[0] + 30, bbox[1] + 30), title, fill=C_BLACK, font=F_TEXT_BOLD)

    # Error box (Out of stock)
    err_box = (1330, 650, 1580, 740)
    draw_box(draw, err_box, fill=C_WHITE, outline=C_BLACK, width=3, radius=8)
    draw.text((err_box[0] + 16, err_box[1] + 16), "Báo lỗi: Kho không đủ\nsố lượng xuất khả dụng", fill=C_BLACK, font=F_TEXT_BOLD)

    # Connections
    draw_arrow(draw, (800, 275), (800, 330), fill=C_BLACK, width=3)
    draw_arrow(draw, (800, 425), (800, 480), fill=C_BLACK, width=3)
    draw_arrow(draw, (800, 575), (800, 630), fill=C_BLACK, width=3)

    # Decision 1
    draw_arrow(draw, (800, 760), (800, 830), fill=C_BLACK, width=3, label="Đủ hàng [Yes]", label_offset=(15, -20))
    draw_arrow(draw, (1280, 695), (1330, 695), fill=C_BLACK, width=3, label="Hết hàng [No]", is_dashed=True, label_offset=(10, -22))
    draw_dashed_line(draw, (1455, 740), (1455, 1677), fill=C_BLACK, width=3)
    draw_arrow(draw, (1455, 1677), (1250, 1677), fill=C_BLACK, width=3, label="Đóng đơn hàng", is_dashed=True)

    draw_arrow(draw, (800, 925), (800, 980), fill=C_BLACK, width=3)
    draw_arrow(draw, (800, 1075), (800, 1130), fill=C_BLACK, width=3)

    # Decision 2
    draw_arrow(draw, (800, 1260), (800, 1330), fill=C_BLACK, width=3, label="Dưới ngưỡng [Yes]", label_offset=(15, -20))
    draw_arrow(draw, (800, 1425), (800, 1480), fill=C_BLACK, width=3)
    # Bypass Decision 2
    draw.line([(320, 1195), (220, 1195)], fill=C_BLACK, width=3)
    draw.line([(220, 1195), (220, 1527)], fill=C_BLACK, width=3)
    draw_arrow(draw, (220, 1527), (300, 1527), fill=C_BLACK, width=3, label="Tồn an toàn [No]", label_offset=(15, -20))

    draw_arrow(draw, (800, 1575), (800, 1630), fill=C_BLACK, width=3)

    draw_footer(draw, W, H)
    out_png = os.path.join(DIAGRAM_DIR, "05_luoc_do_hoat_dong_xuat_kho.png")
    im.save(out_png, dpi=(300, 300))
    shutil.copy2(out_png, os.path.join(LATEX_IMG_DIR, "05_luoc_do_hoat_dong_xuat_kho.png"))
    print("Generated (B&W Large 300 DPI): 05_luoc_do_hoat_dong_xuat_kho.png")

# =========================================================================
# 6. SƠ ĐỒ TUẦN TỰ GIAO DỊCH KHO
# =========================================================================
def make_sequence_transaction_diagram():
    W, H = 1600, 1950
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ TUẦN TỰ GIAO DỊCH KHO (SEQUENCE DIAGRAM: IMPORT / EXPORT)",
                "Luồng tương tác: Người dùng -> React Frontend -> FastAPI Router -> Inventory Service -> Database -> Audit Log")

    lifelines = [
        ("Thủ kho (User)", 130),
        ("React Frontend", 420),
        ("FastAPI APIRouter", 720),
        ("InventoryService", 1020),
        ("SQL Database", 1300),
        ("AuditLog Service", 1520),
    ]

    for title, x in lifelines:
        draw_box(draw, (x - 85, 170, x + 85, 240), fill=C_WHITE, outline=C_BLACK, width=3, radius=8)
        draw.text((x - 70, 190), title, fill=C_BLACK, font=F_TEXT_BOLD)
        draw_dashed_line(draw, (x, 250), (x, 1860), fill=C_BLACK, width=3, dash_len=18, gap_len=12)

    msgs = [
        (130, 420, 310, "1. Nhập thông tin phiếu & nhấn 'Tạo phiếu giao dịch'", False),
        (420, 720, 430, "2. POST /api/inventory/trans (Payload, Bearer JWT)", False),
        (720, 1020, 550, "3. validate_payload() & check_role_permission()", False),
        (1020, 1300, 670, "4. SELECT stock FROM inventory_items FOR UPDATE", False),
        (1300, 1020, 790, "5. Trả về số lượng tồn kho khả dụng", True),
        (1020, 1300, 910, "6. INSERT INTO inventory_transactions & items", False),
        (1020, 1300, 1030, "7. UPDATE inventory_items SET quantity = quantity +/- N", False),
        (1020, 1520, 1150, "8. log_audit_event('TRANSACTION_CREATED', details)", False),
        (1520, 1020, 1270, "9. Ghi vết kiểm toán thành công (audit_logs)", True),
        (1020, 720, 1390, "10. Commit DB Transaction & trả về TransactionModel", True),
        (720, 420, 1510, "11. HTTP 201 Created (JSON Response Model)", True),
        (420, 130, 1630, "12. Hiển thị Toast thành công & reload Realtime KPI", True),
    ]

    for x1, x2, y, text, is_ret in msgs:
        draw_arrow(draw, (x1, y), (x2, y), fill=C_BLACK, width=3, is_dashed=is_ret)
        mx = min(x1, x2) + 20
        draw.text((mx, y - 34), text, fill=C_BLACK, font=F_TEXT_BOLD if not is_ret else F_TEXT)

    draw_footer(draw, W, H)
    out_png = os.path.join(DIAGRAM_DIR, "06_so_do_tuan_tu_nhap_xuat.png")
    im.save(out_png, dpi=(300, 300))
    shutil.copy2(out_png, os.path.join(LATEX_IMG_DIR, "06_so_do_tuan_tu_nhap_xuat.png"))
    print("Generated (B&W Large 300 DPI): 06_so_do_tuan_tu_nhap_xuat.png")

# =========================================================================
# 7. SƠ ĐỒ PIPELINE AI 2 LỚP FALLBACK
# =========================================================================
def make_ai_pipeline_diagram():
    W, H = 1600, 1950
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ KIẾN TRÚC PIPELINE XỬ LÝ AI 2 LỚP (DUAL-LAYER AI FALLBACK)",
                "Cơ chế chuyển đổi dự phòng: Google Gemini Cloud LLM -> Local Rule Engine (Deterministic)")

    # Box 1: Client Request
    b1 = (50, 180, 750, 450)
    draw_box(draw, b1, fill=C_WHITE, outline=C_BLACK, width=4, radius=10)
    draw.text((80, 205), "1. Yêu cầu Phân tích từ Client", fill=C_BLACK, font=F_HEADER)
    draw.line([(50, 260), (750, 260)], fill=C_BLACK, width=2)
    draw.text((80, 280), "• Dự báo nhu cầu nhập hàng cạn tồn\n• Phát hiện dị biệt & bất thường Z-score\n• Trợ lý hỏi đáp kho bằng ngôn ngữ tự nhiên", fill=C_DARK, font=F_TEXT)

    # Box 2: Snapshot Aggregator
    b2 = (850, 180, 1550, 450)
    draw_box(draw, b2, fill=C_WHITE, outline=C_BLACK, width=4, radius=10)
    draw.text((880, 205), "2. Data Snapshot Aggregator", fill=C_BLACK, font=F_HEADER)
    draw.line([(850, 260), (1550, 260)], fill=C_BLACK, width=2)
    draw.text((880, 280), "• Trích xuất CSDL thực tế 100% chính xác\n• Vận tốc tiêu thụ xuất kho 30 ngày gần nhất\n• Ground-Truth Context: Chống ảo giác số liệu", fill=C_DARK, font=F_TEXT)

    # Arrow 1 -> 2
    draw_arrow(draw, (750, 315), (850, 315), fill=C_BLACK, width=4)

    # Decision Diamond: Check Cloud Connection
    b3 = (550, 520, 1050, 720)
    cx = (b3[0] + b3[2]) // 2
    cy = (b3[1] + b3[3]) // 2
    w2 = (b3[2] - b3[0]) // 2
    h2 = (b3[3] - b3[1]) // 2
    draw.polygon([(cx, cy - h2), (cx + w2, cy), (cx, cy + h2), (cx - w2, cy)], fill=C_WHITE, outline=C_BLACK, width=4)
    draw.text((cx - 150, cy - 30), "Kiểm tra Cloud:\nCó API Key & Mạng OK?", fill=C_BLACK, font=F_TEXT_BOLD)

    # Arrow 2 -> Decision
    draw.line([(1200, 450), (1200, 620)], fill=C_BLACK, width=3)
    draw_arrow(draw, (1200, 620), (1050, 620), fill=C_BLACK, width=3)

    # Box 4: Gemini Cloud (Layer 1)
    b4 = (80, 800, 750, 1100)
    draw_box(draw, b4, fill=C_WHITE, outline=C_BLACK, width=4, radius=10)
    draw.text((110, 825), "LỚP 1: CLOUD LLM (GEMINI)", fill=C_BLACK, font=F_HEADER)
    draw.line([(80, 880), (750, 880)], fill=C_BLACK, width=2)
    draw.text((110, 900), "• Mô hình Google Gemini 1.5 Flash\n• Markdown Table Output cấu trúc chuẩn\n• Suy luận sâu, phân tích hành văn tự nhiên\n• Đề xuất khuyến nghị thông minh", fill=C_DARK, font=F_TEXT)

    # Box 5: Local Rule Engine (Layer 2)
    b5 = (850, 800, 1520, 1100)
    draw_box(draw, b5, fill=C_WHITE, outline=C_BLACK, width=4, radius=10)
    draw.text((880, 825), "LỚP 2: LOCAL RULE ENGINE", fill=C_BLACK, font=F_HEADER)
    draw.line([(850, 880), (1520, 880)], fill=C_BLACK, width=2)
    draw.text((880, 900), "• Hoạt động Offline 100% không cần Internet\n• Công thức: Burn-rate = Tồn / Vận tốc xuất\n• Phát hiện dị biệt qua độ lệch chuẩn Z-score\n• Khớp từ khóa NLP chính xác, không chia 0", fill=C_DARK, font=F_TEXT)

    # Arrows Decision -> Layers
    draw_arrow(draw, (650, 670), (415, 800), fill=C_BLACK, width=4, label="Có [Cloud OK]", label_offset=(-180, -20))
    draw_arrow(draw, (950, 670), (1185, 800), fill=C_BLACK, width=4, label="Mất mạng / Hết Quota [Fallback]", is_dashed=True, label_offset=(15, -20))

    # Box 6: Output Formatter & Smart UI
    b6 = (80, 1200, 1520, 1850)
    draw_box(draw, b6, fill=C_WHITE, outline=C_BLACK, width=4, radius=12)
    draw.rectangle([80, 1200, 1520, 1275], fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
    draw.text((110, 1225), "3. STRUCTURED OUTPUT & SMART UI COMPONENT (DÙNG CHUNG CẢ 2 LỚP)", fill=C_BLACK, font=F_HEADER)

    out_items = [
        ("Bảng Dữ Liệu Tailwind UI", "Render bảng trực quan với định dạng chuẩn Markdown, hiển thị rõ số liệu"),
        ("Đèn LED Cảnh Báo Trực Quan", "Huy hiệu trạng thái: Đỏ (Cạn tồn khẩn) - Vàng (Cảnh báo) - Xanh (An toàn)"),
        ("Nút Hành Động Nhanh (Quick Action)", "Cho phép tạo tức thời phiếu nhập kho cho mặt hàng thiếu hụt chỉ với 1 click"),
        ("Tab Snapshot Dữ Liệu Thật", "Cung cấp JSON CSDL gốc chứng minh tính minh bạch, không bịa đặt số liệu"),
    ]
    y_out = 1300
    for it_title, it_desc in out_items:
        draw_box(draw, (110, y_out, 1490, y_out + 110), fill=C_WHITE, outline=C_BLACK, width=2, radius=8)
        draw.text((130, y_out + 20), f"• {it_title}:", fill=C_BLACK, font=F_TEXT_BOLD)
        draw.text((130, y_out + 62), it_desc, fill=C_DARK, font=F_TEXT)
        y_out += 135

    # Return Arrows from Layers to Box 6
    draw_arrow(draw, (415, 1100), (415, 1200), fill=C_BLACK, width=4, label="Kết quả LLM")
    draw_arrow(draw, (1185, 1100), (1185, 1200), fill=C_BLACK, width=4, label="Kết quả Rule Engine")

    draw_footer(draw, W, H)
    out_png = os.path.join(DIAGRAM_DIR, "07_so_do_pipeline_ai_fallback.png")
    im.save(out_png, dpi=(300, 300))
    shutil.copy2(out_png, os.path.join(LATEX_IMG_DIR, "07_so_do_pipeline_ai_fallback.png"))
    print("Generated (B&W Large 300 DPI): 07_so_do_pipeline_ai_fallback.png")

# =========================================================================
# 8. SƠ ĐỒ TUẦN TỰ TRỢ LÝ HỎI ĐÁP AI
# =========================================================================
def make_ai_qa_sequence_diagram():
    W, H = 1600, 1950
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ TUẦN TỰ TRỢ LÝ HỎI ĐÁP KHO AI (NLP ASSISTANT SEQUENCE)",
                "Quy trình xử lý: Thu thập Ground Truth CSDL, suy luận ngữ cảnh 2 lớp và hiển thị Smart UI")

    lifelines = [
        ("Người dùng", 130),
        ("AI Chat Console", 420),
        ("POST /api/ai/ask", 720),
        ("Data Aggregator", 1020),
        ("AI Dual Engine", 1300),
        ("Smart Table Viewer", 1520),
    ]

    for title, x in lifelines:
        draw_box(draw, (x - 85, 170, x + 85, 240), fill=C_WHITE, outline=C_BLACK, width=3, radius=8)
        draw.text((x - 70, 190), title, fill=C_BLACK, font=F_TEXT_BOLD)
        draw_dashed_line(draw, (x, 250), (x, 1860), fill=C_BLACK, width=3, dash_len=18, gap_len=12)

    msgs = [
        (130, 420, 310, "1. Nhập câu hỏi: 'Kho còn bao nhiêu bàn phím cơ AKKO?'", False),
        (420, 720, 430, "2. Gửi request HTTP: { question: '...', user_token: '...' }", False),
        (720, 1020, 550, "3. Trích xuất CSDL: products, inventory_items, vận tốc 30 ngày", False),
        (1020, 720, 670, "4. Trả về dữ liệu gốc 100% chính xác (Ground-Truth Snapshot)", True),
        (720, 1300, 790, "5. answer_user_question(question, data_context)", False),
        (1300, 1300, 910, "6. [Gemini / Rule Engine]: Khớp SKU, tính tồn, định dạng bảng", False),
        (1300, 720, 1030, "7. Trả về nội dung trả lời Markdown + data_snapshot JSON", True),
        (720, 420, 1150, "8. Trả kết quả HTTP 200 OK kèm payload hoàn chỉnh", True),
        (420, 1520, 1270, "9. SmartMarkdownViewer parse bảng Markdown thành React Component", False),
        (1520, 420, 1390, "10. Render giao diện đẹp mắt (Badges, LED, Nút bấm nhanh)", True),
        (420, 130, 1510, "11. Người dùng nhận câu trả lời trực quan & xem số liệu minh chứng", True),
    ]

    for x1, x2, y, text, is_ret in msgs:
        draw_arrow(draw, (x1, y), (x2, y), fill=C_BLACK, width=3, is_dashed=is_ret)
        mx = min(x1, x2) + 20
        draw.text((mx, y - 34), text, fill=C_BLACK, font=F_TEXT_BOLD if not is_ret else F_TEXT)

    draw_footer(draw, W, H)
    out_png = os.path.join(DIAGRAM_DIR, "08_so_do_tuan_tu_hoi_dap_ai.png")
    im.save(out_png, dpi=(300, 300))
    shutil.copy2(out_png, os.path.join(LATEX_IMG_DIR, "08_so_do_tuan_tu_hoi_dap_ai.png"))
    print("Generated (B&W Large 300 DPI): 08_so_do_tuan_tu_hoi_dap_ai.png")

# =========================================================================
# 9. LƯU ĐỒ THUẬT TOÁN BẤT THƯỜNG & BURN-RATE
# =========================================================================
def make_algorithm_flowchart():
    W, H = 1600, 2050
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "LƯU ĐỒ THUẬT TOÁN PHÁT HIỆN BẤT THƯỜNG & TÍNH BURN-RATE",
                "Mô hình tính toán: Vận tốc tiêu thụ, số ngày cạn tồn và phát hiện dị biệt (Z-score Outlier)")

    nodes = [
        ("Thu thập dữ liệu giao dịch xuất kho 30 ngày gần nhất (T = 30 ngày)", (300, 180, 1300, 275), False),
        ("Tính tốc độ xuất bình quân ngày: V = Tổng xuất / 30", (350, 330, 1250, 425), False),
        ("V > 0 (Sản phẩm có phát sinh xuất kho trong 30 ngày)?", (320, 480, 1280, 610), True), # Decision 1
        ("Tính số ngày cạn tồn dự báo: DepletionDays = Stock / V", (350, 680, 1250, 775), False),
        ("Days <= 7 ngày hoặc Stock < min_threshold?", (320, 830, 1280, 960), True), # Decision 2
        ("Kích hoạt cảnh báo khẩn: 'Cần lập kế hoạch nhập hàng ngay'", (350, 1030, 1250, 1125), False),
        ("Tính độ lệch chuẩn sản lượng xuất ngày: Z-score", (350, 1180, 1250, 1275), False),
        ("|Z-score| > 2.5 (Xuất kho đột biến hoặc tồn kho đóng băng)?", (300, 1330, 1300, 1460), True), # Decision 3
        ("Gắn cờ Bất thường (Anomaly Flag) & Đề xuất rà soát kiểm kê", (300, 1530, 1300, 1625), False),
        ("Kết thúc: Lưu kết quả phân tích vào bộ nhớ tạm & CSDL", (350, 1680, 1250, 1775), False),
    ]

    for title, bbox, is_decision in nodes:
        if is_decision:
            cx = (bbox[0] + bbox[2]) // 2
            cy = (bbox[1] + bbox[3]) // 2
            w2 = (bbox[2] - bbox[0]) // 2
            h2 = (bbox[3] - bbox[1]) // 2
            draw.polygon([(cx, cy - h2), (cx + w2, cy), (cx, cy + h2), (cx - w2, cy)], fill=C_WHITE, outline=C_BLACK, width=3)
            draw.text((bbox[0] + 50, cy - 18), title, fill=C_BLACK, font=F_TEXT_BOLD)
        else:
            draw_box(draw, bbox, fill=C_WHITE, outline=C_BLACK, width=3, radius=10)
            draw.text((bbox[0] + 30, bbox[1] + 30), title, fill=C_BLACK, font=F_TEXT_BOLD)

    # Zero Velocity Box
    zero_v = (1330, 500, 1580, 590)
    draw_box(draw, zero_v, fill=C_WHITE, outline=C_BLACK, width=3, radius=8)
    draw.text((zero_v[0] + 16, zero_v[1] + 16), "Gán Days = 999\n(Tồn kho ổn định)", fill=C_BLACK, font=F_TEXT_BOLD)

    # Connections
    draw_arrow(draw, (800, 275), (800, 330), fill=C_BLACK, width=3)
    draw_arrow(draw, (800, 425), (800, 480), fill=C_BLACK, width=3)

    # Decision 1
    draw_arrow(draw, (800, 610), (800, 680), fill=C_BLACK, width=3, label="Có xuất [Yes]", label_offset=(15, -20))
    draw_arrow(draw, (1280, 545), (1330, 545), fill=C_BLACK, width=3, label="V = 0 [No]", is_dashed=True, label_offset=(10, -22))
    draw_dashed_line(draw, (1455, 590), (1455, 1227), fill=C_BLACK, width=3)
    draw_arrow(draw, (1455, 1227), (1250, 1227), fill=C_BLACK, width=3, is_dashed=True)

    draw_arrow(draw, (800, 775), (800, 830), fill=C_BLACK, width=3)

    # Decision 2
    draw_arrow(draw, (800, 960), (800, 1030), fill=C_BLACK, width=3, label="Cạn tồn [Yes]", label_offset=(15, -20))
    draw_arrow(draw, (800, 1125), (800, 1180), fill=C_BLACK, width=3)
    # Bypass Decision 2
    draw.line([(320, 895), (200, 895)], fill=C_BLACK, width=3)
    draw.line([(200, 895), (200, 1227)], fill=C_BLACK, width=3)
    draw_arrow(draw, (200, 1227), (350, 1227), fill=C_BLACK, width=3, label="Tồn an toàn [No]", label_offset=(15, -20))

    draw_arrow(draw, (800, 1275), (800, 1330), fill=C_BLACK, width=3)

    # Decision 3
    draw_arrow(draw, (800, 1460), (800, 1530), fill=C_BLACK, width=3, label="Bất thường [Yes]", label_offset=(15, -20))
    draw_arrow(draw, (800, 1625), (800, 1680), fill=C_BLACK, width=3)
    # Bypass Decision 3
    draw.line([(300, 1395), (200, 1395)], fill=C_BLACK, width=3)
    draw.line([(200, 1395), (200, 1727)], fill=C_BLACK, width=3)
    draw_arrow(draw, (200, 1727), (350, 1727), fill=C_BLACK, width=3, label="Bình thường [No]", label_offset=(15, -20))

    draw_footer(draw, W, H)
    out_png = os.path.join(DIAGRAM_DIR, "09_so_do_phan_tich_bat_thuong.png")
    im.save(out_png, dpi=(300, 300))
    shutil.copy2(out_png, os.path.join(LATEX_IMG_DIR, "09_so_do_phan_tich_bat_thuong.png"))
    print("Generated (B&W Large 300 DPI): 09_so_do_phan_tich_bat_thuong.png")

# =========================================================================
# 10. SƠ ĐỒ ĐIỀU HƯỚNG CẤU TRÚC GIAO DIỆN (SITEMAP)
# =========================================================================
def make_sitemap_diagram():
    W, H = 1600, 1950
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ ĐIỀU HƯỚNG CẤU TRÚC GIAO DIỆN HỆ THỐNG (FRONTEND SITEMAP)",
                "Cấu trúc ứng dụng Web SaaS Single Page Application (React 18 Vite + Tailwind CSS)")

    # Root Box
    draw_box(draw, (550, 180, 1050, 265), fill=C_WHITE, outline=C_BLACK, width=4, radius=10)
    draw.text((580, 205), "HỆ THỐNG QUẢN LÝ KHO AI", fill=C_BLACK, font=F_HEADER)

    sections = [
        ("1. TỔNG QUAN", 160, [
            "Dashboard 6 thẻ chỉ số KPI",
            "Biểu đồ Nhập/Xuất 30 ngày",
            "Cảnh báo hàng sắp cạn kho",
            "Top sản phẩm xuất chạy",
        ]),
        ("2. KHO HÀNG", 480, [
            "Danh mục Sản phẩm & SKU",
            "Tồn theo kệ (Zone/Shelf)",
            "Quản lý Nhà cung cấp & DM",
            "Quản lý Sức chứa vị trí",
        ]),
        ("3. GIAO DỊCH", 800, [
            "Tạo Phiếu Nhập hàng",
            "Tạo Phiếu Xuất hàng",
            "Chi tiết & Duyệt phiếu",
            "In phiếu bàn giao kho",
        ]),
        ("4. AI HUB", 1120, [
            "Dự báo số ngày cạn tồn",
            "Phát hiện bất thường",
            "Trợ lý Hỏi Đáp Kho NLP",
            "Xem Snapshot JSON CSDL",
        ]),
        ("5. BẢO MẬT", 1440, [
            "Quản lý Người dùng",
            "Nhật ký kiểm toán Audit",
            "Cấu hình API Gemini",
            "Đăng xuất an toàn JWT",
        ]),
    ]

    for title, cx, items in sections:
        draw_box(draw, (cx - 140, 350, cx + 140, 430), fill=C_WHITE, outline=C_BLACK, width=3, radius=8)
        draw.text((cx - 115, 370), title, fill=C_BLACK, font=F_TEXT_BOLD)
        draw.line([(800, 265), (cx, 350)], fill=C_BLACK, width=3)

        cy = 480
        for it in items:
            draw_box(draw, (cx - 145, cy, cx + 145, cy + 90), fill=C_WHITE, outline=C_BLACK, width=2, radius=8)
            draw.text((cx - 130, cy + 25), it, fill=C_DARK, font=F_TEXT)
            draw.line([(cx, cy - 20), (cx, cy)], fill=C_BLACK, width=2)
            cy += 130

    draw_footer(draw, W, H)
    out_png = os.path.join(DIAGRAM_DIR, "10_so_do_sitemap_giao_dien.png")
    im.save(out_png, dpi=(300, 300))
    shutil.copy2(out_png, os.path.join(LATEX_IMG_DIR, "10_so_do_sitemap_giao_dien.png"))
    print("Generated (B&W Large 300 DPI): 10_so_do_sitemap_giao_dien.png")

# =========================================================================
# COPY AUTHENTIC FULL-COLOR SCREENSHOTS
# =========================================================================
def copy_ui_screenshots():
    src_dir = os.path.join(BASE_DIR, "report", "LaTeX", "figures")
    screenshot_mappings = [
        ("screenshot_dashboard.png", "11_screenshot_dashboard.png"),
        ("screenshot_products.png", "12_screenshot_products.png"),
        ("screenshot_ai_report.png", "13_screenshot_ai_report.png"),
        ("screenshot_ai_assistant.png", "14_screenshot_ai_assistant.png"),
    ]
    for src_name, dest_name in screenshot_mappings:
        src_path = os.path.join(src_dir, src_name)
        if os.path.exists(src_path):
            dest_diagram = os.path.join(DIAGRAM_DIR, dest_name)
            dest_latex = os.path.join(LATEX_IMG_DIR, dest_name)
            shutil.copy2(src_path, dest_diagram)
            shutil.copy2(src_path, dest_latex)
            print(f"Copied authentic full-color UI screenshot: {dest_name}")

if __name__ == "__main__":
    make_arch_diagram()
    make_usecase_diagram()
    make_erd_diagram()
    make_activity_import_diagram()
    make_activity_export_diagram()
    make_sequence_transaction_diagram()
    make_ai_pipeline_diagram()
    make_ai_qa_sequence_diagram()
    make_algorithm_flowchart()
    make_sitemap_diagram()
    copy_ui_screenshots()
    print("All 10 B&W technical diagrams and 4 authentic color UI screenshots generated successfully!")
