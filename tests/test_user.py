# tests/test_user.py - супер простые тесты
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_all_endpoints_return_something():
    '''Просто проверяем что все endpoints что-то возвращают'''
    
    # 1. Root
    response = client.get("/")
    assert response.status_code == 200
    print(f"GET / -> {response.status_code}")
    
    # 2. Health
    response = client.get("/health")
    assert response.status_code == 200
    print(f"GET /health -> {response.status_code}")
    
    # 3. Get user (любой email)
    response = client.get("/users", params={"email": "test@test.com"})
    assert response.status_code == 200
    print(f"GET /users -> {response.status_code}")
    
    # 4. Create user
    response = client.post("/users", json={"name": "Test", "email": "test@test.com"})
    assert response.status_code == 200
    print(f"POST /users -> {response.status_code}")
    
    # 5. Delete user
    response = client.delete("/users", params={"email": "test@test.com"})
    assert response.status_code == 200
    print(f"DELETE /users -> {response.status_code}")
    
    print(" All endpoints respond with 200 OK")
    assert True
