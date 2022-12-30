import streamlit as st
import pandas as pd
import json
from datetime import datetime
from datetime import timedelta

st.set_page_config(page_title='CCIC', layout='wide')

@st.cache(allow_output_mutation=True)
def get_data():
    return pd.read_csv(r'csv_files\news_scraped.csv')


@st.cache
def get_groww():
    f = open('json_files\groww_all.json')
    data = json.load(f)
    return data


@st.cache
def get_capital():
    f = open(r'json_files\capital_fo.json')
    data = json.load(f)
    return data


@st.cache
def get_upfo():
    f = open(r'json_files\upstox_fo.json')
    data = json.load(f)
    return data


@st.cache
def get_upmo():
    f = open(r'json_files\upstox_morning.json')
    data = json.load(f)
    return data


@st.cache
def get_nse():
    f = open(r'index_json_files\nseindia.json')
    data = json.load(f)
    return data


@st.cache
def get_cashmc():
    f = open(r'index_json_files\cash_moneycontrol.json')
    data = json.load(f)
    return data


@st.cache
def get_fnomc():
    f = open(r'index_json_files\fno_moneycontrol.json')
    data = json.load(f)
    return data


@st.cache
def get_eqsis():
    f = open(r'index_json_files\eqsis.json')
    data = json.load(f)
    return data


today = datetime.today()
day = today.strftime("%d %B %Y")
yesterday = today - timedelta(days=1)
day1 = yesterday.strftime("%d %B")
yesterday1 = today - timedelta(days=2)
day2 = yesterday1.strftime("%d %B")

# add day
st.markdown("<h1 style='text-align: center;'><b>CCIC 4.0 : Group J</b></h1>",
            unsafe_allow_html=True)
st.write("")
st.write("")

col1, col2, col3 = st.columns((1, 4, 1))

with col1:
    st.write("")


