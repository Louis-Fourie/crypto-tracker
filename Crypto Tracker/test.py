# chart for BTC over the last 5 years, 3-monthly intervals

import pandas as pd
import numpy as np
import requests
import json
from IPython.display import HTML
import matplotlib.pyplot as plt

url = "https://www.alphavantage.co/query"
symbol = input("Input a cryptocurrency symbol: ")

params = {
    "function": "DIGITAL_CURRENCY_MONTHLY",
    "symbol": symbol,
    "market": "USD",
    "apikey": "MMMZR5JJJXW4HBO1",
    "outputsize": "full",
    "interval": "monthly"
    }
response = requests.get(url, params=params)
data = response.json()

time_series_data = data['Time Series (Digital Currency Monthly)']
time_series_list = [{**{'date': key}, **value} for key, value in time_series_data.items()]
time_series_short_list = time_series_list[:61]

df = pd.json_normalize(time_series_short_list)
df = df.drop(0)
df = df.drop(df.columns[[1, 2, 3, 4, 5, 6, 8, 9, 10]], axis=1)

df = df.drop(df.index[2::3])
df = df.reset_index(drop=True)
df = df.drop(df.index[1::2])
df = df.reset_index(drop=True)
df.index = df.index + 1

df = df.rename(columns={'date': 'Date', '4a. close (USD)': 'Price'})
df = df.astype({'Price': float})

testTable_html = df.to_html()
with open('testTable.html', 'w') as f:
    f.write(testTable_html)

plt.plot(df['Date'], df['Price'])
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Bitcoin Price over Time')
plt.show()