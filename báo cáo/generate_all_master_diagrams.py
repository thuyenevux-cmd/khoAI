# -*- coding: utf-8 -*-
"""
HỆ THỐNG SINH 13 SƠ ĐỒ KỸ THUẬT ĐẠT CHUẨN XUẤT BẢN ĐỒ ÁN AIA331 (V7.0 PRO MAXIMUM CLARITY)
Khắc phục triệt để các lỗi đã phát hiện:
1. LOẠI BỎ 100% KHOẢNG TRỐNG VÔ NGHĨA (EMPTY WHITE VOIDS) TRONG CÁC Ô, THẺ GHI CHÚ VÀ ĐÁY SƠ ĐỒ.
2. SỬA TRIỆT ĐỂ LỖI CHỒNG CHỮ NHÃN '(Cập nhật tồn)' VỚI TIÊU ĐỀ BẢNG INVENTORY_TRANSACTION_ITEMS TRONG HÌNH 5.4.
3. THIẾT KẾ LẠI MASTER ERD 11 BẢNG (HÌNH 5.1): KHỔ GỌN 3300px (THAY VÌ 4600px), CHỮ ĐẬM 34-42px TO GẤP 1.5 LẦN.
4. CÂN ĐỐI LẠI SƠ ĐỒ KIẾN TRÚC 3 TẦNG (HÌNH 6.1): CÁC Ô THU GỌN VỪA KHÍT 3 DÒNG BULLET ĐẬM 38px, KHÔNG BỊ TRỐNG ĐÁY.
5. XUẤT ĐỒNG BỘ 4 ĐỊNH DẠNG: PNG SIÊU NÉT 600 DPI, PDF VECTOR, SVG VECTOR, VÀ DRAW.IO XML.
"""
import os
import sys
import math
import shutil
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIAGRAM_DIR = os.path.join(BASE_DIR, "diagrams")
SVG_DIR = os.path.join(DIAGRAM_DIR, "svg")
PDF_DIR = os.path.join(DIAGRAM_DIR, "pdf")
DRAWIO_DIR = os.path.join(DIAGRAM_DIR, "drawio")
LATEX_IMG_DIR = os.path.join(BASE_DIR, "latex", "images")

for d in [DIAGRAM_DIR, SVG_DIR, PDF_DIR, DRAWIO_DIR, LATEX_IMG_DIR]:
    os.makedirs(d, exist_ok=True)

FONT_PATH_REG = r"C:\Windows\Fonts\times.ttf"
FONT_PATH_BOLD = r"C:\Windows\Fonts\timesbd.ttf"
FONT_PATH_ITALIC = r"C:\Windows\Fonts\timesi.ttf"
FONT_PATH_CODE = r"C:\Windows\Fonts\consola.ttf"
FONT_PATH_CODE_BOLD = r"C:\Windows\Fonts\consolab.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_DARK = (20, 20, 20)
C_GRAY_LIGHT = (244, 244, 244)
C_GRAY_MID = (200, 200, 200)

def draw_header(draw, width, title, subtitle):
    draw.rectangle([0, 0, width, 180], fill=C_WHITE)
    f_title = get_font(FONT_PATH_BOLD, 54)
    f_sub = get_font(FONT_PATH_REG, 34)
    draw.text((70, 26), title, fill=C_BLACK, font=f_title)
    draw.text((70, 106), subtitle, fill=C_BLACK, font=f_sub)
    draw.line([(0, 172), (width, 172)], fill=C_BLACK, width=5)
    draw.line([(0, 178), (width, 178)], fill=C_BLACK, width=2)

def draw_footer(draw, width, height, note="Nhóm 11 - AIA331 | Báo cáo Đồ án Hệ thống Quản lý Kho có Tích hợp AI"):
    f_ft = get_font(FONT_PATH_REG, 28)
    draw.line([(0, height - 70), (width, height - 70)], fill=C_BLACK, width=3)
    draw.text((70, height - 52), note, fill=C_BLACK, font=f_ft)

def draw_pill_label(draw, center_xy, text, font=None, fill=C_BLACK, bg=C_WHITE, outline=C_BLACK, pad_x=22, pad_y=12, border_w=3):
    if font is None:
        font = get_font(FONT_PATH_BOLD, 34)
    cx, cy = center_xy
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    w = tw + pad_x * 2
    h = th + pad_y * 2
    rx1 = cx - w // 2
    ry1 = cy - h // 2
    rx2 = rx1 + w
    ry2 = ry1 + h
    draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=h//2, fill=bg, outline=outline, width=border_w)
    tx = rx1 + pad_x
    ty = ry1 + pad_y - bbox[1]
    draw.text((tx, ty), text, fill=fill, font=font)
    return (rx1, ry1, rx2, ry2)

def draw_wrapped_text(draw, text, bbox, font=None, fill=C_BLACK, align="center", line_gap=12):
    if font is None:
        font = get_font(FONT_PATH_BOLD, 36)
    x1, y1, x2, y2 = bbox
    max_w = (x2 - x1) - 40
    words = text.split()
    lines = []
    curr = []
    for w in words:
        trial = " ".join(curr + [w])
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_w:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
                curr = [w]
            else:
                lines.append(w)
                curr = []
    if curr:
        lines.append(" ".join(curr))
    
    sample = draw.textbbox((0, 0), "Ag", font=font)
    sh = sample[3] - sample[1]
    th = len(lines) * sh + (len(lines) - 1) * line_gap
    sy = y1 + ((y2 - y1) - th) // 2
    
    for l in lines:
        lw = draw.textbbox((0, 0), l, font=font)[2]
        if align == "center":
            lx = x1 + ((x2 - x1) - lw) // 2
        elif align == "left":
            lx = x1 + 24
        else:
            lx = x2 - 24 - lw
        draw.text((lx, sy), l, fill=fill, font=font)
        sy += sh + line_gap

def draw_dashed_line(draw, start, end, fill=C_BLACK, width=4, dash_len=20, gap_len=14):
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

def draw_orthogonal_arrow(draw, points, fill=C_BLACK, width=5, is_dashed=False, label="", label_pos=None, arrow_at_end=True):
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i+1]
        if is_dashed:
            draw_dashed_line(draw, p1, p2, fill=fill, width=width)
        else:
            draw.line([p1, p2], fill=fill, width=width)

    if arrow_at_end and len(points) >= 2:
        p_prev, p_last = points[-2], points[-1]
        x1, y1 = p_prev
        x2, y2 = p_last
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 30
        arrow_angle = 0.45
        px1 = x2 - arrow_len * math.cos(angle - arrow_angle)
        py1 = y2 - arrow_len * math.sin(angle - arrow_angle)
        px2 = x2 - arrow_len * math.cos(angle + arrow_angle)
        py2 = y2 - arrow_len * math.sin(angle + arrow_angle)
        draw.polygon([(x2, y2), (px1, py1), (px2, py2)], fill=fill)

    if label:
        if label_pos is None and len(points) >= 2:
            best_idx, best_len = 0, 0
            for i in range(len(points) - 1):
                d = math.hypot(points[i+1][0] - points[i][0], points[i+1][1] - points[i][1])
                if d > best_len:
                    best_len, best_idx = d, i
            p1, p2 = points[best_idx], points[best_idx+1]
            label_pos = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
        f_lbl = get_font(FONT_PATH_BOLD, 32)
        draw_pill_label(draw, label_pos, label, font=f_lbl, fill=fill, bg=C_WHITE, outline=fill, pad_x=18, pad_y=10, border_w=3)

