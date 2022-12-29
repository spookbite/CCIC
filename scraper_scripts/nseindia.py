import requests
import json

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
