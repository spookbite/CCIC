import requests
import json
from bs4 import BeautifulSoup
import os

URL = "https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/index.php"
DEBUG = False

if DEBUG and os.path.exists("data.html"):
    with open("data.html", "r", encoding="utf-8") as f:
        html = f.read()
else:
    response = requests.get(URL)
    html = response.text

bs4_object = BeautifulSoup(html, "html.parser")
if DEBUG:
    with open("data.html", "w", encoding="utf-8") as f:
        f.write(bs4_object.prettify())


table = bs4_object.find("table", {"class": "mctable1 tble1"})

total = table.find("tr", {"class": "total"})
total_cells = total.find_all("th")
total_cash_data = {
    "fii": {
        "gross_purchase": float(total_cells[1].text.strip().replace(",", "")),
        "gross_sales": float(total_cells[2].text.strip().replace(",", "")),
        "net_purchase_sales": float(total_cells[3].text.strip().replace(",", "")),
    },
    "dii": {
        "gross_purchase": float(total_cells[4].text.strip().replace(",", "")),
        "gross_sales": float(total_cells[5].text.strip().replace(",", "")),
        "net_purchase_sales": float(total_cells[6].text.strip().replace(",", "")),
    },
}

cash_data = {
    "total": total_cash_data,
    "dates": [],
}

for row in table.find("tbody").find_all("tr"):
    cells = row.find_all("td")
    date = cells[0].find("span", {"class": "desk-hide"}).text.strip()
    fii = {
        "gross_purchase": float(cells[1].text.strip().replace(",", "")),
        "gross_sales": float(cells[2].text.strip().replace(",", "")),
        "net_purchase_sales": float(cells[3].text.strip().replace(",", "")),
    }
    dii = {
        "gross_purchase": float(cells[4].text.strip().replace(",", "")),
        "gross_sales": float(cells[5].text.strip().replace(",", "")),
        "net_purchase_sales": float(cells[6].text.strip().replace(",", "")),
    }
    cash_data["dates"].append(
        {
            "date": date,
            "fii": fii,
            "dii": dii,
        }
    )

with open(r"index_json_files\cash_moneycontrol.json", "w", encoding="utf-8") as f:
    json.dump(cash_data, f, indent=2)

print(json.dumps(cash_data, indent=2))
