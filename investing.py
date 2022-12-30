import cfscrape
import os
import json
from bs4 import BeautifulSoup

URL_A = "https://in.investing.com/equities/india-adrs"
URL_B = "https://in.investing.com/equities/india-adrs/performance"
DEBUG = False

if DEBUG and os.path.exists("data.html") and os.path.exists("datb.html"):
    with open("data.html", "r") as f:
        html_a = f.read()
    with open("datb.html", "r") as f:
        html_b = f.read()
else:
    scraper = cfscrape.create_scraper()
    response = scraper.get(URL_A)
    html_a = response.text
    response = scraper.get(URL_B)
    html_b = response.text

bs4_object_a = BeautifulSoup(html_a, "html.parser")
bs4_object_b = BeautifulSoup(html_b, "html.parser")

if DEBUG:
    with open("data.html", "w") as f:
        f.write(bs4_object_a.prettify())
    with open("datb.html", "w") as f:
        f.write(bs4_object_b.prettify())

table = bs4_object_a.find(
    "table", {"class": "common-table medium js-table js-streamable-table"}
).find("tbody")

rows = table.find_all("tr")

data = {}

for row in rows:
    name = row.find("td", {"class": "col-name"})
    if not name:
        continue
    name = name.text.strip()
    chg_pct = row.find("td", {"class": "col-chg_pct"})
    if not chg_pct:
        continue
    chg_pct = chg_pct.text.strip()
    volume = row.find("td", {"class": "col-volume"})
    if not volume:
        continue
    volume = volume.text.strip()
    data.setdefault(name, {}).update({"chg_pct": chg_pct, "volume": volume})

table = bs4_object_b.find(
    "table", {"class": "common-table medium js-table js-streamable-table"}
).find("tbody")

rows = table.find_all("tr")

for row in rows:
    name = row.find("td", {"class": "col-name"})
    if not name:
        continue
    name = name.text.strip()
    month_chg_pct = row.find("td", {"class": "col-performance_month"})
    if not month_chg_pct:
        continue
    month_chg_pct = month_chg_pct.text.strip()
    data.setdefault(name, {}).update({"month_chg_pct": month_chg_pct})

with open("investing.json", "w") as f:
    json.dump(data, f, indent=2)

print(json.dumps(data, indent=2))
