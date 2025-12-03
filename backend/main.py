from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import authenticate
from services.price_service import get_all_prices

from parsers.site1_parser import get_price_from_site1
from parsers.site2_parser import get_price_from_site2

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

@app.get("/test")
async def test():
    return {"status": "ok", "message": "API работает!"}

@app.get("/price")
def get_product_price():
    url = "https://smartcode.ru/shtrihkodirovanie_i_identifikatsiya/printery_shtrih_koda/godex_ge330_use_011-ge3e02-000"
    price = get_price_from_site1(url)
    return {"price": price}

@app.get("/price2")
def get_product_price():
    url = "https://smartcode.ru/shtrihkodirovanie_i_identifikatsiya/printery_shtrih_koda/godex_ge330_use_011-ge3e02-000"
    price = get_price_from_site1(url)
    return {"price": price}