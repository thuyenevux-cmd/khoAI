import os, sys, math
from PIL import Image, ImageDraw, ImageFont

FONT_TIMES_BD = r"C:\Windows\Fonts\timesbd.ttf"
FONT_TIMES_REG = r"C:\Windows\Fonts\times.ttf"

def get_font(path, sz):
    try:
        return ImageFont.truetype(path, sz)
    except:
        return ImageFont.load_default()

W, H = 2700, 1750
im = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(im)

# Header
draw.rectangle([0, 0, W, 160], fill=(255, 255, 255))
f_head_title = get_font(FONT_TIMES_BD, 54)
f_head_sub = get_font(FONT_TIMES_REG, 34)
draw.text((60, 24), "SƠ ĐỒ USE CASE TỔNG THỂ HỆ THỐNG KHO AI (12 USE CASES)", fill=(0, 0, 0), font=f_head_title)
draw.text((60, 92), "Phân quyền 3 Tác nhân: Quản trị viên (ADMIN), Thủ kho (WAREHOUSE), Kế toán (ACCOUNTANT)", fill=(40, 40, 40), font=f_head_sub)
draw.line([(0, 152), (W, 152)], fill=(0, 0, 0), width=5)
draw.line([(0, 158), (W, 158)], fill=(0, 0, 0), width=2)

# System Boundary Box
f_sys = get_font(FONT_TIMES_BD, 44)
bx1, by1, bx2, by2 = 500, 185, 2640, 1640
draw.rounded_rectangle([bx1, by1, bx2, by2], radius=16, fill=(255, 255, 255), outline=(0, 0, 0), width=5)
draw.rectangle([bx1, by1, bx2, by1 + 75], fill=(240, 240, 240), outline=(0, 0, 0), width=4)
draw.text((bx1 + 35, by1 + 16), "RANH GIỚI HỆ THỐNG: QUẢN LÝ KHO TÍCH HỢP AI (AIA331)", fill=(0, 0, 0), font=f_sys)

# Actor Drawer (All 3 on the Left)
f_actor_title = get_font(FONT_TIMES_BD, 42)
f_actor_sub = get_font(FONT_TIMES_BD, 34)

