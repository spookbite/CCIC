import pandas as pd

df = pd.read_csv('ind_nifty200list.csv')

SEARCH_URL = "http://www.moneycontrol.com/stocks/cptmarket/compsearchnew.php?search_data=&cid=&mbsearch_str=&topsearch_type=1&search_str="
isincode = df['ISIN Code']
moneycontrolpages = str(SEARCH_URL) + isincode
# print(moneycontrolpages)
df['mcURL'] = moneycontrolpages

df.to_csv('nifty200list.csv', header=True, index=False)
