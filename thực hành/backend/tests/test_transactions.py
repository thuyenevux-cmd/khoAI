def test_import_transaction_success(client, warehouse_headers):
    # Fetch product ID
    prod_res = client.get("/api/products", headers=warehouse_headers)
    product_id = prod_res.json()[0]["id"]
    initial_stock = prod_res.json()[0]["current_stock"]

    # Import 10 items
    payload = {
        "supplier_id": 1,
        "note": "Test Import Receipt",
        "details": [{"product_id": product_id, "quantity": 10, "unit_price": 500.0}]
    }
    response = client.post("/api/imports", json=payload, headers=warehouse_headers)
    assert response.status_code == 201
    
    # Check inventory increased
    prod_res_after = client.get(f"/api/products/{product_id}", headers=warehouse_headers)
    assert prod_res_after.json()["current_stock"] == initial_stock + 10

def test_export_transaction_success(client, warehouse_headers):
    prod_res = client.get("/api/products", headers=warehouse_headers)
    product_id = prod_res.json()[0]["id"]
    stock_before = prod_res.json()[0]["current_stock"]

    # Export 5 items
    payload = {
        "receiver": "Phòng Kế Hoạch",
        "note": "Test Export Receipt",
        "details": [{"product_id": product_id, "quantity": 5}]
    }
    response = client.post("/api/exports", json=payload, headers=warehouse_headers)
    assert response.status_code == 201

    prod_res_after = client.get(f"/api/products/{product_id}", headers=warehouse_headers)
    assert prod_res_after.json()["current_stock"] == stock_before - 5

def test_export_transaction_refuse_overflow_negative_stock(client, warehouse_headers):
    prod_res = client.get("/api/products", headers=warehouse_headers)
    product_id = prod_res.json()[0]["id"]
    stock_before = prod_res.json()[0]["current_stock"]

    # Attempt to export 9999 items (far exceeding current stock)
    payload = {
        "receiver": "Phòng Kế Hoạch",
        "note": "Attempt Overflow Export",
        "details": [{"product_id": product_id, "quantity": 9999}]
    }
    response = client.post("/api/exports", json=payload, headers=warehouse_headers)
    assert response.status_code == 400
    assert "không đủ để xuất" in response.json()["detail"]

    # Verify stock remains UNCHANGED
    prod_res_after = client.get(f"/api/products/{product_id}", headers=warehouse_headers)
    assert prod_res_after.json()["current_stock"] == stock_before

def test_accountant_cannot_create_export(client, accountant_headers):
    payload = {
        "receiver": "Test Accountant",
        "details": [{"product_id": 1, "quantity": 1}]
    }
    response = client.post("/api/exports", json=payload, headers=accountant_headers)
    assert response.status_code == 403
