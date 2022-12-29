import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import date
from datetime import datetime
from datetime import timedelta
import pandas as pd
from dateutil import parser
import groww

def moneycontrol():
    # Get today's date
    todate = date.today()
    today = date.today().weekday()

    # Yesterday date
    yesterday = todate - timedelta(days=1)
    fridate = todate - timedelta(days=3)
    saturdate = todate - timedelta(days=2)

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
                news_content_wrapper = news_soup.find(
                    'div', class_='content_wrapper')
                news_content = ""
                for p in news_content_wrapper.find_all('p'):
                    news_content += p.text

                #add the date filter -> if date == yesterday OR (today = MONDAY and date = timedelta(3))
                temp = parser.parse(dat)
                if temp.date() == yesterday or (today == 0 and (temp.date() == fridate or temp.date() == saturdate)):
                    res.append({
                        'date': dat,
                        'title': title,
                        'content': news_content,
                        'company': COMPANY
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

def grow():
    data = groww.get_data()
    data = groww.parse_data(data)
    with open("json_files\groww_all.json", "w") as f:
        json.dump(data, f, indent=2)

    print(json.dumps(data, indent=2))

def upstox_fo():
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

def upstox_mo():
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
        count+=1
        if (count > 3 and count < 12 and count % 3 != 0):
            row = row.replace(u'\xa0', u' ')
            row = row.replace('\n', '')
            ls.append(row.strip())

    data = {
        "news1": ls[0] + " : " + ls[1],
        "news2": ls[2] + " : " + ls[3],
        "news3": ls[4] + " : " + ls[5]
    }

    # Open the JSON file for writing
    with open(r'json_files\upstox_morning.json', 'w', encoding="utf-8") as outfile:
        # Write the data to the file
        json.dump(data, outfile)

def capital():
    URL='https://www.capitalmarket.com/News/Derivatives-News'
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib')
    # print(soup.prettify)

    link=soup.find('div', class_='frst_news')
    url_link = link.find('a')['href']
    article_url=URL+str(url_link)
    print(article_url)
    r1 = requests.get(article_url) 
    soup1 = BeautifulSoup(r1.content, 'html5lib')

    data=soup1.find('div',id='PrintNews')
    with open("temp_txt_files\capital_output.txt", "w", encoding="utf-8") as output:
        output.write(data.text)

    ls = []

    with open('temp_txt_files\capital_output.txt', 'r', encoding="utf-8") as file:
        # Read the contents of the file
        mf = file.readlines()
        count = 0
        for line in mf:
            text = line.strip()
            for c in text:
                if c.isalpha():
                    #news.append(text)
                    count += 1
                    if count >= 5:
                        ls.append(text)
                break

    final_text = " ".join(ls[:])

    data = {
        "fno": final_text
    }

    # Open the JSON file for writing
    with open("json_files\capital_fo.json", "w", encoding="utf-8") as outfile:
        # Write the data to the file
        json.dump(data, outfile)


moneycontrol()
grow()
upstox_fo()
upstox_mo()
capital()
