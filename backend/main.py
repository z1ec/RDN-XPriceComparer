from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from pathlib import Path
import json
import secrets

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OVERRIDES_DIR = DATA_DIR / "overrides"
USERS_FILE = DATA_DIR / "users.json"
PRICES_FILE = DATA_DIR / "prices.json"

OVERRIDES_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="XPriceComparer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    username: str

class ProductUpdate(BaseModel):
    product_id: str
    name_user: Optional[str] = None
    tags: Optional[List[str]] = None
    comment: Optional[str] = None

sessions: Dict[str, str] = {}

def load_users() -> Dict[str, str]:
    with USERS_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return {u["username"]: u["password"] for u in data.get("users", [])}

def get_current_username(authorization: str = Header(...)) -> str:
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = authorization[len(prefix):]
    username = sessions.get(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username

def load_prices() -> dict:
    with PRICES_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def overrides_path(username: str) -> Path:
    return OVERRIDES_DIR / f"{username}.json"

def load_overrides(username: str) -> dict:
    path = overrides_path(username)
    if not path.exists():
        return {"overrides": []}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_overrides(username: str, data: dict) -> None:
    path = overrides_path(username)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    users = load_users()
    if payload.username not in users or users[payload.username] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = secrets.token_hex(32)
    sessions[token] = payload.username

    return LoginResponse(token=token, username=payload.username)

@app.get("/data")
def get_data(username: str = Depends(get_current_username)):
    prices = load_prices()
    overrides = load_overrides(username)

    overrides_by_id = {o["product_id"]: o for o in overrides.get("overrides", [])}

    merged_products = []
    for p in prices.get("products", []):
        o = overrides_by_id.get(p["id"], {})
        merged_products.append(
            {
                "id": p["id"],
                "store": p.get("store"),
                "name_original": p.get("name_original"),
                "name_user": o.get("name_user"),
                "price": p.get("price"),
                "tags": o.get("tags", []),
                "comment": o.get("comment", ""),
            }
        )

    return {
        "user": username,
        "updated_at": prices.get("updated_at"),
        "products": merged_products,
    }

@app.post("/update_product")
def update_product(update: ProductUpdate, username: str = Depends(get_current_username)):
    prices = load_prices()
    product_ids = {p["id"] for p in prices.get("products", [])}
    if update.product_id not in product_ids:
        raise HTTPException(status_code=404, detail="Product not found")

    overrides = load_overrides(username)
    items = overrides.get("overrides", [])

    for item in items:
        if item["product_id"] == update.product_id:
            if update.name_user is not None:
                item["name_user"] = update.name_user
            if update.tags is not None:
                item["tags"] = update.tags
            if update.comment is not None:
                item["comment"] = update.comment
            break
    else:
        items.append(
            {
                "product_id": update.product_id,
                "name_user": update.name_user,
                "tags": update.tags or [],
                "comment": update.comment or "",
            }
        )

    overrides["overrides"] = items
    save_overrides(username, overrides)

    return {"status": "ok", "product_id": update.product_id}
