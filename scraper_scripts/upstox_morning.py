import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://upstox.com/market-talk/category/newsletters/morning-update/'
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')
# print(soup.prettify())
link = soup.find('div', class_='blog-card')
url_link = link.find('a')['href']
# article_url=URL+str(url_link)
r1 = requests.get(url_link)
soup1 = BeautifulSoup(r1.content, 'html5lib')
# print(soup1.prettify())

article = soup1.find('div', class_='single-article-content')
data = []

for s in article.find_all('p'):
    data.append(s.text)

count = 0
ls = []
for row in data:
  count += 1
  if (count > 3 and count < 12 and count % 3 != 0):
    row = row.replace(u'\xa0', u' ')
    row = row.replace('\n', '')
    ls.append(row.strip())

data = {
    "news1": ls[0] + " : " + ls[1],
    "news2": ls[2] + " : " + ls[3],
    "news3": ls[4] + " : " + ls[5]
}
# print(data)
# Open the JSON file for writing
with open(r'json_files\upstox_morning.json', 'w', encoding="utf-8") as outfile:
    # Write the data to the file
    json.dump(data, outfile)


    
