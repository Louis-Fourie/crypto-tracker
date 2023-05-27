# imports
import pandas as pd
import numpy as np
import requests
import json
from IPython.display import HTML
import matplotlib.pyplot as plt
# API endpoint
url = "https://www.alphavantage.co/query"
# symbols to iterate through
symbols = ["DOT", "ETC", "ATOM", "SOL", "AVAX"]
# empty list to store DataFrames
dfs = []
# request Alpha Vantage API cryptocurrency data using parameters
for symbol in symbols:
    params = {
        "function": "DIGITAL_CURRENCY_DAILY",
        "symbol": symbol,
        "market": "USD",
        "apikey": "MMMZR5JJJXW4HBO1",
        "outputsize": "compact"
    }
    try:
        # receive response from API
        response = requests.get(url, params=params)
        # decode response and store as a JSON object
        data = response.json()
    except requests.exceptions.HTTPError as http_error:
        # check for API request error
        print(f"HTTP error occurred: {http_error}")
    except requests.exceptions.RequestException as error:
        # check for any other errors occurring during the request
        print(f"An error occurred: {error}")
    # extract useful data from JSON object
    time_series_data = data['Time Series (Digital Currency Daily)']
    # Create a list of dictionaries where each dictionary contains date-value pairs for the cryptocurrency symbol, using dictionary unpacking to combine the date key with the other keys and values in the time series data.
    time_series_list = [{**{'date': key}, **value} for key, value in time_series_data.items()]
    time_series_short_list = time_series_list[:5]

    df = pd.json_normalize(time_series_short_list)
    df = df.drop(['1b. open (USD)', '2b. high (USD)', '3b. low (USD)', '4b. close (USD)'], axis=1)
    df = df.rename(columns={'date': 'Date', '1a. open (USD)': '1. Open (USD)', '2a. high (USD)': '2. High (USD)', '3a. low (USD)': '3. Low (USD)', '4a. close (USD)': '4. Close (USD)', '5. volume': '5. Volume', '6. market cap (USD)': '6. Market Cap (USD)'})
    df = df.astype({'1. Open (USD)': float,'2. High (USD)' : float, '3. Low (USD)': float, '4. Close (USD)': float, '5. Volume': float, '6. Market Cap (USD)': float})
    df = df.round(2)
    df["symbol"] = symbol
    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)

table_html = df.to_html()
with open('table.html', 'w') as f:
    f.write(table_html)

# Set up the figure and axes
fig, ax = plt.subplots()

# Loop through each stock symbol and plot the closing price over time
for symbol in symbols:
    # Get the data for the current symbol
    df_symbol = df[df["symbol"] == symbol]
    
    # Plot the closing price over time
    ax.plot(df_symbol["Date"], df_symbol["4. Close (USD)"], label=symbol)

# Set the title and axis labels
ax.set_title("Stock Prices Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Closing Price (USD)")

# Add a legend and show the plot
ax.legend()
plt.show()
