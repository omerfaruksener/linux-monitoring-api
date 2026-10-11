from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_System_info():
    response = client.get("/api/system")
    assert response.status_code == 200
    data = response.json()
    assert "os" in data
    assert "uptime_seconds" in data
    assert data["cpu_count"] > 0

def test_top_processes_valid_limit():
    response = client.get("/api/processes?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3 #Dönen süreç sayısı 3 veya daha a olmalı

def test_top_processes_invalid_limit():
    # 50'den büyük bir limit göndererek API'nin bunu reddettiğini test ediyoruz
    response = client.get("/api/processes?limit=100")
    assert response.status_code == 422  # 422 Unprocessable Entity dönmeli