from parsers.site1_parser import get_price_from_site1
from parsers.site2_parser import get_price_from_site2

def get_all_prices(product_id: str):
    return {
        "site1": get_price_from_site1(product_id),
        "site2": get_price_from_site2(product_id),
    }
