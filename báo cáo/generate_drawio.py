# -*- coding: utf-8 -*-
"""
Script sinh trọn bộ 13 tệp Draw.io XML (.drawio) chuẩn mở
Phong cách Kỹ thuật Đen Trắng (Monochrome / Print-Ready)
Hệ thống Quản lý Kho có Tích hợp AI - Nhóm 11 (AIA331)
Bao gồm:
- 01: Kiến trúc tổng thể 3 tầng
- 02: Use Case tổng thể 3 tác nhân
- 03: ERD Tổng quan 11 bảng CSDL chuẩn 3NF (Landscape)
- 03a: ERD Phân hệ Quản trị, Phân quyền RBAC & AI Logs
- 03b: ERD Phân hệ Danh mục Hàng hóa & Vị trí Kệ kho
- 03c: ERD Phân hệ Quản lý Tồn kho & Giao dịch Xuất Nhập
- 04: Lược đồ hoạt động Nhập kho
- 05: Lược đồ hoạt động Xuất kho (Khối báo lỗi mở rộng)
- 06: Sơ đồ tuần tự Giao dịch kho an toàn
- 07: Sơ đồ Pipeline AI 2 lớp Fallback
- 08: Sơ đồ tuần tự Trợ lý Hỏi Đáp Kho AI
- 09: Lưu đồ thuật toán Bất thường & Burn-rate
- 10: Sơ đồ điều hướng Frontend Sitemap
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DRAWIO_DIR = os.path.join(BASE_DIR, "diagrams", "drawio")
os.makedirs(DRAWIO_DIR, exist_ok=True)

def create_drawio_file(filename, diagram_name, cells_xml, page_w=1800, page_h=2200):
    content = f"""<mxfile host="app.diagrams.net" modified="2026-09-22T08:00:00.000Z" agent="Antigravity" version="22.0.0" type="device">
  <diagram id="diag_{diagram_name}" name="{diagram_name}">
    <mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{page_w}" pageHeight="{page_h}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{cells_xml}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    filepath = os.path.join(DRAWIO_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Generated B&W drawio: {filename}")

# 1. Kiến trúc 3 tầng
c1 = """
        <mxCell id="hdr" value="&lt;b&gt;SƠ ĐỒ KIẾN TRÚC TỔNG THỂ HỆ THỐNG 3 TẦNG (3-TIER ARCHITECTURE)&lt;/b&gt;&lt;br&gt;Nhóm 11 - AIA331 | Đại học Thái Nguyên (ICTU)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;fontColor=#000000;strokeColor=#000000;strokeWidth=2;fontSize=16;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1280" height="60" as="geometry" />
        </mxCell>
        <mxCell id="t1" value="&lt;b&gt;TẦNG 1: TRÌNH DIỄN (PRESENTATION TIER) - REACT VITE SPA&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=15;spacingTop=10;fontSize=14;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="100" width="1280" height="150" as="geometry" />
        </mxCell>
        <mxCell id="t1_1" value="&lt;b&gt;Dashboard &amp;amp; KPI Hub&lt;/b&gt;&lt;br&gt;• Thẻ chỉ số real-time&lt;br&gt;• Biểu đồ nhập/xuất 30 ngày&lt;br&gt;• Cảnh báo thiếu hàng" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=12;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="70" y="140" width="260" height="90" as="geometry" />
        </mxCell>
        <mxCell id="t1_2" value="&lt;b&gt;Nghiệp Vụ Kho Hàng&lt;/b&gt;&lt;br&gt;• Quản lý Sản phẩm, SKU&lt;br&gt;• Tạo phiếu Nhập/Xuất kho&lt;br&gt;• Quản lý Vị trí kệ, NCC" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=12;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="370" y="140" width="260" height="90" as="geometry" />
        </mxCell>
        <mxCell id="t1_3" value="&lt;b&gt;AI Analytics &amp;amp; NLP Hub&lt;/b&gt;&lt;br&gt;• Trợ lý hỏi đáp tự nhiên&lt;br&gt;• Dự báo số ngày cạn kho&lt;br&gt;• Phát hiện dị biệt/bất thường" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=12;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="670" y="140" width="260" height="90" as="geometry" />
        </mxCell>
        <mxCell id="t1_4" value="&lt;b&gt;Bảo Mật &amp;amp; Quản Trị&lt;/b&gt;&lt;br&gt;• Xác thực Bearer JWT&lt;br&gt;• Phân quyền RBAC (3 Roles)&lt;br&gt;• Nhật ký kiểm toán Audit Logs" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=12;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="970" y="140" width="320" height="90" as="geometry" />
        </mxCell>

        <mxCell id="t2" value="&lt;b&gt;TẦNG 2: NGHIỆP VỤ (APPLICATION LOGIC TIER) - FASTAPI ASYNC PYTHON&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=15;spacingTop=10;fontSize=14;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="310" width="1280" height="170" as="geometry" />
        </mxCell>
        <mxCell id="t2_1" value="&lt;b&gt;API Gateway / Routers&lt;/b&gt;&lt;br&gt;FastAPI Routers, CORS,&lt;br&gt;OAuth2PasswordBearer" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=12;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="70" y="360" width="260" height="90" as="geometry" />
        </mxCell>
        <mxCell id="t2_2" value="&lt;b&gt;Inventory &amp;amp; Core Services&lt;/b&gt;&lt;br&gt;Validation, Stock Deduct,&lt;br&gt;Row Locking, Audit Service" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=12;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="370" y="360" width="260" height="90" as="geometry" />
        </mxCell>
        <mxCell id="t2_3" value="&lt;b&gt;AI Dual-Layer Engine&lt;/b&gt;&lt;br&gt;Lớp 1: Google Gemini Cloud&lt;br&gt;Lớp 2: Local Rule-Engine&lt;br&gt;Burn-rate &amp;amp; Outlier Engine" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=12;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="670" y="360" width="260" height="90" as="geometry" />
        </mxCell>
        <mxCell id="t2_4" value="&lt;b&gt;Bảo Mật &amp;amp; RBAC Engine&lt;/b&gt;&lt;br&gt;Argon2 password hash,&lt;br&gt;SQLAlchemy ORM anti-SQLi,&lt;br&gt;Access Control Decorators" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=12;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="970" y="360" width="320" height="90" as="geometry" />
        </mxCell>

        <mxCell id="t3" value="&lt;b&gt;TẦNG 3: DỮ LIỆU &amp;amp; ĐÁM MÂY (DATA PERSISTENCE &amp;amp; EXTERNAL AI LAYER)&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=15;spacingTop=10;fontSize=14;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="540" width="1280" height="150" as="geometry" />
        </mxCell>
        <mxCell id="t3_1" value="&lt;b&gt;Cơ Sở Dữ Liệu Quan Hệ&lt;/b&gt;&lt;br&gt;SQLite / PostgreSQL (11 Bảng)&lt;br&gt;Chuẩn hóa 3NF, Alembic Migrations" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=12;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="70" y="580" width="360" height="80" as="geometry" />
        </mxCell>
        <mxCell id="t3_2" value="&lt;b&gt;Audit Trail &amp;amp; Query Logs&lt;/b&gt;&lt;br&gt;Bảng audit_logs ghi vết thay đổi CSDL&lt;br&gt;Bảng ai_query_logs ghi nhận prompt" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=12;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="470" y="580" width="380" height="80" as="geometry" />
        </mxCell>
        <mxCell id="t3_3" value="&lt;b&gt;Google Gemini AI Cloud&lt;/b&gt;&lt;br&gt;gemini-1.5-flash / gemini-2.0&lt;br&gt;Ground-Truth Context Injection" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=12;fontColor=#000000;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="890" y="580" width="400" height="80" as="geometry" />
        </mxCell>

        <mxCell id="e1" value="REST JSON API" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="t1" target="t2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e2" value="SQLAlchemy ORM &amp;amp; AI Requests" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="t2" target="t3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
"""
create_drawio_file("01_so_do_kien_truc_he_thong.drawio", "Architecture", c1)

# 2. Use Case
c2 = """
        <mxCell id="hdr2" value="&lt;b&gt;SƠ ĐỒ USE CASE TỔNG THỂ HỆ THỐNG QUẢN LÝ KHO AI&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;fontColor=#000000;strokeColor=#000000;strokeWidth=2;fontSize=16;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1200" height="50" as="geometry" />
        </mxCell>
        <mxCell id="boundary" value="&lt;b&gt;Ranh Giới Hệ Thống Quản Lý Kho Tích Hợp AI&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=center;verticalAlign=top;spacingTop=10;fontSize=14;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="260" y="90" width="760" height="650" as="geometry" />
        </mxCell>
        <mxCell id="act_admin" value="Quản Trị Viên&lt;br&gt;(ADMIN)" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="80" y="150" width="60" height="120" as="geometry" />
        </mxCell>
        <mxCell id="act_wh" value="Thủ Kho&lt;br&gt;(WAREHOUSE)" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="80" y="380" width="60" height="120" as="geometry" />
        </mxCell>
        <mxCell id="act_acc" value="Kế Toán&lt;br&gt;(ACCOUNTANT)" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="80" y="580" width="60" height="120" as="geometry" />
        </mxCell>

        <mxCell id="uc1" value="UC01: Đăng nhập &amp;amp; Xác thực JWT" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="140" width="280" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc2" value="UC02: Quản lý Người dùng &amp;amp; Phân quyền" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="210" width="280" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc3" value="UC03: Xem Nhật ký Kiểm toán Audit Logs" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="280" width="280" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc4" value="UC04: Quản lý Danh mục, NCC, Vị trí kệ" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="370" width="280" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc5" value="UC05: Quản lý Sản phẩm &amp;amp; Ngưỡng an toàn" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="440" width="280" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc6" value="UC06: Tạo Phiếu Nhập Kho &amp;amp; Phân kệ" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="510" width="280" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc7" value="UC07: Tạo Phiếu Xuất Kho &amp;amp; Trừ tồn khả dụng" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="580" width="280" height="50" as="geometry" />
        </mxCell>

        <mxCell id="uc8" value="UC08: Báo cáo Tài chính &amp;amp; Định giá kho" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="680" y="370" width="300" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc9" value="UC09: Dự báo cạn tồn &amp;amp; Tái nhập hàng (AI)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="680" y="440" width="300" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc10" value="UC10: Phát hiện Bất thường Tồn kho (AI)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="680" y="510" width="300" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc11" value="UC11: Trợ lý Hỏi Đáp Kho Tự Nhiên (NLP)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="680" y="580" width="300" height="50" as="geometry" />
        </mxCell>
        <mxCell id="uc12" value="UC12: Xem Dashboard Realtime 6 Thẻ KPI" style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="500" y="660" width="320" height="50" as="geometry" />
        </mxCell>

        <mxCell id="e_a1" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="act_admin" target="uc1" />
        <mxCell id="e_a2" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="act_admin" target="uc2" />
        <mxCell id="e_a3" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="act_admin" target="uc3" />
        <mxCell id="e_a12" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=1;" edge="1" parent="1" source="act_admin" target="uc12" />

        <mxCell id="e_w1" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=1;" edge="1" parent="1" source="act_wh" target="uc1" />
        <mxCell id="e_w4" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="act_wh" target="uc4" />
        <mxCell id="e_w5" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="act_wh" target="uc5" />
        <mxCell id="e_w6" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="act_wh" target="uc6" />
        <mxCell id="e_w7" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="act_wh" target="uc7" />
        <mxCell id="e_w9" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="act_wh" target="uc9" />
        <mxCell id="e_w11" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="act_wh" target="uc11" />
        <mxCell id="e_w12" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=1;" edge="1" parent="1" source="act_wh" target="uc12" />

        <mxCell id="e_c1" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=1;" edge="1" parent="1" source="act_acc" target="uc1" />
        <mxCell id="e_c8" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="act_acc" target="uc8" />
        <mxCell id="e_c9" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="act_acc" target="uc9" />
        <mxCell id="e_c10" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="act_acc" target="uc10" />
        <mxCell id="e_c12" style="edgeStyle=straight;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="act_acc" target="uc12" />
"""
create_drawio_file("02_so_do_usecase_tong_the.drawio", "UseCase", c2)

# 3. Master ERD 11 Tables
c3 = """
        <mxCell id="hdr_erd" value="&lt;b&gt;SƠ ĐỒ THỰC THỂ LIÊN KẾT (ERD) - 11 BẢNG CSDL CHUẨN 3NF&lt;/b&gt;&lt;br&gt;Dự án Hệ thống Quản lý Kho có Tích hợp AI - AIA331 | Nhóm 11" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;fontColor=#000000;strokeColor=#000000;strokeWidth=2;fontSize=16;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1680" height="60" as="geometry" />
        </mxCell>

        <!-- Column 1: Governance & Logs -->
        <mxCell id="tb_roles" value="&lt;b&gt;ROLES&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ role_name: VARCHAR(30) [U]&lt;br&gt;+ description: VARCHAR(255)&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="60" y="110" width="480" height="110" as="geometry" />
        </mxCell>
        <mxCell id="tb_users" value="&lt;b&gt;USERS&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ role_id: INTEGER [FK]&lt;br&gt;+ username: VARCHAR(50) [U]&lt;br&gt;+ password_hash: VARCHAR(255)&lt;br&gt;+ full_name: VARCHAR(100)&lt;br&gt;+ email: VARCHAR(100)&lt;br&gt;+ is_active: BOOLEAN&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="60" y="260" width="480" height="170" as="geometry" />
        </mxCell>
        <mxCell id="tb_audit" value="&lt;b&gt;AUDIT_LOGS&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ user_id: INTEGER [FK]&lt;br&gt;+ action_type: VARCHAR(30)&lt;br&gt;+ entity_name: VARCHAR(50)&lt;br&gt;+ entity_id: INTEGER&lt;br&gt;+ old_value: TEXT (JSON)&lt;br&gt;+ new_value: TEXT (JSON)&lt;br&gt;+ ip_address: VARCHAR(45)&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="60" y="470" width="480" height="180" as="geometry" />
        </mxCell>
        <mxCell id="tb_ai_logs" value="&lt;b&gt;AI_QUERY_LOGS&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ user_id: INTEGER [FK]&lt;br&gt;+ query_type: VARCHAR(30)&lt;br&gt;+ prompt_text: TEXT&lt;br&gt;+ context_snapshot: TEXT (JSON)&lt;br&gt;+ response_text: TEXT&lt;br&gt;+ execution_time_ms: INTEGER&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="60" y="690" width="480" height="170" as="geometry" />
        </mxCell>

        <!-- Column 2: Master Data -->
        <mxCell id="tb_cat" value="&lt;b&gt;CATEGORIES&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ code: VARCHAR(50) [U]&lt;br&gt;+ name: VARCHAR(100)&lt;br&gt;+ description: TEXT&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="620" y="110" width="480" height="120" as="geometry" />
        </mxCell>
        <mxCell id="tb_sup" value="&lt;b&gt;SUPPLIERS&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ name: VARCHAR(150)&lt;br&gt;+ contact_person: VARCHAR(100)&lt;br&gt;+ phone: VARCHAR(20)&lt;br&gt;+ email: VARCHAR(100)&lt;br&gt;+ address: VARCHAR(255)&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="620" y="270" width="480" height="150" as="geometry" />
        </mxCell>
        <mxCell id="tb_loc" value="&lt;b&gt;LOCATIONS&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ code: VARCHAR(50) [U]&lt;br&gt;+ zone: VARCHAR(20)&lt;br&gt;+ shelf_level: VARCHAR(20)&lt;br&gt;+ max_capacity: INTEGER&lt;br&gt;+ is_active: BOOLEAN&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="620" y="460" width="480" height="150" as="geometry" />
        </mxCell>
        <mxCell id="tb_prod" value="&lt;b&gt;PRODUCTS&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ category_id: INTEGER [FK]&lt;br&gt;+ supplier_id: INTEGER [FK]&lt;br&gt;+ sku: VARCHAR(50) [U]&lt;br&gt;+ name: VARCHAR(150)&lt;br&gt;+ unit: VARCHAR(20)&lt;br&gt;+ cost_price: DECIMAL(12,2)&lt;br&gt;+ selling_price: DECIMAL(12,2)&lt;br&gt;+ min_threshold: INTEGER&lt;br&gt;+ max_threshold: INTEGER&lt;br&gt;+ is_active: BOOLEAN&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="620" y="650" width="480" height="230" as="geometry" />
        </mxCell>

        <!-- Column 3: Inventory & Transactions -->
        <mxCell id="tb_inv" value="&lt;b&gt;INVENTORY_ITEMS&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ product_id: INTEGER [FK]&lt;br&gt;+ location_id: INTEGER [FK]&lt;br&gt;+ current_stock: INTEGER&lt;br&gt;+ batch_number: VARCHAR(50)&lt;br&gt;+ expiry_date: DATE&lt;br&gt;+ last_audited_at: DATETIME&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="1180" y="110" width="500" height="170" as="geometry" />
        </mxCell>
        <mxCell id="tb_trans" value="&lt;b&gt;INVENTORY_TRANSACTIONS&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ transaction_code: VARCHAR(50) [U]&lt;br&gt;+ transaction_type: VARCHAR(20)&lt;br&gt;+ supplier_id: INTEGER [FK]&lt;br&gt;+ created_by: INTEGER [FK]&lt;br&gt;+ total_amount: DECIMAL(15,2)&lt;br&gt;+ note: TEXT&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="1180" y="320" width="500" height="180" as="geometry" />
        </mxCell>
        <mxCell id="tb_trans_items" value="&lt;b&gt;INVENTORY_TRANSACTION_ITEMS&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ transaction_id: INTEGER [FK]&lt;br&gt;+ product_id: INTEGER [FK]&lt;br&gt;+ location_id: INTEGER [FK]&lt;br&gt;+ quantity: INTEGER&lt;br&gt;+ unit_price: DECIMAL(12,2)&lt;br&gt;+ subtotal: DECIMAL(15,2)&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="1180" y="540" width="500" height="180" as="geometry" />
        </mxCell>

        <!-- Relationships -->
        <mxCell id="rel1" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_roles" target="tb_users" />
        <mxCell id="rel2" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_users" target="tb_audit" />
        <mxCell id="rel3" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_users" target="tb_ai_logs" />
        <mxCell id="rel4" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_cat" target="tb_prod" />
        <mxCell id="rel5" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_sup" target="tb_prod" />
        <mxCell id="rel6" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_prod" target="tb_inv" />
        <mxCell id="rel7" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_loc" target="tb_inv" />
        <mxCell id="rel8" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_trans" target="tb_trans_items" />
        <mxCell id="rel9" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_prod" target="tb_trans_items" />
"""
create_drawio_file("03_so_do_erd_11_bang.drawio", "MasterERD", c3, page_w=1800, page_h=1000)

# 3A. ERD Chi tiết Phân hệ Quản trị & AI
c3a = """
        <mxCell id="hdr_3a" value="&lt;b&gt;SƠ ĐỒ ERD CHI TIẾT PHÂN HỆ QUẢN TRỊ, PHÂN QUYỀN RBAC &amp;amp; AI LOGS&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;fontColor=#000000;strokeColor=#000000;strokeWidth=2;fontSize=16;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1200" height="50" as="geometry" />
        </mxCell>
        <mxCell id="tb_roles_a" value="&lt;b&gt;ROLES (Vai trò)&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ role_name: VARCHAR(30) [U] (ADMIN/WAREHOUSE/ACCOUNTANT)&lt;br&gt;+ description: VARCHAR(255)&lt;br&gt;+ created_at: DATETIME DEFAULT NOW" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="50" y="100" width="520" height="130" as="geometry" />
        </mxCell>
        <mxCell id="tb_users_a" value="&lt;b&gt;USERS (Tài khoản người dùng)&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ role_id: INTEGER [FK -> roles.id]&lt;br&gt;+ username: VARCHAR(50) [U]&lt;br&gt;+ password_hash: VARCHAR(255) (Argon2id băm an toàn)&lt;br&gt;+ full_name: VARCHAR(100)&lt;br&gt;+ email: VARCHAR(100)&lt;br&gt;+ is_active: BOOLEAN&lt;br&gt;+ created_at: DATETIME DEFAULT NOW" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="640" y="100" width="580" height="190" as="geometry" />
        </mxCell>
        <mxCell id="tb_audit_a" value="&lt;b&gt;AUDIT_LOGS (Vết kiểm toán bất biến)&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ user_id: INTEGER [FK -> users.id]&lt;br&gt;+ action_type: VARCHAR(30) (CREATE / UPDATE / DELETE)&lt;br&gt;+ entity_name: VARCHAR(50)&lt;br&gt;+ entity_id: INTEGER&lt;br&gt;+ old_value: TEXT (Snapshot JSON cũ)&lt;br&gt;+ new_value: TEXT (Snapshot JSON mới)&lt;br&gt;+ ip_address: VARCHAR(45)&lt;br&gt;+ created_at: DATETIME DEFAULT NOW" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="50" y="340" width="520" height="210" as="geometry" />
        </mxCell>
        <mxCell id="tb_ai_logs_a" value="&lt;b&gt;AI_QUERY_LOGS (Nhật ký AI &amp;amp; Bối cảnh Ground-Truth)&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ user_id: INTEGER [FK -> users.id]&lt;br&gt;+ query_type: VARCHAR(30) (RESTOCK / ANOMALY / QA)&lt;br&gt;+ prompt_text: TEXT (Câu hỏi tự nhiên)&lt;br&gt;+ context_snapshot: TEXT (Ground-Truth JSON snapshot)&lt;br&gt;+ response_text: TEXT (Câu trả lời Markdown)&lt;br&gt;+ execution_time_ms: INTEGER (Thời gian thực thi ms)&lt;br&gt;+ created_at: DATETIME DEFAULT NOW" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="640" y="340" width="580" height="210" as="geometry" />
        </mxCell>

        <mxCell id="r_a1" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_roles_a" target="tb_users_a" />
        <mxCell id="r_a2" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_users_a" target="tb_audit_a" />
        <mxCell id="r_a3" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_users_a" target="tb_ai_logs_a" />
"""
create_drawio_file("03a_erd_nhom_nguoi_dung_ai.drawio", "SubsystemUsersAI", c3a, page_w=1300, page_h=650)

# 3B. ERD Chi tiết Phân hệ Danh mục & Kệ kho
c3b = """
        <mxCell id="hdr_3b" value="&lt;b&gt;SƠ ĐỒ ERD CHI TIẾT PHÂN HỆ DANH MỤC HÀNG HÓA &amp;amp; VỊ TRÍ KỆ KHO&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;fontColor=#000000;strokeColor=#000000;strokeWidth=2;fontSize=16;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1200" height="50" as="geometry" />
        </mxCell>
        <mxCell id="tb_cat_b" value="&lt;b&gt;CATEGORIES (Danh mục nhóm hàng)&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ code: VARCHAR(50) [U] (Vd: CAT-KEYBOARD)&lt;br&gt;+ name: VARCHAR(100) (Bàn phím cơ)&lt;br&gt;+ description: TEXT&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="50" y="100" width="520" height="140" as="geometry" />
        </mxCell>
        <mxCell id="tb_sup_b" value="&lt;b&gt;SUPPLIERS (Nhà cung cấp đối tác)&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ name: VARCHAR(150)&lt;br&gt;+ contact_person: VARCHAR(100)&lt;br&gt;+ phone: VARCHAR(20)&lt;br&gt;+ email: VARCHAR(100)&lt;br&gt;+ address: VARCHAR(255)&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="640" y="100" width="580" height="170" as="geometry" />
        </mxCell>
        <mxCell id="tb_loc_b" value="&lt;b&gt;LOCATIONS (Vị trí ô kệ vật lý trong kho)&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ code: VARCHAR(50) [U] (Định dạng: Zone-Shelf-Level: A1-01)&lt;br&gt;+ zone: VARCHAR(20) (Khu vực Zone A / Zone B)&lt;br&gt;+ shelf_level: VARCHAR(20) (Tầng 1 / Tầng 2)&lt;br&gt;+ max_capacity: INTEGER DEFAULT 500&lt;br&gt;+ is_active: BOOLEAN DEFAULT TRUE&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="50" y="320" width="520" height="190" as="geometry" />
        </mxCell>
        <mxCell id="tb_prod_b" value="&lt;b&gt;PRODUCTS (Hàng hóa &amp;amp; SKU chuẩn)&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ category_id: INTEGER [FK -> categories.id]&lt;br&gt;+ supplier_id: INTEGER [FK -> suppliers.id]&lt;br&gt;+ sku: VARCHAR(50) [U] (Mã sản phẩm duy nhất)&lt;br&gt;+ name: VARCHAR(150)&lt;br&gt;+ unit: VARCHAR(20) DEFAULT 'Cái'&lt;br&gt;+ cost_price: DECIMAL(12,2)&lt;br&gt;+ selling_price: DECIMAL(12,2)&lt;br&gt;+ min_threshold: INTEGER (Ngưỡng kích hoạt cảnh báo AI cạn tồn)&lt;br&gt;+ max_threshold: INTEGER (Sức chứa tối đa kho)&lt;br&gt;+ is_active: BOOLEAN&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="640" y="320" width="580" height="240" as="geometry" />
        </mxCell>

        <mxCell id="r_b1" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_cat_b" target="tb_prod_b" />
        <mxCell id="r_b2" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_sup_b" target="tb_prod_b" />
"""
create_drawio_file("03b_erd_nhom_danh_muc_kho.drawio", "SubsystemMasterData", c3b, page_w=1300, page_h=650)

# 3C. ERD Chi tiết Phân hệ Tồn kho & Giao dịch
c3c = """
        <mxCell id="hdr_3c" value="&lt;b&gt;SƠ ĐỒ ERD CHI TIẾT PHÂN HỆ QUẢN LÝ TỒN KHO &amp;amp; GIAO DỊCH XUẤT NHẬP&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;fontColor=#000000;strokeColor=#000000;strokeWidth=2;fontSize=16;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1300" height="50" as="geometry" />
        </mxCell>
        <mxCell id="tb_inv_c" value="&lt;b&gt;INVENTORY_ITEMS (Tồn kho thực tế tại vị trí kệ)&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ product_id: INTEGER [FK -> products.id]&lt;br&gt;+ location_id: INTEGER [FK -> locations.id]&lt;br&gt;+ current_stock: INTEGER CHECK(current_stock &gt;= 0)&lt;br&gt;+ batch_number: VARCHAR(50) (Số lô sản xuất)&lt;br&gt;+ expiry_date: DATE (Hạn sử dụng lô)&lt;br&gt;+ last_audited_at: DATETIME (Ngày kiểm kê gần nhất)&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="50" y="100" width="580" height="190" as="geometry" />
        </mxCell>
        <mxCell id="tb_trans_c" value="&lt;b&gt;INVENTORY_TRANSACTIONS (Phiếu giao dịch kho)&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ transaction_code: VARCHAR(50) [U] (Vd: PN-2026-001, PX-2026-001)&lt;br&gt;+ transaction_type: VARCHAR(20) (IMPORT / EXPORT / ADJUSTMENT)&lt;br&gt;+ supplier_id: INTEGER [FK -> suppliers.id]&lt;br&gt;+ created_by: INTEGER [FK -> users.id]&lt;br&gt;+ total_amount: DECIMAL(15,2) DEFAULT 0.00&lt;br&gt;+ note: TEXT&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="700" y="100" width="600" height="190" as="geometry" />
        </mxCell>
        <mxCell id="tb_trans_items_c" value="&lt;b&gt;INVENTORY_TRANSACTION_ITEMS (Chi tiết từng dòng mặt hàng trong phiếu)&lt;/b&gt;&lt;hr&gt;+ id: INTEGER [PK]&lt;br&gt;+ transaction_id: INTEGER [FK -> inventory_transactions.id]&lt;br&gt;+ product_id: INTEGER [FK -> products.id]&lt;br&gt;+ location_id: INTEGER [FK -> locations.id]&lt;br&gt;+ quantity: INTEGER CHECK(quantity &gt; 0)&lt;br&gt;+ unit_price: DECIMAL(12,2) NOT NULL&lt;br&gt;+ subtotal: DECIMAL(15,2) NOT NULL&lt;br&gt;+ created_at: DATETIME" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;align=left;spacingLeft=10;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="360" y="360" width="640" height="190" as="geometry" />
        </mxCell>

        <mxCell id="r_c1" value="1 : N" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_trans_c" target="tb_trans_items_c" />
        <mxCell id="r_c2" value="Cập nhật số dư kho" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;dashed=1;fontFamily=Times New Roman;" edge="1" parent="1" source="tb_trans_items_c" target="tb_inv_c" />
"""
create_drawio_file("03c_erd_nhom_ton_kho_giao_dich.drawio", "SubsystemInventoryTrans", c3c, page_w=1400, page_h=650)

# 4. Hoạt động Nhập kho
c4 = """
        <mxCell id="i_hdr" value="&lt;b&gt;LƯỢC ĐỒ HOẠT ĐỘNG QUY TRÌNH NHẬP KHO (IMPORT ACTIVITY)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;fontColor=#000000;strokeColor=#000000;strokeWidth=2;fontSize=16;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1200" height="50" as="geometry" />
        </mxCell>
        <mxCell id="i_start" value="Khởi đầu: Hàng cập bến kho từ Nhà cung cấp" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="100" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="i_step1" value="Kiểm tra chứng từ giao nhận &amp;amp; Hóa đơn vận chuyển" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="190" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="i_step2" value="Thủ kho kiểm tra quy cách thực tế sản phẩm" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="280" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="i_dec" value="Quy cách đạt chuẩn &amp;amp; Đầy đủ số lượng?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontStyle=1;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="380" y="370" width="340" height="100" as="geometry" />
        </mxCell>
        <mxCell id="i_reject" value="&lt;b&gt;TỪ CHỐI NHẬP HÀNG&lt;/b&gt;&lt;br&gt;Lập biên bản sự cố lỗi&lt;br&gt;&amp;amp; Hoàn trả Nhà cung cấp" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="850" y="380" width="260" height="80" as="geometry" />
        </mxCell>
        <mxCell id="i_step3" value="Phân bổ hàng hóa vào vị trí kệ còn sức chứa (locations)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="510" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="i_step4" value="Nhập thông tin phiếu nhập &amp;amp; số lô / hạn sử dụng vào hệ thống" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="600" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="i_step5" value="Tạo phiếu nhập trong inventory_transactions &amp;amp; items" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="690" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="i_step6" value="Cộng dồn số lượng thực tế trong bảng inventory_items" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="780" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="i_step7" value="Ghi nhận nhật ký kiểm toán Audit Log &amp;amp; Cập nhật Realtime KPI" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="870" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="i_end" value="Kết thúc: Hoàn tất nhập kho, in biên bản &amp;amp; cập nhật báo cáo" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="960" width="500" height="60" as="geometry" />
        </mxCell>

        <mxCell id="ie1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="i_start" target="i_step1" />
        <mxCell id="ie2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="i_step1" target="i_step2" />
        <mxCell id="ie3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="i_step2" target="i_dec" />
        <mxCell id="ie4" value="[Yes: Đạt chuẩn]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="i_dec" target="i_step3" />
        <mxCell id="ie5" value="[No: Lỗi]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;dashed=1;fontFamily=Times New Roman;" edge="1" parent="1" source="i_dec" target="i_reject" />
        <mxCell id="ie6" value="Đóng giao dịch lỗi" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;dashed=1;fontFamily=Times New Roman;" edge="1" parent="1" source="i_reject" target="i_end" />
        <mxCell id="ie7" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="i_step3" target="i_step4" />
        <mxCell id="ie8" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="i_step4" target="i_step5" />
        <mxCell id="ie9" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="i_step5" target="i_step6" />
        <mxCell id="ie10" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="i_step6" target="i_step7" />
        <mxCell id="ie11" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="i_step7" target="i_end" />
"""
create_drawio_file("04_luoc_do_hoat_dong_nhap_kho.drawio", "ImportActivity", c4, page_w=1400, page_h=1100)

# 5. Hoạt động Xuất kho
c5 = """
        <mxCell id="e_hdr" value="&lt;b&gt;LƯỢC ĐỒ HOẠT ĐỘNG QUY TRÌNH XUẤT KHO (EXPORT ACTIVITY)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;fontColor=#000000;strokeColor=#000000;strokeWidth=2;fontSize=16;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1200" height="50" as="geometry" />
        </mxCell>
        <mxCell id="e_start" value="Khởi đầu: Nhận yêu cầu xuất kho từ khách hàng / đại lý" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="100" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="e_step1" value="Thủ kho chọn khách hàng &amp;amp; tạo phiếu xuất kho mới" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="190" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="e_step2" value="Thêm danh mục SKU và số lượng yêu cầu xuất" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="280" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="e_dec1" value="Kiểm tra tồn kho:&lt;br&gt;Số lượng xuất &amp;lt;= Tồn khả dụng?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontStyle=1;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="380" y="370" width="340" height="100" as="geometry" />
        </mxCell>
        <mxCell id="e_err" value="&lt;b&gt;BÁO LỖI NGHIỆP VỤ&lt;/b&gt;&lt;br&gt;Kho không đủ số lượng&lt;br&gt;tồn khả dụng (HTTP 400)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="850" y="380" width="260" height="80" as="geometry" />
        </mxCell>
        <mxCell id="e_step3" value="Khóa bản ghi tồn kho tạm thời (Row-level Locking FOR UPDATE)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="510" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="e_step4" value="Trừ số lượng thực tế trong bảng inventory_items" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="600" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="e_dec2" value="Kiểm tra ngưỡng an toàn:&lt;br&gt;Tồn kho &amp;lt; min_threshold?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontStyle=1;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="380" y="690" width="340" height="100" as="geometry" />
        </mxCell>
        <mxCell id="e_ai_alert" value="Kích hoạt cảnh báo AI Alert: Đề xuất lập phiếu tái nhập" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="830" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="e_step5" value="Ghi nhận nhật ký kiểm toán Audit Log và cập nhật Realtime KPI" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="920" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="e_end" value="Kết thúc: Bàn giao hàng hóa và in phiếu xuất kho" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="1020" width="500" height="60" as="geometry" />
        </mxCell>

        <mxCell id="ee1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="e_start" target="e_step1" />
        <mxCell id="ee2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="e_step1" target="e_step2" />
        <mxCell id="ee3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="e_step2" target="e_dec1" />
        <mxCell id="ee4" value="[Yes: Đủ hàng]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="e_dec1" target="e_step3" />
        <mxCell id="ee5" value="[No: Hết hàng]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;dashed=1;fontFamily=Times New Roman;" edge="1" parent="1" source="e_dec1" target="e_err" />
        <mxCell id="ee6" value="Hủy &amp;amp; Rollback" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;dashed=1;fontFamily=Times New Roman;" edge="1" parent="1" source="e_err" target="e_end" />
        <mxCell id="ee7" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="e_step3" target="e_step4" />
        <mxCell id="ee8" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="e_step4" target="e_dec2" />
        <mxCell id="ee9" value="[Yes: Cạn tồn]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="e_dec2" target="e_ai_alert" />
        <mxCell id="ee10" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="e_ai_alert" target="e_step5" />
        <mxCell id="ee11" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="e_step5" target="e_end" />
"""
create_drawio_file("05_luoc_do_hoat_dong_xuat_kho.drawio", "ExportActivity", c5, page_w=1400, page_h=1150)

# 6. Sơ đồ tuần tự Giao dịch kho
c6 = """
        <mxCell id="hdr6" value="&lt;b&gt;SƠ ĐỒ TUẦN TỰ GIAO DỊCH KHO (SEQUENCE DIAGRAM)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;fontColor=#000000;strokeColor=#000000;strokeWidth=2;fontSize=16;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1200" height="50" as="geometry" />
        </mxCell>
        <mxCell id="ll_user" value="Thủ kho (User)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="60" y="90" width="130" height="50" as="geometry" />
        </mxCell>
        <mxCell id="ll_fe" value="React Frontend" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="270" y="90" width="130" height="50" as="geometry" />
        </mxCell>
        <mxCell id="ll_api" value="FastAPI APIRouter" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="480" y="90" width="140" height="50" as="geometry" />
        </mxCell>
        <mxCell id="ll_svc" value="InventoryService" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="700" y="90" width="140" height="50" as="geometry" />
        </mxCell>
        <mxCell id="ll_db" value="SQL Database" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="920" y="90" width="130" height="50" as="geometry" />
        </mxCell>
        <mxCell id="ll_audit" value="AuditLog Service" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="1120" y="90" width="130" height="50" as="geometry" />
        </mxCell>
"""
create_drawio_file("06_so_do_tuan_tu_nhap_xuat.drawio", "SequenceTrans", c6, page_w=1350, page_h=900)

# 7. Pipeline AI Fallback
c7 = """
        <mxCell id="hdrai" value="&lt;b&gt;SƠ ĐỒ KIẾN TRÚC PIPELINE AI 2 LỚP (DUAL-LAYER AI FALLBACK)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;fontColor=#000000;strokeColor=#000000;strokeWidth=2;fontSize=16;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1150" height="50" as="geometry" />
        </mxCell>
        <mxCell id="req" value="&lt;b&gt;Client Request&lt;/b&gt;&lt;br&gt;Dự báo tồn kho / Hỏi đáp NLP" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="60" y="140" width="220" height="80" as="geometry" />
        </mxCell>
        <mxCell id="agg" value="&lt;b&gt;Data Aggregator (Snapshot)&lt;/b&gt;&lt;br&gt;Trích xuất CSDL thực tế 100%&lt;br&gt;Tồn kho, vận tốc xuất 30 ngày" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="340" y="140" width="240" height="80" as="geometry" />
        </mxCell>
        <mxCell id="dec" value="Có API Key &amp;amp;&lt;br&gt;Kết nối Cloud OK?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontStyle=1;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="650" y="125" width="170" height="110" as="geometry" />
        </mxCell>
        <mxCell id="gemini" value="&lt;b&gt;Lớp 1: Google Gemini LLM&lt;/b&gt;&lt;br&gt;gemini-1.5-flash / gemini-2.0&lt;br&gt;Ground-truth Context Injection" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="900" y="140" width="260" height="80" as="geometry" />
        </mxCell>
        <mxCell id="rule" value="&lt;b&gt;Lớp 2: Local Rule Engine (Fallback)&lt;/b&gt;&lt;br&gt;Tính toán công thức Burn-rate,&lt;br&gt;Z-score Outlier, NLP Keyword Matcher" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="605" y="320" width="260" height="90" as="geometry" />
        </mxCell>
        <mxCell id="out" value="&lt;b&gt;Structured Output &amp;amp; Smart UI Formatter&lt;/b&gt;&lt;br&gt;Render Bảng Tailwind với đèn LED cảnh báo, Nút tạo phiếu nhập nhanh, Tab CSDL JSON" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="400" y="470" width="550" height="80" as="geometry" />
        </mxCell>

        <mxCell id="ea1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="req" target="agg" />
        <mxCell id="ea2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="agg" target="dec" />
        <mxCell id="ea3" value="Có [Yes]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;" edge="1" parent="1" source="dec" target="gemini" />
        <mxCell id="ea4" value="Mất mạng / Không Key [Fallback]" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;dashed=1;fontFamily=Times New Roman;" edge="1" parent="1" source="dec" target="rule" />
        <mxCell id="ea5" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="gemini" target="out" />
        <mxCell id="ea6" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=2;" edge="1" parent="1" source="rule" target="out" />
"""
create_drawio_file("07_so_do_pipeline_ai_fallback.drawio", "AIPipeline", c7)

# 8. Sơ đồ tuần tự Hỏi đáp AI
c8 = """
        <mxCell id="hdr8" value="&lt;b&gt;SƠ ĐỒ TUẦN TỰ TRỢ LÝ HỎI ĐÁP AI (NLP SEQUENCE DIAGRAM)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;fontColor=#000000;strokeColor=#000000;strokeWidth=2;fontSize=16;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1200" height="50" as="geometry" />
        </mxCell>
        <mxCell id="l8_user" value="Người dùng" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="60" y="90" width="130" height="50" as="geometry" />
        </mxCell>
        <mxCell id="l8_ui" value="AI Chat Console" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="270" y="90" width="140" height="50" as="geometry" />
        </mxCell>
        <mxCell id="l8_api" value="FastAPI /api/ai/ask" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="490" y="90" width="140" height="50" as="geometry" />
        </mxCell>
        <mxCell id="l8_agg" value="Data Aggregator" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="710" y="90" width="140" height="50" as="geometry" />
        </mxCell>
        <mxCell id="l8_ai" value="AI Dual Engine" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="930" y="90" width="140" height="50" as="geometry" />
        </mxCell>
        <mxCell id="l8_view" value="Smart Table Viewer" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="1140" y="90" width="140" height="50" as="geometry" />
        </mxCell>
"""
create_drawio_file("08_so_do_tuan_tu_hoi_dap_ai.drawio", "SequenceAI", c8, page_w=1350, page_h=900)

# 9. Thuật toán bất thường
c9 = """
        <mxCell id="hdr9" value="&lt;b&gt;LƯU ĐỒ THUẬT TOÁN PHÁT HIỆN BẤT THƯỜNG &amp;amp; TÍNH BURN-RATE&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;fontColor=#000000;strokeColor=#000000;strokeWidth=2;fontSize=16;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1200" height="50" as="geometry" />
        </mxCell>
        <mxCell id="a_step1" value="Thu thập dữ liệu giao dịch xuất kho 30 ngày gần nhất (T = 30)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="100" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="a_step2" value="Tính tốc độ xuất bình quân ngày: V = Tổng xuất 30 ngày / 30" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="190" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="a_dec1" value="V &amp;gt; 0 (Có phát sinh xuất kho)?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontStyle=1;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="380" y="280" width="340" height="90" as="geometry" />
        </mxCell>
        <mxCell id="a_zero" value="&lt;b&gt;TỒN KHO ỔN ĐỊNH&lt;/b&gt;&lt;br&gt;Gán Days = 999 ngày" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="840" y="290" width="240" height="70" as="geometry" />
        </mxCell>
        <mxCell id="a_step3" value="Tính số ngày cạn tồn: DepletionDays = Stock / V" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="400" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="a_dec2" value="Days &amp;lt;= 7 ngày hoặc Stock &amp;lt; min_threshold?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontStyle=1;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="380" y="490" width="340" height="90" as="geometry" />
        </mxCell>
        <mxCell id="a_alert" value="Kích hoạt cảnh báo khẩn: Cần lập kế hoạch nhập hàng" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="610" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="a_step4" value="Tính độ lệch chuẩn sản lượng xuất ngày: Z-score" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="700" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="a_dec3" value="|Z-score| &amp;gt; 2.5 (Dị biệt sản lượng)?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontStyle=1;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="380" y="790" width="340" height="90" as="geometry" />
        </mxCell>
        <mxCell id="a_flag" value="Gắn cờ Bất thường (Anomaly Flag) &amp;amp; Đề xuất kiểm kê" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="910" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="a_end" value="Kết thúc: Lưu kết quả phân tích vào bộ nhớ &amp;amp; CSDL" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="300" y="1000" width="500" height="60" as="geometry" />
        </mxCell>
"""
create_drawio_file("09_so_do_phan_tich_bat_thuong.drawio", "AnomalyFlowchart", c9, page_w=1400, page_h=1100)

# 10. Sitemap
c10 = """
        <mxCell id="hdr10" value="&lt;b&gt;SƠ ĐỒ ĐIỀU HƯỚNG CẤU TRÚC GIAO DIỆN (FRONTEND SITEMAP)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;fontColor=#000000;strokeColor=#000000;strokeWidth=2;fontSize=16;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1400" height="50" as="geometry" />
        </mxCell>
        <mxCell id="sm_root" value="&lt;b&gt;HỆ THỐNG QUẢN LÝ KHO AI&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=14;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="580" y="90" width="320" height="50" as="geometry" />
        </mxCell>
        <mxCell id="c_1" value="&lt;b&gt;1. TỔNG QUAN&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="60" y="180" width="240" height="40" as="geometry" />
        </mxCell>
        <mxCell id="c_2" value="&lt;b&gt;2. KHO HÀNG&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="340" y="180" width="240" height="40" as="geometry" />
        </mxCell>
        <mxCell id="c_3" value="&lt;b&gt;3. GIAO DỊCH&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="620" y="180" width="240" height="40" as="geometry" />
        </mxCell>
        <mxCell id="c_4" value="&lt;b&gt;4. AI HUB&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="900" y="180" width="240" height="40" as="geometry" />
        </mxCell>
        <mxCell id="c_5" value="&lt;b&gt;5. BẢO MẬT&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=13;fontFamily=Times New Roman;" vertex="1" parent="1">
          <mxGeometry x="1180" y="180" width="240" height="40" as="geometry" />
        </mxCell>
"""
create_drawio_file("10_so_do_sitemap_giao_dien.drawio", "FrontendSitemap", c10, page_w=1500, page_h=700)

print("================================================================")
print("ĐÃ HOÀN THÀNH XUẤT TOÀN BỘ 13 TỆP DRAW.IO CHUẨN MỞ CHỈNH SỬA ĐƯỢC!")
print("================================================================")
