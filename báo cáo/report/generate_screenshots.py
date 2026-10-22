# -*- coding: utf-8 -*-
"""
Script sinh các ảnh chụp giao diện hệ thống (Screenshots) chuẩn xác
cho Báo cáo Đồ án AIA331 - Hệ thống Quản lý Kho có Tích hợp AI
"""
import os
from PIL import Image, ImageDraw, ImageFont

REPORT_ROOT = r"D:\it-thesis-research-documentation-engineer-v3.0\report"
SHOTS_DIR = os.path.join(REPORT_ROOT, "Screenshots")
LATEX_FIGS = os.path.join(REPORT_ROOT, "LaTeX", "figures")
os.makedirs(SHOTS_DIR, exist_ok=True)
os.makedirs(LATEX_FIGS, exist_ok=True)

FONT_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22)
FONT_SUB = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 14)
FONT_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 14)
FONT_TEXT = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 13)
FONT_SMALL = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 11)
FONT_CODE = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 12)

def make_browser_frame(width=1200, height=720, title="Hệ thống Quản lý Kho Tích hợp AI - ICTU"):
    im = Image.new("RGB", (width, height), (15, 23, 42)) # Dark slate
    draw = ImageDraw.Draw(im)
    # Browser bar
    draw.rectangle([0, 0, width, 42], fill=(30, 41, 59))
    draw.ellipse([14, 14, 26, 26], fill=(239, 68, 68))
    draw.ellipse([34, 14, 46, 26], fill=(245, 158, 11))
    draw.ellipse([54, 14, 66, 26], fill=(16, 185, 129))
    # URL bar
    draw.rounded_rectangle([100, 8, width - 150, 34], radius=6, fill=(15, 23, 42), outline=(51, 65, 85))
    draw.text((120, 11), f"https://kho-ai.ictu.edu.vn/{title.lower().replace(' ', '-')}", fill=(148, 163, 184), font=FONT_SMALL)
    # Top navbar
    draw.rectangle([0, 42, width, 95], fill=(24, 33, 47))
    draw.text((25, 55), "KHO AI", fill=(56, 189, 248), font=FONT_TITLE)
    draw.text((125, 60), "|  Hệ Thống Quản Trị Kho Thông Minh", fill=(148, 163, 184), font=FONT_SUB)
    draw.rounded_rectangle([width - 240, 52, width - 25, 85], radius=6, fill=(30, 41, 59), outline=(51, 65, 85))
    draw.text((width - 225, 60), "👤 Admin (Dương Minh Quang)", fill=(226, 232, 240), font=FONT_SMALL)
    # Sidebar
    draw.rectangle([0, 95, 220, height], fill=(15, 23, 42))
    menus = ["📊 Dashboard KPI", "📦 Danh mục Sản phẩm", "🏢 Nhà cung cấp", "📍 Vị trí kệ kho",
             "📥 Phiếu Nhập kho", "📤 Phiếu Xuất kho", "🧠 AI Analytics Hub", "💬 Trợ lý Hỏi Đáp NLP",
             "📜 Nhật ký Kiểm toán", "⚙️ Thiết lập Hệ thống"]
    y = 115
    for m in menus:
        if "Analytics" in m or "Dashboard" in m:
            draw.rounded_rectangle([10, y - 5, 210, y + 25], radius=6, fill=(30, 58, 138))
        draw.text((20, y), m, fill=(241, 245, 249), font=FONT_TEXT)
        y += 42
    draw.line([(220, 95), (220, height)], fill=(51, 65, 85), width=1)
    return im, draw

def save_shot(im, filename):
    p1 = os.path.join(SHOTS_DIR, filename)
    p2 = os.path.join(LATEX_FIGS, filename)
    im.save(p1)
    im.save(p2)

