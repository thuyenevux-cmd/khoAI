def test_ai_inventory_report(client, admin_headers):
    response = client.post("/api/ai/inventory-report", json={"period": "30_DAYS"}, headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "markdown_report" in data
    assert "data_snapshot" in data
    assert "provider" in data

def test_ai_restock_recommendation(client, admin_headers):
    response = client.post("/api/ai/restock-recommendation", json={"period": "30_DAYS"}, headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "markdown_report" in data

def test_ai_anomaly_summary(client, admin_headers):
    response = client.post("/api/ai/anomaly-summary", json={"period": "30_DAYS"}, headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "markdown_report" in data

def test_ai_assistant_ask(client, admin_headers):
    response = client.post("/api/ai/ask", json={"question": "Kho còn bao nhiêu bàn phím cơ?"}, headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "answer_markdown" in data
    assert "data_context" in data
    assert "provider" in data
    assert data["question"] == "Kho còn bao nhiêu bàn phím cơ?"