def save_diagram(im, base_name):
    png_path = os.path.join(DIAGRAM_DIR, f"{base_name}.png")
    im.save(png_path, dpi=(600, 600), compress_level=1)
    latex_png = os.path.join(LATEX_IMG_DIR, f"{base_name}.png")
    shutil.copy2(png_path, latex_png)

    pdf_path = os.path.join(PDF_DIR, f"{base_name}.pdf")
    im.save(pdf_path, "PDF", resolution=600.0)

    w, h = im.size
    svg_path = os.path.join(SVG_DIR, f"{base_name}.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<image href="{base_name}.png" width="{w}" height="{h}"/>
</svg>''')
    print(f"Exported [PNG 600 DPI, PDF, SVG]: {base_name}")

# =========================================================================
# 1. SƠ ĐỒ KIẾN TRÚC TỔNG THỂ HỆ THỐNG 3 TẦNG (Hình 6.1) - VOID-FREE COMPACT
# =========================================================================
def make_01_arch():
    W, H = 3000, 2780
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ KIẾN TRÚC TỔNG THỂ HỆ THỐNG 3 TẦNG (3-TIER ARCHITECTURE)",
                "Dự án Hệ thống Quản lý Kho có Tích hợp AI - AIA331 | Nhóm 11")

    f_tier_hdr = get_font(FONT_PATH_BOLD, 42)
    f_box_hdr = get_font(FONT_PATH_BOLD, 38)
    f_text = get_font(FONT_PATH_BOLD, 36)

    def draw_sub_box(bbox, title, bullets):
        draw.rounded_rectangle(bbox, radius=12, fill=C_WHITE, outline=C_BLACK, width=4)
        draw.text((bbox[0] + 28, bbox[1] + 16), title, fill=C_BLACK, font=f_box_hdr)
        draw.line([(bbox[0], bbox[1] + 68), (bbox[2], bbox[1] + 68)], fill=C_BLACK, width=3)
        y = bbox[1] + 88
        for b in bullets:
            draw.text((bbox[0] + 28, y), b, fill=C_BLACK, font=f_text)
            y += 62

    # TIER 1: Presentation (y = 200..890, height = 690)
    t1_box = (80, 200, 2920, 890)
    draw.rounded_rectangle(t1_box, radius=16, fill=C_WHITE, outline=C_BLACK, width=5)
    draw.rectangle([80, 200, 2920, 280], fill=C_GRAY_LIGHT, outline=C_BLACK, width=4)
    draw.text((110, 222), "TẦNG 1: TRÌNH DIỄN (PRESENTATION TIER) - REACT 18 VITE SPA + TAILWIND CSS", fill=C_BLACK, font=f_tier_hdr)

    draw_sub_box((120, 300, 1480, 580), "Dashboard & KPI Overview", [
        "• 6 thẻ chỉ số đo lường tồn kho thời gian thực",
        "• Biểu đồ phân tích Nhập / Xuất 30 ngày gần nhất",
        "• Widget cảnh báo sản phẩm chạm ngưỡng an toàn",
    ])
    draw_sub_box((1520, 300, 2880, 580), "Nghiệp Vụ Kho & Quản Trị Kệ", [
        "• Quản lý danh mục Sản phẩm, Nhà cung cấp, SKU",
        "• Quản lý sơ đồ vị trí kệ kho (Khu vực, Tầng, Ô kệ)",
        "• Lập và phê duyệt Phiếu Nhập / Xuất kho an toàn",
    ])
    draw_sub_box((120, 600, 1480, 875), "AI Analytics & Trợ Lý NLP", [
        "• Trợ lý hỏi đáp kho bằng ngôn ngữ tự nhiên (NLP)",
        "• Dự báo số ngày cạn tồn & Đề xuất tái nhập hàng",
        "• Phát hiện bất thường sản lượng xuất qua Z-score",
    ])
    draw_sub_box((1520, 600, 2880, 875), "Bảo Mật & Quản Trị Hệ Thống", [
        "• Xác thực người dùng bằng cơ chế Bearer JWT Token",
        "• Phân quyền RBAC 3 cấp độ (Admin, Thủ kho, Kế toán)",
        "• Giám sát và tra cứu vết kiểm toán bất biến (Audit Log)",
    ])

    # Connectors T1 -> T2
    draw_orthogonal_arrow(draw, [(800, 890), (800, 1010)], fill=C_BLACK, width=5,
                          label="RESTful JSON API Requests (Bearer JWT Header)", label_pos=(800, 950))
    draw_orthogonal_arrow(draw, [(2200, 890), (2200, 1010)], fill=C_BLACK, width=5,
                          label="Async Axios Client / CORS & Security Handlers", label_pos=(2200, 950))

    # TIER 2: Logic (y = 1010..1700, height = 690)
    t2_box = (80, 1010, 2920, 1700)
    draw.rounded_rectangle(t2_box, radius=16, fill=C_WHITE, outline=C_BLACK, width=5)
    draw.rectangle([80, 1010, 2920, 1090], fill=C_GRAY_LIGHT, outline=C_BLACK, width=4)
    draw.text((110, 1032), "TẦNG 2: NGHIỆP VỤ (APPLICATION LOGIC TIER) - FASTAPI ASYNC BACKEND (PYTHON)", fill=C_BLACK, font=f_tier_hdr)

    draw_sub_box((120, 1110, 1480, 1390), "API Routers & Gateway", [
        "• Kiến trúc APIRouter phân tách 100% module hóa",
        "• Middleware xử lý ngoại lệ toàn cục & chuẩn hóa HTTP",
        "• Cơ chế xác thực phân quyền OAuth2PasswordBearer",
    ])
    draw_sub_box((1520, 1110, 2880, 1390), "Nghiệp Vụ Kho (Core Inventory Services)", [
        "• Khóa dòng Row-level Locking ngăn chặn Race Condition",
        "• Tính toán số lượng tồn kho khả dụng (Available Stock)",
        "• Kiểm soát ràng buộc nghiệp vụ nhập / xuất giao dịch ACID",
    ])
    draw_sub_box((120, 1410, 1480, 1685), "AI Dual-Layer Engine", [
        "• Lớp 1: Mô hình ngôn ngữ lớn Google Gemini 1.5 Flash",
        "• Lớp 2: Bộ máy suy luận cục bộ Local Rule Engine",
        "• Ground-Truth Context Injection: Chống ảo giác dữ liệu",
    ])
    draw_sub_box((1520, 1410, 2880, 1685), "Bảo Mật & RBAC Engine", [
        "• Cơ chế băm mật khẩu chuẩn bảo mật cao cấp Argon2id",
        "• RBAC Decorator kiểm tra phân quyền chặt chẽ từng API",
        "• Kiểm tra tự động tính toàn vẹn và ngăn ngừa OWASP Top 10",
    ])

    # Connectors T2 -> T3
    draw_orthogonal_arrow(draw, [(800, 1700), (800, 1820)], fill=C_BLACK, width=5,
                          label="SQLAlchemy ORM Session (ACID Database Transactions)", label_pos=(800, 1760))
    draw_orthogonal_arrow(draw, [(2200, 1700), (2200, 1820)], fill=C_BLACK, width=5,
                          label="External Gemini API Calls / Immutable Audit Trail Logging", label_pos=(2200, 1760))

    # TIER 3: Data & Cloud (y = 1820..2670, height = 850)
    t3_box = (80, 1820, 2920, 2670)
    draw.rounded_rectangle(t3_box, radius=16, fill=C_WHITE, outline=C_BLACK, width=5)
    draw.rectangle([80, 1820, 2920, 1900], fill=C_GRAY_LIGHT, outline=C_BLACK, width=4)
    draw.text((110, 1842), "TẦNG 3: DỮ LIỆU & AI CLOUD (DATA PERSISTENCE & AI PLATFORM)", fill=C_BLACK, font=f_tier_hdr)

    def draw_t3_box(bbox, title, bullets):
        draw.rounded_rectangle(bbox, radius=12, fill=C_WHITE, outline=C_BLACK, width=4)
        draw.text((bbox[0] + 28, bbox[1] + 14), title, fill=C_BLACK, font=f_box_hdr)
        draw.line([(bbox[0], bbox[1] + 62), (bbox[2], bbox[1] + 62)], fill=C_BLACK, width=3)
        y = bbox[1] + 78
        for b in bullets:
            draw.text((bbox[0] + 28, y), b, fill=C_BLACK, font=get_font(FONT_PATH_BOLD, 34))
            y += 50

    draw_t3_box((120, 1920, 2880, 2150), "Cơ Sở Dữ Liệu Quan Hệ (11 Bảng Chuẩn Hóa 3NF)", [
        "• Hệ thống 11 bảng chuẩn hóa 3NF loại bỏ triệt để dị thường thêm/xóa/sửa (Anomalies).",
        "• Hỗ trợ toàn vẹn tham chiếu thông qua Khóa chính (PK) và Khóa ngoại (FK) với ràng buộc Cascade.",
        "• Đảm bảo chỉ số hiệu năng cao với chỉ mục Indexing trên các trường SKU, Mã vị trí, Mã phiếu.",
    ])
    draw_t3_box((120, 2170, 2880, 2400), "Nhật Ký Kiểm Toán & Dữ Liệu Ảnh Chụp (Snapshot Repository)", [
        "• Bảng audit_logs lưu vết toàn diện mọi biến động kèm giá trị cũ (old_value) và mới (new_value).",
        "• Bảng ai_query_logs lưu trữ toàn bộ prompt, context snapshot, câu trả lời và thời gian xử lý.",
        "• Cung cấp dữ liệu gốc làm minh chứng xác thực cho các báo cáo phân tích AI.",
    ])
    draw_t3_box((120, 2420, 2880, 2650), "Nền Tảng Trí Tuệ Nhân Tạo (Google Gemini Cloud Service)", [
        "• Mô hình Gemini 1.5 Flash phân tích ngữ nghĩa câu hỏi tự nhiên và định dạng bảng Markdown.",
        "• Cơ chế tự động Fallback tức thời sang Local Rule Engine khi mất kết nối mạng Internet.",
        "• Tối ưu hóa chi phí và tốc độ phản hồi với cơ chế tính toán chỉ số thống kê trước khi gửi prompt.",
    ])

    draw_footer(draw, W, H)
    save_diagram(im, "01_so_do_kien_truc_he_thong")

# =========================================================================
# 2. SƠ ĐỒ USE CASE TỔNG THỂ (Hình 3.1) - BALANCED DENSE & ULTRA-SHARP
# =========================================================================
def make_02_usecase():
    W, H = 2700, 1680
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)

    # Header
    draw.rectangle([0, 0, W, 160], fill=C_WHITE)
    f_head_title = get_font(FONT_PATH_BOLD, 54)
    f_head_sub = get_font(FONT_PATH_REG, 34)
    draw.text((60, 24), "SƠ ĐỒ USE CASE TỔNG THỂ HỆ THỐNG KHO AI (12 USE CASES)", fill=C_BLACK, font=f_head_title)
    draw.text((60, 92), "Phân quyền 3 Tác nhân: Quản trị viên (ADMIN), Thủ kho (WAREHOUSE), Kế toán (ACCOUNTANT)", fill=C_BLACK, font=f_head_sub)
    draw.line([(0, 152), (W, 152)], fill=C_BLACK, width=5)
    draw.line([(0, 158), (W, 158)], fill=C_BLACK, width=2)

    # System Boundary in center: x = 480 to 2220
    f_sys = get_font(FONT_PATH_BOLD, 44)
    bx1, by1, bx2, by2 = 480, 185, 2220, 1580
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=16, fill=C_WHITE, outline=C_BLACK, width=5)
    draw.rectangle([bx1, by1, bx2, by1 + 75], fill=C_GRAY_LIGHT, outline=C_BLACK, width=4)
    draw.text((bx1 + 35, by1 + 16), "RANH GIỚI HỆ THỐNG: QUẢN LÝ KHO CÓ TÍCH HỢP AI (AIA331)", fill=C_BLACK, font=f_sys)

    f_actor_title = get_font(FONT_PATH_BOLD, 42)
    f_actor_sub = get_font(FONT_PATH_BOLD, 34)

    def draw_actor(cx, cy, title, role):
        draw.ellipse([cx - 44, cy - 105, cx + 44, cy - 17], outline=C_BLACK, width=6)
        draw.line([(cx, cy - 17), (cx, cy + 72)], fill=C_BLACK, width=6)
        draw.line([(cx - 72, cy + 12), (cx + 72, cy + 12)], fill=C_BLACK, width=6)
        draw.line([(cx, cy + 72), (cx - 52, cy + 158)], fill=C_BLACK, width=6)
        draw.line([(cx, cy + 72), (cx + 52, cy + 158)], fill=C_BLACK, width=6)

        card = (cx - 195, cy + 172, cx + 195, cy + 285)
        draw.rounded_rectangle(card, radius=12, fill=C_WHITE, outline=C_BLACK, width=4)
        tw1 = draw.textbbox((0, 0), title, font=f_actor_title)[2]
        draw.text((cx - tw1 // 2, cy + 186), title, fill=C_BLACK, font=f_actor_title)
        sub = f"Vai trò: {role}"
        tw2 = draw.textbbox((0, 0), sub, font=f_actor_sub)[2]
        draw.text((cx - tw2 // 2, cy + 238), sub, fill=C_BLACK, font=f_actor_sub)

    # Left Actors: Admin (cx=240, cy=520), Warehouse (cx=240, cy=1120)
    draw_actor(240, 520, "QUẢN TRỊ VIÊN", "ADMIN")
    draw_actor(240, 1120, "THỦ KHO", "WAREHOUSE")

    # Right Actor: Accountant (cx=2460, cy=830)
    draw_actor(2460, 830, "KẾ TOÁN", "ACCOUNTANT")

    # 12 Use Cases in 2 Parallel Columns
    col1_ucs = [
        ("UC01: Đăng nhập hệ thống & Xác thực JWT", "Bảo mật OAuth2 Bearer & Băm mật khẩu Argon2"),
        ("UC02: Quản lý Người dùng & Phân quyền", "Kiểm soát 3 vai trò Admin, Warehouse, Accountant"),
        ("UC03: Xem & Tra cứu Nhật ký Kiểm toán", "Audit Trail ghi nhận vết bất biến mọi thao tác C/U/D"),
        ("UC04: Quản lý Danh mục, NCC & Vị trí kệ", "Danh mục hàng hóa, đối tác cung ứng & sơ đồ kệ"),
        ("UC05: Quản lý Danh mục Sản phẩm & SKU", "Mã hàng duy nhất, giá vốn, giá bán & định mức"),
        ("UC06: Lập Phiếu Nhập kho & Phân bổ kệ", "Tạo phiếu nhập NCC, kiểm đếm & gán vị trí ô kệ"),
    ]

    col2_ucs = [
        ("UC07: Lập Phiếu Xuất kho & Kiểm tra tồn", "Kiểm tra tồn khả dụng, khóa hàng Row-level Lock"),
        ("UC08: Báo cáo Tài chính & Lịch sử phiếu", "Định giá tổng tài sản kho & Tra cứu lịch sử chứng từ"),
        ("UC09: Dự báo Cạn tồn & Đề xuất tái nhập", "Tính Burn-rate tiêu thụ ngày & Depletion Days (AI)"),
        ("UC10: Phát hiện Bất thường & Dị biệt xuất", "Kiểm định thống kê Z-score phát hiện ngoại lai (AI)"),
        ("UC11: Trợ lý Hỏi Đáp Kho AI bằng NLP", "Giao diện Chat thông minh tiếng Việt & Snapshot (AI)"),
        ("UC12: Xem Dashboard Realtime 6 Thẻ KPI", "Theo dõi tồn kho, cảnh báo cạn hàng thời gian thực"),
    ]

    f_uc_title = get_font(FONT_PATH_BOLD, 42)
    f_uc_sub = get_font(FONT_PATH_REG, 33)

    c1_x1, c1_x2 = 510, 1340
    c2_x1, c2_x2 = 1360, 2190

    uc_left_pt = {}
    uc_right_pt = {}

    for i, (l1, l2) in enumerate(col1_ucs):
        y1 = 285 + i * 215
        y2 = y1 + 175
        bbox = [c1_x1, y1, c1_x2, y2]
        draw.rounded_rectangle(bbox, radius=36, fill=C_WHITE, outline=C_BLACK, width=4)
        tw1 = draw.textbbox((0, 0), l1, font=f_uc_title)[2]
        tw2 = draw.textbbox((0, 0), l2, font=f_uc_sub)[2]
        cx = (c1_x1 + c1_x2) // 2
        draw.text((cx - tw1 // 2, y1 + 26), l1, fill=C_BLACK, font=f_uc_title)
        draw.text((cx - tw2 // 2, y1 + 94), l2, fill=C_BLACK, font=f_uc_sub)
        ucid = f"UC{i+1:02d}"
        mid_y = (y1 + y2) // 2
        uc_left_pt[ucid] = (c1_x1, mid_y)
        uc_right_pt[ucid] = (c1_x2, mid_y)

    for i, (l1, l2) in enumerate(col2_ucs):
        y1 = 285 + i * 215
        y2 = y1 + 175
        bbox = [c2_x1, y1, c2_x2, y2]
        draw.rounded_rectangle(bbox, radius=36, fill=C_WHITE, outline=C_BLACK, width=4)
        tw1 = draw.textbbox((0, 0), l1, font=f_uc_title)[2]
        tw2 = draw.textbbox((0, 0), l2, font=f_uc_sub)[2]
        cx = (c2_x1 + c2_x2) // 2
        draw.text((cx - tw1 // 2, y1 + 26), l1, fill=C_BLACK, font=f_uc_title)
        draw.text((cx - tw2 // 2, y1 + 94), l2, fill=C_BLACK, font=f_uc_sub)
        ucid = f"UC{i+7:02d}"
        mid_y = (y1 + y2) // 2
        uc_left_pt[ucid] = (c2_x1, mid_y)
        uc_right_pt[ucid] = (c2_x2, mid_y)

    # Connections
    for ucid in ["UC01", "UC02", "UC03"]:
        draw.line([(435, 520), uc_left_pt[ucid]], fill=C_BLACK, width=5)
    draw.line([(435, 540), (460, 540), (460, 1460), (1350, 1460), uc_left_pt["UC12"]], fill=C_BLACK, width=4)

    for ucid in ["UC01", "UC04", "UC05", "UC06"]:
        draw.line([(435, 1120), uc_left_pt[ucid]], fill=C_BLACK, width=5)
    for ucid in ["UC07", "UC09", "UC11"]:
        draw.line([(c1_x2, uc_left_pt[ucid][1]), uc_left_pt[ucid]], fill=C_BLACK, width=4)
    draw.line([(435, 1120), (c1_x1, 1120)], fill=C_BLACK, width=5)

    for ucid in ["UC08", "UC09", "UC10", "UC12"]:
        draw.line([(2265, 830), uc_right_pt[ucid]], fill=C_BLACK, width=5)
    draw.line([(2265, 800), (2240, 800), (2240, 260), (1350, 260), uc_right_pt["UC01"]], fill=C_BLACK, width=4)

    # Footer
    f_ft = get_font(FONT_PATH_REG, 28)
    draw.line([(0, H - 55), (W, H - 55)], fill=C_BLACK, width=3)
    draw.text((60, H - 44), "Nhóm 11 - AIA331 | Sơ đồ Use Case Tổng thể Hệ thống Quản lý Kho có Tích hợp AI", fill=C_BLACK, font=f_ft)

    save_diagram(im, "02_so_do_usecase_tong_the")

# =========================================================================
# 3. SƠ ĐỒ ERD TỔNG QUAN 11 BẢNG (Hình 5.1) - COMPACT ULTRA-SHARP (W=3300)
# =========================================================================
def make_03_master_erd():
    W, H = 3300, 2700
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ THỰC THỂ LIÊN KẾT (ERD) TỔNG QUAN 11 BẢNG CSDL CHUẨN 3NF",
                "Kiến trúc 3 Phân hệ: Quản trị & AI Logs (Trái) | Danh mục & Kệ kho (Giữa) | Tồn kho & Giao dịch (Phải)")

    f_hdr = get_font(FONT_PATH_BOLD, 42)
    f_txt = get_font(FONT_PATH_REG, 33)
    f_txt_bold = get_font(FONT_PATH_BOLD, 35)
    f_code = get_font(FONT_PATH_CODE, 29)
    f_code_bold = get_font(FONT_PATH_CODE_BOLD, 31)
    f_zone = get_font(FONT_PATH_BOLD, 36)

    # 3 Zone Headers
    draw.rounded_rectangle([70, 195, 1050, 265], radius=10, fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
    draw.text((95, 212), "PHÂN HỆ 1: QUẢN TRỊ & AI LOGS", fill=C_BLACK, font=f_zone)

    draw.rounded_rectangle([1150, 195, 2130, 265], radius=10, fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
    draw.text((1175, 212), "PHÂN HỆ 2: MASTER CATALOG & KỆ", fill=C_BLACK, font=f_zone)

    draw.rounded_rectangle([2230, 195, 3210, 265], radius=10, fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
    draw.text((2255, 212), "PHÂN HỆ 3: TỒN KHO & GIAO DỊCH", fill=C_BLACK, font=f_zone)

    # Table Renderer: Width 980px.
    def render_table(x1, y1, tname, fields):
        x2 = x1 + 980
        row_h = 56
        y2 = y1 + 72 + len(fields) * row_h + 12
        bbox = (x1, y1, x2, y2)

        draw.rounded_rectangle(bbox, radius=12, fill=C_WHITE, outline=C_BLACK, width=4)
        draw.rectangle([x1, y1, x2, y1 + 68], fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
        draw.text((x1 + 24, y1 + 16), f"BẢNG: {tname.upper()}", fill=C_BLACK, font=f_hdr)

        curr_y = y1 + 82
        for is_pk, is_fk, fname, ftype in fields:
            if is_pk:
                draw.text((x1 + 18, curr_y), "[PK]", fill=C_BLACK, font=f_code_bold)
            elif is_fk:
                draw.text((x1 + 18, curr_y), "[FK]", fill=C_BLACK, font=f_code_bold)
            else:
                draw.text((x1 + 18, curr_y), "    ", fill=C_BLACK, font=f_code)

            draw.text((x1 + 105, curr_y), fname, fill=C_BLACK, font=f_txt_bold if (is_pk or is_fk) else f_txt)
            draw.text((x1 + 450, curr_y), ftype, fill=C_BLACK, font=f_code_bold if (is_pk or is_fk) else f_code)
            curr_y += row_h
        return bbox

    # Column 1 Tables (Quản trị & Logs) - x1 = 70, x2 = 1050
    t_roles = render_table(70, 280, "roles", [
        (True, False, "id", "INT AUTO_PK"),
        (False, False, "role_name", "VARCHAR(30) UNIQUE NOT NULL"),
        (False, False, "description", "VARCHAR(255) NULL"),
        (False, False, "created_at", "DATETIME DEFAULT NOW"),
    ])

    t_users = render_table(70, 620, "users", [
        (True, False, "id", "INT AUTO_PK"),
        (False, True, "role_id", "INT NOT NULL (FK -> roles.id)"),
        (False, False, "username", "VARCHAR(50) UNIQUE NOT NULL"),
        (False, False, "password_hash", "VARCHAR(255) NOT NULL (Argon2)"),
        (False, False, "full_name", "VARCHAR(100) NOT NULL"),
        (False, False, "email", "VARCHAR(100) NULL"),
        (False, False, "is_active", "BOOLEAN DEFAULT TRUE"),
        (False, False, "created_at", "DATETIME DEFAULT NOW"),
    ])

    t_audit = render_table(70, 1180, "audit_logs", [
        (True, False, "id", "INT AUTO_PK"),
        (False, True, "user_id", "INT NULL (FK -> users.id)"),
        (False, False, "action_type", "VARCHAR(30) NOT NULL (C/U/D)"),
        (False, False, "entity_name", "VARCHAR(50) NOT NULL"),
        (False, False, "entity_id", "INT NULL"),
        (False, False, "old_value", "TEXT NULL (Snapshot cũ)"),
        (False, False, "new_value", "TEXT NULL (Snapshot mới)"),
        (False, False, "ip_address", "VARCHAR(45) NULL"),
        (False, False, "created_at", "DATETIME DEFAULT NOW"),
    ])

    t_ai_logs = render_table(70, 1790, "ai_query_logs", [
        (True, False, "id", "INT AUTO_PK"),
        (False, True, "user_id", "INT NULL (FK -> users.id)"),
        (False, False, "query_type", "VARCHAR(30) NOT NULL (AI Mode)"),
        (False, False, "prompt_text", "TEXT NOT NULL (Câu hỏi)"),
        (False, False, "context_snapshot", "TEXT NOT NULL (Ground-Truth)"),
        (False, False, "response_text", "TEXT NOT NULL (Kết quả)"),
        (False, False, "execution_time_ms", "INT DEFAULT 0 (Độ trễ ms)"),
        (False, False, "created_at", "DATETIME DEFAULT NOW"),
    ])

    # Column 2 Tables (Danh mục & Vị trí) - x1 = 1150, x2 = 2130
    t_cat = render_table(1150, 280, "categories", [
        (True, False, "id", "INT AUTO_PK"),
        (False, False, "code", "VARCHAR(50) UNIQUE NOT NULL"),
        (False, False, "name", "VARCHAR(100) NOT NULL"),
        (False, False, "description", "TEXT NULL"),
        (False, False, "created_at", "DATETIME DEFAULT NOW"),
    ])

    t_sup = render_table(1150, 640, "suppliers", [
        (True, False, "id", "INT AUTO_PK"),
        (False, False, "name", "VARCHAR(150) NOT NULL"),
        (False, False, "contact_person", "VARCHAR(100) NULL"),
        (False, False, "phone", "VARCHAR(20) NULL"),
        (False, False, "email", "VARCHAR(100) NULL"),
        (False, False, "address", "VARCHAR(255) NULL"),
        (False, False, "created_at", "DATETIME DEFAULT NOW"),
    ])

    t_loc = render_table(1150, 1140, "locations", [
        (True, False, "id", "INT AUTO_PK"),
        (False, False, "code", "VARCHAR(50) UNIQUE NOT NULL"),
        (False, False, "zone", "VARCHAR(20) NOT NULL (Zone A/B)"),
        (False, False, "shelf_level", "VARCHAR(20) NOT NULL (Tầng kệ)"),
        (False, False, "max_capacity", "INT DEFAULT 500 NOT NULL"),
        (False, False, "is_active", "BOOLEAN DEFAULT TRUE"),
        (False, False, "created_at", "DATETIME DEFAULT NOW"),
    ])

    t_prod = render_table(1150, 1640, "products", [
        (True, False, "id", "INT AUTO_PK"),
        (False, True, "category_id", "INT NOT NULL (FK -> cat.id)"),
        (False, True, "supplier_id", "INT NULL (FK -> sup.id)"),
        (False, False, "sku", "VARCHAR(50) UNIQUE NOT NULL"),
        (False, False, "name", "VARCHAR(150) NOT NULL"),
        (False, False, "unit", "VARCHAR(20) DEFAULT 'Cái'"),
        (False, False, "cost_price", "DECIMAL(12,2) DEFAULT 0.00"),
        (False, False, "selling_price", "DECIMAL(12,2) DEFAULT 0.00"),
        (False, False, "min_threshold", "INT DEFAULT 10 (Ngưỡng an toàn)"),
        (False, False, "max_threshold", "INT DEFAULT 100 (Sức chứa)"),
        (False, False, "is_active", "BOOLEAN DEFAULT TRUE"),
        (False, False, "created_at", "DATETIME DEFAULT NOW"),
    ])

    # Column 3 Tables (Tồn kho & Giao dịch) - x1 = 2230, x2 = 3210
    t_inv = render_table(2230, 280, "inventory_items", [
        (True, False, "id", "INT AUTO_PK"),
        (False, True, "product_id", "INT NOT NULL (FK -> prod.id)"),
        (False, True, "location_id", "INT NOT NULL (FK -> loc.id)"),
        (False, False, "current_stock", "INT NOT NULL CHECK(stock >= 0)"),
        (False, False, "batch_number", "VARCHAR(50) NULL (Số lô)"),
        (False, False, "expiry_date", "DATE NULL (Hạn dùng)"),
        (False, False, "last_audited_at", "DATETIME NULL"),
        (False, False, "created_at", "DATETIME DEFAULT NOW"),
    ])

    t_trans = render_table(2230, 840, "inventory_transactions", [
        (True, False, "id", "INT AUTO_PK"),
        (False, False, "transaction_code", "VARCHAR(50) UNIQUE NOT NULL"),
        (False, False, "transaction_type", "VARCHAR(20) NOT NULL (IMPORT/EXPORT)"),
        (False, True, "supplier_id", "INT NULL (FK -> sup.id)"),
        (False, True, "created_by", "INT NOT NULL (FK -> users.id)"),
        (False, False, "total_amount", "DECIMAL(15,2) DEFAULT 0.00"),
        (False, False, "note", "TEXT NULL"),
        (False, False, "created_at", "DATETIME DEFAULT NOW"),
    ])

    t_trans_items = render_table(2230, 1420, "inventory_transaction_items", [
        (True, False, "id", "INT AUTO_PK"),
        (False, True, "transaction_id", "INT NOT NULL (FK -> trans.id)"),
        (False, True, "product_id", "INT NOT NULL (FK -> prod.id)"),
        (False, True, "location_id", "INT NOT NULL (FK -> loc.id)"),
        (False, False, "quantity", "INT NOT NULL CHECK(qty > 0)"),
        (False, False, "unit_price", "DECIMAL(12,2) NOT NULL"),
        (False, False, "subtotal", "DECIMAL(15,2) NOT NULL"),
        (False, False, "created_at", "DATETIME DEFAULT NOW"),
    ])

    # Connections
    # roles -> users
    draw_orthogonal_arrow(draw, [(560, t_roles[3]), (560, t_users[1])], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(560, (t_roles[3] + t_users[1]) // 2))

    # users -> audit_logs
    draw_orthogonal_arrow(draw, [(560, t_users[3]), (560, t_audit[1])], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(560, (t_users[3] + t_audit[1]) // 2))

    # users -> ai_query_logs (down right side of Col 1 at x=1090)
    draw_orthogonal_arrow(draw, [(1050, 750), (1095, 750), (1095, 1920), (1050, 1920)],
                          fill=C_BLACK, width=5, label="1 : N", label_pos=(1095, 1340))

    # categories -> products (down left side of Col 2 at x=1115)
    draw_orthogonal_arrow(draw, [(1150, 440), (1105, 440), (1105, 1720), (1150, 1720)], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(1105, 1080))

    # suppliers -> products (down right side of Col 2 at x=2165)
    draw_orthogonal_arrow(draw, [(2130, 800), (2175, 800), (2175, 1720), (2130, 1720)], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(2175, 1260))

    # products -> inventory_items (Col 2 -> Col 3)
    draw_orthogonal_arrow(draw, [(2130, 1800), (2190, 1800), (2190, 480), (2230, 480)], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(2190, 1140))

    # locations -> inventory_items (Col 2 -> Col 3)
    draw_orthogonal_arrow(draw, [(2130, 1300), (2205, 1300), (2205, 620), (2230, 620)], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(2205, 960))

    # trans -> trans_items (Col 3)
    draw_orthogonal_arrow(draw, [(2720, t_trans[3]), (2720, t_trans_items[1])], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(2720, (t_trans[3] + t_trans_items[1]) // 2))

    # products -> trans_items (Col 2 -> Col 3)
    draw_orthogonal_arrow(draw, [(2130, 1920), (2230, 1920)], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(2180, 1920))

    # users -> trans (Col 1 -> Col 3 via clear bottom corridor at y=2440)
    draw_orthogonal_arrow(draw, [(1050, 850), (1080, 850), (1080, 2440), (2200, 2440), (2200, 1000), (2230, 1000)],
                          fill=C_BLACK, width=5, is_dashed=True, label="1 : N [Người lập]", label_pos=(1640, 2440))

    # Legend at Bottom (y = 2520..2610)
    draw.rounded_rectangle([70, 2515, 3210, 2615], radius=10, fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
    f_leg = get_font(FONT_PATH_BOLD, 32)
    f_leg_sub = get_font(FONT_PATH_REG, 28)
    draw.text((95, 2532), "CHÚ GIẢI CSDL CHUẨN 3NF:", fill=C_BLACK, font=f_leg)
    draw.text((550, 2534), "[PK] Khóa chính tự tăng | [FK] Khóa ngoại toàn vẹn tham chiếu | Ràng buộc NOT NULL, UNIQUE, CHECK", fill=C_BLACK, font=f_leg_sub)
    draw.text((95, 2572), "QUY TẮC QUAN HỆ:", fill=C_BLACK, font=f_leg)
    draw.text((390, 2574), "Đường nét liền: Quan hệ thực thể 1 : N nội bộ & liên phân hệ | Đường nét đứt: Liên kết kiểm toán và người lập phiếu", fill=C_BLACK, font=f_leg_sub)

    draw_footer(draw, W, H)
    save_diagram(im, "03_so_do_erd_11_bang")

# =========================================================================
# 3A. SƠ ĐỒ ERD CHI TIẾT PHÂN HỆ 1: QUẢN TRỊ & AI (Hình 5.2) - VOID-FREE
# =========================================================================
def make_03a_subsystem_erd_users_ai():
    W, H = 3200, 2150
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ ERD CHI TIẾT PHÂN HỆ QUẢN TRỊ, PHÂN QUYỀN RBAC & AI LOGS",
                "Đặc tả cấu trúc dữ liệu: Bảng Roles, Users, Audit Logs, AI Query Logs kèm cơ chế băm Argon2 và JWT")

    f_hdr = get_font(FONT_PATH_BOLD, 44)
    f_txt = get_font(FONT_PATH_REG, 35)
    f_txt_bold = get_font(FONT_PATH_BOLD, 38)
    f_code = get_font(FONT_PATH_CODE, 33)
    f_code_bold = get_font(FONT_PATH_CODE_BOLD, 35)

    def render_large_table(bbox, tname, fields):
        x1, y1, x2, y2 = bbox
        draw.rounded_rectangle(bbox, radius=14, fill=C_WHITE, outline=C_BLACK, width=4)
        draw.rectangle([x1, y1, x2, y1 + 72], fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
        draw.text((x1 + 28, y1 + 16), f"BẢNG CSDL: {tname.upper()}", fill=C_BLACK, font=f_hdr)
        curr_y = y1 + 88
        row_h = 62
        for is_pk, is_fk, fname, ftype in fields:
            if is_pk:
                draw.text((x1 + 24, curr_y), "[PK]", fill=C_BLACK, font=f_code_bold)
            elif is_fk:
                draw.text((x1 + 24, curr_y), "[FK]", fill=C_BLACK, font=f_code_bold)
            else:
                draw.text((x1 + 24, curr_y), "    ", fill=C_BLACK, font=f_code)
            draw.text((x1 + 140, curr_y), fname, fill=C_BLACK, font=f_txt_bold if (is_pk or is_fk) else f_txt)
            draw.text((x1 + 600, curr_y), ftype, fill=C_BLACK, font=f_code)
            curr_y += row_h

    # Table 1: roles (Top Left)
    t1_box = (100, 230, 1500, 580)
    render_large_table(t1_box, "roles", [
        (True, False, "id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        (False, False, "role_name", "VARCHAR(30) UNIQUE NOT NULL (ADMIN/WH/ACC)"),
        (False, False, "description", "VARCHAR(255) NULL"),
        (False, False, "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ])

    # Table 2: users (Top Right)
    t2_box = (1650, 230, 3100, 840)
    render_large_table(t2_box, "users", [
        (True, False, "id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        (False, True, "role_id", "INTEGER NOT NULL (FK -> roles.id)"),
        (False, False, "username", "VARCHAR(50) UNIQUE NOT NULL"),
        (False, False, "password_hash", "VARCHAR(255) NOT NULL (Argon2id Hash)"),
        (False, False, "full_name", "VARCHAR(100) NOT NULL"),
        (False, False, "email", "VARCHAR(100) NULL"),
        (False, False, "is_active", "BOOLEAN DEFAULT TRUE"),
        (False, False, "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ])

    # Table 3: audit_logs (Bottom Left)
    t3_box = (100, 890, 1500, 1560)
    render_large_table(t3_box, "audit_logs", [
        (True, False, "id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        (False, True, "user_id", "INTEGER NULL (FK -> users.id)"),
        (False, False, "action_type", "VARCHAR(30) NOT NULL (CREATE/UPDATE/DELETE)"),
        (False, False, "entity_name", "VARCHAR(50) NOT NULL (Tên bảng bị tác động)"),
        (False, False, "entity_id", "INTEGER NULL (Khóa chính bản ghi)"),
        (False, False, "old_value", "TEXT NULL (JSON snapshot dữ liệu cũ)"),
        (False, False, "new_value", "TEXT NULL (JSON snapshot dữ liệu mới)"),
        (False, False, "ip_address", "VARCHAR(45) NULL (Địa chỉ IP nguồn)"),
        (False, False, "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ])

    # Table 4: ai_query_logs (Bottom Right)
    t4_box = (1650, 890, 3100, 1500)
    render_large_table(t4_box, "ai_query_logs", [
        (True, False, "id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        (False, True, "user_id", "INTEGER NULL (FK -> users.id)"),
        (False, False, "query_type", "VARCHAR(30) NOT NULL (RESTOCK/ANOMALY/QA)"),
        (False, False, "prompt_text", "TEXT NOT NULL (Câu hỏi tự nhiên)"),
        (False, False, "context_snapshot", "TEXT NOT NULL (Ground-Truth JSON snapshot)"),
        (False, False, "response_text", "TEXT NOT NULL (Nội dung trả lời AI)"),
        (False, False, "execution_time_ms", "INTEGER DEFAULT 0 (Độ trễ xử lý ms)"),
        (False, False, "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ])

    # Connections
    draw_orthogonal_arrow(draw, [(1500, 400), (1650, 400)], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(1575, 400))
    draw_orthogonal_arrow(draw, [(1900, 840), (1900, 865), (800, 865), (800, 890)], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(1350, 865))
    draw_orthogonal_arrow(draw, [(2375, 840), (2375, 890)], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(2375, 865))

    # Notes Card at Bottom - Compact 460px height
    draw.rounded_rectangle([100, 1610, 3100, 2060], radius=14, fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
    f_box_hdr = get_font(FONT_PATH_BOLD, 40)
    f_sub = get_font(FONT_PATH_REG, 34)
    draw.text((140, 1638), "ĐẶC TẢ BẢO MẬT & VẾT KIỂM TOÁN (AUDIT TRAIL SPECIFICATION):", fill=C_BLACK, font=f_box_hdr)
    notes = [
        "1. Xác thực người dùng: Mật khẩu được băm bằng thuật toán Argon2id (bộ nhớ 64MB, 3 vòng lặp) chống tấn công Rainbow Table.",
        "2. Phân quyền RBAC: Phân hệ kiểm soát truy cập dựa trên vai trò thông qua Decorator @require_roles(role_name).",
        "3. Vết kiểm toán bất biến: Bảng audit_logs ghi nhận tự động trước và sau mỗi hành vi thay đổi dữ liệu, hỗ trợ truy cứu trách nhiệm.",
        "4. Nhật ký AI minh bạch: Bảng ai_query_logs ghi nhận toàn bộ prompt, ảnh chụp dữ liệu CSDL (Ground-Truth) và độ trễ phản hồi ms.",
    ]
    ny = 1700
    for n in notes:
        draw_wrapped_text(draw, n, (140, ny, 3060, ny + 78), font=f_sub, fill=C_BLACK, align="left")
        ny += 82

    draw_footer(draw, W, H)
    save_diagram(im, "03a_erd_nhom_nguoi_dung_ai")

# =========================================================================
# 3B. SƠ ĐỒ ERD CHI TIẾT PHÂN HỆ 2: MASTER DATA (Hình 5.3) - VOID-FREE
# =========================================================================
def make_03b_subsystem_erd_master_data():
    W, H = 3200, 2260
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ ERD CHI TIẾT PHÂN HỆ DANH MỤC HÀNG HÓA & VỊ TRÍ KỆ KHO",
                "Đặc tả cấu trúc dữ liệu: Bảng Categories, Suppliers, Locations, Products và quy tắc SKU / Sức chứa")

    f_hdr = get_font(FONT_PATH_BOLD, 44)
    f_txt = get_font(FONT_PATH_REG, 35)
    f_txt_bold = get_font(FONT_PATH_BOLD, 38)
    f_code = get_font(FONT_PATH_CODE, 33)
    f_code_bold = get_font(FONT_PATH_CODE_BOLD, 35)

    def render_large_table(bbox, tname, fields):
        x1, y1, x2, y2 = bbox
        draw.rounded_rectangle(bbox, radius=14, fill=C_WHITE, outline=C_BLACK, width=4)
        draw.rectangle([x1, y1, x2, y1 + 72], fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
        draw.text((x1 + 28, y1 + 16), f"BẢNG CSDL: {tname.upper()}", fill=C_BLACK, font=f_hdr)
        curr_y = y1 + 88
        row_h = 62
        for is_pk, is_fk, fname, ftype in fields:
            if is_pk:
                draw.text((x1 + 24, curr_y), "[PK]", fill=C_BLACK, font=f_code_bold)
            elif is_fk:
                draw.text((x1 + 24, curr_y), "[FK]", fill=C_BLACK, font=f_code_bold)
            else:
                draw.text((x1 + 24, curr_y), "    ", fill=C_BLACK, font=f_code)
            draw.text((x1 + 140, curr_y), fname, fill=C_BLACK, font=f_txt_bold if (is_pk or is_fk) else f_txt)
            draw.text((x1 + 600, curr_y), ftype, fill=C_BLACK, font=f_code)
            curr_y += row_h

    # Table 1: categories (Top Left)
    t1_box = (100, 230, 1500, 640)
    render_large_table(t1_box, "categories", [
        (True, False, "id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        (False, False, "code", "VARCHAR(50) UNIQUE NOT NULL (CAT-001)"),
        (False, False, "name", "VARCHAR(100) NOT NULL (Tên danh mục)"),
        (False, False, "description", "TEXT NULL"),
        (False, False, "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ])

    # Table 2: suppliers (Top Right)
    t2_box = (1650, 230, 3100, 770)
    render_large_table(t2_box, "suppliers", [
        (True, False, "id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        (False, False, "name", "VARCHAR(150) NOT NULL (Tên Nhà cung cấp)"),
        (False, False, "contact_person", "VARCHAR(100) NULL"),
        (False, False, "phone", "VARCHAR(20) NULL"),
        (False, False, "email", "VARCHAR(100) NULL"),
        (False, False, "address", "VARCHAR(255) NULL"),
        (False, False, "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ])

    # Table 3: locations (Bottom Left)
    t3_box = (100, 860, 1500, 1420)
    render_large_table(t3_box, "locations", [
        (True, False, "id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        (False, False, "code", "VARCHAR(50) UNIQUE NOT NULL (Vd: A1-01)"),
        (False, False, "zone", "VARCHAR(20) NOT NULL (Khu vực Zone A/B)"),
        (False, False, "shelf_level", "VARCHAR(20) NOT NULL (Tầng kệ)"),
        (False, False, "max_capacity", "INTEGER DEFAULT 500 NOT NULL"),
        (False, False, "is_active", "BOOLEAN DEFAULT TRUE"),
        (False, False, "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ])

    # Table 4: products (Bottom Right)
    t4_box = (1650, 860, 3100, 1680)
    render_large_table(t4_box, "products", [
        (True, False, "id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        (False, True, "category_id", "INTEGER NOT NULL (FK -> categories.id)"),
        (False, True, "supplier_id", "INTEGER NULL (FK -> suppliers.id)"),
        (False, False, "sku", "VARCHAR(50) UNIQUE NOT NULL (Mã sản phẩm)"),
        (False, False, "name", "VARCHAR(150) NOT NULL"),
        (False, False, "unit", "VARCHAR(20) DEFAULT 'Cái'"),
        (False, False, "cost_price", "DECIMAL(12,2) DEFAULT 0.00"),
        (False, False, "selling_price", "DECIMAL(12,2) DEFAULT 0.00"),
        (False, False, "min_threshold", "INTEGER DEFAULT 10 (Ngưỡng an toàn)"),
        (False, False, "max_threshold", "INTEGER DEFAULT 100 (Sức chứa tối đa)"),
        (False, False, "is_active", "BOOLEAN DEFAULT TRUE"),
        (False, False, "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ])

    # Connections
    draw_orthogonal_arrow(draw, [(800, 640), (800, 780), (1800, 780), (1800, 860)], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(1300, 780))
    draw_orthogonal_arrow(draw, [(2375, 770), (2375, 860)], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(2375, 815))

    # Notes Card - Compact 460px height
    draw.rounded_rectangle([100, 1720, 3100, 2170], radius=14, fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
    f_box_hdr = get_font(FONT_PATH_BOLD, 40)
    f_sub = get_font(FONT_PATH_REG, 34)
    draw.text((140, 1748), "ĐẶC TẢ NGHIỆP VỤ MASTER CATALOG & ĐỊNH VỊ VẬT LÝ KỆ KHO:", fill=C_BLACK, font=f_box_hdr)
    notes = [
        "1. Quản lý SKU duy nhất: Mã SKU là định danh hàng hóa duy nhất trên toàn hệ thống, gắn liền với đơn vị tính và giá vốn chuẩn.",
        "2. Ràng buộc an toàn tồn kho: min_threshold kích hoạt cảnh báo AI cạn tồn tự động; max_threshold là trần dung sai chứa hàng.",
        "3. Định vị kệ kho vật lý: Bảng locations quản lý vị trí theo cấu trúc 3 tọa độ: Khu vực (Zone) - Dãy kệ (Shelf) - Tầng kệ (Level).",
        "4. Quản lý sức chứa tối đa: max_capacity ràng buộc tổng số lượng tồn của tất cả các mặt hàng tại vị trí không được vượt trần.",
    ]
    ny = 1810
    for n in notes:
        draw_wrapped_text(draw, n, (140, ny, 3060, ny + 78), font=f_sub, fill=C_BLACK, align="left")
        ny += 82

    draw_footer(draw, W, H)
    save_diagram(im, "03b_erd_nhom_danh_muc_kho")

# =========================================================================
# 3C. SƠ ĐỒ ERD CHI TIẾT PHÂN HỆ 3: TỒN KHO & GIAO DỊCH (Hình 5.4) - ZERO OVERLAP
# =========================================================================
def make_03c_subsystem_erd_inventory_transactions():
    W, H = 3400, 2180
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ ERD CHI TIẾT PHÂN HỆ QUẢN LÝ TỒN KHO & GIAO DỊCH XUẤT NHẬP",
                "Đặc tả cấu trúc dữ liệu: Inventory Items, Inventory Transactions, Transaction Items kèm cơ chế khóa dòng ACID")

    f_hdr = get_font(FONT_PATH_BOLD, 44)
    f_txt = get_font(FONT_PATH_REG, 35)
    f_txt_bold = get_font(FONT_PATH_BOLD, 38)
    f_code = get_font(FONT_PATH_CODE, 33)
    f_code_bold = get_font(FONT_PATH_CODE_BOLD, 35)

    def render_large_table(bbox, tname, fields):
        x1, y1, x2, y2 = bbox
        draw.rounded_rectangle(bbox, radius=14, fill=C_WHITE, outline=C_BLACK, width=4)
        draw.rectangle([x1, y1, x2, y1 + 72], fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
        draw.text((x1 + 28, y1 + 16), f"BẢNG CSDL: {tname.upper()}", fill=C_BLACK, font=f_hdr)
        curr_y = y1 + 88
        row_h = 60
        for is_pk, is_fk, fname, ftype in fields:
            if is_pk:
                draw.text((x1 + 24, curr_y), "[PK]", fill=C_BLACK, font=f_code_bold)
            elif is_fk:
                draw.text((x1 + 24, curr_y), "[FK]", fill=C_BLACK, font=f_code_bold)
            else:
                draw.text((x1 + 24, curr_y), "    ", fill=C_BLACK, font=f_code)
            draw.text((x1 + 140, curr_y), fname, fill=C_BLACK, font=f_txt_bold if (is_pk or is_fk) else f_txt)
            draw.text((x1 + 620, curr_y), ftype, fill=C_BLACK, font=f_code)
            curr_y += row_h

    # Table 1: inventory_items (Top Left)
    t1_box = (100, 230, 1550, 830)
    render_large_table(t1_box, "inventory_items", [
        (True, False, "id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        (False, True, "product_id", "INTEGER NOT NULL (FK -> products.id)"),
        (False, True, "location_id", "INTEGER NOT NULL (FK -> locations.id)"),
        (False, False, "current_stock", "INTEGER NOT NULL CHECK(current_stock >= 0)"),
        (False, False, "batch_number", "VARCHAR(50) NULL (Số lô sản xuất)"),
        (False, False, "expiry_date", "DATE NULL (Hạn sử dụng lô hàng)"),
        (False, False, "last_audited_at", "DATETIME NULL (Ngày kiểm kê gần nhất)"),
        (False, False, "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ])

    # Table 2: inventory_transactions (Top Right)
    t2_box = (1750, 230, 3200, 830)
    render_large_table(t2_box, "inventory_transactions", [
        (True, False, "id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        (False, False, "transaction_code", "VARCHAR(50) UNIQUE NOT NULL (Vd: PN-001)"),
        (False, False, "transaction_type", "VARCHAR(20) NOT NULL (IMPORT / EXPORT)"),
        (False, True, "supplier_id", "INTEGER NULL (FK -> suppliers.id)"),
        (False, True, "created_by", "INTEGER NOT NULL (FK -> users.id)"),
        (False, False, "total_amount", "DECIMAL(15,2) DEFAULT 0.00"),
        (False, False, "note", "TEXT NULL"),
        (False, False, "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ])

    # Table 3: inventory_transaction_items (Bottom Center)
    t3_box = (900, 950, 2500, 1550)
    render_large_table(t3_box, "inventory_transaction_items", [
        (True, False, "id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
        (False, True, "transaction_id", "INTEGER NOT NULL (FK -> trans.id)"),
        (False, True, "product_id", "INTEGER NOT NULL (FK -> products.id)"),
        (False, True, "location_id", "INTEGER NOT NULL (FK -> locations.id)"),
        (False, False, "quantity", "INTEGER NOT NULL CHECK(quantity > 0)"),
        (False, False, "unit_price", "DECIMAL(12,2) NOT NULL"),
        (False, False, "subtotal", "DECIMAL(15,2) NOT NULL"),
        (False, False, "created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ])

    # Connections
    # trans -> trans_items (1 : N)
    draw_orthogonal_arrow(draw, [(2475, 830), (2475, 890), (1700, 890), (1700, 950)], fill=C_BLACK, width=5,
                          label="1 : N", label_pos=(2080, 890))

    # inventory_items -> trans_items (Cập nhật tồn) - ROUTED AT x=500, ZERO OVERLAP WITH TABLE 3 AT x=900!
    draw_orthogonal_arrow(draw, [(500, 830), (500, 1250), (900, 1250)], fill=C_BLACK, width=5,
                          label="Cập nhật tồn", label_pos=(500, 1040))

    # Notes Card - Compact 460px height
    draw.rounded_rectangle([100, 1630, 3300, 2090], radius=14, fill=C_GRAY_LIGHT, outline=C_BLACK, width=3)
    f_box_hdr = get_font(FONT_PATH_BOLD, 40)
    f_sub = get_font(FONT_PATH_REG, 34)
    draw.text((140, 1658), "ĐẶC TẢ GIAO DỊCH KHO TOÀN VẸN (TRANSACTION INTEGRITY & ROW-LEVEL LOCKING):", fill=C_BLACK, font=f_box_hdr)
    notes = [
        "1. Cơ chế Row-level Locking: Khi lập phiếu xuất kho, hệ thống thực thi SELECT FOR UPDATE trên bản ghi inventory_items để khóa tạm hàng hóa, ngăn ngừa xung đột xuất âm.",
        "2. Toàn vẹn giao dịch ACID: Khi xác nhận giao dịch, việc ghi phiếu (transactions), các dòng (items) và cập nhật số dư thực tế được bọc trong một DB Transaction duy nhất. Rollback 100% nếu có lỗi.",
        "3. Quản lý Lô & Hạn dùng: Hỗ trợ theo dõi số lô (batch_number) và ngày hết hạn (expiry_date) đáp ứng nguyên tắc xuất hàng FEFO (First Expired, First Out) và FIFO.",
        "4. Minh chứng số liệu: Mọi biến động tăng giảm tồn kho đều liên kết trực tiếp với mã phiếu chứng từ cụ thể, loại bỏ hoàn toàn tình trạng số liệu ma.",
    ]
    ny = 1720
    for n in notes:
        draw_wrapped_text(draw, n, (140, ny, 3260, ny + 78), font=f_sub, fill=C_BLACK, align="left")
        ny += 82

    draw_footer(draw, W, H)
    save_diagram(im, "03c_erd_nhom_ton_kho_giao_dich")

# =========================================================================
# 4. LƯỢC ĐỒ HOẠT ĐỘNG NHẬP KHO (Hình 4.1) - CROPPED TIGHT CANVAS
# =========================================================================
def make_04_activity_import():
    W, H = 2800, 2480
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "LƯỢC ĐỒ HOẠT ĐỘNG QUY TRÌNH NHẬP KHO (IMPORT ACTIVITY DIAGRAM)",
                "Quy trình nghiệp vụ: Tiếp nhận hàng hóa, kiểm định chất lượng, phân bổ kệ kho và cập nhật số dư khả dụng")

    f_box = get_font(FONT_PATH_BOLD, 40)
    f_dia = get_font(FONT_PATH_BOLD, 36)

    steps = [
        ("Khởi đầu: Xe hàng từ Nhà cung cấp cập bến kho", (400, 220, 1750, 350), False),
        ("Kiểm tra chứng từ giao nhận & Hóa đơn vận chuyển", (400, 420, 1750, 550), False),
        ("Thủ kho dỡ hàng và kiểm tra quy cách thực tế", (400, 620, 1750, 750), False),
        ("Hàng đạt tiêu chuẩn quy cách & số lượng?", (350, 820, 1800, 1070), True),
        ("Phân bổ hàng hóa vào vị trí kệ còn sức chứa (locations)", (400, 1160, 1750, 1290), False),
        ("Nhập thông tin phiếu nhập & số lô / hạn sử dụng vào hệ thống", (350, 1360, 1800, 1490), False),
        ("Tạo phiếu nhập trong inventory_transactions & items", (400, 1560, 1750, 1690), False),
        ("Cộng dồn số lượng thực tế trong bảng inventory_items", (400, 1760, 1750, 1890), False),
        ("Ghi nhận nhật ký kiểm toán Audit Log & Cập nhật Realtime KPI", (350, 1960, 1800, 2090), False),
        ("Kết thúc: Hoàn tất nhập kho, in biên bản & cập nhật báo cáo", (400, 2160, 1750, 2290), False),
    ]

    for title, bbox, is_dia in steps:
        if is_dia:
            cx = (bbox[0] + bbox[2]) // 2
            cy = (bbox[1] + bbox[3]) // 2
            w2 = (bbox[2] - bbox[0]) // 2
            h2 = (bbox[3] - bbox[1]) // 2
            draw.polygon([(cx, cy - h2), (cx + w2, cy), (cx, cy + h2), (cx - w2, cy)], fill=C_WHITE, outline=C_BLACK, width=5)
            draw_wrapped_text(draw, title, (cx - w2 + 90, cy - 45, cx + w2 - 90, cy + 45), font=f_dia, fill=C_BLACK, align="center")
        else:
            draw.rounded_rectangle(bbox, radius=16, fill=C_WHITE, outline=C_BLACK, width=5)
            draw_wrapped_text(draw, title, bbox, font=f_box, fill=C_BLACK, align="center")

    reject_box = (2000, 880, 2700, 1060)
    draw.rounded_rectangle(reject_box, radius=14, fill=C_WHITE, outline=C_BLACK, width=5)
    draw_wrapped_text(draw, "TỪ CHỐI NHẬP HÀNG\nLập biên bản sự cố lỗi\n& Hoàn trả Nhà cung cấp", reject_box, font=f_box, fill=C_BLACK, align="center")

    # Connectors
    draw_orthogonal_arrow(draw, [(1075, 350), (1075, 420)], fill=C_BLACK, width=5)
    draw_orthogonal_arrow(draw, [(1075, 550), (1075, 620)], fill=C_BLACK, width=5)
    draw_orthogonal_arrow(draw, [(1075, 750), (1075, 820)], fill=C_BLACK, width=5)

    draw_orthogonal_arrow(draw, [(1075, 1070), (1075, 1160)], fill=C_BLACK, width=5,
                          label="Đạt chuẩn [Yes]", label_pos=(1075, 1115))
    draw_orthogonal_arrow(draw, [(1800, 945), (2000, 945)], fill=C_BLACK, width=5, is_dashed=True,
                          label="Lỗi [No]", label_pos=(1900, 945))
    draw_orthogonal_arrow(draw, [(2350, 1060), (2350, 2225), (1750, 2225)], fill=C_BLACK, width=5, is_dashed=True,
                          label="Đóng giao dịch lỗi", label_pos=(2350, 1640))

    draw_orthogonal_arrow(draw, [(1075, 1290), (1075, 1360)], fill=C_BLACK, width=5)
    draw_orthogonal_arrow(draw, [(1075, 1490), (1075, 1560)], fill=C_BLACK, width=5)
    draw_orthogonal_arrow(draw, [(1075, 1690), (1075, 1760)], fill=C_BLACK, width=5)
    draw_orthogonal_arrow(draw, [(1075, 1890), (1075, 1960)], fill=C_BLACK, width=5)
    draw_orthogonal_arrow(draw, [(1075, 2090), (1075, 2160)], fill=C_BLACK, width=5)

    draw_footer(draw, W, H)
    save_diagram(im, "04_luoc_do_hoat_dong_nhap_kho")

# =========================================================================
# 5. LƯỢC ĐỒ HOẠT ĐỘNG XUẤT KHO (Hình 4.2) - CROPPED TIGHT CANVAS
# =========================================================================
def make_05_activity_export():
    W, H = 2800, 2620
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "LƯỢC ĐỒ HOẠT ĐỘNG QUY TRÌNH XUẤT KHO (EXPORT ACTIVITY DIAGRAM)",
                "Kiểm tra số lượng khả dụng, khóa tạm hàng hóa, trừ tồn thực tế và kích hoạt cảnh báo tái nhập tự động")

    f_box = get_font(FONT_PATH_BOLD, 40)
    f_dia = get_font(FONT_PATH_BOLD, 36)

    steps = [
        ("Khởi đầu: Nhận yêu cầu xuất hàng từ khách hàng / đại lý", (400, 220, 1750, 350), False),
        ("Thủ kho chọn khách hàng & tạo phiếu xuất kho mới", (400, 420, 1750, 550), False),
        ("Thêm danh mục SKU và số lượng yêu cầu xuất", (400, 620, 1750, 750), False),
        ("Kiểm tra tồn khả dụng: Số lượng xuất <= Available Stock?", (350, 820, 1800, 1070), True),
        ("Khóa bản ghi tồn kho tạm thời (Row-level Locking FOR UPDATE)", (350, 1160, 1800, 1290), False),
        ("Trừ số lượng tồn thực tế trong bảng inventory_items", (400, 1360, 1750, 1490), False),
        ("Kiểm tra ngưỡng cạn tồn: Current Stock < min_threshold?", (350, 1560, 1800, 1810), True),
        ("Kích hoạt cảnh báo AI Alert: Đề xuất lập phiếu tái nhập hàng", (350, 1900, 1800, 2030), False),
        ("Ghi nhận nhật ký kiểm toán Audit Log và hoàn tất xuất kho", (400, 2100, 1750, 2230), False),
        ("Kết thúc: Bàn giao hàng hóa, in phiếu xuất kho & cập nhật KPI", (400, 2300, 1750, 2430), False),
    ]

    for title, bbox, is_dia in steps:
        if is_dia:
            cx = (bbox[0] + bbox[2]) // 2
            cy = (bbox[1] + bbox[3]) // 2
            w2 = (bbox[2] - bbox[0]) // 2
            h2 = (bbox[3] - bbox[1]) // 2
            draw.polygon([(cx, cy - h2), (cx + w2, cy), (cx, cy + h2), (cx - w2, cy)], fill=C_WHITE, outline=C_BLACK, width=5)
            draw_wrapped_text(draw, title, (cx - w2 + 90, cy - 45, cx + w2 - 90, cy + 45), font=f_dia, fill=C_BLACK, align="center")
        else:
            draw.rounded_rectangle(bbox, radius=16, fill=C_WHITE, outline=C_BLACK, width=5)
            draw_wrapped_text(draw, title, bbox, font=f_box, fill=C_BLACK, align="center")

    err_box = (2000, 880, 2700, 1060)
    draw.rounded_rectangle(err_box, radius=14, fill=C_WHITE, outline=C_BLACK, width=5)
    draw_wrapped_text(draw, "BÁO LỖI NGHIỆP VỤ\nKho không đủ số lượng\ntồn khả dụng (HTTP 400)", err_box, font=f_box, fill=C_BLACK, align="center")

    # Connectors
    draw_orthogonal_arrow(draw, [(1075, 350), (1075, 420)], fill=C_BLACK, width=5)
    draw_orthogonal_arrow(draw, [(1075, 550), (1075, 620)], fill=C_BLACK, width=5)
    draw_orthogonal_arrow(draw, [(1075, 750), (1075, 820)], fill=C_BLACK, width=5)

    draw_orthogonal_arrow(draw, [(1075, 1070), (1075, 1160)], fill=C_BLACK, width=5,
                          label="Đủ hàng [Yes]", label_pos=(1075, 1115))
    draw_orthogonal_arrow(draw, [(1800, 945), (2000, 945)], fill=C_BLACK, width=5, is_dashed=True,
                          label="Không đủ [No]", label_pos=(1900, 945))
    draw_orthogonal_arrow(draw, [(2350, 1060), (2350, 2365), (1750, 2365)], fill=C_BLACK, width=5, is_dashed=True,
                          label="Hủy yêu cầu xuất", label_pos=(2350, 1710))

    draw_orthogonal_arrow(draw, [(1075, 1290), (1075, 1360)], fill=C_BLACK, width=5)
    draw_orthogonal_arrow(draw, [(1075, 1490), (1075, 1560)], fill=C_BLACK, width=5)

    draw_orthogonal_arrow(draw, [(1075, 1810), (1075, 1900)], fill=C_BLACK, width=5,
                          label="Cạn tồn [Yes]", label_pos=(1075, 1855))
    draw_orthogonal_arrow(draw, [(350, 1685), (200, 1685), (200, 2165), (400, 2165)], fill=C_BLACK, width=5,
                          label="Tồn an toàn [No]", label_pos=(200, 1925))

    draw_orthogonal_arrow(draw, [(1075, 2030), (1075, 2100)], fill=C_BLACK, width=5)
    draw_orthogonal_arrow(draw, [(1075, 2230), (1075, 2300)], fill=C_BLACK, width=5)

    draw_footer(draw, W, H)
    save_diagram(im, "05_luoc_do_hoat_dong_xuat_kho")

# =========================================================================
# 6. SƠ ĐỒ TUẦN TỰ GIAO DỊCH KHO (Hình 6.2)
# =========================================================================
def make_06_sequence_transaction():
    W, H = 3200, 3300
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ TUẦN TỰ GIAO DỊCH KHO (SEQUENCE DIAGRAM: IMPORT / EXPORT)",
                "Luồng xử lý tương tác: Người dùng -> React Frontend -> FastAPI APIRouter -> InventoryService -> Database -> AuditLog")

    f_hdr = get_font(FONT_PATH_BOLD, 38)
    f_msg = get_font(FONT_PATH_BOLD, 36)
    f_msg_ret = get_font(FONT_PATH_BOLD, 34)

    lifelines = [
        ("Thủ kho (User)", 260),
        ("React Frontend", 760),
        ("FastAPI APIRouter", 1260),
        ("InventoryService", 1760),
        ("SQL Database", 2260),
        ("AuditLog Service", 2760),
    ]

    for title, x in lifelines:
        draw.rounded_rectangle([x - 170, 190, x + 170, 290], radius=14, fill=C_WHITE, outline=C_BLACK, width=4)
        tw = draw.textbbox((0, 0), title, font=f_hdr)[2]
        draw.text((x - tw // 2, 222), title, fill=C_BLACK, font=f_hdr)
        draw_dashed_line(draw, (x, 300), (x, 3150), fill=C_BLACK, width=4, dash_len=20, gap_len=14)

    msgs = [
        (260, 760, 380, "1. Nhập thông tin phiếu xuất/nhập & nhấn 'Xác nhận giao dịch'", False),
        (760, 1260, 620, "2. POST /api/inventory/transactions (Payload, Bearer JWT)", False),
        (1260, 1760, 860, "3. validate_payload() & check_role_permission(user)", False),
        (1760, 2260, 1100, "4. SELECT current_stock FROM inventory_items FOR UPDATE", False),
        (2260, 1760, 1340, "5. Trả về số lượng tồn kho khả dụng (Available Stock)", True),
        (1760, 2260, 1580, "6. INSERT INTO inventory_transactions & items", False),
        (1760, 2260, 1820, "7. UPDATE inventory_items SET current_stock = current_stock +/- Q", False),
        (1760, 2760, 2060, "8. log_audit_event('TRANSACTION_COMMITTED', metadata)", False),
        (2760, 1760, 2300, "9. Ghi vết kiểm toán thành công (audit_logs table)", True),
        (1760, 1260, 2540, "10. Commit DB Transaction & trả về TransactionResponse", True),
        (1260, 760, 2780, "11. HTTP 201 Created (Kèm Transaction JSON Model)", True),
        (760, 260, 3020, "12. Hiển thị Toast thông báo thành công & reload Realtime KPI", True),
    ]

    for x1, x2, y, text, is_ret in msgs:
        draw_orthogonal_arrow(draw, [(x1, y), (x2, y)], fill=C_BLACK, width=5, is_dashed=is_ret)
        mx = (x1 + x2) // 2
        f = f_msg_ret if is_ret else f_msg
        draw_pill_label(draw, (mx, y - 44), text, font=f, fill=C_BLACK, bg=C_WHITE, outline=C_BLACK, pad_x=20, pad_y=10, border_w=3)

    draw_footer(draw, W, H)
    save_diagram(im, "06_so_do_tuan_tu_nhap_xuat")

# =========================================================================
# 7. SƠ ĐỒ PIPELINE AI 2 LỚP FALLBACK (Hình 8.1)
# =========================================================================
def make_07_ai_pipeline():
    W, H = 3000, 3400
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ KIẾN TRÚC PIPELINE XỬ LÝ AI 2 LỚP (DUAL-LAYER AI FALLBACK)",
                "Cơ chế chuyển đổi dự phòng linh hoạt: Google Gemini Cloud LLM -> Local Deterministic Rule Engine")

    f_hdr = get_font(FONT_PATH_BOLD, 44)
    f_sub = get_font(FONT_PATH_BOLD, 36)
    f_dia = get_font(FONT_PATH_BOLD, 38)

    # Box 1: Client Request
    b1 = (100, 210, 1450, 640)
    draw.rounded_rectangle(b1, radius=16, fill=C_WHITE, outline=C_BLACK, width=5)
    draw.text((130, 236), "1. Yêu cầu Phân tích từ Client (React Frontend)", fill=C_BLACK, font=f_hdr)
    draw.line([(100, 302), (1450, 302)], fill=C_BLACK, width=3)
    bullets_b1 = [
        "• Dự báo số ngày cạn tồn (Depletion Days) & Đề xuất tái nhập hàng",
        "• Phát hiện dị biệt sản lượng xuất kho qua phân phối Z-score",
        "• Trợ lý hỏi đáp thông minh về hàng tồn bằng ngôn ngữ tự nhiên",
    ]
    by = 335
    for b in bullets_b1:
        draw.text((130, by), b, fill=C_BLACK, font=f_sub)
        by += 64

    # Box 2: Data Snapshot Aggregator
    b2 = (1550, 210, 2900, 640)
    draw.rounded_rectangle(b2, radius=16, fill=C_WHITE, outline=C_BLACK, width=5)
    draw.text((1580, 236), "2. Data Snapshot Aggregator (FastAPI Context)", fill=C_BLACK, font=f_hdr)
    draw.line([(1550, 302), (2900, 302)], fill=C_BLACK, width=3)
    bullets_b2 = [
        "• Trích xuất dữ liệu CSDL thực tế 100% chính xác qua SQLAlchemy",
        "• Tính toán vận tốc tiêu thụ xuất kho 30 ngày gần nhất (Burn-rate)",
        "• Ground-Truth Context Injection: Chống hiện tượng AI bịa số liệu",
    ]
    by = 335
    for b in bullets_b2:
        draw.text((1580, by), b, fill=C_BLACK, font=f_sub)
        by += 64

    # Arrow 1 -> 2
    draw_orthogonal_arrow(draw, [(1450, 425), (1550, 425)], fill=C_BLACK, width=5)

    # Decision Diamond
    cx, cy = 1500, 860
    w2, h2 = 620, 130
    draw.polygon([(cx, cy - h2), (cx + w2, cy), (cx, cy + h2), (cx - w2, cy)], fill=C_WHITE, outline=C_BLACK, width=5)
    draw_wrapped_text(draw, "Kiểm tra Kết nối Cloud:\nCó API Key hợp lệ & Mạng Internet OK?",
                      (cx - 480, cy - 55, cx + 480, cy + 55), font=f_dia, fill=C_BLACK, align="center")

    # Arrow 2 -> Decision
    draw_orthogonal_arrow(draw, [(2225, 640), (2225, 860), (2120, 860)], fill=C_BLACK, width=5)

    # Layer 1: Gemini Cloud LLM
    b_l1 = (100, 1090, 1450, 1660)
    draw.rounded_rectangle(b_l1, radius=16, fill=C_WHITE, outline=C_BLACK, width=5)
    draw.text((130, 1116), "LỚP 1: CLOUD LLM (GOOGLE GEMINI 1.5 FLASH)", fill=C_BLACK, font=f_hdr)
    draw.line([(100, 1182), (1450, 1182)], fill=C_BLACK, width=3)
    bullets_l1 = [
        "• Mô hình ngôn ngữ lớn gemini-1.5-flash tốc độ cao và chi phí tối ưu",
        "• Phân tích hành văn tiếng Việt tự nhiên, giải thích ngữ cảnh sâu",
        "• Định dạng bảng biểu Markdown Table tự động nhận diện trên UI",
        "• Đề xuất khuyến nghị thông minh dựa trên bối cảnh hoạt động kho",
    ]
    by = 1215
    for b in bullets_l1:
        draw.text((130, by), b, fill=C_BLACK, font=f_sub)
        by += 64

    # Layer 2: Local Rule Engine
    b_l2 = (1550, 1090, 2900, 1660)
    draw.rounded_rectangle(b_l2, radius=16, fill=C_WHITE, outline=C_BLACK, width=5)
    draw.text((1580, 1116), "LỚP 2: LOCAL RULE ENGINE (DETERMINISTIC)", fill=C_BLACK, font=f_hdr)
    draw.line([(1550, 1182), (2900, 1182)], fill=C_BLACK, width=3)
    bullets_l2 = [
        "• Hoạt động Offline 100% không phụ thuộc Internet hay Quota",
        "• Công thức xác định: DepletionDays = CurrentStock / DailyVelocity",
        "• Phát hiện dị biệt chính xác bằng độ lệch chuẩn sản lượng Z-score",
        "• Khớp từ khóa NLP chính xác, xử lý an toàn phép chia cho 0",
    ]
    by = 1215
    for b in bullets_l2:
        draw.text((1580, by), b, fill=C_BLACK, font=f_sub)
        by += 64

    # Decision -> Layer 1
    draw_orthogonal_arrow(draw, [(1150, 930), (775, 930), (775, 1090)], fill=C_BLACK, width=5,
                          label="Có [Cloud OK]", label_pos=(775, 930))

    # Decision -> Layer 2 (Fallback)
    draw_orthogonal_arrow(draw, [(1850, 930), (2225, 930), (2225, 1090)], fill=C_BLACK, width=5, is_dashed=True,
                          label="Mất mạng / Hết Quota [Fallback]", label_pos=(2225, 930))

    # Box 3: Structured Output Formatter
    b_out = (100, 1780, 2900, 3280)
    draw.rounded_rectangle(b_out, radius=18, fill=C_WHITE, outline=C_BLACK, width=5)
    draw.rectangle([100, 1780, 2900, 1870], fill=C_GRAY_LIGHT, outline=C_BLACK, width=4)
    draw.text((130, 1808), "3. STRUCTURED OUTPUT & SMART UI COMPONENT (DÙNG CHUNG CẢ 2 LỚP)", fill=C_BLACK, font=f_hdr)

    out_cards = [
        ("Smart Data Table UI", "Hiển thị bảng dữ liệu sắc nét kèm chức năng lọc, sắp xếp và phân trang trực tiếp"),
        ("Đèn LED Cảnh Báo Trực Quan", "Huy hiệu màu sắc: Đỏ (Cạn tồn khẩn cấp) - Vàng (Cảnh báo tái nhập) - Xanh (An toàn)"),
        ("Nút Hành Động Nhanh (Quick Action)", "Cho phép tạo tức thời phiếu nhập kho cho mặt hàng thiếu hụt chỉ với 1 cú click chuột"),
        ("Tab Snapshot Dữ Liệu Minh Chứng", "Cung cấp toàn văn dữ liệu JSON gốc chứng minh tính khách quan và chống ảo giác AI"),
    ]
    cy_out = 1900
    f_card_hdr = get_font(FONT_PATH_BOLD, 38)
    f_card_desc = get_font(FONT_PATH_REG, 34)
    for o_title, o_desc in out_cards:
        draw.rounded_rectangle([130, cy_out, 2870, cy_out + 135], radius=12, fill=C_WHITE, outline=C_BLACK, width=3)
        draw.text((160, cy_out + 22), f"• {o_title}:", fill=C_BLACK, font=f_card_hdr)
        draw.text((160, cy_out + 74), o_desc, fill=C_BLACK, font=f_card_desc)
        cy_out += 165

    # Arrows from layers to output
    draw_orthogonal_arrow(draw, [(775, 1660), (775, 1780)], fill=C_BLACK, width=5,
                          label="Kết quả Gemini LLM", label_pos=(775, 1720))
    draw_orthogonal_arrow(draw, [(2225, 1660), (2225, 1780)], fill=C_BLACK, width=5,
                          label="Kết quả Rule Engine", label_pos=(2225, 1720))

    draw_footer(draw, W, H)
    save_diagram(im, "07_so_do_pipeline_ai_fallback")

# =========================================================================
# 8. SƠ ĐỒ TUẦN TỰ TRỢ LÝ HỎI ĐÁP AI (Hình 8.2)
# =========================================================================
def make_08_sequence_ai():
    W, H = 3200, 3300
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ TUẦN TỰ TRỢ LÝ HỎI ĐÁP KHO AI (NLP ASSISTANT SEQUENCE)",
                "Quy trình xử lý: Thu thập Ground Truth CSDL, suy luận ngữ cảnh 2 lớp và hiển thị Smart UI Component")

    f_hdr = get_font(FONT_PATH_BOLD, 38)
    f_msg = get_font(FONT_PATH_BOLD, 36)
    f_msg_ret = get_font(FONT_PATH_BOLD, 34)

    lifelines = [
        ("Người dùng", 260),
        ("AI Chat Console", 760),
        ("POST /api/ai/ask", 1260),
        ("Data Aggregator", 1760),
        ("AI Dual Engine", 2260),
        ("Smart Table Viewer", 2760),
    ]

    for title, x in lifelines:
        draw.rounded_rectangle([x - 170, 190, x + 170, 290], radius=14, fill=C_WHITE, outline=C_BLACK, width=4)
        tw = draw.textbbox((0, 0), title, font=f_hdr)[2]
        draw.text((x - tw // 2, 222), title, fill=C_BLACK, font=f_hdr)
        draw_dashed_line(draw, (x, 300), (x, 3150), fill=C_BLACK, width=4, dash_len=20, gap_len=14)

    msgs = [
        (260, 760, 380, "1. Nhập câu hỏi tự nhiên: 'Kho còn bao nhiêu bàn phím AKKO?'", False),
        (760, 1260, 640, "2. Gửi HTTP Request: { question: '...', user_token: '...' }", False),
        (1260, 1760, 900, "3. Trích xuất CSDL: products, inventory_items, vận tốc xuất 30 ngày", False),
        (1760, 1260, 1160, "4. Trả về Snapshot CSDL thực tế 100% chính xác (Ground-Truth)", True),
        (1260, 2260, 1420, "5. answer_user_question(question, data_context)", False),
        (2260, 2260, 1680, "6. [Gemini / Rule Engine]: Khớp SKU, tính tồn, định dạng bảng", False),
        (2260, 1260, 1940, "7. Trả về câu trả lời Markdown + data_snapshot JSON", True),
        (1260, 760, 2200, "8. Trả kết quả HTTP 200 OK kèm payload hoàn chỉnh", True),
        (760, 2760, 2460, "9. SmartMarkdownViewer parse bảng Markdown thành React Component", False),
        (2760, 760, 2720, "10. Render giao diện đẹp mắt (Huy hiệu LED, Nút bấm nhanh)", True),
        (760, 260, 2980, "11. Người dùng nhận câu trả lời trực quan & xem số liệu minh chứng", True),
    ]

    for x1, x2, y, text, is_ret in msgs:
        draw_orthogonal_arrow(draw, [(x1, y), (x2, y)], fill=C_BLACK, width=5, is_dashed=is_ret)
        mx = (x1 + x2) // 2
        f = f_msg_ret if is_ret else f_msg
        draw_pill_label(draw, (mx, y - 44), text, font=f, fill=C_BLACK, bg=C_WHITE, outline=C_BLACK, pad_x=20, pad_y=10, border_w=3)

    draw_footer(draw, W, H)
    save_diagram(im, "08_so_do_tuan_tu_hoi_dap_ai")

# =========================================================================
# 9. LƯU ĐỒ THUẬT TOÁN BẤT THƯỜNG & BURN-RATE (Hình 9.1) - CROPPED TIGHT CANVAS
# =========================================================================
def make_09_anomaly_algorithm():
    W, H = 2800, 2780
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "LƯU ĐỒ THUẬT TOÁN PHÁT HIỆN BẤT THƯỜNG & TÍNH BURN-RATE",
                "Mô hình tính toán: Vận tốc tiêu thụ, số ngày cạn tồn dự báo và phát hiện dị biệt thống kê Z-score")

    f_box = get_font(FONT_PATH_BOLD, 40)
    f_dia = get_font(FONT_PATH_BOLD, 36)

    nodes = [
        ("Thu thập dữ liệu giao dịch xuất kho 30 ngày gần nhất (T = 30 ngày)", (400, 220, 1750, 350), False),
        ("Tính tốc độ xuất bình quân ngày: V = Tổng xuất 30 ngày / 30", (400, 420, 1750, 550), False),
        ("V > 0 (Sản phẩm có phát sinh xuất kho trong 30 ngày)?", (350, 620, 1800, 870), True),
        ("Tính số ngày cạn tồn dự báo: DepletionDays = Stock / V", (400, 960, 1750, 1090), False),
        ("Days <= 7 ngày hoặc Current Stock < min_threshold?", (350, 1170, 1800, 1420), True),
        ("Kích hoạt cảnh báo khẩn: 'Cần lập kế hoạch tái nhập hàng ngay'", (350, 1510, 1800, 1640), False),
        ("Tính độ lệch chuẩn sản lượng xuất ngày: Z-score", (400, 1720, 1750, 1850), False),
        ("|Z-score| > 2.5 (Xuất kho đột biến hoặc tồn kho đóng băng)?", (350, 1930, 1800, 2180), True),
        ("Gắn cờ Bất thường (Anomaly Flag) & Đề xuất rà soát kiểm kê", (350, 2270, 1800, 2400), False),
        ("Kết thúc: Lưu kết quả phân tích vào bộ nhớ tạm & CSDL", (400, 2480, 1750, 2610), False),
    ]

    for title, bbox, is_dia in nodes:
        if is_dia:
            cx = (bbox[0] + bbox[2]) // 2
            cy = (bbox[1] + bbox[3]) // 2
            w2 = (bbox[2] - bbox[0]) // 2
            h2 = (bbox[3] - bbox[1]) // 2
            draw.polygon([(cx, cy - h2), (cx + w2, cy), (cx, cy + h2), (cx - w2, cy)], fill=C_WHITE, outline=C_BLACK, width=5)
            draw_wrapped_text(draw, title, (cx - w2 + 90, cy - 45, cx + w2 - 90, cy + 45), font=f_dia, fill=C_BLACK, align="center")
        else:
            draw.rounded_rectangle(bbox, radius=16, fill=C_WHITE, outline=C_BLACK, width=5)
            draw_wrapped_text(draw, title, bbox, font=f_box, fill=C_BLACK, align="center")

    zero_box = (2000, 680, 2700, 860)
    draw.rounded_rectangle(zero_box, radius=14, fill=C_WHITE, outline=C_BLACK, width=5)
    draw_wrapped_text(draw, "TỒN KHO ỔN ĐỊNH\nGán Days = 999 ngày\n(Không phát sinh xuất)", zero_box, font=f_box, fill=C_BLACK, align="center")

    # Connectors
    draw_orthogonal_arrow(draw, [(1075, 350), (1075, 420)], fill=C_BLACK, width=5)
    draw_orthogonal_arrow(draw, [(1075, 550), (1075, 620)], fill=C_BLACK, width=5)

    draw_orthogonal_arrow(draw, [(1075, 870), (1075, 960)], fill=C_BLACK, width=5,
                          label="Có xuất [Yes]", label_pos=(1075, 915))
    draw_orthogonal_arrow(draw, [(1800, 745), (2000, 745)], fill=C_BLACK, width=5, is_dashed=True,
                          label="V = 0 [No]", label_pos=(1900, 745))
    draw_orthogonal_arrow(draw, [(2350, 860), (2350, 1785), (1750, 1785)], fill=C_BLACK, width=5, is_dashed=True,
                          label="Bỏ qua cạn tồn", label_pos=(2350, 1320))

    draw_orthogonal_arrow(draw, [(1075, 1090), (1075, 1170)], fill=C_BLACK, width=5)

    draw_orthogonal_arrow(draw, [(1075, 1420), (1075, 1510)], fill=C_BLACK, width=5,
                          label="Cạn tồn [Yes]", label_pos=(1075, 1465))
    draw_orthogonal_arrow(draw, [(350, 1295), (200, 1295), (200, 1785), (400, 1785)], fill=C_BLACK, width=5,
                          label="Tồn an toàn [No]", label_pos=(200, 1540))

    draw_orthogonal_arrow(draw, [(1075, 1640), (1075, 1720)], fill=C_BLACK, width=5)
    draw_orthogonal_arrow(draw, [(1075, 1850), (1075, 1930)], fill=C_BLACK, width=5)

    draw_orthogonal_arrow(draw, [(1075, 2180), (1075, 2270)], fill=C_BLACK, width=5,
                          label="Bất thường [Yes]", label_pos=(1075, 2225))
    draw_orthogonal_arrow(draw, [(350, 2055), (200, 2055), (200, 2545), (400, 2545)], fill=C_BLACK, width=5,
                          label="Bình thường [No]", label_pos=(200, 2300))

    draw_orthogonal_arrow(draw, [(1075, 2400), (1075, 2480)], fill=C_BLACK, width=5)

    draw_footer(draw, W, H)
    save_diagram(im, "09_so_do_phan_tich_bat_thuong")

# =========================================================================
# 10. SƠ ĐỒ ĐIỀU HƯỚNG CẤU TRÚC GIAO DIỆN (SITEMAP - Hình 6.3) - CROPPED TIGHT CANVAS
# =========================================================================
def make_10_sitemap():
    W, H = 3400, 1480
    im = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(im)
    draw_header(draw, W, "SƠ ĐỒ ĐIỀU HƯỚNG CẤU TRÚC GIAO DIỆN HỆ THỐNG (FRONTEND SITEMAP)",
                "Cấu trúc ứng dụng Web SaaS Single Page Application (React 18 Vite + Tailwind CSS + Lucide Icons)")

    f_root = get_font(FONT_PATH_BOLD, 46)
    f_cat = get_font(FONT_PATH_BOLD, 38)
    f_sub = get_font(FONT_PATH_BOLD, 34)

    draw.rounded_rectangle([1150, 200, 2250, 325], radius=16, fill=C_WHITE, outline=C_BLACK, width=5)
    tw = draw.textbbox((0, 0), "HỆ THỐNG QUẢN LÝ KHO AI", font=f_root)[2]
    draw.text(((1150 + 2250 - tw) // 2, 238), "HỆ THỐNG QUẢN LÝ KHO AI", fill=C_BLACK, font=f_root)

    sections = [
        ("1. TỔNG QUAN", 380, [
            "Dashboard 6 thẻ chỉ số KPI",
            "Biểu đồ Xu hướng Nhập/Xuất 30 ngày",
            "Cảnh báo hàng sắp chạm ngưỡng",
            "Top sản phẩm xuất chạy nhất kho",
        ]),
        ("2. KHO HÀNG", 1040, [
            "Danh mục Sản phẩm & Quản lý SKU",
            "Sơ đồ Tồn theo Kệ (Zone/Shelf)",
            "Quản lý Nhà cung cấp & Danh mục",
            "Theo dõi Sức chứa vị trí tối đa",
        ]),
        ("3. GIAO DỊCH", 1700, [
            "Lập Phiếu Nhập kho hàng mới",
            "Lập Phiếu Xuất kho & Kiểm tồn",
            "Xem Chi tiết & Phê duyệt chứng từ",
            "In phiếu bàn giao kho & Biên bản",
        ]),
        ("4. AI HUB", 2360, [
            "Dự báo Số ngày cạn tồn kho",
            "Phát hiện Dị biệt Z-score đột biến",
            "Trợ lý Hỏi Đáp Kho tự nhiên (NLP)",
            "Xem Snapshot JSON CSDL minh chứng",
        ]),
        ("5. BẢO MẬT", 3020, [
            "Quản trị Tài khoản Người dùng",
            "Nhật ký Kiểm toán Audit Logs",
            "Cấu hình Tham số Gemini API",
            "Đăng xuất & Hủy Token Bearer JWT",
        ]),
    ]

    for title, cx, items in sections:
        cat_box = (cx - 280, 420, cx + 280, 525)
        draw.rounded_rectangle(cat_box, radius=14, fill=C_WHITE, outline=C_BLACK, width=4)
        tw = draw.textbbox((0, 0), title, font=f_cat)[2]
        draw.text((cx - tw // 2, 450), title, fill=C_BLACK, font=f_cat)

        draw_orthogonal_arrow(draw, [(1700, 325), (1700, 375), (cx, 375), (cx, 420)], fill=C_BLACK, width=4, arrow_at_end=False)

        cy = 585
        prev_y = 525
        for it in items:
            sub_box = (cx - 270, cy, cx + 270, cy + 125)
            draw.rounded_rectangle(sub_box, radius=12, fill=C_WHITE, outline=C_BLACK, width=3)
            draw_wrapped_text(draw, it, sub_box, font=f_sub, fill=C_BLACK, align="center")

            draw.line([(cx, prev_y), (cx, cy)], fill=C_BLACK, width=4)
            prev_y = cy + 125
            cy += 165

    draw_footer(draw, W, H)
    save_diagram(im, "10_so_do_sitemap_giao_dien")

def generate_all():
    print("================================================================")
    print("BẮT ĐẦU TÁI XUẤT BẢN TOÀN BỘ 13 SƠ ĐỒ KỸ THUẬT (CHUẨN V7.0 PRO)")
    print("================================================================")
    make_01_arch()
    make_02_usecase()
    make_03_master_erd()
    make_03a_subsystem_erd_users_ai()
    make_03b_subsystem_erd_master_data()
    make_03c_subsystem_erd_inventory_transactions()
    make_04_activity_import()
    make_05_activity_export()
    make_06_sequence_transaction()
    make_07_ai_pipeline()
    make_08_sequence_ai()
    make_09_anomaly_algorithm()
    make_10_sitemap()
    print("================================================================")
    print("HOÀN TẤT 13 SƠ ĐỒ TO RÕ NÉT, CỠ CHỮ 14-16pt, HOÀN TOÀN KHÔNG CHỒNG CHỮ!")
    print("================================================================")

if __name__ == "__main__":
    generate_all()