with col2:
    st.write("Date: " + day)
    st.header("Market Commentary - Intended for Institutional Clients")
    st.write("")
    grow = get_groww()
    capital = get_capital()
    upfo = get_upfo()
    upmo = get_upmo()

    gsector = grow["news"][0]['description']
    gsector = gsector.split('\n')
    gnews = grow["news"][1]['description']
    gnews = gnews.split('\n')
    summary = grow["introduction"]["content"].split('\n')
    summary = " ".join(summary[1:])
    derivatives_cap = capital['fno']
    globalm = upfo['asian']
    index = upfo['index']
    fiidii = upfo['fiidii']
    indiavix = upfo['indiavix']
    stock = upfo['stock']
    stock = stock.split('.')
    disc = upfo['disclaimer']
    news1 = upmo['news1']
    news2 = upmo['news2']
    news3 = upmo['news3']

    st.write(summary)
    st.subheader("Global Markets 🌎")
    st.write(globalm)
    st.subheader("Index Action 📈📉")
    st.write(index)
    st.subheader("Sector Update 🗞️")
    for upd in gsector:
        st.write("⭐️ " + upd[1:])
    # st.write(gsector)
    st.write(news1)
    st.write(news2)
    st.write(news3)
    st.subheader("FII/FPI and DII 💰")
    st.write(fiidii)
    st.subheader("Derivatives 💵")
    st.write(derivatives_cap)
    st.subheader("Stock Futures 📊")
    st.write("**Long Build-up**" + stock[0][13:])
    st.write("**Short Build-up**" + stock[1][16:])
    st.write("**Under F&O Ban**" + stock[2][15:])
    st.info(disc, icon="ℹ️")


    st.write("")
    st.write("")

    st.header("Nifty200 NEWS 📰")
    st.write("")
    newsdf = get_data()
    for i in range(len(newsdf)):
        company = newsdf.loc[i, 'company'] + " : "
        title = newsdf.loc[i, 'title']
        st.write("👉" + f"{company} {title}")

    for i in range(len(gnews)):
        st.write("👉" + gnews[i])

    st.write("")
    st.write("")

    st.header("Index level Reporting 🪙")
    st.write("")
    
    st.subheader("Market Turnover 📝")
    st.write("")
    nse = get_nse()
    # st.json(nse)
    equity_prev = nse["equities"]["previous"]["volume"]
    equity_tod = nse["equities"]["today"]["volume"]
    delta_eq = ((equity_tod-equity_prev)/equity_prev)*100
    indexfut_prev = nse["index_futures"]["previous"]["volume"]
    indexfut_tod = nse["index_futures"]["today"]["volume"]
    indexfut_oi = int(nse["index_futures"]["previous"]["open_interest"])
    delta_indexfut = ((indexfut_tod-indexfut_prev)/indexfut_prev)*100
    indexopt_prev = nse["index_options"]["previous"]["volume"]
    indexopt_tod = nse["index_options"]["today"]["volume"]
    indexopt_oi = int(nse["index_options"]["previous"]["open_interest"])
    delta_indexopt = ((indexopt_tod-indexopt_prev)/indexopt_prev)*100
    stockfut_prev = nse["stock_futures"]["previous"]["volume"]
    stockfut_tod = nse["stock_futures"]["today"]["volume"]
    stockfut_oi = int(nse["stock_futures"]["previous"]["open_interest"])
    delta_stockfut = ((stockfut_tod-stockfut_prev)/stockfut_prev)*100
    stockopt_prev = nse["stock_options"]["previous"]["volume"]
    stockopt_tod = nse["stock_options"]["today"]["volume"]
    stockopt_oi = int(nse["stock_options"]["previous"]["open_interest"])
    delta_stockopt = ((stockopt_tod-stockopt_prev)/stockopt_prev)*100
    data = [[equity_tod, delta_eq, '-'], [indexfut_tod, delta_indexfut, indexfut_oi], [indexopt_tod, delta_indexopt, indexopt_oi], [stockfut_tod, delta_stockfut, stockfut_oi], [stockopt_tod, delta_stockopt, stockopt_oi]]
    df = pd.DataFrame(data, columns=['Previous Volume', '🛆 Volume (%)', 'Prev OI'], index=['Equity', 'Index Futures', 'Index Options', 'Stock Futures', 'Stock Options'])
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Product'}, inplace=True)
    # s1 = dict(selector='th', props=[('text-align', 'center')])
    # s2 = dict(selector='td', props=[('text-align', 'center')])
    # # you can include more styling paramteres, check the pandas docs
    # table = df.style.set_table_styles([s1, s2]).hide(axis=0).to_html()
    # st.write(f'{table}', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    st.write("")

    st.subheader("FII and DII Activity(₹crores) 🏤")
    st.write("")
    cashmc = get_cashmc()
    sum_purchase_fii = 0
    sum_sales_fii = 0
    sum_purchase_dii = 0
    sum_sales_dii = 0
    count = 0
    for i in cashmc['dates']:
        sum_purchase_fii += i["fii"]["gross_purchase"]
        sum_sales_fii += i["fii"]["gross_sales"]
        sum_purchase_dii += i["dii"]["gross_purchase"]
        sum_sales_dii += i["dii"]["gross_sales"]
        count += 1

    prev_purchase_fii = cashmc['dates'][0]['fii']['gross_purchase']
    prev_purchase_dii = cashmc['dates'][0]['dii']['gross_purchase']
    prev_sale_fii = cashmc['dates'][0]['fii']['gross_sales']
    prev_sale_dii = cashmc['dates'][0]['dii']['gross_sales']
    prev1_purchase_fii = cashmc['dates'][1]['fii']['gross_purchase']
    prev1_purchase_dii = cashmc['dates'][1]['dii']['gross_purchase']
    prev1_sale_fii = cashmc['dates'][1]['fii']['gross_sales']
    prev1_sale_dii = cashmc['dates'][1]['dii']['gross_sales']
    avg_purchase_fii = sum_purchase_fii/count
    avg_sale_fii = sum_sales_fii/count
    avg_purchase_dii = sum_purchase_dii/count
    avg_sale_dii = sum_sales_dii/count
    month_change_fii = sum_purchase_fii-sum_sales_fii
    month_change_dii = sum_purchase_dii-sum_sales_dii


    fnomc = get_fnomc()
    sum_purchase_fii_indexfut = 0
    sum_sales_fii_indexfut = 0
    sum_purchase_fii_indexopt = 0
    sum_sales_fii_indexopt = 0
    count = 0
    for i in fnomc["index"]['dates']:
        sum_purchase_fii_indexfut += i["fii_index_put"]["gross_purchase"]
        sum_sales_fii_indexfut += i["fii_index_put"]["gross_sales"]
        sum_purchase_fii_indexopt += i["fii_index_opt"]["gross_purchase"]
        sum_sales_fii_indexopt += i["fii_index_opt"]["gross_sales"]
        count += 1

    prev_purchase_fii_indexfut = fnomc["index"]['dates'][0]['fii_index_put']['gross_purchase']
    prev_purchase_fii_indexopt = fnomc["index"]['dates'][0]['fii_index_opt']['gross_purchase']
    prev_sale_fii_indexfut = fnomc["index"]['dates'][0]['fii_index_put']['gross_sales']
    prev_sale_fii_indexopt = fnomc["index"]['dates'][0]['fii_index_opt']['gross_sales']
    prev1_purchase_fii_indexfut = fnomc["index"]['dates'][0]['fii_index_put']['gross_purchase']
    prev1_purchase_fii_indexopt = fnomc["index"]['dates'][0]['fii_index_opt']['gross_purchase']
    prev1_sale_fii_indexfut = fnomc["index"]['dates'][0]['fii_index_put']['gross_sales']
    prev1_sale_fii_indexopt = fnomc["index"]['dates'][0]['fii_index_opt']['gross_sales']
    avg_purchase_fii_indexfut = sum_purchase_fii_indexfut/count
    avg_sale_fii_indexfut = sum_sales_fii_indexfut/count
    avg_purchase_fii_indexopt = sum_purchase_fii_indexopt/count
    avg_sale_fii_indexopt = sum_sales_fii_indexopt/count
    month_change_fii_indexfut = sum_purchase_fii_indexfut-sum_sales_fii_indexfut
    month_change_fii_indexopt = sum_purchase_fii_indexopt-sum_sales_fii_indexopt

    sum_purchase_fii_stockfut = 0
    sum_sales_fii_stockfut = 0
    sum_purchase_fii_stockopt = 0
    sum_sales_fii_stockopt = 0
    count = 0
    for i in fnomc["stock"]['dates']:
        sum_purchase_fii_stockfut += i["fii_stock_put"]["gross_purchase"]
        sum_sales_fii_stockfut += i["fii_stock_put"]["gross_sales"]
        sum_purchase_fii_stockopt += i["fii_stock_opt"]["gross_purchase"]
        sum_sales_fii_stockopt += i["fii_stock_opt"]["gross_sales"]
        count += 1

    prev_purchase_fii_stockfut = fnomc["stock"]['dates'][0]['fii_stock_put']['gross_purchase']
    prev_purchase_fii_stockopt = fnomc["stock"]['dates'][0]['fii_stock_opt']['gross_purchase']
    prev_sale_fii_stockfut = fnomc["stock"]['dates'][0]['fii_stock_put']['gross_sales']
    prev_sale_fii_stockopt = fnomc["stock"]['dates'][0]['fii_stock_opt']['gross_sales']
    prev1_purchase_fii_stockfut = fnomc["stock"]['dates'][0]['fii_stock_put']['gross_purchase']
    prev1_purchase_fii_stockopt = fnomc["stock"]['dates'][0]['fii_stock_opt']['gross_purchase']
    prev1_sale_fii_stockfut = fnomc["stock"]['dates'][0]['fii_stock_put']['gross_sales']
    prev1_sale_fii_stockopt = fnomc["stock"]['dates'][0]['fii_stock_opt']['gross_sales']
    avg_purchase_fii_stockfut = sum_purchase_fii_stockfut/count
    avg_sale_fii_stockfut = sum_sales_fii_stockfut/count
    avg_purchase_fii_stockopt = sum_purchase_fii_stockopt/count
    avg_sale_fii_stockopt = sum_sales_fii_stockopt/count
    month_change_fii_stockfut = sum_purchase_fii_stockfut-sum_sales_fii_stockfut
    month_change_fii_stockopt = sum_purchase_fii_stockopt-sum_sales_fii_stockopt

    data = [
        [prev_purchase_fii - prev_sale_fii, prev1_purchase_fii - prev1_sale_fii, avg_purchase_fii - avg_sale_fii], 
        [prev_purchase_dii - prev_sale_dii, prev1_purchase_dii - prev1_sale_dii, avg_purchase_dii - avg_sale_dii],
        [prev_purchase_fii_indexfut - prev_sale_fii_indexfut, prev1_purchase_fii_indexfut - prev1_sale_fii_indexfut, avg_purchase_fii_indexfut - avg_sale_fii_indexfut],
        [prev_purchase_fii_indexopt - prev_sale_fii_indexopt, prev1_purchase_fii_indexopt - prev1_sale_fii_indexopt, avg_purchase_fii_indexopt - avg_sale_fii_indexopt], 
        [prev_purchase_fii_stockfut - prev_sale_fii_stockfut, prev1_purchase_fii_stockfut - prev1_sale_fii_stockfut, avg_purchase_fii_stockfut - avg_sale_fii_stockfut],
        [prev_purchase_fii_stockopt - prev_sale_fii_stockopt, prev1_purchase_fii_stockopt - prev1_sale_fii_stockopt, avg_purchase_fii_stockopt - avg_sale_fii_stockopt], 
    ]
    df = pd.DataFrame(data, columns=[day1, day2,'30D Average Net Purchase'], 
                        index=['FII Cash', 'DII Cash', 'FII Index Futures', 'FII Index Options', 'FII Stock Futures', 'FII Stock Options'])
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Category'}, inplace=True)
    st.dataframe(df, use_container_width=True)
    st.write("")

    st.subheader("Options Snapshot 📸")
    st.write("")
    eqsis = get_eqsis()
    long_fii_ic = eqsis["index_call"]["data"][1]["long"]
    short_fii_ic = eqsis["index_call"]["data"][1]["short"]
    long_dii_ic = eqsis["index_call"]["data"][2]["long"]
    short_dii_ic = eqsis["index_call"]["data"][2]["short"]
    long_fii_ip = eqsis["index_put"]["data"][1]["long"]
    short_fii_ip = eqsis["index_put"]["data"][1]["short"]
    long_dii_ip = eqsis["index_put"]["data"][2]["long"]
    short_dii_ip = eqsis["index_put"]["data"][2]["short"]

    long_fii_ic1 = eqsis["index_call"]["data"][1]["long"]
    short_fii_ic1 = eqsis["index_call"]["data"][1]["short"]
    long_dii_ic1 = eqsis["index_call"]["data"][2]["long"]
    short_dii_ic1 = eqsis["index_call"]["data"][2]["short"]
    long_fii_ip1 = eqsis["index_put"]["data"][1]["long"]
    short_fii_ip1 = eqsis["index_put"]["data"][1]["short"]
    long_dii_ip1 = eqsis["index_put"]["data"][2]["long"]
    short_dii_ip1 = eqsis["index_put"]["data"][2]["short"]
    
    data = [
        [long_fii_ic-short_fii_ic, long_fii_ic1-short_fii_ic1, (long_fii_ic-short_fii_ic)-(long_fii_ic1-short_fii_ic1)],
        [long_dii_ic-short_dii_ic, long_dii_ic1-short_dii_ic1, (long_dii_ic-short_dii_ic)-(long_dii_ic1-short_dii_ic1)],
        [long_fii_ip-short_fii_ip, long_fii_ip1-short_fii_ip1, (long_fii_ip-short_fii_ip)-(long_fii_ip1-short_fii_ip1)],
        [long_dii_ip-short_dii_ip, long_dii_ip1-short_dii_ip1, (long_dii_ip-short_dii_ip)-(long_dii_ip1-short_dii_ip1)],
    ]

    df = pd.DataFrame(data, columns=[day1, day2, "1D change"],
                      index=['FII Index Call Options', 'DII Index Call Options', 'FII Index Put Options', 'DII Index Put Options'])
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Category'}, inplace=True)
    st.dataframe(df, use_container_width=True)
    st.write("")
    st.write("")
    st.info("Sources: MoneyControl, NSE India, Eqsis, Groww, Upstox, Capital Market", icon="💁🏻")


with col3:
    st.write("")

