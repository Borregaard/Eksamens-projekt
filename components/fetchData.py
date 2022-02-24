import yfinance as yf
import pandas as pd
import json


def fecthData(TickerSymbol, saveCSV=False):
    with open('components\config.json', 'r') as json_file:
	    settings = json.load(json_file)
    
    data = yf.download(tickers=f'{TickerSymbol}', period=settings["period"], interval=settings["interval"], index_col='date', parse_dates=True)
    df = pd.DataFrame(data)
    
    if saveCSV:
        df.to_csv('BTC-USD', index=True)
        
    return df
