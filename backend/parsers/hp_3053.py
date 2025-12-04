"""Пример парсера для HP LaserJet 3053.

Замените логику внутри parse() на реальные запросы (requests + BeautifulSoup).
"""

# import requests
# from bs4 import BeautifulSoup

PRODUCT_ID = "hp-3053"


def parse():
    # TODO: реализовать реальный парсинг. Пока — стабильные данные.
    return [
        {"store": "demo-store", "name": "HP LaserJet 3053", "price": 16500},
    ]
