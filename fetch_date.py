import json
from datetime import datetime
from datetime import timedelta

today = datetime.today()
day = today.strftime("%d %B %Y")
yesterday = today - timedelta(days=1)
day1 = yesterday.strftime("%d %B")
yesterday1 = today - timedelta(days=2)
day2 = yesterday1.strftime("%d %B")
fridate = today - timedelta(days=3)
saturdate = today - timedelta(days=2)
dayno = datetime.today().weekday()
day = today.strftime("%d")
month = today.strftime("%B").lower()
year = today.strftime("%Y")
dat = day+'-'+month+'-'+year

data = {
    "today": today,
    "day": day,
    "yesterday": yesterday,
    "day1": day1,
    "yesterday1": yesterday1,
    "day2": day2,
    "fridate": fridate,
    "saturdate": saturdate,
    "dayno": dayno,
    "dat":dat
}

with open("date.json", "w") as outfile:
    # Write the data to the file
    json.dump(data, outfile)
