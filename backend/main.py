from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import authenticate
from services.price_service import get_all_prices

app = FastAPI()

# Разрешаем React обращаться к API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
def login(data: dict):
    username = data["username"]
    password = data["password"]

    authenticate(username, password)
    return {"status": "ok"}

@app.get("/prices/{product_id}")
def get_prices(product_id: str):
    prices = get_all_prices(product_id)
    return prices
