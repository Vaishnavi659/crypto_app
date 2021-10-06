import streamlit as st
import pandas as pd 
from PIL import Image
import base64
import matplotlib.pyplot as plt 
import seaborn as sns
from bs4 import BeautifulSoup
import requests
import json
import time






#Page expands to full width
st.set_page_config(layout = "wide")
#Logo for the app
image = Image.open('logo.jpeg')

st.image(image,width=500)


# title----------------------------------------
st.title('Crypto-Price App')
st.markdown(""" 
This app retrieves top 100 Cryptocurrencies """)

#about------------------------------------------
expander_bar  = st.beta_expander("About")

expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
* **Data source:** [CoinMarketCap](http://coinmarketcap.com).
* **Credit:** Web scraper adapted from the Medium article *[Web Scraping Crypto Prices With Python](https://towardsdatascience.com/web-scraping-crypto-prices-with-python-41072ea5b5bf)* written by [Bryan Feng](https://medium.com/@bryanf).
* **Contributed by:** Vaishnavi Kalgutkar, Diksha Negi 
""")


#-------------------------------------
#col1 is sidebar and col2 and col3 page contents
col1  = st.sidebar
# col2 is twice in width as col1
col2,col3 = st.beta_columns((2,1))

#header for col1 
col1.header('Input options')
#sidebar - currency price unit
currency_price_unit = col1.selectbox('Select currency for price',('USD','BTC','ETH'))


#@st.cache
def load_data():
    cmc=requests.get('https://coinmarketcap.com')
    soup=BeautifulSoup(cmc.content,'html.parser')
    # using soup.prettify to find the webpage's format 
    # print(soup.prettify())

    data=soup.find('script',id='__NEXT_DATA__',type='application/json')
    coins={}
    coin_data=json.loads(data.contents[0])
    listings=coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    for i in listings[1:]:
        coins[str(i[8])]=i[125]

    coin_name=[]
    coin_symbol=[]
    market_cap=[]
    percent_change_1h=[]
    percent_change_24h=[]
    percent_change_7d=[]
    price=[]
    volume_24h=[]



    for i in listings[1:]:
        coin_name.append(i[125])
        coin_symbol.append(i[126])
        if currency_price_unit == 'BTC':
            price.append(i[28])
            percent_change_1h.append(i[22])
            percent_change_24h.append(i[23])
            percent_change_7d.append(i[26])
            market_cap.append(i[19])
            volume_24h.append(i[30])

        if currency_price_unit == 'USD':
            price.append(i[64])
            percent_change_1h.append(i[58])
            percent_change_24h.append(i[59])
            percent_change_7d.append(i[62])
            market_cap.append(i[55])
            volume_24h.append(i[66])
        if currency_price_unit == 'ETH':
            price.append(i[46])
            percent_change_1h.append(i[40])
            percent_change_24h.append(i[41])
            percent_change_7d.append(i[44])
            market_cap.append(i[37])
            volume_24h.append(i[48])






    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h
    return df


df = load_data()



sorted_coin = sorted(df['coin_symbol'])
selected_coin = col1.multiselect('Cryptocurrency',sorted_coin,sorted_coin)

df_selected_coin = df[df['coin_symbol'].isin(selected_coin)]

num_coin = col1.slider('Display Top N coins',1,100,100)
df_coins = df_selected_coin[:num_coin]

percent_timeframe = col1.selectbox('Percent change time frame',['7d','24h','1h'])
percent_dict={"7d":'percent_change_7d','24h':'percent_change_24h','1h':'percent_change_1h'}
selected_percent_timeframe=percent_dict[percent_timeframe]


sort_values = col1.selectbox('Sort values?',['Yes','No'])

col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')

col2.dataframe(df_coins)
