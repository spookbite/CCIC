import json
import requests 

from bs4 import BeautifulSoup
import pandas as pd 
from datetime import datetime
from datetime import date
from datetime import timedelta

# Get today's date
todate = date.today()
today = date.today().weekday()

# Yesterday date
yesterday = todate - timedelta(days=1)
fridate = todate - timedelta(days=3)
saturdate = todate - timedelta(days=2)

# Get today's date
today = datetime.today()

# Print the date in the desired format
day = today.strftime("%d")
month = today.strftime("%B").lower()
year = today.strftime("%Y")
date = day+'-'+month+'-'+year
pg = "fo-morning-update-for-"+date+'/'
base = "https://upstox.com/market-talk/"
URL = base+pg
print(URL)
# load the projectpro webpage content 

r = requests.get(URL) 

# convert to beautiful soup 

soup = BeautifulSoup(r.content, 'html5lib')
# print(soup.prettify)

article=soup.find('div', class_='single-article-content')
data=[]

for s in article.find_all('p'):
    data.append(s.text)

with open(r"temp_txt_files\upstox_output_fo.txt", "w", encoding="utf-8") as output:
    for line in data:
        output.write(line)


# Open the file in read mode
with open(r'temp_txt_files\upstox_output_fo.txt', 'r', encoding="utf-8") as file:
  # Read the contents of the file
  mf = file.read()
  f = mf.replace("\n", " ")

  parts1 = f.split("Index Action")
  asian = parts1[0].strip()
  list2 = ". ".join(parts1[1:])

  parts2 = list2.split("FII and DII Data")
  indexaction = parts2[0].strip()
  list3 = ". ".join(parts2[1:])
  #list4 = parts2[1].strip().split("\n")

  parts3 = list3.split("India VIX")
  fiidii = parts3[0].strip()
  list4 = ". ".join(parts3[1:])

  parts4 = list4.split("Stock Action")
  indiavix = parts4[0].strip()
  list5 = ". ".join(parts4[1:])

  parts5 = list5.split("*")
  stockaction = parts5[0].strip()
  list6 = ". ".join(parts5[1:])

  parts6 = list6.split("Enjoy")
  disc = parts6[0].strip()
  list7 = ". ".join(parts6[1:])


asian = asian.split(
    "Asian Markets Update @ 7:30 am  ")[1].split("Global Markets Update ")
asian = "".join(asian[:])

fiidii = fiidii[5:]

indiavix = indiavix.replace('. ', 'India Vix')

stockaction = stockaction[3:]

data = {
    "asian": asian,
    "index": indexaction,
    "fiidii": fiidii,
    "indiavix": indiavix,
    "stock": stockaction,
    "disclaimer": disc
}

# Open the JSON file for writing
with open(r"json_files\upstox_fo.json", "w", encoding="utf-8") as outfile:
    # Write the data to the file
    json.dump(data, outfile)






