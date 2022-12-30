#This will not run on online IDE
import requests
from bs4 import BeautifulSoup
import json
from datetime import date
from datetime import timedelta
import pandas as pd
from dateutil import parser

# Get today's date
today = date.today()
dayno = date.today().weekday()

# Yesterday date
yesterday = today - timedelta(days=1)
fridate = today - timedelta(days=3)
saturdate = today - timedelta(days=2)

data = pd.read_csv('nifty200list.csv')

res = []
  
for i in range(len(data)):
    URL = data.loc[i, 'mcURL']
    COMPANY = data.loc[i, 'Company Name']
    SYMBOL = data.loc[i, 'Symbol']
    print(COMPANY)
    r = requests.get(URL)
    
    soup = BeautifulSoup(r.content, 'html5lib')
    news_list = soup.find('div', class_="news_list")

    try:
        news_items = news_list.find_all('li')



        for news_item in news_items:
            news_link = news_item.find('a')['href']
            news_res = requests.get(news_link)
            news_soup = BeautifulSoup(news_res.content, 'html5lib')

            dat = news_soup.find('div', class_='article_schedule').text

            # Extract Title
            title = news_soup.find('h1', class_='article_title').text

            # Extract news content
            news_content_wrapper = news_soup.find('div', class_='content_wrapper')
            news_content = ""
            for p in news_content_wrapper.find_all('p'):
                news_content += p.text

            #add the date filter -> if date == yesterday OR (today = MONDAY and date = timedelta(3))
            temp = parser.parse(dat)
            if temp.date() == yesterday or (dayno == 0 and (temp.date() == fridate or temp.date() == saturdate)):
                res.append({
                    'date': dat,
                    'title': title,
                    'content': news_content,
                    'company': COMPANY + "(" + str(SYMBOL) + ")"
                    })

    except:
        print("DNF")

l = []

for dct in res:
  l.append(pd.DataFrame([dct]))

tmp = pd.concat(l)
tmp.reset_index(inplace=True)
tmp.drop(['index'], axis=1, inplace=True)

tmp.to_csv(r'csv_files\news_scraped.csv', header=True, index=False)
