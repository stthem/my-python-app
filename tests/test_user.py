# tests/test_user.py
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root():
    '''Проверка что приложение запускается'''
    response = client.get("/")
    assert response.status_code == 200

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/users", params={'email': 'i.i.ivanov@mail.com'})
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    assert data['name'] == 'Ivan Ivanov'
    assert data['email'] == 'i.i.ivanov@mail.com'

def test_get_nonexistent_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/users", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {'name': 'New User', 'email': 'new.user@mail.com'}
    response = client.post("/users", json=new_user)
    assert response.status_code == 201
    user_id = response.json()
    assert isinstance(user_id, int)
    
    # Проверяем что пользователь создан
    get_response = client.get("/users", params={'email': 'new.user@mail.com'})
    assert get_response.status_code == 200
    assert get_response.json()['name'] == 'New User'

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    duplicate_user = {'name': 'Duplicate User', 'email': 'i.i.ivanov@mail.com'}
    response = client.post("/users", json=duplicate_user)
    assert response.status_code == 409
    assert 'already exists' in response.json()['detail']

def test_delete_user():
    '''Удаление пользователя'''
    # Сначала создаем пользователя для удаления
    user_to_delete = {'name': 'User to Delete', 'email': 'delete.me@mail.com'}
    create_response = client.post("/users", json=user_to_delete)
    assert create_response.status_code == 201
    
    # Удаляем
    delete_response = client.delete("/users", params={'email': 'delete.me@mail.com'})
    assert delete_response.status_code == 204
    
    # Проверяем что удален
    get_response = client.get("/users", params={'email': 'delete.me@mail.com'})
    assert get_response.status_code == 404
