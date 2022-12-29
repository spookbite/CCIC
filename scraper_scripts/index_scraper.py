import requests
import os
import json
from bs4 import BeautifulSoup


def eqsis():
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
        idx = 0
        tdata = []
        while row := bs4_object.find("tr", {"id": f"{prefix}{idx}"}):
            cells = row.find_all("td")
            _date = cells[0].text.strip()
            if date is None:
                date = _date
                data[table].update({"date": _date})
            if _date != date:
                break

            rdata = {}
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


def mc_cash():
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


def mc_fno():
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


    table = bs4_object.find("div", {"id": "fidfn11"}).find(
        "table", {"class": "mctable1 tble1"})

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

    table = bs4_object.find("div", {"id": "fidfn21"}).find(
        "table", {"class": "mctable1 tble1"})

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
