import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import pypdfium2 as pdfium

PDF_PATH = r"D:\khoAI\báo cáo\báo cáo dự án Kho AI nhóm 11.pdf"
OUT_DIR = r"D:\khoAI\báo cáo\zoom_verification"
os.makedirs(OUT_DIR, exist_ok=True)

pdf = pdfium.PdfDocument(PDF_PATH)
total_pages = len(pdf)
print(f"Total pages in PDF: {total_pages}")

# Pages to verify:
# Page 17: Bảng 2.1 (Yêu cầu chức năng)
# Page 21: Hình 3.1 (Use Case)
# Page 22: Hình 4.1 (Activity Nhập kho)
# Page 24: Hình 5.1 (Master ERD 11 bảng)
# Page 27: Hình 5.4 (ERD Tồn kho) & Bảng 5.1
# Page 30: Hình 6.1 (Kiến trúc 3 tầng)
# Page 31: Hình 6.2 (Sequence Diagram)
# Page 34: Hình 8.1 (AI Dual-layer Pipeline)
# Page 38: Bảng 10.1 (Bộ kiểm thử tự động)
# Page 40: Bảng 11.1 (Ma trận RBAC)
# Page 47: Bảng PL.1 (77 trường CSDL)
# Page 55: Bảng PL.2 (12 ca test Pytest)

test_pages = [
    (17, "page17_bang2_1_chuc_nang"),
    (21, "page21_hinh3_1_usecase"),
    (22, "page22_hinh4_1_activity_nhap"),
    (24, "page24_hinh5_1_master_erd"),
    (27, "page27_hinh5_4_erd_ton_kho_va_bang5_1"),
    (30, "page30_hinh6_1_kien_truc"),
    (31, "page31_hinh6_2_sequence"),
    (34, "page34_hinh8_1_ai_pipeline"),
    (38, "page38_bang10_1_pytest"),
    (40, "page40_bang11_1_rbac"),
    (47, "page47_bangPL1_data_dictionary"),
    (55, "page55_bangPL2_test_cases"),
]

for pg_num, label in test_pages:
    page = pdf[pg_num - 1] # 0-indexed
    # 100% zoom = 72 dpi (scale = 1.0)
    img_100 = page.render(scale=1.0).to_pil()
    img_100_path = os.path.join(OUT_DIR, f"{label}_zoom100.png")
    img_100.save(img_100_path)

    # 200% zoom = 144 dpi (scale = 2.0)
    img_200 = page.render(scale=2.0).to_pil()
    img_200_path = os.path.join(OUT_DIR, f"{label}_zoom200.png")
    img_200.save(img_200_path)

    print(f"Verified Page {pg_num} [{label}]: 100% ({img_100.size}), 200% ({img_200.size})")

print("\nAll zoom inspection images generated successfully in:", OUT_DIR)
