import requests
import json
from bs4 import BeautifulSoup
import os

URL = "https://www.moneycontrol.com/techmvc/responsive/fiidii/getFiiDii?classic=true&data=fno"
DEBUG = False

if DEBUG and os.path.exists("data.html"):
    with open("data.html", "r") as f:
        html = f.read()
else:
    response = requests.get(URL)
    html = response.text

bs4_object = BeautifulSoup(html, "html.parser")
if DEBUG:
    with open("data.html", "w") as f:
        f.write(bs4_object.prettify())


table = bs4_object.find("div", {"id": "fidfn11"}).find("table", {"class": "mctable1 tble1"})

total = table.find("tr", {"class": "total"})
total_cells = total.find_all("th")
total_index_data = {
    "fii_index_put": {
        "gross_purchase": float(total_cells[1].text.strip().replace(",", "")),
        "gross_sales": float(total_cells[2].text.strip().replace(",", "")),
        "net_purchase_sales": float(total_cells[3].text.strip().replace(",", "")),
    },
    "fii_index_opt": {
        "gross_purchase": float(total_cells[4].text.strip().replace(",", "")),
        "gross_sales": float(total_cells[5].text.strip().replace(",", "")),
        "net_purchase_sales": float(total_cells[6].text.strip().replace(",", "")),
    },
}

index_data = {
    "total": total_index_data,
    "dates": [],
}

for row in table.find("tbody").find_all("tr"):
    cells = row.find_all("td")
    date = cells[0].find("span", {"class": "desk-hide"}).text.strip()
    fii_put = {
        "gross_purchase": float(cells[1].text.strip().replace(",", "")),
        "gross_sales": float(cells[2].text.strip().replace(",", "")),
        "net_purchase_sales": float(cells[3].text.strip().replace(",", "")),
    }
    fii_opt = {
        "gross_purchase": float(cells[4].text.strip().replace(",", "")),
        "gross_sales": float(cells[5].text.strip().replace(",", "")),
        "net_purchase_sales": float(cells[6].text.strip().replace(",", "")),
    }
    index_data["dates"].append(
        {
            "date": date,
            "fii_index_put": fii_put,
            "fii_index_opt": fii_opt,
        }
    )

table = bs4_object.find("div", {"id": "fidfn21"}).find("table", {"class": "mctable1 tble1"})

total = table.find("tr", {"class": "total"})
total_cells = total.find_all("th")
total_stock_data = {
    "fii_stock_put": {
        "gross_purchase": float(total_cells[1].text.strip().replace(",", "")),
        "gross_sales": float(total_cells[2].text.strip().replace(",", "")),
        "net_purchase_sales": float(total_cells[3].text.strip().replace(",", "")),
    },
    "fii_stock_opt": {
        "gross_purchase": float(total_cells[4].text.strip().replace(",", "")),
        "gross_sales": float(total_cells[5].text.strip().replace(",", "")),
        "net_purchase_sales": float(total_cells[6].text.strip().replace(",", "")),
    },
}

stock_data = {
    "total": total_stock_data,
    "dates": [],
}

for row in table.find("tbody").find_all("tr"):
    cells = row.find_all("td")
    date = cells[0].find("span", {"class": "desk-hide"}).text.strip()
    fii_put = {
        "gross_purchase": float(cells[1].text.strip().replace(",", "")),
        "gross_sales": float(cells[2].text.strip().replace(",", "")),
        "net_purchase_sales": float(cells[3].text.strip().replace(",", "")),
    }
    fii_opt = {
        "gross_purchase": float(cells[4].text.strip().replace(",", "")),
        "gross_sales": float(cells[5].text.strip().replace(",", "")),
        "net_purchase_sales": float(cells[6].text.strip().replace(",", "")),
    }
    stock_data["dates"].append(
        {
            "date": date,
            "fii_stock_put": fii_put,
            "fii_stock_opt": fii_opt,
        }
    )

data = {
    "index": index_data,
    "stock": stock_data,
}

with open(r"index_json_files\fno_moneycontrol.json", "w") as f:
    json.dump(data, f, indent=2)

print(json.dumps(data, indent=2))