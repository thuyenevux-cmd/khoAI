import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app
from app.db.seed import seed_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_inventory.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Run seed data on test DB
    from app.core.security import get_password_hash
    from app.models import User, Category, Unit, Supplier, Product, Inventory
    
    db = TestingSessionLocal()
    admin = User(username="admin_test", password_hash=get_password_hash("Admin@123"), full_name="Admin Test", role="ADMIN")
    wh = User(username="warehouse_test", password_hash=get_password_hash("Warehouse@123"), full_name="WH Test", role="WAREHOUSE")
    acc = User(username="accountant_test", password_hash=get_password_hash("Accountant@123"), full_name="Acc Test", role="ACCOUNTANT")
    db.add_all([admin, wh, acc])
    
    cat = Category(code="CAT_TEST", name="Cat Test")
    unit = Unit(code="UNIT_TEST", name="Unit Test")
    sup = Supplier(code="SUP_TEST", name="Sup Test")
    db.add_all([cat, unit, sup])
    db.commit()
    
    prod = Product(code="HH_TEST", name="Bàn phím cơ Test", category_id=cat.id, unit_id=unit.id, minimum_stock=10)
    db.add(prod)
    db.flush()
    inv = Inventory(product_id=prod.id, quantity=15)
    db.add(inv)
    db.commit()
    db.close()

    yield

    Base.metadata.drop_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def admin_headers(client):
    res = client.post("/api/auth/login", json={"username": "admin_test", "password": "Admin@123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def warehouse_headers(client):
    res = client.post("/api/auth/login", json={"username": "warehouse_test", "password": "Warehouse@123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def accountant_headers(client):
    res = client.post("/api/auth/login", json={"username": "accountant_test", "password": "Accountant@123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
