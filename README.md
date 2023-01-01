# CCIC 4.0
[![run app.py](https://github.com/spookbite/CCIC/actions/workflows/runapp.yml/badge.svg)](https://github.com/spookbite/CCIC/actions/workflows/runapp.yml)
[![run master_scraper](https://github.com/spookbite/CCIC/actions/workflows/scrape.yml/badge.svg)](https://github.com/spookbite/CCIC/actions/workflows/scrape.yml)
## Overview:
Markets summary helps traders taking the extra advantage of indices across globe, depository receipts
(DR), commodities and foreign currencies movement and additionally, how FII and DII are placed across
derivatives and equities segments. Further, extracting key information related to NSE200 Index and
Sectoral highlights from different sources and creating One Page summary gives the traders/clients all
pieces of information before the start of a trading day. Equities and Derivatives Radar information are
useful to make decision for sales traders quickly rather than looking at different sources.

## Objective:
The objective of this project is to extract important information for NSE200 Index constituents and any
other notable sectoral information at Start of Day for sales traders to make quicker and productive
decision.
System should have following functionalities:
1. Extracting top News related to NSE200 Index and Sectoral highlights
• Highlights/News from sources for NSE200 Index constituents and any other notable sectoral
news
2. Build Index level reporting for ETF and Option FLOWS, Market Turn Over, Overnight ADR and
GDR moves, Top Surfers for NSE 100 as per attached template from defined sources 

## Methodology:
We have made a concerted effort to ensure that the news stories we present to our users are from reputable and reliable sources. In order to achieve this, we have carefully selected a number of prominent news outlets to serve as our sources, and have implemented a web scraper to gather news stories from these sources on a regular basis.

With that said, in order to maintain the integrity and relevance of our news feed, we have implemented a filter that removes any news stories that does not meet the following criteria:
• The company is listed in the NIFTY200 index.
• The news story was published yesterday.
• The news story was published over the weekend (if we are viewing the news feed on a Monday).

This filter helps us to provide our users with the most current and relevant news stories, and ensures that our news feed is as useful as possible.

In order to provide our users with up-to-date and accurate Index level reporting, we have implemented a similar process for gathering and displaying data. Specifically, we have scraped data from reliable sources and used it to create a web app using Streamlit. This app allows users to easily view and interact with the data, and we have hosted it on Streamlit Cloud for convenient access.

In order to make this process as efficient as possible, we have also set up a workflow using GitHub Actions that runs the code to update the content every day at 7:30 AM IST. This ensures that the data is always current and accurate, without requiring us to manually update it on a daily basis.

Overall, we believe that this combination of reliable data sources, a user-friendly web app, and automated updates allows our users to have the most comprehensive and up-to-date overview of the market before the start of the trading session.
