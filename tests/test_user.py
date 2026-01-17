from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

NEW_USER = {
	'name': 'New User',
	'email': 'new.user@mail.com'
}

def setup_module(module):
	pass

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/users/", params={'email': EXISTING_USERS[0]['email']})
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == EXISTING_USERS[0]['id']
    assert data['name'] == EXISTING_USERS[0]['name']
    assert data['email'] == EXISTING_USERS[0]['email']

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/users/", params={'email': 'nonexisten@mail.com'})
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'
   

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    response = client.post("/users/", json=NEW_USER)
    assert response.status_code == 201
    user_id = response.json()
    assert isinstance(user_id, int)

    get_response = client.get("/users/", params={'email': NEW_USER['email']})
    assert get_response.status_code == 200
    assert get_response.json()['name'] == NEW_USER['name']
    

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    duplicate_user = {
        'name': 'Duplicate User',
        'email': EXISTING_USERS[0]['email']  # Существующий email
    }
    
    response = client.post("/users/", json=duplicate_user)
    assert response.status_code == 409
    assert response.json()['detail'] == 'User with this email already exists'

def test_delete_user():
    '''Удаление пользователя'''
    user_to_delete = {
        'name': 'User to Delete',
        'email': 'delete.me@mail.com'
    }
    
    create_response = client.post("/users/", json=user_to_delete)
    user_id = create_response.json()
    
    # Удаляем пользователя
    delete_response = client.delete("/users/", params={'email': user_to_delete['email']})
    assert delete_response.status_code == 204
    
    # Проверяем что пользователь удален
    get_response = client.get("/users/", params={'email': user_to_delete['email']})
    assert get_response.status_code == 404
