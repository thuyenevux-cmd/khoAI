import os, sys, math
from PIL import Image, ImageDraw, ImageFont

FONT_TIMES_BD = r"C:\Windows\Fonts\timesbd.ttf"
FONT_TIMES_REG = r"C:\Windows\Fonts\times.ttf"

def get_font(path, sz):
    try:
        return ImageFont.truetype(path, sz)
    except:
        return ImageFont.load_default()

# Use 2600 x 1700 canvas (1.53:1 aspect ratio, perfect for Word 6.2 x 4.0 inches)
W, H = 2600, 1700
im = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(im)

# Header
draw.rectangle([0, 0, W, 160], fill=(255, 255, 255))
f_head_title = get_font(FONT_TIMES_BD, 52)
f_head_sub = get_font(FONT_TIMES_REG, 32)
draw.text((60, 24), "SƠ ĐỒ USE CASE TỔNG THỂ HỆ THỐNG QUẢN LÝ KHO CÓ TÍCH HỢP AI", fill=(0, 0, 0), font=f_head_title)
draw.text((60, 92), "Phân quyền 3 Tác nhân: Quản trị viên (ADMIN), Thủ kho (WAREHOUSE), Kế toán (ACCOUNTANT)", fill=(50, 50, 50), font=f_head_sub)
draw.line([(0, 152), (W, 152)], fill=(0, 0, 0), width=5)
draw.line([(0, 158), (W, 158)], fill=(0, 0, 0), width=2)

# System Boundary Box
f_sys = get_font(FONT_TIMES_BD, 42)
bx1, by1, bx2, by2 = 520, 185, 2550, 1610
draw.rounded_rectangle([bx1, by1, bx2, by2], radius=16, fill=(255, 255, 255), outline=(0, 0, 0), width=5)
draw.rectangle([bx1, by1, bx2, by1 + 72], fill=(242, 242, 242), outline=(0, 0, 0), width=4)
draw.text((bx1 + 35, by1 + 16), "RANH GIỚI HỆ THỐNG: HỆ THỐNG QUẢN LÝ KHO KHOAI NHÓM 11", fill=(0, 0, 0), font=f_sys)

# Actors Drawer
f_actor_title = get_font(FONT_TIMES_BD, 40)
f_actor_sub = get_font(FONT_TIMES_BD, 32)

