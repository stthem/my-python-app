from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root():
    '''Проверка корневого endpoint'''
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    '''Проверка health check'''
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_user():
    '''Проверка получения пользователя'''
    # Существующий
    response = client.get("/users", params={"email": "i.i.ivanov@mail.com"})
    assert response.status_code == 200
    assert response.json()["id"] == 1
    
    # Несуществующий
    response = client.get("/users", params={"email": "nonexistent@mail.com"})
    assert response.status_code == 404

def test_create_user():
    '''Проверка создания пользователя'''
    response = client.post("/users", json={"name": "Test", "email": "test@mail.com"})
    assert response.status_code == 201
    assert "id" in response.json()

def test_delete_user():
    '''Проверка удаления пользователя'''
    response = client.delete("/users", params={"email": "any@mail.com"})
    assert response.status_code == 204
