# -*- coding: utf-8 -*-
"""
Chứa toàn bộ dữ liệu nội dung của Báo cáo Đồ án AIA331
Chuẩn học thuật ICTU - Đại học Thái Nguyên
"""

METADATA = {
    "university": "ĐẠI HỌC THÁI NGUYÊN",
    "school": "TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG",
    "faculty": "KHOA CÔNG NGHỆ THÔNG TIN",
    "subject": "HỌC PHẦN: ỨNG DỤNG TRÍ TUỆ NHÂN TẠO (AIA331)",
    "course_code": "80273",
    "report_type": "BÁO CÁO DỰ ÁN HỌC PHẦN",
    "title_vn": "HỆ THỐNG QUẢN LÝ KHO CÓ TÍCH HỢP AI",
    "title_en": "AI-POWERED INVENTORY MANAGEMENT SYSTEM",
    "supervisor": "ThS. NGUYỄN TUẤN ANH",
    "students": [
        {"name": "Dương Minh Quang", "code": "DTC245200225"},
        {"name": "Vũ Ngọc Anh Thuyên", "code": "DTC245200428"}
    ],
    "class_name": "Công nghệ Thông tin - K24 ICTU",
    "location_year": "THÁI NGUYÊN, NĂM 2026"
}

ABBREVIATIONS = [
    ("AI", "Artificial Intelligence", "Trí tuệ nhân tạo"),
    ("API", "Application Programming Interface", "Giao diện lập trình ứng dụng"),
    ("CRUD", "Create, Read, Update, Delete", "Thao tác Tạo, Đọc, Cập nhật, Xóa"),
    ("DFD", "Data Flow Diagram", "Sơ đồ luồng dữ liệu"),
    ("ERD", "Entity Relationship Diagram", "Sơ đồ thực thể liên kết"),
    ("FIFO", "First In First Out", "Phương pháp nhập trước xuất trước"),
    ("ICTU", "Information and Communication Technology University", "Trường Đại học Công nghệ Thông tin và Truyền thông"),
    ("JWT", "JSON Web Token", "Chuẩn mã thông báo xác thực web"),
    ("LLM", "Large Language Model", "Mô hình ngôn ngữ lớn"),
    ("NLP", "Natural Language Processing", "Xử lý ngôn ngữ tự nhiên"),
    ("ORM", "Object-Relational Mapping", "Ánh xạ quan hệ đối tượng"),
    ("RBAC", "Role-Based Access Control", "Kiểm soát truy cập dựa trên vai trò"),
    ("REST", "Representational State Transfer", "Kiến trúc truyền trạng thái đại diện"),
    ("SKU", "Stock Keeping Unit", "Mã đơn vị lưu kho"),
    ("SPA", "Single Page Application", "Ứng dụng web một trang"),
    ("SQL", "Structured Query Language", "Ngôn ngữ truy vấn có cấu trúc"),
    ("UML", "Unified Modeling Language", "Ngôn ngữ mô hình hóa thống nhất"),
    ("URI", "Uniform Resource Identifier", "Định danh tài nguyên thống nhất"),
    ("WMS", "Warehouse Management System", "Hệ thống quản lý kho")
]

