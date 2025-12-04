import requests
from bs4 import BeautifulSoup

PRODUCT_ID = "00"


def parse() -> list[dict]:
    store = "smartcode.ru"
    url = "https://smartcode.ru/shtrihkodirovanie_i_identifikatsiya/printery_shtrih_koda/godex_ge330_use_011-ge3e02-000"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup)



    price_tag = soup.select_one(".product-price__price")
    price = price_tag.get_text(strip=True) if price_tag else "Цена не найдена"
    price_clean = (
        price.replace("₽", "")
        .replace(" ", "")
        .replace("\xa0", "")
        .strip()
    )

    name_tag = soup.select_one("h1.ttl-base-l")
    name = name_tag.get_text(strip=True) if name_tag else "Название не найдено"

    return [
        {
            "store": store,
            "name": name,
            "price": price
        }
    ]

print(parse())