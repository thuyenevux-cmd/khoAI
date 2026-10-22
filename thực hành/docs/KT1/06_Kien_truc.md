# 06. KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)

---

## 1. TỔNG QUAN KIẾN TRÚC HỆ THỐNG

Hệ thống được thiết kế theo kiến trúc 3-Tier phân rã sạch sẽ (Clean Layered Architecture):

```text
[ React + Vite Client (Frontend SPA) ]
                  │
                  ▼ HTTP / REST APIs (JSON + JWT)
[ FastAPI Backend (Router Layer) ]
                  │
                  ▼ Service Layer (Transaction & Business Logic)
        ┌─────────┴─────────┐
        ▼                   ▼
[ SQLAlchemy ORM ]   [ AI Analytics Adapter ]
        │                   │
        ▼                   ▼
 [ MySQL / SQLite ]  [ OpenAI API / Prompt Templates ]
```

---

## 2. PHÂN RÃ CÁC TẦNG CHỨC NĂNG BACKEND

1. **Router / Controller Layer (`app/routers/`)**:
   - Khai báo các REST API endpoints (`/api/auth`, `/api/products`, `/api/imports`, `/api/exports`, `/api/ai`).
   - Xử lý Request/Response validation bằng Pydantic schemas.
   - Áp dụng Middleware bảo mật xác thực JWT token và phân quyền vai trò (`require_roles`).

2. **Service Layer (`app/services/`)**:
   - Chứa logic nghiệp vụ cốt lõi: Tính toán tồn kho, kiểm tra điều kiện xuất kho, gọi AI Engine.
   - Đảm bảo ranh giới **DB Transaction (ACID)**. Mọi thao tác Nhập/Xuất kho được bọc trong block `db.commit()` / `db.rollback()`.

3. **Repository / Data Access Layer (`app/repositories/`)**:
   - Truy vấn CSDL thông qua SQLAlchemy ORM Models.
   - Thực thi các câu lệnh Pessimistic Locking `with_for_update()` khi truy vấn tồn kho cho nghiệp vụ xuất.

4. **AI Integration Layer (`app/services/ai_service.py`)**:
   - Tách biệt logic gọi AI ra khỏi Controller.
   - Đọc các Prompt Template từ file tĩnh `app/prompts/*.txt`.
   - Chuẩn bị payload JSON dữ liệu thật và tương tác với OpenAI API Client.

---

## 3. CẤU TRÚC THƯ MỤC CHUẨN DỰ ÁN

```text
d:\khoAI/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/           # config, security, database
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic validation schemas
│   │   ├── routers/        # FastAPI API endpoints
│   │   ├── services/       # Business & AI services
│   │   ├── repositories/   # DB data access layer
│   │   ├── prompts/        # System & User prompt templates
│   │   ├── utils/          # Helpers & formatters
│   │   └── db/             # Seed data script
│   ├── tests/              # Pytest automated test suite
│   ├── alembic/            # Database migrations
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # App views (Dashboard, Products, Import, Export, AI)
│   │   ├── layouts/        # Sidebar, Header layout
│   │   ├── services/       # Axios API client services
│   │   ├── contexts/       # Auth context
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── docs/                   # Full documentation suites (KT1, KT2, KT3, ai-evidence, final)
└── docker-compose.yml
```
