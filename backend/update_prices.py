from pathlib import Path
import json
import random
from datetime import datetime

BASE_DIR = Path(__file__).parent
PRICES_FILE = BASE_DIR / "data" / "prices.json"

def update_prices():
    with PRICES_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    for product in data.get("products", []):
        price = product.get("current_price", 0)
        if price:
            delta = price * random.uniform(-0.05, 0.05)
            product["current_price"] = round(price + delta)

        for k, v in list(product.get("competitors", {}).items()):
            delta = v * random.uniform(-0.05, 0.05)
            product["competitors"][k] = round(v + delta)

    data["updated_at"] = datetime.utcnow().isoformat()

    with PRICES_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Prices updated.")

if __name__ == "__main__":
    update_prices()