RUBRIC_CRITERIA = [
    ("01", "Khảo sát bối cảnh, đối tượng người dùng, quy trình nghiệp vụ kho", "Chương 1, 3", "Đạt"),
    ("02", "Đặc tả các yêu cầu chức năng (REQ-AUTH -> REQ-AUDIT) & phi chức năng", "Chương 3", "Đạt"),
    ("03", "Phân tích quy trình hệ thống qua Use Case Diagram chuẩn UML", "Chương 3, Hình 3.1", "Đạt"),
    ("04", "Mô hình hóa nghiệp vụ Đăng nhập qua Activity Diagram", "Chương 4, Hình 4.1", "Đạt"),
    ("05", "Mô hình hóa nghiệp vụ Nhập kho qua Activity Diagram", "Chương 4, Hình 4.2", "Đạt"),
    ("06", "Mô hình hóa nghiệp vụ Xuất kho chống âm qua Activity Diagram", "Chương 4, Hình 4.3", "Đạt"),
    ("07", "Mô hình hóa luồng xử lý AI qua Activity Diagram", "Chương 4, Hình 4.4", "Đạt"),
    ("08", "Thiết kế Cơ sở dữ liệu quan hệ chuẩn 3NF (11 bảng)", "Chương 5, Bảng 5.1-5.11", "Đạt"),
    ("09", "Sơ đồ thực thể liên kết ERD chuẩn hóa", "Chương 5, Hình 5.1", "Đạt"),
    ("10", "Khóa chính, khóa ngoại, ràng buộc toàn vẹn và Indexing tối ưu", "Chương 5, ddl.sql", "Đạt"),
    ("11", "Mô hình kiến trúc tổng thể 3-Tier Client-Server", "Chương 6, Hình 6.1", "Đạt"),
    ("12", "Sơ đồ luồng dữ liệu DFD Mức 0 (Context Diagram)", "Chương 6, Hình 6.2a", "Đạt"),
    ("13", "Sơ đồ luồng dữ liệu DFD Mức 1 (Chi tiết phân rã nghiệp vụ)", "Chương 6, Hình 6.2b", "Đạt"),
    ("14", "Sơ đồ tuần tự Sequence Diagram cho quy trình Nhập kho", "Chương 7, Hình 7.1", "Đạt"),
    ("15", "Sơ đồ tuần tự Sequence Diagram cho quy trình Xuất kho", "Chương 7, Hình 7.2", "Đạt"),
    ("16", "Sơ đồ tuần tự Sequence Diagram cho quy trình Hỏi đáp AI NLP", "Chương 8, Hình 8.1", "Đạt"),
    ("17", "Thuật toán tính toán tồn an toàn và tốc độ tiêu thụ (Burn-rate)", "Chương 8, Công thức (8.1)", "Đạt"),
    ("18", "Xử lý an toàn ngoại lệ chia cho 0 (ZeroDivisionError) khi sales=0", "Chương 8, Mã nguồn 8.1", "Đạt"),
    ("19", "Cơ chế Strict Grounding Context chống ảo giác cho mô hình ngôn ngữ", "Chương 8, Bảng 8.3", "Đạt"),
    ("20", "Cơ chế Fallback tự động sang Rule Engine khi mất kết nối LLM", "Chương 8, Bảng 8.4", "Đạt"),
    ("21", "Kiến trúc Backend FastAPI, Pydantic Schemas và SQLAlchemy ORM", "Chương 9", "Đạt"),
    ("22", "Thiết kế hệ thống RESTful API chuẩn HTTP status codes", "Chương 9, Bảng 9.1", "Đạt"),
    ("23", "Quản lý phiên và phân quyền RBAC (ADMIN, WAREHOUSE, ACCOUNTANT)", "Chương 9, 11", "Đạt"),
    ("24", "Giao diện người dùng React Vite Responsive hiện đại", "Chương 10, Hình 10.1-10.5", "Đạt"),
    ("25", "Bảng điều khiển KPI Dashboard trực quan hóa số liệu thời gian thực", "Chương 10, Hình 10.2", "Đạt"),
    ("26", "Giao diện AI Hub phân tích báo cáo kho tự động", "Chương 10, Hình 10.3", "Đạt"),
    ("27", "Giao diện Trợ lý thông minh hỏi đáp bằng tiếng Việt tự nhiên", "Chương 10, Hình 10.4", "Đạt"),
    ("28", "Cơ chế bảo mật JWT Bearer Token với thuật toán mã hóa HS256", "Chương 11", "Đạt"),
    ("29", "Mã hóa mật khẩu một chiều sử dụng thuật toán Argon2/Bcrypt", "Chương 11", "Đạt"),
    ("30", "Giao dịch CSDL đảm bảo tính ACID và Rollback khi xuất vượt tồn", "Chương 11, Bảng 11.2", "Đạt"),
    ("31", "Ghi nhật ký kiểm toán (Audit Trail) cho mọi biến động xuất nhập tồn", "Chương 11", "Đạt"),
    ("32", "Cấu hình biến môi trường an toàn qua .env / .env.example", "Chương 12", "Đạt"),
    ("33", "Quy trình đóng gói Docker container và triển khai hệ thống", "Chương 12", "Đạt"),
    ("34", "Chiến lược kiểm thử tự động Unit Test và Integration Test", "Chương 13", "Đạt"),
    ("35", "Bộ kịch bản kiểm thử 12 Test Cases bao phủ chức năng chính", "Chương 13, Bảng 13.1", "Đạt"),
    ("36", "Kết quả thực thi Pytest 100% Passed (12/12 test cases)", "Chương 14, Bảng 14.1", "Đạt"),
    ("37", "Đo lường định lượng độ trễ API (<100ms) và phản hồi AI (<1.5s)", "Chương 14, Bảng 14.2", "Đạt"),
    ("38", "Phân loại minh bạch 5 hạng mục: IMPLEMENTED, TESTED, PROPOSED...", "Chương 15, Bảng 15.1", "Đạt"),
    ("39", "Ma trận truy vết yêu cầu (Traceability Matrix) từ Req đến Test", "Phụ lục A, Bảng A.1", "Đạt"),
    ("40", "Định dạng báo cáo chuẩn ICTU (Font Times, lề, khung TikZ, caption)", "Toàn bộ báo cáo", "Đạt")
]
print("Loaded metadata, abbreviations, and rubric criteria.")
