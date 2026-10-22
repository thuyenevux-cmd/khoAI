def test_login_success(client):
    response = client.post("/api/auth/login", json={"username": "admin_test", "password": "Admin@123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "admin_test"
    assert data["user"]["role"] == "ADMIN"

def test_login_failure_wrong_password(client):
    response = client.post("/api/auth/login", json={"username": "admin_test", "password": "WrongPassword"})
    assert response.status_code == 401

def test_get_me(client, admin_headers):
    response = client.get("/api/auth/me", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "admin_test"

def test_user_management_rbac(client, warehouse_headers):
    # Warehouse user trying to list users -> 403 Forbidden
    response = client.get("/api/auth/users", headers=warehouse_headers)
    assert response.status_code == 403
