import requests
import os
import json
from bs4 import BeautifulSoup

URL = "https://www.eqsis.com/fii-activity-in-nse-index-futures-and-options/"
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

row_prefixes = (
    ("index_future", "table_186_row_", ("participant", "long", "short")),
    ("index_call", "table_187_row_", ("participant", "long", "short")),
    ("index_put", "table_188_row_", ("participant", "long", "short")),
    (
        "index_future_increases",
        "table_207_row_",
        ("symbol", "expiry", "price", "chg_oi"),
    ),
    (
        "index_future_decreases",
        "table_208_row_",
        ("symbol", "expiry", "price", "chg_oi"),
    ),
    (
        "index_call_increases",
        "table_193_row_",
        ("symbol", "expiry", "strike", "premium", "chg_oi"),
    ),
    (
        "index_call_decreases",
        "table_194_row_",
        ("symbol", "expiry", "strike", "premium", "chg_oi"),
    ),
    (
        "index_put_increases",
        "table_195_row_",
        ("symbol", "expiry", "strike", "premium", "chg_oi"),
    ),
    (
        "index_put_decreases",
        "table_196_row_",
        ("symbol", "expiry", "strike", "premium", "chg_oi"),
    ),
)

data = {}

for table, prefix, keys in row_prefixes:
    data[table] = {}
    date = None
    first = True
    idx = 0
    tdata = []
    while row := bs4_object.find("tr", {"id": f"{prefix}{idx}"}):
        cells = row.find_all("td")
        _date = cells[0].text.strip()
        if date is None:
            date = _date
        if _date != date:
            if first:
                first = False
                date = _date
            else:
                break

        rdata = {"date": _date}
        for i, key in enumerate(keys):
            if key in ("long", "short", "strike", "chg_oi"):
                rdata[key] = int(cells[i + 1].text.strip().replace(",", ""))
            elif key in ("price", "premium"):
                rdata[key] = float(cells[i + 1].text.strip().replace(",", ""))
            else:
                rdata[key] = cells[i + 1].text.strip()
        tdata.append(rdata)
        idx += 1
    data[table].update({"data": tdata})

with open(r"index_json_files\eqsis.json", "w") as f:
    json.dump(data, f, indent=2)

print(json.dumps(data, indent=2))
