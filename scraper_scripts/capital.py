
import json
import requests 
from bs4 import BeautifulSoup
import pandas as pd 

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
with open(r"temp_txt_files\capital_output.txt", "w", encoding="utf-8") as output:
    output.write(data.text)

ls = []

with open('temp_txt_files\capital_output.txt', 'r') as file:
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
# print(final_text)

data = {
    "fno": final_text
}

# Open the JSON file for writing
with open("json_files\capital_fo.json", "w") as outfile:
    # Write the data to the file
    json.dump(data, outfile)