def draw_actor(cx, cy, title, role):
    # Head
    draw.ellipse([cx - 44, cy - 105, cx + 44, cy - 17], outline=(0, 0, 0), width=6)
    # Body
    draw.line([(cx, cy - 17), (cx, cy + 72)], fill=(0, 0, 0), width=6)
    # Arms
    draw.line([(cx - 72, cy + 12), (cx + 72, cy + 12)], fill=(0, 0, 0), width=6)
    # Legs
    draw.line([(cx, cy + 72), (cx - 52, cy + 158)], fill=(0, 0, 0), width=6)
    draw.line([(cx, cy + 72), (cx + 52, cy + 158)], fill=(0, 0, 0), width=6)
    # Card
    card = (cx - 195, cy + 172, cx + 195, cy + 285)
    draw.rounded_rectangle(card, radius=12, fill=(255, 255, 255), outline=(0, 0, 0), width=4)
    tw1 = draw.textbbox((0, 0), title, font=f_actor_title)[2]
    draw.text((cx - tw1 // 2, cy + 186), title, fill=(0, 0, 0), font=f_actor_title)
    sub = f"Vai trò: {role}"
    tw2 = draw.textbbox((0, 0), sub, font=f_actor_sub)[2]
    draw.text((cx - tw2 // 2, cy + 238), sub, fill=(40, 40, 40), font=f_actor_sub)

# 3 Actors on the Left: cx = 250
draw_actor(250, 430, "QUẢN TRỊ VIÊN", "ADMIN")
draw_actor(250, 890, "THỦ KHO", "WAREHOUSE")
draw_actor(250, 1340, "KẾ TOÁN", "ACCOUNTANT")

# 12 Use Cases in 2 Parallel Columns
col1_ucs = [
    ("UC01: Đăng nhập hệ thống", "Xác thực JWT Bearer & Argon2"),
    ("UC02: Quản lý Người dùng", "Phân định 3 vai trò RBAC"),
    ("UC03: Nhật ký Kiểm toán", "Audit Trail vết bất biến C/U/D"),
    ("UC04: Quản lý Danh mục", "Nhóm hàng, NCC & Vị trí kệ"),
    ("UC05: Danh mục Sản phẩm", "Quản lý SKU, Giá & Định mức"),
    ("UC06: Lập Phiếu Nhập kho", "Kiểm đếm & Phân bổ kệ lưu"),
]

col2_ucs = [
    ("UC07: Lập Phiếu Xuất kho", "Kiểm tra tồn khả dụng an toàn"),
    ("UC08: Báo cáo Tài chính", "Định giá tài sản kho & Lịch sử"),
    ("UC09: Dự báo Cạn tồn (AI)", "Burn-rate & Gợi ý tái nhập"),
    ("UC10: Phát hiện Bất thường", "Kiểm định thống kê Z-score (AI)"),
    ("UC11: Trợ lý Kho Tự nhiên", "Hỏi đáp NLP bằng tiếng Việt (AI)"),
    ("UC12: Dashboard Realtime", "Theo dõi 6 thẻ chỉ số KPI kho"),
]

f_uc_code = get_font(FONT_TIMES_BD, 44)
f_uc_desc = get_font(FONT_TIMES_REG, 36)

c1_x1, c1_x2 = 540, 1540
c2_x1, c2_x2 = 1600, 2600

uc_targets = {}

for i, (l1, l2) in enumerate(col1_ucs):
    y1 = 290 + i * 220
    y2 = y1 + 180
    bbox = [c1_x1, y1, c1_x2, y2]
    draw.rounded_rectangle(bbox, radius=36, fill=(255, 255, 255), outline=(0, 0, 0), width=4)
    tw1 = draw.textbbox((0, 0), l1, font=f_uc_code)[2]
    tw2 = draw.textbbox((0, 0), l2, font=f_uc_desc)[2]
    cx = (c1_x1 + c1_x2) // 2
    draw.text((cx - tw1 // 2, y1 + 28), l1, fill=(0, 0, 0), font=f_uc_code)
    draw.text((cx - tw2 // 2, y1 + 96), l2, fill=(40, 40, 40), font=f_uc_desc)
    ucid = f"UC{i+1:02d}"
    uc_targets[ucid] = (c1_x1, (y1 + y2) // 2)

for i, (l1, l2) in enumerate(col2_ucs):
    y1 = 290 + i * 220
    y2 = y1 + 180
    bbox = [c2_x1, y1, c2_x2, y2]
    draw.rounded_rectangle(bbox, radius=36, fill=(255, 255, 255), outline=(0, 0, 0), width=4)
    tw1 = draw.textbbox((0, 0), l1, font=f_uc_code)[2]
    tw2 = draw.textbbox((0, 0), l2, font=f_uc_desc)[2]
    cx = (c2_x1 + c2_x2) // 2
    draw.text((cx - tw1 // 2, y1 + 28), l1, fill=(0, 0, 0), font=f_uc_code)
    draw.text((cx - tw2 // 2, y1 + 96), l2, fill=(40, 40, 40), font=f_uc_desc)
    ucid = f"UC{i+7:02d}"
    uc_targets[ucid] = (c2_x1, (y1 + y2) // 2)

# CONNECTIONS:
# 1. ADMIN (cx=250, cy=430) -> UC01, UC02, UC03, UC12
for ucid in ["UC01", "UC02", "UC03"]:
    tx, ty = uc_targets[ucid]
    draw.line([(445, 430), (tx, ty)], fill=(0, 0, 0), width=5)

# Admin to UC12 via top bypass channel
draw.line([(445, 410), (475, 410), (475, 270), (1570, 270), (uc_targets["UC12"][0], uc_targets["UC12"][1])], fill=(0, 0, 0), width=4)

# 2. THỦ KHO (cx=250, cy=890) -> UC01, UC04, UC05, UC06, UC07, UC09, UC11, UC12
for ucid in ["UC01", "UC04", "UC05", "UC06"]:
    tx, ty = uc_targets[ucid]
    draw.line([(445, 890), (tx, ty)], fill=(0, 0, 0), width=5)

# Thủ kho to Col 2 (UC07, UC09, UC11, UC12) via gap corridors:
for ucid in ["UC07", "UC09", "UC11", "UC12"]:
    ty = uc_targets[ucid][1]
    # Draw horizontal link across gap
    draw.line([(c1_x2, ty), (c2_x1, ty)], fill=(0, 0, 0), width=4)
# Vertical bridge between gap
draw.line([(c1_x2, 890), (c2_x1, 890)], fill=(0, 0, 0), width=4)
draw.line([(445, 890), (c1_x1, 890)], fill=(0, 0, 0), width=5)

# 3. KẾ TOÁN (cx=250, cy=1340) -> UC01, UC08, UC09, UC10, UC12
# Kế toán to UC01
draw.line([(445, 1340), (uc_targets["UC01"][0], uc_targets["UC01"][1])], fill=(0, 0, 0), width=3)
# Kế toán to UC04
draw.line([(445, 1340), (uc_targets["UC04"][0], uc_targets["UC04"][1])], fill=(0, 0, 0), width=4)
# Kế toán to Col 2 (UC08, UC10) via horizontal links across gap
for ucid in ["UC08", "UC10"]:
    ty = uc_targets[ucid][1]
    draw.line([(c1_x2, ty), (c2_x1, ty)], fill=(0, 0, 0), width=4)
draw.line([(445, 1340), (c1_x1, 1340)], fill=(0, 0, 0), width=5)

# Footer
f_ft = get_font(FONT_TIMES_REG, 28)
draw.line([(0, H - 55), (W, H - 55)], fill=(0, 0, 0), width=3)
draw.text((60, H - 44), "Nhóm 11 - AIA331 | Sơ đồ Use Case Tổng thể Hệ thống Quản lý Kho có Tích hợp AI", fill=(60, 60, 60), font=f_ft)

im.save(r"D:\khoAI\báo cáo\zoom_verification\test_usecase_left3.png", dpi=(600, 600))
print("Exported test_usecase_left3.png successfully!")
