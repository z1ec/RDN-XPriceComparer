import json
from fastapi import HTTPException

USERS_FILE = "users.json"

def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["users"]

def authenticate(username: str, password: str):
    users = load_users()
    for u in users:
        if u["username"] == username and u["password"] == password:
            return True
    raise HTTPException(status_code=401, detail="Invalid credentials")
