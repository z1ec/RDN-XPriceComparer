"""Парсеры цен по товарам.

Каждый модуль в этой директории должен объявлять:
- PRODUCT_ID: str (совпадает с id товара в prices.json)
- parse() -> List[Dict]: возвращает список предложений вида
  {"store": str, "name": str, "price": int|float}
"""

from __future__ import annotations

import importlib
from pathlib import Path
from types import ModuleType
from typing import List, Dict

PARSERS_DIR = Path(__file__).parent


def load_parsers() -> List[ModuleType]:
    modules = []
    for path in PARSERS_DIR.glob("*.py"):
        if path.name.startswith("__"):
            continue
        module_name = f"{__name__}.{path.stem}"
        modules.append(importlib.import_module(module_name))
    return modules


def run_parser(module: ModuleType) -> Dict:
    if not hasattr(module, "PRODUCT_ID"):
        raise ValueError(f"Parser {module.__name__} missing PRODUCT_ID")
    if not hasattr(module, "parse"):
        raise ValueError(f"Parser {module.__name__} missing parse()")

    offers = module.parse()  # type: ignore[attr-defined]
    normalized = []
    for offer in offers or []:
        store = str(offer.get("store", "")).strip()
        name = str(offer.get("name", "")).strip()
        price = offer.get("price")
        if not store or not name or price is None:
            continue
        try:
            price_num = float(price)
        except (TypeError, ValueError):
            continue
        normalized.append({"store": store, "name": name, "price": price_num})

    return {
        "product_id": getattr(module, "PRODUCT_ID"),
        "offers": normalized,
    }
