"""Фейковая база данных для тестирования"""

class FakeDB:
    def __init__(self):
        self.users = []
        self.next_id = 1
        # Инициализируем тестовыми пользователями
        self.create_user('Ivan Ivanov', 'i.i.ivanov@mail.com')
        self.create_user('Petr Petrov', 'p.p.petrov@mail.com')
    
    def get_user_by_email(self, email: str):
        for user in self.users:
            if user['email'] == email:
                return user
        return None
    
    def create_user(self, name: str, email: str):
        user = {
            'id': self.next_id,
            'name': name,
            'email': email
        }
        self.users.append(user)
        self.next_id += 1
        return user
    
    def delete_user_by_email(self, email: str):
        user = self.get_user_by_email(email)
        if user:
            self.users.remove(user)
            return True
        return False

# Глобальный инстанс
db = FakeDB()
