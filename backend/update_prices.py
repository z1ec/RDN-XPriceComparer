from pathlib import Path
import json
from datetime import datetime, timezone
from typing import Dict, List, Any

from parsers import load_parsers, run_parser

BASE_DIR = Path(__file__).parent
PRICES_FILE = BASE_DIR / "data" / "prices.json"


def _index_by_id(products: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {p.get("id"): p for p in products}


def _build_product_entry(result: Dict[str, Any], previous: Dict[str, Any]) -> Dict[str, Any]:
    offers = result.get("offers") or []
    product_id = result.get("product_id")
    if not offers:
        if previous:
            return previous
        raise ValueError(f"No offers collected for {product_id}")

    first_offer = offers[0]

    return {
        "id": product_id,
        "store": first_offer.get("store") or previous.get("store"),
        "name_original": first_offer.get("name") or previous.get("name_original"),
        "price": round(first_offer.get("price") or 0),
    }


def update_prices():
    existing_data: Dict[str, Any] = {"products": []}
    if PRICES_FILE.exists():
        with PRICES_FILE.open("r", encoding="utf-8") as f:
            existing_data = json.load(f)

    existing_by_id = _index_by_id(existing_data.get("products", []))

    modules = load_parsers()
    products: List[Dict[str, Any]] = []

    for module in modules:
        result = run_parser(module)
        previous = existing_by_id.get(result.get("product_id"), {})
        try:
            product_entry = _build_product_entry(result, previous)
        except ValueError:
            # пропускаем если ничего не спарсили и нет прошлых данных
            continue
        products.append(product_entry)

    data = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "products": products,
    }

    with PRICES_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Prices updated.")


if __name__ == "__main__":
    update_prices()
