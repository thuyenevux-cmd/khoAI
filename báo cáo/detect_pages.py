import sys, pypdf
sys.stdout.reconfigure(encoding='utf-8')

reader = pypdf.PdfReader('D:/khoAI/báo cáo/báo cáo dự án Kho AI nhóm 11.pdf')
page_texts = [p.extract_text() or '' for p in reader.pages]

check_items = [
    ('thanks', 'LỜI CẢM ƠN'),
    ('abstract', 'TÓM TẮT BÁO CÁO'),
    ('abbr', 'DANH MỤC CÁC TỪ VIẾT TẮT'),
    ('toc', 'MỤC LỤC BÁO CÁO'),
    ('lof', 'DANH MỤC HÌNH VẼ'),
    ('lot', 'DANH MỤC BẢNG BIỂU'),
    ('matrix', 'BẢNG TRA CỨU NỘI DUNG THEO BÀI KIỂM TRA'),
    ('ch1', 'CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI'),
    ('ch2', 'CHƯƠNG 2. PHÂN TÍCH YÊU CẦU'),
    ('ch3', 'CHƯƠNG 3. PHÂN TÍCH ACTOR VÀ USE CASE'),
    ('ch4', 'CHƯƠNG 4. THIẾT KẾ QUY TRÌNH NGHIỆP VỤ'),
    ('ch5', 'CHƯƠNG 5. THIẾT KẾ CƠ SỞ DỮ LIỆU'),
    ('ch6', 'CHƯƠNG 6. KIẾN TRÚC HỆ THỐNG'),
    ('ch7', 'CHƯƠNG 7. THIẾT KẾ CHI TIẾT CHỨC NĂNG VÀ GIAO DIỆN'),
    ('ch8', 'CHƯƠNG 8. TÍCH HỢP TRÍ TUỆ NHÂN TẠO'),
    ('ch9', 'CHƯƠNG 9. THIẾT KẾ PROMPT VÀ THỬ NGHIỆM'),
    ('ch10', 'CHƯƠNG 10. KIỂM THỬ'),
    ('ch11', 'CHƯƠNG 11. BẢO MẬT VÀ ĐẠO ĐỨC AI'),
    ('ch12', 'CHƯƠNG 12. TRIỂN KHAI HỆ THỐNG'),
    ('ch13', 'CHƯƠNG 13. MINH CHỨNG SỬ DỤNG AI TRONG SDLC'),
    ('ch14', 'CHƯƠNG 14. ĐÁNH GIÁ ĐỒ ÁN THEO RUBRIC'),
    ('ch15', 'CHƯƠNG 15. HƯỚNG DẪN DEMO HỆ THỐNG THỰC TẾ'),
    ('ch16', 'CHƯƠNG 16. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN'),
    ('refs', 'TÀI LIỆU THAM KHẢO'),
    ('appendix', 'PHỤ LỤC CÁC BẢNG VÀ MÃ NGUỒN'),
]

print('pm = {')
for key, title in check_items:
    start_pg = 14 if (key.startswith('ch') or key in ['refs', 'appendix']) else 0
    for p_idx in range(start_pg, len(page_texts)):
        if title in page_texts[p_idx]:
            print(f'    "{key}": "{p_idx + 1}",')
            break
print('}')

figs = [
    ("Hình 3.1", "Hình 3.1"),
    ("Hình 4.1", "Hình 4.1"),
    ("Hình 4.2", "Hình 4.2"),
    ("Hình 5.1", "Hình 5.1"),
    ("Hình 5.2", "Hình 5.2"),
    ("Hình 5.3", "Hình 5.3"),
    ("Hình 5.4", "Hình 5.4"),
    ("Hình 6.1", "Hình 6.1"),
    ("Hình 6.2", "Hình 6.2"),
    ("Hình 6.3", "Hình 6.3"),
    ("Hình 8.1", "Hình 8.1"),
    ("Hình 8.2", "Hình 8.2"),
    ("Hình 9.1", "Hình 9.1"),
    ("Hình 15.1", "Hình 15.1"),
    ("Hình 15.2", "Hình 15.2"),
    ("Hình 15.3", "Hình 15.3"),
    ("Hình 15.4", "Hình 15.4"),
]
print('\nFigures pages:')
for f_code, f_str in figs:
    for p_idx in range(14, len(page_texts)):
        if f_str in page_texts[p_idx]:
            print(f'    ("{f_code}", "{p_idx + 1}"),')
            break

tables = [
    ("Bảng 1.1", "BẢNG PHÂN CÔNG NHIỆM VỤ"),
    ("Bảng 2.1", "Bảng 2.1:"),
    ("Bảng 5.1", "Bảng 5.1:"),
    ("Bảng 10.1", "Bảng 10.1:"),
    ("Bảng 11.1", "Bảng 11.1:"),
    ("Bảng 12.1", "Bảng 12.1:"),
    ("Bảng 14.1", "Bảng 14.1:"),
    ("Bảng PL.1", "Bảng PL.1:"),
    ("Bảng PL.2", "Bảng PL.2:"),
]
print('\nTables pages:')
for t_code, t_str in tables:
    for p_idx in range(len(page_texts)):
        if t_str in page_texts[p_idx]:
            print(f'    ("{t_code}", "{p_idx + 1}"),')
            break

