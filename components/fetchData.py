import yfinance as yf
import pandas as pd
import json


def fecthData(TickerSymbol, saveCSV=False):
    with open('components\config.json', 'r') as json_file:
        settings = json.load(json_file)

    data = yf.download(tickers=f'{TickerSymbol.upper()}', period=settings["period"],
                       interval=settings["interval"], index_col='date', parse_dates=True)
    df = pd.DataFrame(data)

    if saveCSV == True:
        df.to_csv(f'{TickerSymbol}', index=True)

    return df

