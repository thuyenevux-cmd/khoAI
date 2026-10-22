import os, sys, math
from PIL import Image, ImageDraw, ImageFont

FONT_TIMES_BD = r"C:\Windows\Fonts\timesbd.ttf"
FONT_TIMES_REG = r"C:\Windows\Fonts\times.ttf"

def get_font(path, sz):
    try:
        return ImageFont.truetype(path, sz)
    except:
        return ImageFont.load_default()

W, H = 2700, 1680
im = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(im)

# Header
draw.rectangle([0, 0, W, 160], fill=(255, 255, 255))
f_head_title = get_font(FONT_TIMES_BD, 54)
f_head_sub = get_font(FONT_TIMES_REG, 34)
draw.text((60, 24), "SƠ ĐỒ USE CASE TỔNG THỂ HỆ THỐNG KHO AI (12 USE CASES)", fill=(0, 0, 0), font=f_head_title)
draw.text((60, 92), "Phân quyền 3 Tác nhân: Quản trị viên (ADMIN), Thủ kho (WAREHOUSE), Kế toán (ACCOUNTANT)", fill=(50, 50, 50), font=f_head_sub)
draw.line([(0, 152), (W, 152)], fill=(0, 0, 0), width=5)
draw.line([(0, 158), (W, 158)], fill=(0, 0, 0), width=2)

# System Boundary in center: x = 480 to 2220
f_sys = get_font(FONT_TIMES_BD, 44)
bx1, by1, bx2, by2 = 480, 185, 2220, 1580
draw.rounded_rectangle([bx1, by1, bx2, by2], radius=16, fill=(255, 255, 255), outline=(0, 0, 0), width=5)
draw.rectangle([bx1, by1, bx2, by1 + 75], fill=(242, 242, 242), outline=(0, 0, 0), width=4)
draw.text((bx1 + 35, by1 + 16), "RANH GIỚI HỆ THỐNG: QUẢN LÝ KHO CÓ TÍCH HỢP AI (AIA331)", fill=(0, 0, 0), font=f_sys)

# Actor Drawer
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
    draw.text((cx - tw2 // 2, cy + 238), sub, fill=(50, 50, 50), font=f_actor_sub)

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

f_uc_title = get_font(FONT_TIMES_BD, 42)
f_uc_sub = get_font(FONT_TIMES_REG, 33)

c1_x1, c1_x2 = 510, 1340
c2_x1, c2_x2 = 1360, 2190

uc_left_pt = {}
uc_right_pt = {}

for i, (l1, l2) in enumerate(col1_ucs):
    y1 = 285 + i * 215
    y2 = y1 + 175
    bbox = [c1_x1, y1, c1_x2, y2]
    draw.rounded_rectangle(bbox, radius=36, fill=(255, 255, 255), outline=(0, 0, 0), width=4)
    tw1 = draw.textbbox((0, 0), l1, font=f_uc_title)[2]
    tw2 = draw.textbbox((0, 0), l2, font=f_uc_sub)[2]
    cx = (c1_x1 + c1_x2) // 2
    draw.text((cx - tw1 // 2, y1 + 26), l1, fill=(0, 0, 0), font=f_uc_title)
    draw.text((cx - tw2 // 2, y1 + 94), l2, fill=(40, 40, 40), font=f_uc_sub)
    ucid = f"UC{i+1:02d}"
    mid_y = (y1 + y2) // 2
    uc_left_pt[ucid] = (c1_x1, mid_y)
    uc_right_pt[ucid] = (c1_x2, mid_y)

for i, (l1, l2) in enumerate(col2_ucs):
    y1 = 285 + i * 215
    y2 = y1 + 175
    bbox = [c2_x1, y1, c2_x2, y2]
    draw.rounded_rectangle(bbox, radius=36, fill=(255, 255, 255), outline=(0, 0, 0), width=4)
    tw1 = draw.textbbox((0, 0), l1, font=f_uc_title)[2]
    tw2 = draw.textbbox((0, 0), l2, font=f_uc_sub)[2]
    cx = (c2_x1 + c2_x2) // 2
    draw.text((cx - tw1 // 2, y1 + 26), l1, fill=(0, 0, 0), font=f_uc_title)
    draw.text((cx - tw2 // 2, y1 + 94), l2, fill=(40, 40, 40), font=f_uc_sub)
    ucid = f"UC{i+7:02d}"
    mid_y = (y1 + y2) // 2
    uc_left_pt[ucid] = (c2_x1, mid_y)
    uc_right_pt[ucid] = (c2_x2, mid_y)

# ----------------- CONNECTIONS -----------------
# 1. ADMIN (Left, cx=240, cy=520) -> UC01, UC02, UC03, UC12
for ucid in ["UC01", "UC02", "UC03"]:
    draw.line([(435, 520), uc_left_pt[ucid]], fill=(0, 0, 0), width=5)

# Admin to UC12 (Dashboard) via bottom left connector
draw.line([(435, 540), (460, 540), (460, 1460), (1350, 1460), uc_left_pt["UC12"]], fill=(0, 0, 0), width=4)

# 2. THỦ KHO (Left, cx=240, cy=1120) -> UC01, UC04, UC05, UC06, UC07, UC09, UC11
for ucid in ["UC01", "UC04", "UC05", "UC06"]:
    draw.line([(435, 1120), uc_left_pt[ucid]], fill=(0, 0, 0), width=5)

# Thủ kho across middle gap to UC07, UC09, UC11
for ucid in ["UC07", "UC09", "UC11"]:
    draw.line([(c1_x2, uc_left_pt[ucid][1]), uc_left_pt[ucid]], fill=(0, 0, 0), width=4)
draw.line([(435, 1120), (c1_x1, 1120)], fill=(0, 0, 0), width=5)

# 3. KẾ TOÁN (Right, cx=2460, cy=830) -> UC01, UC08, UC09, UC10, UC12
for ucid in ["UC08", "UC09", "UC10", "UC12"]:
    draw.line([(2265, 830), uc_right_pt[ucid]], fill=(0, 0, 0), width=5)

# Kế toán to UC01 via middle gap at top
draw.line([(2265, 800), (2240, 800), (2240, 260), (1350, 260), uc_right_pt["UC01"]], fill=(0, 0, 0), width=4)

# Footer
f_ft = get_font(FONT_TIMES_REG, 28)
draw.line([(0, H - 55), (W, H - 55)], fill=(0, 0, 0), width=3)
draw.text((60, H - 44), "Nhóm 11 - AIA331 | Sơ đồ Use Case Tổng thể Hệ thống Quản lý Kho có Tích hợp AI", fill=(60, 60, 60), font=f_ft)

im.save(r"D:\khoAI\báo cáo\zoom_verification\test_usecase_balanced_v2.png", dpi=(600, 600))
print("Exported test_usecase_balanced_v2.png successfully!")
