import streamlit as st
import pandas as pd
import json
from datetime import datetime

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


today = datetime.today()
day = today.strftime("%d %B %Y")

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

    st.header("Index level Reporting")


with col3:
    st.write("")

