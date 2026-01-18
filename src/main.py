from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Простые endpoints для тестов
@app.get("/users")
def get_user(email: str):
    if email == "i.i.ivanov@mail.com":
        return {"id": 1, "name": "Ivan Ivanov", "email": email}
    return {"detail": "User not found"}, 404

@app.post("/users")
def create_user(user: dict):
    return {"id": 999, "message": "User created"}, 201

@app.delete("/users")
def delete_user(email: str):
    return {"message": "User deleted"}, 204