def draw_actor(cx, cy, title, role):
    # Head
    draw.ellipse([cx - 42, cy - 100, cx + 42, cy - 16], outline=(0, 0, 0), width=6)
    # Body
    draw.line([(cx, cy - 16), (cx, cy + 68)], fill=(0, 0, 0), width=6)
    # Arms
    draw.line([(cx - 68, cy + 12), (cx + 68, cy + 12)], fill=(0, 0, 0), width=6)
    # Legs
    draw.line([(cx, cy + 68), (cx - 50, cy + 150)], fill=(0, 0, 0), width=6)
    draw.line([(cx, cy + 68), (cx + 50, cy + 150)], fill=(0, 0, 0), width=6)
    # Card
    card = (cx - 185, cy + 165, cx + 185, cy + 270)
    draw.rounded_rectangle(card, radius=12, fill=(255, 255, 255), outline=(0, 0, 0), width=4)
    tw1 = draw.textbbox((0, 0), title, font=f_actor_title)[2]
    draw.text((cx - tw1 // 2, cy + 178), title, fill=(0, 0, 0), font=f_actor_title)
    sub = f"Vai trò: {role}"
    tw2 = draw.textbbox((0, 0), sub, font=f_actor_sub)[2]
    draw.text((cx - tw2 // 2, cy + 226), sub, fill=(50, 50, 50), font=f_actor_sub)

# 3 Actors on Left (cx = 250)
draw_actor(250, 420, "QUẢN TRỊ VIÊN", "ADMIN")
draw_actor(250, 870, "THỦ KHO", "WAREHOUSE")
draw_actor(250, 1310, "KẾ TOÁN", "ACCOUNTANT")

# 12 Use Cases in 2 Parallel Columns
# Column 1: UC01 - UC06 (x = 560 to 1480, width 920px)
# Column 2: UC07 - UC12 (x = 1580 to 2510, width 930px)
col1_ucs = [
    ("UC01: Đăng nhập hệ thống & Xác thực JWT", "Bảo mật OAuth2 Password Bearer & Băm Argon2"),
    ("UC02: Quản lý Người dùng & Phân quyền", "Kiểm soát 3 vai trò Admin, Warehouse, Accountant"),
    ("UC03: Xem & Tra cứu Nhật ký Kiểm toán", "Audit Trail ghi nhận vết bất biến mọi thao tác C/U/D"),
    ("UC04: Quản lý Danh mục, NCC & Vị trí kệ", "Danh mục hàng hóa, đối tác cung ứng & ô kệ kho"),
    ("UC05: Quản lý Danh mục Sản phẩm & SKU", "Mã hàng duy nhất, giá vốn, giá bán & định mức"),
    ("UC06: Lập Phiếu Nhập kho & Phân bổ kệ", "Tạo phiếu nhập từ NCC, kiểm đếm & gán vị trí ô kệ"),
]

col2_ucs = [
    ("UC07: Lập Phiếu Xuất kho & Kiểm tra tồn", "Kiểm tra tồn khả dụng, khóa hàng Row-level Lock"),
    ("UC08: Báo cáo Tài chính & Lịch sử phiếu", "Định giá tổng tài sản kho & Tra cứu lịch sử chứng từ"),
    ("UC09: Dự báo Cạn tồn & Đề xuất tái nhập", "Tính Burn-rate tiêu thụ ngày & Depletion Days (AI)"),
    ("UC10: Phát hiện Bất thường & Dị biệt xuất", "Áp dụng kiểm định thống kê Z-score phát hiện ngoại lai (AI)"),
    ("UC11: Trợ lý Hỏi Đáp Kho bằng Ngôn ngữ tự nhiên", "Giao diện Chat NLP tiếng Việt & JSON snapshot (AI)"),
    ("UC12: Xem Dashboard Realtime 6 Thẻ KPI", "Theo dõi tồn kho, cảnh báo cạn hàng thời gian thực"),
]

f_uc_title = get_font(FONT_TIMES_BD, 42)
f_uc_sub = get_font(FONT_TIMES_REG, 33)

c1_x1, c1_x2 = 560, 1490
c2_x1, c2_x2 = 1570, 2500

uc_targets = {}

for i, (l1, l2) in enumerate(col1_ucs):
    y1 = 285 + i * 215
    y2 = y1 + 175
    bbox = [c1_x1, y1, c1_x2, y2]
    draw.rounded_rectangle(bbox, radius=36, fill=(255, 255, 255), outline=(0, 0, 0), width=4)
    tw1 = draw.textbbox((0, 0), l1, font=f_uc_title)[2]
    tw2 = draw.textbbox((0, 0), l2, font=f_uc_sub)[2]
    cx = (c1_x1 + c1_x2) // 2
    draw.text((cx - tw1 // 2, y1 + 26), l1, fill=(0, 0, 0), font=f_uc_title)
    draw.text((cx - tw2 // 2, y1 + 92), l2, fill=(40, 40, 40), font=f_uc_sub)
    ucid = f"UC{i+1:02d}"
    uc_targets[ucid] = (c1_x1, (y1 + y2) // 2)

for i, (l1, l2) in enumerate(col2_ucs):
    y1 = 285 + i * 215
    y2 = y1 + 175
    bbox = [c2_x1, y1, c2_x2, y2]
    draw.rounded_rectangle(bbox, radius=36, fill=(255, 255, 255), outline=(0, 0, 0), width=4)
    tw1 = draw.textbbox((0, 0), l1, font=f_uc_title)[2]
    tw2 = draw.textbbox((0, 0), l2, font=f_uc_sub)[2]
    cx = (c2_x1 + c2_x2) // 2
    draw.text((cx - tw1 // 2, y1 + 26), l1, fill=(0, 0, 0), font=f_uc_title)
    draw.text((cx - tw2 // 2, y1 + 92), l2, fill=(40, 40, 40), font=f_uc_sub)
    ucid = f"UC{i+7:02d}"
    uc_targets[ucid] = (c2_x1, (y1 + y2) // 2)

# Connector lines:
# 1. ADMIN (cx=250, cy=420)
# Admin connects to UC01, UC02, UC03, UC12
for ucid in ["UC01", "UC02", "UC03"]:
    tx, ty = uc_targets[ucid]
    draw.line([(435, 420), (tx, ty)], fill=(0, 0, 0), width=5)
# Admin to UC12 (Dashboard) via clean top outer corridor
draw.line([(435, 400), (475, 400), (475, 260), (1530, 260), (uc_targets["UC12"][0], uc_targets["UC12"][1])], fill=(0, 0, 0), width=4)

# 2. THỦ KHO (cx=250, cy=870)
# Connects to UC01, UC04, UC05, UC06
for ucid in ["UC01", "UC04", "UC05", "UC06"]:
    tx, ty = uc_targets[ucid]
    draw.line([(435, 870), (tx, ty)], fill=(0, 0, 0), width=5)
# Connects to Col 2: UC07, UC09, UC11, UC12 via central vertical bus
# Central bus at x = 1530
draw.line([(435, 870), (510, 870), (510, 1500), (1530, 1500)], fill=(0, 0, 0), width=4)
draw.line([(1530, uc_targets["UC07"][1]), (1530, uc_targets["UC12"][1])], fill=(0, 0, 0), width=4)
for ucid in ["UC07", "UC09", "UC11", "UC12"]:
    ty = uc_targets[ucid][1]
    draw.line([(1530, ty), (c2_x1, ty)], fill=(0, 0, 0), width=4)

# 3. KẾ TOÁN (cx=250, cy=1310)
# Connects to UC01, UC08, UC09, UC10, UC12
# Kế toán to UC01
draw.line([(435, 1310), (uc_targets["UC01"][0], uc_targets["UC01"][1])], fill=(0, 0, 0), width=3)
# Kế toán to UC04
draw.line([(435, 1310), (uc_targets["UC04"][0], uc_targets["UC04"][1])], fill=(0, 0, 0), width=4)
# Kế toán to Col 2 via bottom connector:
for ucid in ["UC08", "UC10"]:
    ty = uc_targets[ucid][1]
    draw.line([(1530, ty), (c2_x1, ty)], fill=(0, 0, 0), width=4)
draw.line([(435, 1310), (510, 1310), (510, 1530), (1530, 1530)], fill=(0, 0, 0), width=4)

# Footer
f_ft = get_font(FONT_TIMES_REG, 28)
draw.line([(0, H - 55), (W, H - 55)], fill=(0, 0, 0), width=3)
draw.text((60, H - 44), "Nhóm 11 - AIA331 | Sơ đồ Use Case Tổng thể Hệ thống Quản lý Kho có Tích hợp AI", fill=(60, 60, 60), font=f_ft)

im.save(r"D:\khoAI\báo cáo\zoom_verification\test_usecase_perfect.png", dpi=(600, 600))
print("Exported test_usecase_perfect.png!")
