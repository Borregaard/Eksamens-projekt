import yfinance as yf
import pandas as pd
import json

with open('src\components\config.json', 'r') as json_file:
	settings = json.load(json_file)

def fecthData(TickerSymbol, saveCSV=False):
    data = yf.download(tickers=f'{TickerSymbol}', period=settings["period"], interval=settings["interval"])
    df = pd.DataFrame(data)
    
    if saveCSV:
        df.to_csv('BTC-USD', index=False)
        
    return df

