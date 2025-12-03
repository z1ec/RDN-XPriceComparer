import requests
from bs4 import BeautifulSoup


def get_price_from_site2(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    name = soup.select_one(".ttl-base-l")
    price = soup.select_one(".product-price__price")
    if price:
        return price.get_text(strip=True), name.get_text(strip=True)
    return None