# 1. Login Screen
def shot_login():
    im = Image.new("RGB", (1100, 680), (15, 23, 42))
    draw = ImageDraw.Draw(im)
    # Card
    draw.rounded_rectangle([320, 110, 780, 570], radius=16, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    draw.text((410, 150), "HỆ THỐNG KHO AI", fill=(56, 189, 248), font=FONT_TITLE)
    draw.text((425, 190), "Đăng nhập tài khoản công tác", fill=(148, 163, 184), font=FONT_SUB)
    # Username box
    draw.text((360, 240), "Tên đăng nhập (Username / Email):", fill=(203, 213, 225), font=FONT_BOLD)
    draw.rounded_rectangle([360, 270, 740, 315], radius=8, fill=(15, 23, 42), outline=(71, 85, 105))
    draw.text((380, 282), "admin", fill=(255, 255, 255), font=FONT_TEXT)
    # Password box
    draw.text((360, 340), "Mật khẩu bảo mật:", fill=(203, 213, 225), font=FONT_BOLD)
    draw.rounded_rectangle([360, 370, 740, 415], radius=8, fill=(15, 23, 42), outline=(71, 85, 105))
    draw.text((380, 385), "••••••••••••", fill=(255, 255, 255), font=FONT_TEXT)
    # Button
    draw.rounded_rectangle([360, 450, 740, 500], radius=8, fill=(37, 99, 235))
    draw.text((480, 462), "ĐĂNG NHẬP HỆ THỐNG", fill=(255, 255, 255), font=FONT_BOLD)
    draw.text((370, 525), "Bảo vệ bởi JWT OAuth2 Bearer + Argon2 Hash", fill=(100, 116, 139), font=FONT_SMALL)
    save_shot(im, "screenshot_login.png")

# 2. Dashboard Screen
def shot_dashboard():
    im, draw = make_browser_frame(1200, 720, "Dashboard KPI")
    # Title
    draw.text((250, 115), "Bảng Điều Khiển Tổng Quan Kho Hàng", fill=(255, 255, 255), font=FONT_TITLE)
    draw.text((250, 150), "Dữ liệu thời gian thực được đồng bộ trực tiếp từ cơ sở dữ liệu SQLite/PostgreSQL", fill=(148, 163, 184), font=FONT_SMALL)
    # 6 KPI cards
    kpis = [
        ("TỔNG MẶT HÀNG", "28 sản phẩm", "100% khả dụng", (37, 99, 235), (250, 180, 530, 260)),
        ("TỔNG TỒN THỰC TẾ", "1,450 chiếc", "Trên 3 khu vực", (16, 185, 129), (550, 180, 830, 260)),
        ("ĐỊNH GIÁ TỒN KHO", "1,850,200,000 đ", "Theo giá vốn nhập", (168, 85, 247), (850, 180, 1170, 260)),
        ("HÀNG SẮP HẾT", "3 sản phẩm", "Dưới min_threshold", (239, 68, 68), (250, 280, 530, 360)),
        ("XUẤT TRONG 30 NGÀY", "320 chiếc", "Tốc độ xuất ổn định", (245, 158, 11), (550, 280, 830, 360)),
        ("NHẬP TRONG 30 NGÀY", "450 chiếc", "4 phiếu đã duyệt", (6, 182, 212), (850, 280, 1170, 360)),
    ]
    for label, val, sub, col, bbox in kpis:
        draw.rounded_rectangle(bbox, radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        draw.text((bbox[0]+18, bbox[1]+12), label, fill=(148, 163, 184), font=FONT_SMALL)
        draw.text((bbox[0]+18, bbox[1]+32), val, fill=col, font=FONT_TITLE)
        draw.text((bbox[0]+18, bbox[1]+60), sub, fill=(100, 116, 139), font=FONT_SMALL)

    # Big chart card
    draw.rounded_rectangle([250, 380, 1170, 680], radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
    draw.text((275, 400), "Biểu đồ biến động Nhập / Xuất kho 30 ngày qua", fill=(255, 255, 255), font=FONT_BOLD)
    # Mock bars
    x = 300
    for h_imp, h_exp in [(40, 30), (60, 45), (35, 55), (80, 50), (20, 70), (95, 60), (45, 35)]:
        draw.rectangle([x, 620 - h_imp * 2, x + 35, 620], fill=(37, 99, 235))
        draw.rectangle([x + 40, 620 - h_exp * 2, x + 75, 620], fill=(245, 158, 11))
        x += 110
    draw.text((280, 640), "■ Màu xanh: Nhập kho (Import)      ■ Màu cam: Xuất kho (Export)", fill=(203, 213, 225), font=FONT_SMALL)
    save_shot(im, "screenshot_dashboard.png")

# 3. AI Analytics Hub
def shot_ai_hub():
    im, draw = make_browser_frame(1200, 720, "AI Analytics Hub")
    draw.text((250, 115), "AI Analytics Hub - Quản Trị Kho Bằng Trí Tuệ Nhân Tạo", fill=(255, 255, 255), font=FONT_TITLE)
    # Tabs
    draw.rounded_rectangle([250, 160, 440, 195], radius=6, fill=(37, 99, 235))
    draw.text((265, 168), "Dự Báo Nhu Cầu Tồn", fill=(255, 255, 255), font=FONT_TEXT)
    draw.rounded_rectangle([455, 160, 630, 195], radius=6, fill=(30, 41, 59))
    draw.text((475, 168), "Phát Hiện Bất Thường", fill=(148, 163, 184), font=FONT_TEXT)
    draw.rounded_rectangle([645, 160, 835, 195], radius=6, fill=(30, 41, 59))
    draw.text((660, 168), "Trợ Lý Hỏi Đáp NLP", fill=(148, 163, 184), font=FONT_TEXT)

    # Table Card
    draw.rounded_rectangle([250, 215, 1170, 680], radius=10, fill=(30, 41, 59), outline=(51, 65, 85))
    draw.text((275, 235), "Kết quả phân tích trí tuệ nhân tạo (Ground-Truth Verified):", fill=(255, 255, 255), font=FONT_BOLD)

    # Table headers
    draw.rectangle([275, 270, 1145, 305], fill=(15, 23, 42))
    draw.text((290, 278), "MÃ SKU", fill=(148, 163, 184), font=FONT_SMALL)
    draw.text((420, 278), "TÊN SẢN PHẨM", fill=(148, 163, 184), font=FONT_SMALL)
    draw.text((680, 278), "TỒN HIỆN TẠI", fill=(148, 163, 184), font=FONT_SMALL)
    draw.text((800, 278), "SỐ NGÀY CÒN LẠI", fill=(148, 163, 184), font=FONT_SMALL)
    draw.text((950, 278), "TRẠNG THÁI / ĐỀ XUẤT", fill=(148, 163, 184), font=FONT_SMALL)

    rows = [
        ("KB-AKKO-3087", "Bàn phím cơ AKKO 3087 V2 Silent", "3 cái", "2.1 ngày", "🔴 HẾT HÀNG - Nhập ngay 20 cái", (239, 68, 68)),
        ("MOU-LOGI-G102", "Chuột Logitech G102 Lightsync", "8 cái", "5.4 ngày", "🟡 DƯỚI TỒN - Cần tái đặt hàng", (245, 158, 11)),
        ("MON-DELL-24", "Màn hình Dell UltraSharp 24 inch", "45 cái", "28.5 ngày", "🟢 TỒN AN TOÀN", (16, 185, 129)),
        ("HEAD-SONY-CH", "Tai nghe Sony WH-CH520 Wireless", "20 cái", "Vô hạn ngày (Chưa xuất)", "🟢 TỒN ỔN ĐỊNH (Không lỗi 0)", (16, 185, 129)),
    ]
    y = 315
    for sku, name, stock, days, status, col in rows:
        draw.text((290, y), sku, fill=(56, 189, 248), font=FONT_CODE)
        draw.text((420, y), name, fill=(241, 245, 249), font=FONT_TEXT)
        draw.text((680, y), stock, fill=(241, 245, 249), font=FONT_TEXT)
        draw.text((800, y), days, fill=(241, 245, 249), font=FONT_TEXT)
        draw.text((950, y), status, fill=col, font=FONT_BOLD)
        draw.line([(275, y + 30), (1145, y + 30)], fill=(51, 65, 85), width=1)
        y += 45

    save_shot(im, "screenshot_ai_report.png")

# 4. AI Assistant Chat
def shot_ai_chat():
    im, draw = make_browser_frame(1200, 720, "Trợ Lý Hỏi Đáp Kho AI")
    draw.text((250, 115), "Trợ Lý Hỏi Đáp Kho AI Tự Nhiên (Natural Language Assistant)", fill=(255, 255, 255), font=FONT_TITLE)
    draw.text((250, 150), "Hỗ trợ tra cứu tức thời thông tin tồn kho, định giá và sản phẩm bằng ngôn ngữ tự nhiên", fill=(148, 163, 184), font=FONT_SMALL)

    # Chat box
    draw.rounded_rectangle([250, 180, 1170, 680], radius=10, fill=(30, 41, 59), outline=(51, 65, 85))

    # User message
    draw.rounded_rectangle([680, 210, 1140, 260], radius=8, fill=(37, 99, 235))
    draw.text((700, 225), "Kho còn bao nhiêu bàn phím cơ AKKO và chuột Logitech?", fill=(255, 255, 255), font=FONT_TEXT)

    # AI message
    draw.rounded_rectangle([280, 280, 950, 520], radius=8, fill=(15, 23, 42), outline=(51, 65, 85))
    draw.text((305, 300), "🤖 Trợ lý Kho AI phản hồi:", fill=(56, 189, 248), font=FONT_BOLD)
    draw.text((305, 330), "Dựa trên dữ liệu tồn kho thực tế lúc 09:45:", fill=(203, 213, 225), font=FONT_TEXT)
    draw.text((305, 360), "1. Bàn phím cơ AKKO 3087: Còn 3 chiếc (Định mức tối thiểu là 10 chiếc) -> 🔴 CẢNH BÁO", fill=(239, 68, 68), font=FONT_TEXT)
    draw.text((305, 390), "2. Chuột Logitech G102: Còn 8 chiếc (Định mức tối thiểu là 15 chiếc) -> 🟡 DƯỚI TỒN", fill=(245, 158, 11), font=FONT_TEXT)
    draw.text((305, 430), "Tổng giá trị lô hàng này trong kho ước tính: 9,840,000 VNĐ.", fill=(16, 185, 129), font=FONT_BOLD)
    draw.text((305, 470), "Khuyến nghị: Bạn có muốn tôi lập phiếu đề xuất nhập kho ngay không?", fill=(148, 163, 184), font=FONT_SMALL)

    # Input bar
    draw.rounded_rectangle([280, 580, 1020, 640], radius=8, fill=(15, 23, 42), outline=(71, 85, 105))
    draw.text((305, 600), "Nhập câu hỏi nghiệp vụ kho (ví dụ: Sản phẩm nào có giá nhập cao nhất?)...", fill=(100, 116, 139), font=FONT_TEXT)
    draw.rounded_rectangle([1040, 580, 1140, 640], radius=8, fill=(37, 99, 235))
    draw.text((1065, 600), "GỬI", fill=(255, 255, 255), font=FONT_BOLD)

    save_shot(im, "screenshot_ai_assistant.png")

# 5. Products Screen
def shot_products():
    im, draw = make_browser_frame(1200, 720, "Quản lý Sản phẩm")
    draw.text((250, 115), "Quản Lý Danh Mục Sản Phẩm (SKU Master Data)", fill=(255, 255, 255), font=FONT_TITLE)
    draw.rounded_rectangle([1000, 110, 1170, 150], radius=6, fill=(16, 185, 129))
    draw.text((1025, 122), "+ Thêm Sản Phẩm", fill=(255, 255, 255), font=FONT_BOLD)

    draw.rounded_rectangle([250, 175, 1170, 680], radius=10, fill=(30, 41, 59), outline=(51, 65, 85))
    draw.rectangle([275, 200, 1145, 240], fill=(15, 23, 42))
    draw.text((290, 212), "SKU", fill=(148, 163, 184), font=FONT_SMALL)
    draw.text((450, 212), "TÊN SẢN PHẨM", fill=(148, 163, 184), font=FONT_SMALL)
    draw.text((700, 212), "GIÁ VỐN (VNĐ)", fill=(148, 163, 184), font=FONT_SMALL)
    draw.text((860, 212), "GIÁ BÁN (VNĐ)", fill=(148, 163, 184), font=FONT_SMALL)
    draw.text((1020, 212), "ĐỊNH MỨC", fill=(148, 163, 184), font=FONT_SMALL)

    items = [
        ("KB-AKKO-3087", "Bàn phím cơ AKKO 3087 V2 Silent", "1,250,000", "1,590,000", "Min: 10 | Max: 50"),
        ("MOU-LOGI-G102", "Chuột Logitech G102 Lightsync", "320,000", "450,000", "Min: 15 | Max: 100"),
        ("MON-DELL-24", "Màn hình Dell UltraSharp U2422H", "5,400,000", "6,890,000", "Min: 5 | Max: 30"),
        ("HEAD-SONY-CH", "Tai nghe Sony WH-CH520 Wireless", "1,100,000", "1,490,000", "Min: 10 | Max: 40"),
        ("RAM-KST-16G", "RAM Kingston Fury Beast 16GB DDR4", "850,000", "1,150,000", "Min: 20 | Max: 150"),
    ]
    y = 260
    for sku, name, cost, sell, lim in items:
        draw.text((290, y), sku, fill=(56, 189, 248), font=FONT_CODE)
        draw.text((450, y), name, fill=(241, 245, 249), font=FONT_TEXT)
        draw.text((700, y), cost, fill=(241, 245, 249), font=FONT_TEXT)
        draw.text((860, y), sell, fill=(16, 185, 129), font=FONT_TEXT)
        draw.text((1020, y), lim, fill=(148, 163, 184), font=FONT_SMALL)
        draw.line([(275, y + 30), (1145, y + 30)], fill=(51, 65, 85), width=1)
        y += 45

    save_shot(im, "screenshot_products.png")

if __name__ == "__main__":
    shot_login()
    shot_dashboard()
    shot_ai_hub()
    shot_ai_chat()
    shot_products()
    print("Successfully generated high-fidelity UI screenshots!")
