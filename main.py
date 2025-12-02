import requests
from bs4 import BeautifulSoup


url = "https://labelaire.ru/catalog/printery-etiketok/proton-ttp-4306"

response = requests.get(url)
response.raise_for_status() 

html = response.text
soup = BeautifulSoup(html, "lxml")

price_div = soup.find("span", class_="jbcurrency-value")
price = price_div.text.strip().replace(" ","")

print(price)
