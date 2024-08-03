import yfinance as yf
import pandas as pd

load_csv = pd.read_csv(r'/Users/Ananiev/Desktop/dashing/data/name_data.csv')

tickers = load_csv["tickers"].to_list()

newdf = pd.DataFrame()
newdf['ticker'] = ""
for ticker in tickers:
    data = yf.download(str(ticker), start="2023-01-01", end="2024-01-01", period="1d")
    data['ticker'] = ticker
    newdf = pd.concat([data, newdf], axis =0)
newdf.to_csv("/Users/Ananiev/Desktop/dashing/products_prices.csv")

benches = ["EEM", "EWW", "EWY", "IJH", "SPY", "IWM"]

newdf = pd.DataFrame()
newdf['ticker'] = ""
for ticker in benches:
    data = yf.download(str(ticker), start="2023-01-01", end="2024-01-01", period="1d")
    data['ticker'] = ticker
    newdf = pd.concat([data, newdf], axis =0)
newdf.to_csv("/Users/Ananiev/Desktop/dashing/benches_prices.csv")

