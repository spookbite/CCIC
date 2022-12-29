import os
import json

import requests
from bs4 import BeautifulSoup

API_URL = "https://cmsapi.groww.in/api/v1/dailydigests?_limit=1&_start=0"
DEBUG = False  #  Set to True to use cached response


def get_data():
    if DEBUG and os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    response = requests.get(API_URL)
    json_data = response.json()
    if DEBUG:
        with open("data.json", "w") as f:
            json.dump(json_data, f, indent=2)
    return json_data


def parse_introduction(introduction):
    bs4_object = BeautifulSoup(introduction, "html.parser")
    parsed_data = {}

    if bs4_object.find("img"):
        parsed_data["image"] = bs4_object.find("img")["src"]

    content = []
    for tag in bs4_object.find_all("p"):
        content.append(tag.text.strip())

    parsed_data["content"] = "\n".join([i for i in content if i != ""])
    return parsed_data


def parse_top_list(top_list):
    bs4_object = BeautifulSoup(top_list, "html.parser")
    table = bs4_object.find("table")
    if table is None:
        return []

    parsed_data = []
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        price_change = cells[1].text.strip()
        change = cells[1].find("span").text.strip()
        price = price_change.replace(change, "").strip()
        price = float(price.replace("Rs", "").replace(",", "").strip())

        if "▼" in change:
            change = {
                "change_type": "down",
                "perc_change": float(change.replace("▼", "").replace("%", "").strip()),
            }
        if "▲" in change:
            change = {
                "change_type": "up",
                "perc_change": float(change.replace("▲", "").replace("%", "").strip()),
            }

        data = {
            "name": cells[0].text.strip(),
            "price": price,
            "change": change,
        }
        parsed_data.append(data)

    return parsed_data


def parse_data(data):
    parsed_data = {}
    data = data[0]

    copy_field = lambda x: parsed_data.update({x: data[x]})
    copy_field("title")
    copy_field("date")
    copy_field("slug")
    copy_field("is_indian_market_open")
    copy_field("sensex")
    copy_field("nifty")
    copy_field("us_indices_date")
    copy_field("daily_change")
    copy_field("long_term_change")
    copy_field("news")

    parsed_data["introduction"] = parse_introduction(data["introduction"])
    parsed_data["top_gainers"] = parse_top_list(data["top_gainers"])
    parsed_data["top_losers"] = parse_top_list(data["top_losers"])

    for news in parsed_data["news"]:
        news["description"] = BeautifulSoup(
            news["description"], "html.parser"
        ).text.strip()

    return parsed_data


def main():
    data = get_data()
    data = parse_data(data)
    with open("json_files\groww_all.json", "w") as f:
        json.dump(data, f, indent=2)

    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
