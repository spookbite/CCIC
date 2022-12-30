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


def nse_india():
    API_TODAY_URL = "https://www1.nseindia.com/homepage/mkt_trd_dtl.json"


    API_YESTERDAY_URL = "https://www1.nseindia.com/homepage/mkt_prev_day_trd_dtl.json"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    }

    data_today = requests.get(API_TODAY_URL, headers=HEADERS).json()
    data_yesterday = requests.get(API_YESTERDAY_URL, headers=HEADERS).json()

    with open(r"index_json_files\data_today.json", "w") as f:
        json.dump(data_today, f, indent=2)

    with open(r"index_json_files\data_yesterday.json", "w") as f:
        json.dump(data_yesterday, f, indent=2)

    mkt_map = {
        "CM": "equities",
        "FNOFUT": "index_futures",
        "FNOOPT": "index_options",
        "FNOIVX": "vol_futures",
        "FNOSTKFUT": "stock_futures",
        "FNOSTKOPT": "stock_options",
        "GIFUT": "global_indices_futures",
        "GIOPT": "global_indices_options",
        "FUTCUR": "currency_futures",
        "OPTCUR": "currency_options",
        "IRF": "nse_bond_futures",
        "COMFUT": "commodity_futures",
    }

    all_data = {}

    for key, value in mkt_map.items():
        prev_data = [i for i in data_yesterday["data"] if i["prevMkt"] == key][0]
        today_data = [i for i in data_today["data"] if i["mkt"] == key][0]

        data = {
            "previous": {
                "volume": int(prev_data["prevQty"].replace(",", ""))
                if (prev_data["prevQty"] and prev_data["prevQty"] != "-")
                else None,
                "open_interest": int(prev_data["oi"].replace(",", ""))
                if (prev_data["oi"] and prev_data["oi"] != "-")
                else None,
            },
            "today": {
                "volume": int(today_data["qty"].replace(",", ""))
                if (today_data["qty"] and today_data["qty"] != "-")
                else None,
                "traded_value": float(today_data["val"].replace(",", ""))
                if (today_data["val"] and today_data["val"] != "-")
                else None,
                "trd": int(today_data["trd"].replace(",", ""))
                if (today_data["trd"] and today_data["trd"] != "-")
                else None,
                "pre_val": float(today_data["pre_val"].replace(",", ""))
                if (today_data["pre_val"] and today_data["pre_val"] != "-")
                else None,
                "valb": float(today_data["valb"].replace(",", ""))
                if (today_data["valb"] and today_data["valb"] != "-")
                else None,
                "pre_valb": float(today_data["pre_valb"].replace(",", ""))
                if (today_data["pre_valb"] and today_data["pre_valb"] != "-")
                else None,
                "utm": today_data["utm"],
                "utmAs": today_data["utmAs"],
            },
            "mkt": key,
        }

        all_data[value] = data

    with open(r"index_json_files\nseindia.json", "w") as f:
        json.dump(all_data, f, indent=2)
