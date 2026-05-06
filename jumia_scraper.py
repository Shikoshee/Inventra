import requests
from bs4 import BeautifulSoup
import pandas as pd

# Replace this with your Jumia shop URL
shop_url = "https://www.jumia.com.ng/shop/plugnplay/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

products = []

page = 1
while True:
    print(f"Fetching page {page}...")
    response = requests.get(f"{shop_url}?page={page}", headers=headers)
    if response.status_code != 200:
        break

    soup = BeautifulSoup(response.text, "html.parser")
    product_cards = soup.find_all("article", {"class": "prd _fb col c-prd"})

    if not product_cards:
        break

    for card in product_cards:
        name = card.find("h3", {"class": "name"}).text.strip()
        price = card.find("div", {"class": "prc"}).text.strip()
        link = "https://www.jumia.com.ng" + card.find("a")["href"]
        products.append({"Name": name, "Price": price, "Link": link})

    page += 1

# Export to Excel
df = pd.DataFrame(products)
df.to_excel("jumia_shop_products.xlsx", index=False)
print(f"Fetched {len(products)} products. Saved to jumia_shop_products.xlsx")
