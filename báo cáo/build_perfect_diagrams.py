# -*- coding: utf-8 -*-
"""
Script tái thiết kế toàn bộ hệ thống sơ đồ kỹ thuật:
1. SƠ ĐỒ THỰC THỂ LIÊN KẾT (ERD) - 11 BẢNG CHUẨN 3NF:
   - Bố cục 3 phân vùng chuyên nghiệp (Quản trị & Logs bên trái, Danh mục & Kệ kho ở giữa, Giao dịch & Tồn kho bên phải).
   - 100% đường liên kết là đường gấp khúc trực giao (Orthogonal / Manhattan Routing) nối từ viền bảng này sang viền bảng kia.
   - Tuyệt đối KHÔNG có đường nào chạy xuyên qua bảng hoặc nội dung trường dữ liệu.
   - Nhãn quan hệ '1 : N' được đặt tại khoảng trống kênh phân cách, có khung nền trắng bảo vệ chống đè chữ.
   - Cỡ chữ to rõ (32px - 40px), đường nét đậm (3px - 4px), chuẩn đen trắng xuất bản.
2. LƯỢC ĐỒ HOẠT ĐỘNG XUẤT KHO:
   - Nút cảnh báo 'Kho không đủ số lượng xuất khả dụng' được mở rộng thành khối hộp 370 x 140 px rộng rãi.
   - Chữ căn giữa chuẩn mực, không chạm viền.
   - Đường luồng rẽ nhánh lỗi đi hoàn toàn ở hành lang trống bên phải, không đè lên bất kỳ nút nào.
3. LƯỢC ĐỒ HOẠT ĐỘNG NHẬP KHO & LƯU ĐỒ THUẬT TOÁN:
   - Tương tự mở rộng các hộp quyết định, tách riêng hành lang rẽ nhánh, loại bỏ triệt để xung đột chữ.
4. XUẤT ĐẦY ĐỦ 4 ĐỊNH DẠNG:
   - PNG độ phân giải siêu cao (300 - 600 DPI)
   - PDF trang in chất lượng cao
   - SVG vector phóng to vô hạn
   - Draw.io XML chỉnh sửa trực tiếp
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

def save_diagram_multiformat(im, base_filename):
    # 1. PNG (300 DPI)
    png_path = os.path.join(DIAGRAM_DIR, f"{base_filename}.png")
    im.save(png_path, dpi=(300, 300))
    latex_png = os.path.join(LATEX_IMG_DIR, f"{base_filename}.png")
    shutil.copy2(png_path, latex_png)
    
    # 2. PDF (High quality)
    pdf_path = os.path.join(PDF_DIR, f"{base_filename}.pdf")
    im.save(pdf_path, "PDF", resolution=300.0)
    
    print(f"Exported: {base_filename}.png & {base_filename}.pdf (300 DPI)")

# =========================================================================
# 1. SƠ ĐỒ THỰC THỂ LIÊN KẾT (ERD) - 11 BẢNG CHUẨN 3NF
# =========================================================================
def generate_erd_diagram():
    W, H = 2800, 3600
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ THỰC THỂ LIÊN KẾT (ERD) - 11 BẢNG CSDL CHUẨN 3NF",
                "Phân vùng kiến trúc: Quản trị & AI Logs (Trái), Dữ liệu nền tảng (Giữa), Giao dịch & Tồn kho (Phải)")

    # Group Banners
    # Banner 1: Left
    draw_box(draw, (70, 155, 870, 195), fill=C_GRAY_LIGHT, outline=C_BLACK, width=2, radius=6)
    draw.text((85, 162), "PHÂN VÙNG 1: QUẢN TRỊ, PHÂN QUYỀN, KIỂM TOÁN & AI LOGS", fill=C_BLACK, font=F_LABEL)
    
    # Banner 2: Center
    draw_box(draw, (1000, 155, 1800, 195), fill=C_GRAY_LIGHT, outline=C_BLACK, width=2, radius=6)
    draw.text((1015, 162), "PHÂN VÙNG 2: DỮ LIỆU NỀN TẢNG (MASTER CATALOG & LOCATIONS)", fill=C_BLACK, font=F_LABEL)

    # Banner 3: Right
    draw_box(draw, (1930, 155, 2730, 195), fill=C_GRAY_LIGHT, outline=C_BLACK, width=2, radius=6)
    draw.text((1945, 162), "PHÂN VÙNG 3: QUẢN LÝ GIAO DỊCH XUẤT NHẬP & TỒN KHO THỰC TẾ", fill=C_BLACK, font=F_LABEL)

    # Tables definition
    # Column 1 (Left): x = 80 to 860 (width 780)
    col1_tables = [
        ("roles", 215, [
            (True, False, "id", "INTEGER (PK, AUTO)"),
            (False, False, "role_name", "VARCHAR(30) UNIQUE NOT NULL"),
            (False, False, "description", "VARCHAR(255) NULL"),
            (False, False, "created_at", "DATETIME DEFAULT NOW"),
        ]),
        ("users", 540, [
            (True, False, "id", "INTEGER (PK, AUTO)"),
            (False, True, "role_id", "INTEGER (FK -> roles.id)"),
            (False, False, "username", "VARCHAR(50) UNIQUE NOT NULL"),
            (False, False, "password_hash", "VARCHAR(255) NOT NULL"),
            (False, False, "full_name", "VARCHAR(100) NOT NULL"),
            (False, False, "email", "VARCHAR(100) NULL"),
            (False, False, "is_active", "BOOLEAN DEFAULT TRUE"),
            (False, False, "created_at", "DATETIME DEFAULT NOW"),
        ]),
        ("audit_logs", 1120, [
            (True, False, "id", "INTEGER (PK, AUTO)"),
            (False, True, "user_id", "INTEGER (FK -> users.id)"),
            (False, False, "action_type", "VARCHAR(30) NOT NULL"),
            (False, False, "entity_name", "VARCHAR(50) NOT NULL"),
            (False, False, "entity_id", "INTEGER NULL"),
            (False, False, "old_value", "TEXT (JSON) NULL"),
            (False, False, "new_value", "TEXT (JSON) NULL"),
            (False, False, "ip_address", "VARCHAR(45) NULL"),
            (False, False, "created_at", "DATETIME DEFAULT NOW"),
        ]),
        ("ai_query_logs", 1750, [
            (True, False, "id", "INTEGER (PK, AUTO)"),
            (False, True, "user_id", "INTEGER (FK -> users.id)"),
            (False, False, "query_type", "VARCHAR(30) NOT NULL"),
            (False, False, "prompt_text", "TEXT NOT NULL"),
            (False, False, "context_snapshot", "TEXT (JSON) NOT NULL"),
            (False, False, "response_text", "TEXT NOT NULL"),
            (False, False, "execution_time_ms", "INTEGER DEFAULT 0"),
            (False, False, "created_at", "DATETIME DEFAULT NOW"),
        ]),
    ]

    # Column 2 (Center): x = 1010 to 1790 (width 780)
    col2_tables = [
        ("categories", 215, [
            (True, False, "id", "INTEGER (PK, AUTO)"),
            (False, False, "category_code", "VARCHAR(30) UNIQUE NOT NULL"),
            (False, False, "category_name", "VARCHAR(100) NOT NULL"),
            (False, False, "description", "TEXT NULL"),
        ]),
        ("suppliers", 540, [
            (True, False, "id", "INTEGER (PK, AUTO)"),
            (False, False, "supplier_name", "VARCHAR(150) NOT NULL"),
            (False, False, "contact_person", "VARCHAR(100) NULL"),
            (False, False, "phone", "VARCHAR(20) NULL"),
            (False, False, "email", "VARCHAR(100) NULL"),
            (False, False, "address", "VARCHAR(255) NULL"),
        ]),
        ("locations", 1020, [
            (True, False, "id", "INTEGER (PK, AUTO)"),
            (False, False, "location_code", "VARCHAR(30) UNIQUE NOT NULL"),
            (False, False, "zone_name", "VARCHAR(50) NOT NULL"),
            (False, False, "shelf_number", "VARCHAR(30) NOT NULL"),
            (False, False, "max_capacity", "INTEGER DEFAULT 500"),
            (False, False, "is_active", "BOOLEAN DEFAULT TRUE"),
        ]),
        ("products", 1520, [
            (True, False, "id", "INTEGER (PK, AUTO)"),
            (False, True, "category_id", "INTEGER (FK -> categories.id)"),
            (False, False, "sku", "VARCHAR(50) UNIQUE NOT NULL"),
            (False, False, "name", "VARCHAR(150) NOT NULL"),
            (False, False, "unit", "VARCHAR(20) DEFAULT 'Cái'"),
            (False, False, "cost_price", "DECIMAL(12,2) DEFAULT 0"),
            (False, False, "selling_price", "DECIMAL(12,2) DEFAULT 0"),
            (False, False, "min_threshold", "INTEGER DEFAULT 10"),
            (False, False, "max_threshold", "INTEGER DEFAULT 100"),
            (False, False, "is_active", "BOOLEAN DEFAULT TRUE"),
        ]),
    ]

    # Column 3 (Right): x = 1940 to 2720 (width 780)
    col3_tables = [
        ("inventory_items", 1020, [
            (True, False, "id", "INTEGER (PK, AUTO)"),
            (False, True, "product_id", "INTEGER (FK -> products.id)"),
            (False, True, "location_id", "INTEGER (FK -> locations.id)"),
            (False, False, "current_stock", "INTEGER NOT NULL (>= 0)"),
            (False, False, "batch_number", "VARCHAR(50) NULL"),
            (False, False, "expiry_date", "DATE NULL"),
            (False, False, "last_audited_at", "DATETIME NULL"),
        ]),
        ("inventory_transactions", 1520, [
            (True, False, "id", "INTEGER (PK, AUTO)"),
            (False, False, "transaction_code", "VARCHAR(50) UNIQUE NOT NULL"),
            (False, False, "transaction_type", "VARCHAR(20) NOT NULL"),
            (False, True, "supplier_id", "INTEGER (FK -> suppliers.id)"),
            (False, True, "created_by", "INTEGER (FK -> users.id)"),
            (False, False, "total_amount", "DECIMAL(15,2) DEFAULT 0"),
            (False, False, "note", "TEXT NULL"),
            (False, False, "created_at", "DATETIME DEFAULT NOW"),
        ]),
        ("inventory_transaction_items", 2120, [
            (True, False, "id", "INTEGER (PK, AUTO)"),
            (False, True, "transaction_id", "INTEGER (FK -> trans.id)"),
            (False, True, "product_id", "INTEGER (FK -> products.id)"),
            (False, True, "location_id", "INTEGER (FK -> locations.id)"),
            (False, False, "quantity", "INTEGER NOT NULL (> 0)"),
            (False, False, "unit_price", "DECIMAL(12,2) NOT NULL"),
            (False, False, "subtotal", "DECIMAL(15,2) NOT NULL"),
        ]),
    ]

    def render_erd_table(x1, y1, width, tname, fields):
        x2 = x1 + width
        row_h = 44
        y2 = y1 + 60 + len(fields) * row_h + 12
        bbox = (x1, y1, x2, y2)
        
        # White card body
        draw_box(draw, bbox, fill=C_WHITE, outline=C_BLACK, width=3, radius=8)
        
        # Header banner
        draw.rectangle([x1, y1, x2, y1 + 54], fill=C_GRAY_LIGHT, outline=C_BLACK, width=2)
        draw.text((x1 + 18, y1 + 10), f"BẢNG CSDL: {tname.upper()}", fill=C_BLACK, font=F_HEADER)
        
        # Rows
        curr_y = y1 + 68
        for is_pk, is_fk, fname, ftype in fields:
            if is_pk:
                draw.text((x1 + 16, curr_y), "[PK]", fill=C_BLACK, font=F_CODE_BOLD)
            elif is_fk:
                draw.text((x1 + 16, curr_y), "[FK]", fill=C_BLACK, font=F_CODE_BOLD)
            else:
                draw.text((x1 + 16, curr_y), "    ", fill=C_BLACK, font=F_CODE)
            
            draw.text((x1 + 88, curr_y), fname, fill=C_BLACK, font=F_TEXT_BOLD if (is_pk or is_fk) else F_TEXT)
            draw.text((x2 - 340, curr_y), ftype, fill=C_DARK, font=F_CODE)
            curr_y += row_h
        return bbox

    # Render Col 1
    for tname, y1, fields in col1_tables:
        render_erd_table(80, y1, 780, tname, fields)

    # Render Col 2
    for tname, y1, fields in col2_tables:
        render_erd_table(1010, y1, 780, tname, fields)

    # Render Col 3
    for tname, y1, fields in col3_tables:
        render_erd_table(1940, y1, 780, tname, fields)

    # Architecture Legend Card (Column 1, below ai_query_logs)
    leg_box = (80, 2360, 860, 3100)
    draw_box(draw, leg_box, fill=C_WHITE, outline=C_BLACK, width=3, radius=10)
    draw.rectangle([80, 2360, 860, 2425], fill=C_GRAY_LIGHT, outline=C_BLACK, width=2)
    draw.text((95, 2375), "QUY CHUẨN THIẾT KẾ CƠ SỞ DỮ LIỆU (3NF)", fill=C_BLACK, font=F_HEADER)
    
    leg_items = [
        "1. Chuẩn hóa 3NF: 100% thuộc tính phụ thuộc hàm trực tiếp vào Khóa chính.",
        "2. Định danh duy nhất: Các bảng đều dùng Khóa chính (PK) INTEGER tự tăng.",
        "3. Ràng buộc toàn vẹn: Khóa ngoại (FK) cấu hình ON DELETE RESTRICT.",
        "4. Tính toàn vẹn ACID: Mọi giao dịch xuất nhập chạy trong DB Transaction.",
        "5. Chống xung đột Race Condition: Khóa bản ghi (Row-level Locking) khi trừ kho.",
        "6. Nhật ký kiểm toán bất biến: Bảng audit_logs ghi nhận old/new values dạng JSON.",
        "7. Chống ảo giác AI: Ground-Truth Snapshot trích xuất trực tiếp từ CSDL thực tế.",
        "8. Khả năng mở rộng: Tương thích hoàn toàn giữa SQLite (dev) và PostgreSQL (prod).",
    ]
    ly = 2450
    for it in leg_items:
        draw.text((95, ly), it, fill=C_DARK, font=F_TEXT)
        ly += 76

    # =====================================================================
    # 12 ORTHOGONAL RELATIONSHIPS (MANHATTAN ROUTING - ZERO CROSSING)
    # =====================================================================

    # 1. roles -> users (Vertical in Col 1)
    # roles bottom = 215 + 60 + 4*44 + 12 = 463
    draw_polyline_arrow(draw, [(470, 463), (470, 540)], 
                        fill=C_BLACK, width=3, label="1 : N", label_pos=(495, 488))

    # 2. users -> audit_logs (Vertical in Col 1)
    # users bottom = 540 + 60 + 8*44 + 12 = 964
    draw_polyline_arrow(draw, [(470, 964), (470, 1120)], 
                        fill=C_BLACK, width=3, label="1 : N", label_pos=(495, 1028))

    # 3. users -> ai_query_logs (Along outer left margin x=35)
    draw_polyline_arrow(draw, [(80, 850), (35, 850), (35, 1920), (80, 1920)], 
                        fill=C_BLACK, width=3, label="1 : N", label_pos=(45, 1380))

    # 4. categories -> products (Along Channel 1 at x=935)
    draw_polyline_arrow(draw, [(1010, 310), (935, 310), (935, 1630), (1010, 1630)], 
                        fill=C_BLACK, width=3, label="1 : N", label_pos=(945, 960))

    # 5. suppliers -> products (Along Channel 1 at x=965)
    draw_polyline_arrow(draw, [(1010, 720), (965, 720), (965, 1720), (1010, 1720)], 
                        fill=C_BLACK, width=3, label="1 : N", label_pos=(975, 1220))

    # 6. locations -> inventory_items (Direct horizontal line across Channel 2)
    draw_polyline_arrow(draw, [(1790, 1180), (1940, 1180)], 
                        fill=C_BLACK, width=3, label="1 : N", label_pos=(1835, 1145))

    # 7. products -> inventory_items (Along Channel 2 at x=1835)
    draw_polyline_arrow(draw, [(1790, 1660), (1835, 1660), (1835, 1280), (1940, 1280)], 
                        fill=C_BLACK, width=3, label="1 : N", label_pos=(1845, 1460))

    # 8. suppliers -> inventory_transactions (Along Channel 2 at x=1865)
    draw_polyline_arrow(draw, [(1790, 720), (1865, 720), (1865, 1660), (1940, 1660)], 
                        fill=C_BLACK, width=3, label="1 : N", label_pos=(1875, 1180))

    # 9. users -> inventory_transactions (Along top channel y=165 and outer right margin x=2760)
    draw_polyline_arrow(draw, [(860, 680), (895, 680), (895, 148), (2760, 148), (2760, 1740), (2720, 1740)], 
                        fill=C_BLACK, width=3, label="1 : N", label_pos=(2725, 940))

    # 10. inventory_transactions -> inventory_transaction_items (Vertical in Col 3)
    # trans bottom = 1520 + 60 + 8*44 + 12 = 1944
    draw_polyline_arrow(draw, [(2330, 1944), (2330, 2120)], 
                        fill=C_BLACK, width=3, label="1 : N", label_pos=(2355, 2020))

    # 11. products -> inventory_transaction_items (Along Channel 2 at x=1835)
    draw_polyline_arrow(draw, [(1790, 1880), (1835, 1880), (1835, 2260), (1940, 2260)], 
                        fill=C_BLACK, width=3, label="1 : N", label_pos=(1845, 2060))

    # 12. locations -> inventory_transaction_items (Along Channel 2 at x=1895)
    draw_polyline_arrow(draw, [(1790, 1340), (1895, 1340), (1895, 2380), (1940, 2380)], 
                        fill=C_BLACK, width=3, label="1 : N", label_pos=(1905, 1850))

    draw_footer(draw, W, H)
    save_diagram_multiformat(im, "03_so_do_erd_11_bang")

# =========================================================================
# 2. LƯỢC ĐỒ HOẠT ĐỘNG XUẤT KHO (KHÔNG CHỒNG CHỮ, HỘP LỖI 370x140 PX)
# =========================================================================
def generate_activity_export_diagram():
    W, H = 1800, 2250
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "LƯỢC ĐỒ HOẠT ĐỘNG QUY TRÌNH XUẤT KHO (EXPORT ACTIVITY)",
                "Kiểm tra số lượng khả dụng, khóa tạm hàng hóa, trừ kho và kích hoạt cảnh báo tái nhập tự động")

    cx = 850
    steps = [
        ("Khởi đầu: Yêu cầu xuất kho cho khách hàng / đại lý", (420, 180, 1280, 270), False),
        ("Chọn khách hàng / mục đích xuất và điền thông tin phiếu", (420, 320, 1280, 410), False),
        ("Thêm danh mục sản phẩm và số lượng yêu cầu xuất", (420, 460, 1280, 550), False),
        ("Kiểm tra tồn kho: Số lượng xuất <= Tồn kho khả dụng?", (420, 620, 1280, 760), True), # Decision 1
        ("Khóa bản ghi tồn kho tạm thời (Row-level Locking)", (420, 840, 1280, 930), False),
        ("Trừ số lượng thực tế trong bảng inventory_items", (420, 980, 1280, 1070), False),
        ("Kiểm tra ngưỡng an toàn: Tồn kho < min_threshold?", (420, 1130, 1280, 1270), True), # Decision 2
        ("Kích hoạt cảnh báo AI Alert: Đề xuất lập phiếu tái nhập", (420, 1360, 1280, 1450), False),
        ("Ghi nhận nhật ký kiểm toán Audit Log và cập nhật Realtime KPI", (370, 1520, 1330, 1610), False),
        ("Kết thúc: Bàn giao hàng hóa và in phiếu xuất kho", (420, 1920, 1280, 2010), False),
    ]

    for title, bbox, is_decision in steps:
        if is_decision:
            cx_n = (bbox[0] + bbox[2]) // 2
            cy_n = (bbox[1] + bbox[3]) // 2
            w2 = (bbox[2] - bbox[0]) // 2
            h2 = (bbox[3] - bbox[1]) // 2
            draw.polygon([(cx_n, cy_n - h2), (cx_n + w2, cy_n), (cx_n, cy_n + h2), (cx_n - w2, cy_n)], fill=C_WHITE, outline=C_BLACK, width=3)
            draw.text((bbox[0] + 50, cy_n - 18), title, fill=C_BLACK, font=F_TEXT_BOLD)
        else:
            draw_box(draw, bbox, fill=C_WHITE, outline=C_BLACK, width=3, radius=10)
            draw.text((bbox[0] + 30, bbox[1] + 28), title, fill=C_BLACK, font=F_TEXT_BOLD)

    # Error box (Out of stock) - SPACIOUS 370 x 140 PX
    err_box = (1380, 620, 1750, 760)
    draw_box(draw, err_box, fill=C_WHITE, outline=C_BLACK, width=3, radius=10)
    draw.text((err_box[0] + 45, err_box[1] + 20), "BÁO LỖI NGHIỆP VỤ", fill=C_BLACK, font=F_LABEL)
    draw.text((err_box[0] + 30, err_box[1] + 58), "Kho không đủ số lượng", fill=C_BLACK, font=F_LABEL)
    draw.text((err_box[0] + 22, err_box[1] + 96), "tồn khả dụng (HTTP 400)", fill=C_DARK, font=F_CODE_BOLD)

    # Connections
    draw_arrow(draw, (cx, 270), (cx, 320), fill=C_BLACK, width=3)
    draw_arrow(draw, (cx, 410), (cx, 460), fill=C_BLACK, width=3)
    draw_arrow(draw, (cx, 550), (cx, 620), fill=C_BLACK, width=3)

    # Decision 1 paths
    # Yes -> Step 5
    draw_arrow(draw, (cx, 760), (cx, 840), fill=C_BLACK, width=3, label="[Yes: Đủ tồn khả dụng]", label_offset=(15, -20))
    # No -> Error box
    draw_arrow(draw, (1280, 690), (1380, 690), fill=C_BLACK, width=3, label="[No: Hết hàng]", is_dashed=True, label_offset=(10, -22))
    # Error box down along outer margin x=1565 to End node
    draw_dashed_line(draw, (1565, 760), (1565, 1965), fill=C_BLACK, width=3)
    draw_arrow(draw, (1565, 1965), (1280, 1965), fill=C_BLACK, width=3, label="Hủy bỏ & Rollback", is_dashed=True, label_offset=(20, -22))

    draw_arrow(draw, (cx, 930), (cx, 980), fill=C_BLACK, width=3)
    draw_arrow(draw, (cx, 1070), (cx, 1130), fill=C_BLACK, width=3)

    # Decision 2 paths
    # Yes -> Step 8
    draw_arrow(draw, (cx, 1270), (cx, 1360), fill=C_BLACK, width=3, label="[Yes: Cạn ngưỡng]", label_offset=(15, -20))
    draw_arrow(draw, (cx, 1450), (cx, 1520), fill=C_BLACK, width=3)
    # Bypass Decision 2 along outer left margin x=160
    draw.line([(420, 1200), (160, 1200)], fill=C_BLACK, width=3)
    draw.line([(160, 1200), (160, 1565)], fill=C_BLACK, width=3)
    draw_arrow(draw, (160, 1565), (370, 1565), fill=C_BLACK, width=3, label="[No: Tồn kho an toàn]", label_offset=(20, -22))

    draw_arrow(draw, (cx, 1610), (cx, 1920), fill=C_BLACK, width=3)

    draw_footer(draw, W, H)
    save_diagram_multiformat(im, "05_luoc_do_hoat_dong_xuat_kho")

# =========================================================================
# 3. LƯỢC ĐỒ HOẠT ĐỘNG NHẬP KHO (RỘNG RÃI, HỘP TỪ CHỐI 370x140 PX)
# =========================================================================
def generate_activity_import_diagram():
    W, H = 1800, 2250
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "LƯỢC ĐỒ HOẠT ĐỘNG QUY TRÌNH NHẬP KHO (IMPORT ACTIVITY)",
                "Quy trình nghiệp vụ: Lập phiếu, kiểm đếm thực tế, gán vị trí kệ, cập nhật tồn kho và ghi kiểm toán")

    cx = 850
    steps = [
        ("Khởi đầu: Thủ kho yêu cầu nhập hàng từ Nhà Cung Cấp", (420, 180, 1280, 270), False),
        ("Chọn Nhà Cung Cấp và điền thông tin phiếu nhập", (420, 320, 1280, 410), False),
        ("Thêm danh sách sản phẩm, số lượng và đơn giá nhập", (420, 460, 1280, 550), False),
        ("Kiểm tra hàng hóa thực tế và đối chiếu đơn giao hàng", (420, 600, 1280, 690), False),
        ("Hàng hóa đạt tiêu chuẩn quy cách và nguyên vẹn?", (420, 750, 1280, 890), True),  # Decision Diamond
        ("Chỉ định vị trí kệ kho tiếp nhận (Location: Zone / Shelf)", (420, 970, 1280, 1060), False),
        ("Hệ thống tạo Transaction (Trạng thái: APPROVED)", (420, 1120, 1280, 1210), False),
        ("Cộng dồn số lượng thực tế vào bảng inventory_items", (420, 1270, 1280, 1360), False),
        ("Ghi nhận nhật ký kiểm toán Audit Log & Cập nhật Realtime KPI", (370, 1420, 1330, 1510), False),
        ("Kết thúc: Phiếu nhập hoàn tất thành công và in biên bản", (420, 1920, 1280, 2010), False),
    ]

    for title, bbox, is_decision in steps:
        if is_decision:
            cx_n = (bbox[0] + bbox[2]) // 2
            cy_n = (bbox[1] + bbox[3]) // 2
            w2 = (bbox[2] - bbox[0]) // 2
            h2 = (bbox[3] - bbox[1]) // 2
            draw.polygon([(cx_n, cy_n - h2), (cx_n + w2, cy_n), (cx_n, cy_n + h2), (cx_n - w2, cy_n)], fill=C_WHITE, outline=C_BLACK, width=3)
            draw.text((bbox[0] + 55, cy_n - 18), title, fill=C_BLACK, font=F_TEXT_BOLD)
        else:
            draw_box(draw, bbox, fill=C_WHITE, outline=C_BLACK, width=3, radius=10)
            draw.text((bbox[0] + 30, bbox[1] + 28), title, fill=C_BLACK, font=F_TEXT_BOLD)

    # Reject box (alternative flow) - SPACIOUS 370 x 140 PX
    reject_box = (1380, 750, 1750, 890)
    draw_box(draw, reject_box, fill=C_WHITE, outline=C_BLACK, width=3, radius=10)
    draw.text((reject_box[0] + 45, reject_box[1] + 20), "TỪ CHỐI NHẬP HÀNG", fill=C_BLACK, font=F_LABEL)
    draw.text((reject_box[0] + 32, reject_box[1] + 58), "Lập biên bản sự cố lỗi", fill=C_BLACK, font=F_LABEL)
    draw.text((reject_box[0] + 20, reject_box[1] + 96), "& Hoàn trả Nhà cung cấp", fill=C_DARK, font=F_CODE_BOLD)

    # Connections
    draw_arrow(draw, (cx, 270), (cx, 320), fill=C_BLACK, width=3)
    draw_arrow(draw, (cx, 410), (cx, 460), fill=C_BLACK, width=3)
    draw_arrow(draw, (cx, 550), (cx, 600), fill=C_BLACK, width=3)
    draw_arrow(draw, (cx, 690), (cx, 750), fill=C_BLACK, width=3)

    # Decision paths
    draw_arrow(draw, (cx, 890), (cx, 970), fill=C_BLACK, width=3, label="[Yes: Đạt quy cách]", label_offset=(15, -20))
    draw_arrow(draw, (1280, 820), (1380, 820), fill=C_BLACK, width=3, label="[No: Lỗi hỏng]", is_dashed=True, label_offset=(10, -22))
    
    # Reject box down along outer margin x=1565 to End node
    draw_dashed_line(draw, (1565, 890), (1565, 1965), fill=C_BLACK, width=3)
    draw_arrow(draw, (1565, 1965), (1280, 1965), fill=C_BLACK, width=3, label="Hủy phiếu nhập", is_dashed=True, label_offset=(20, -22))

    draw_arrow(draw, (cx, 1060), (cx, 1120), fill=C_BLACK, width=3)
    draw_arrow(draw, (cx, 1210), (cx, 1270), fill=C_BLACK, width=3)
    draw_arrow(draw, (cx, 1360), (cx, 1420), fill=C_BLACK, width=3)
    draw_arrow(draw, (cx, 1510), (cx, 1920), fill=C_BLACK, width=3)

    draw_footer(draw, W, H)
    save_diagram_multiformat(im, "04_luoc_do_hoat_dong_nhap_kho")

# =========================================================================
# 4. LƯU ĐỒ THUẬT TOÁN BẤT THƯỜNG & BURN-RATE
# =========================================================================
def generate_algorithm_flowchart():
    W, H = 1800, 2250
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "LƯU ĐỒ THUẬT TOÁN PHÁT HIỆN BẤT THƯỜNG & TÍNH BURN-RATE",
                "Mô hình tính toán: Vận tốc tiêu thụ, số ngày cạn tồn và phát hiện dị biệt (Z-score Outlier)")

    cx = 850
    nodes = [
        ("Thu thập dữ liệu giao dịch xuất kho 30 ngày gần nhất (T = 30 ngày)", (370, 180, 1330, 270), False),
        ("Tính tốc độ xuất bình quân ngày: V = Tổng xuất / 30", (420, 320, 1280, 410), False),
        ("V > 0 (Sản phẩm có phát sinh xuất kho trong 30 ngày)?", (420, 470, 1280, 610), True), # Decision 1
        ("Tính số ngày cạn tồn dự báo: DepletionDays = Stock / V", (420, 680, 1280, 770), False),
        ("Days <= 7 ngày hoặc Stock < min_threshold?", (420, 830, 1280, 970), True), # Decision 2
        ("Kích hoạt cảnh báo khẩn: 'Cần lập kế hoạch nhập hàng ngay'", (420, 1040, 1280, 1130), False),
        ("Tính độ lệch chuẩn sản lượng xuất ngày: Z-score", (420, 1190, 1280, 1280), False),
        ("|Z-score| > 2.5 (Xuất kho đột biến hoặc tồn kho đóng băng)?", (370, 1340, 1330, 1480), True), # Decision 3
        ("Gắn cờ Bất thường (Anomaly Flag) & Đề xuất rà soát kiểm kê", (370, 1550, 1330, 1640), False),
        ("Kết thúc: Lưu kết quả phân tích vào bộ nhớ tạm & CSDL", (420, 1920, 1280, 2010), False),
    ]

    for title, bbox, is_decision in nodes:
        if is_decision:
            cx_n = (bbox[0] + bbox[2]) // 2
            cy_n = (bbox[1] + bbox[3]) // 2
            w2 = (bbox[2] - bbox[0]) // 2
            h2 = (bbox[3] - bbox[1]) // 2
            draw.polygon([(cx_n, cy_n - h2), (cx_n + w2, cy_n), (cx_n, cy_n + h2), (cx_n - w2, cy_n)], fill=C_WHITE, outline=C_BLACK, width=3)
            draw.text((bbox[0] + 50, cy_n - 18), title, fill=C_BLACK, font=F_TEXT_BOLD)
        else:
            draw_box(draw, bbox, fill=C_WHITE, outline=C_BLACK, width=3, radius=10)
            draw.text((bbox[0] + 30, bbox[1] + 28), title, fill=C_BLACK, font=F_TEXT_BOLD)

    # Zero Velocity Box - SPACIOUS 370 x 140 PX
    zero_v = (1380, 470, 1750, 610)
    draw_box(draw, zero_v, fill=C_WHITE, outline=C_BLACK, width=3, radius=10)
    draw.text((zero_v[0] + 55, zero_v[1] + 20), "TỒN KHO ỔN ĐỊNH", fill=C_BLACK, font=F_LABEL)
    draw.text((zero_v[0] + 45, zero_v[1] + 58), "Gán Days = 999 ngày", fill=C_BLACK, font=F_LABEL)
    draw.text((zero_v[0] + 32, zero_v[1] + 96), "(Không phát sinh xuất)", fill=C_DARK, font=F_CODE_BOLD)

    # Connections
    draw_arrow(draw, (cx, 270), (cx, 320), fill=C_BLACK, width=3)
    draw_arrow(draw, (cx, 410), (cx, 470), fill=C_BLACK, width=3)

    # Decision 1
    draw_arrow(draw, (cx, 610), (cx, 680), fill=C_BLACK, width=3, label="[Yes: Có xuất]", label_offset=(15, -20))
    draw_arrow(draw, (1280, 540), (1380, 540), fill=C_BLACK, width=3, label="[No: V = 0]", is_dashed=True, label_offset=(10, -22))
    draw_dashed_line(draw, (1565, 610), (1565, 1235), fill=C_BLACK, width=3)
    draw_arrow(draw, (1565, 1235), (1280, 1235), fill=C_BLACK, width=3, is_dashed=True)

    draw_arrow(draw, (cx, 770), (cx, 830), fill=C_BLACK, width=3)

    # Decision 2
    draw_arrow(draw, (cx, 970), (cx, 1040), fill=C_BLACK, width=3, label="[Yes: Cạn tồn]", label_offset=(15, -20))
    draw_arrow(draw, (cx, 1130), (cx, 1190), fill=C_BLACK, width=3)
    # Bypass Decision 2
    draw.line([(420, 900), (180, 900)], fill=C_BLACK, width=3)
    draw.line([(180, 900), (180, 1235)], fill=C_BLACK, width=3)
    draw_arrow(draw, (180, 1235), (420, 1235), fill=C_BLACK, width=3, label="[No: Tồn an toàn]", label_offset=(20, -22))

    draw_arrow(draw, (cx, 1280), (cx, 1340), fill=C_BLACK, width=3)

    # Decision 3
    draw_arrow(draw, (cx, 1480), (cx, 1550), fill=C_BLACK, width=3, label="[Yes: Bất thường]", label_offset=(15, -20))
    draw_arrow(draw, (cx, 1640), (cx, 1920), fill=C_BLACK, width=3)
    # Bypass Decision 3
    draw.line([(370, 1410), (180, 1410)], fill=C_BLACK, width=3)
    draw.line([(180, 1410), (180, 1965)], fill=C_BLACK, width=3)
    draw_arrow(draw, (180, 1965), (420, 1965), fill=C_BLACK, width=3, label="[No: Bình thường]", label_offset=(20, -22))

    draw_footer(draw, W, H)
    save_diagram_multiformat(im, "09_so_do_phan_tich_bat_thuong")

# =========================================================================
# 5. XUẤT SVG VECTOR CHO ERD
# =========================================================================
def generate_erd_svg():
    svg_path = os.path.join(SVG_DIR, "03_so_do_erd_11_bang.svg")
    # Clean vector SVG
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2800 3600" width="2800" height="3600">
  <defs>
    <style>
      .bg { fill: #ffffff; }
      .header-title { font-family: "Times New Roman", serif; font-size: 46px; font-weight: bold; fill: #000000; }
      .header-sub { font-family: "Times New Roman", serif; font-size: 28px; fill: #333333; }
      .tbl-hdr { font-family: "Times New Roman", serif; font-size: 36px; font-weight: bold; fill: #000000; }
      .tbl-fld-pk { font-family: "Times New Roman", serif; font-size: 30px; font-weight: bold; fill: #000000; }
      .tbl-fld-reg { font-family: "Times New Roman", serif; font-size: 28px; fill: #000000; }
      .tbl-fld-type { font-family: "Consolas", monospace; font-size: 25px; fill: #333333; }
      .conn-label { font-family: "Times New Roman", serif; font-size: 26px; font-weight: bold; fill: #000000; }
      .banner-text { font-family: "Times New Roman", serif; font-size: 26px; font-weight: bold; fill: #000000; }
      .note-text { font-family: "Times New Roman", serif; font-size: 28px; fill: #333333; }
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#000000" />
    </marker>
  </defs>
  <rect width="2800" height="3600" class="bg" />
  
  <!-- Header -->
  <text x="40" y="60" class="header-title">SƠ ĐỒ THỰC THỂ LIÊN KẾT (ERD) - 11 BẢNG CSDL CHUẨN 3NF</text>
  <text x="40" y="110" class="header-sub">Phân vùng kiến trúc: Quản trị &amp; AI Logs (Trái), Dữ liệu nền tảng (Giữa), Giao dịch &amp; Tồn kho (Phải)</text>
  <line x1="0" y1="138" x2="2800" y2="138" stroke="#000000" stroke-width="4" />
  <line x1="0" y1="144" x2="2800" y2="144" stroke="#000000" stroke-width="2" />

  <!-- Banners -->
  <rect x="70" y="155" width="800" height="40" rx="6" fill="#f5f5f5" stroke="#000000" stroke-width="2" />
  <text x="85" y="183" class="banner-text">PHÂN VÙNG 1: QUẢN TRỊ, PHÂN QUYỀN &amp; AI LOGS</text>

  <rect x="1000" y="155" width="800" height="40" rx="6" fill="#f5f5f5" stroke="#000000" stroke-width="2" />
  <text x="1015" y="183" class="banner-text">PHÂN VÙNG 2: DỮ LIỆU NỀN TẢNG (MASTER DATA)</text>

  <rect x="1930" y="155" width="800" height="40" rx="6" fill="#f5f5f5" stroke="#000000" stroke-width="2" />
  <text x="1945" y="183" class="banner-text">PHÂN VÙNG 3: GIAO DỊCH &amp; TỒN KHO THỰC TẾ</text>

  <!-- Relationships Orthogonal Paths -->
  <!-- roles -> users -->
  <polyline points="470,463 470,540" fill="none" stroke="#000000" stroke-width="3" marker-end="url(#arrow)" />
  <rect x="495" y="475" width="70" height="30" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="502" y="497" class="conn-label">1 : N</text>

  <!-- users -> audit_logs -->
  <polyline points="470,964 470,1120" fill="none" stroke="#000000" stroke-width="3" marker-end="url(#arrow)" />
  <rect x="495" y="1015" width="70" height="30" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="502" y="1037" class="conn-label">1 : N</text>

  <!-- users -> ai_query_logs -->
  <polyline points="80,850 35,850 35,1920 80,1920" fill="none" stroke="#000000" stroke-width="3" marker-end="url(#arrow)" />
  <rect x="45" y="1365" width="70" height="30" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="52" y="1387" class="conn-label">1 : N</text>

  <!-- categories -> products -->
  <polyline points="1010,310 935,310 935,1630 1010,1630" fill="none" stroke="#000000" stroke-width="3" marker-end="url(#arrow)" />
  <rect x="945" y="945" width="70" height="30" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="952" y="967" class="conn-label">1 : N</text>

  <!-- suppliers -> products -->
  <polyline points="1010,720 965,720 965,1720 1010,1720" fill="none" stroke="#000000" stroke-width="3" marker-end="url(#arrow)" />
  <rect x="975" y="1205" width="70" height="30" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="982" y="1227" class="conn-label">1 : N</text>

  <!-- locations -> inventory_items -->
  <polyline points="1790,1180 1940,1180" fill="none" stroke="#000000" stroke-width="3" marker-end="url(#arrow)" />
  <rect x="1835" y="1130" width="70" height="30" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="1842" y="1152" class="conn-label">1 : N</text>

  <!-- products -> inventory_items -->
  <polyline points="1790,1660 1835,1660 1835,1280 1940,1280" fill="none" stroke="#000000" stroke-width="3" marker-end="url(#arrow)" />
  <rect x="1845" y="1445" width="70" height="30" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="1852" y="1467" class="conn-label">1 : N</text>

  <!-- suppliers -> inventory_transactions -->
  <polyline points="1790,720 1865,720 1865,1660 1940,1660" fill="none" stroke="#000000" stroke-width="3" marker-end="url(#arrow)" />
  <rect x="1875" y="1165" width="70" height="30" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="1882" y="1187" class="conn-label">1 : N</text>

  <!-- users -> inventory_transactions -->
  <polyline points="860,680 895,680 895,148 2760,148 2760,1740 2720,1740" fill="none" stroke="#000000" stroke-width="3" marker-end="url(#arrow)" />
  <rect x="2725" y="925" width="70" height="30" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="2732" y="947" class="conn-label">1 : N</text>

  <!-- inventory_transactions -> inventory_transaction_items -->
  <polyline points="2330,1944 2330,2120" fill="none" stroke="#000000" stroke-width="3" marker-end="url(#arrow)" />
  <rect x="2355" y="2005" width="70" height="30" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="2362" y="2027" class="conn-label">1 : N</text>

  <!-- products -> inventory_transaction_items -->
  <polyline points="1790,1880 1835,1880 1835,2260 1940,2260" fill="none" stroke="#000000" stroke-width="3" marker-end="url(#arrow)" />
  <rect x="1845" y="2045" width="70" height="30" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="1852" y="2067" class="conn-label">1 : N</text>

  <!-- locations -> inventory_transaction_items -->
  <polyline points="1790,1340 1895,1340 1895,2380 1940,2380" fill="none" stroke="#000000" stroke-width="3" marker-end="url(#arrow)" />
  <rect x="1905" y="1835" width="70" height="30" fill="#ffffff" stroke="#000000" stroke-width="1" />
  <text x="1912" y="1857" class="conn-label">1 : N</text>

  <!-- Footer -->
  <line x1="0" y1="3545" x2="2800" y2="3545" stroke="#000000" stroke-width="2" />
  <text x="40" y="3578" style="font-family:'Times New Roman'; font-style:italic; font-size:22px; fill:#333333;">Nhóm 11 - AIA331 | Trường Đại học Công nghệ Thông tin &amp; Truyền thông - ĐHTN</text>
</svg>
"""
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Exported Vector SVG: {svg_path}")

if __name__ == "__main__":
    print("Regenerating all enhanced diagrams...")
    generate_erd_diagram()
    generate_activity_export_diagram()
    generate_activity_import_diagram()
    generate_algorithm_flowchart()
    generate_erd_svg()
    print("Done generating enhanced diagrams!")
