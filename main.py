import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from tqdm import tqdm
import plotly.graph_objects as go
import json

from components.wallet import wallet
from components.algo import EMAStrategy, SMAStrategy
from components.fetchData import fecthData

def test(df, filename: str):
    dfdata = {'SMA_1': [], 'SMA_2': [], 'Equity_SMA': [], 'Equity_EMA': []}
    dataframe = pd.DataFrame(dfdata)
    columns = list(dataframe)
    data = []
    
    for sma1 in tqdm(range(1, 51), desc = 'Progress Bar'):
        for sma2 in range(40, 151):
            walletName = str(sma1)+'_'+str(sma2)
            walletName = wallet(10000)
            walletName.smaValue(sma1, sma2)
            
            df1 = df.copy()
            df2 = df.copy()

            SMA_results = SMAStrategy(walletName, sma1, sma2, df1)
            EMA_results = EMAStrategy(walletName, sma1, sma2, df2)

            values = [walletName.sma1, walletName.sma2, SMA_results[0], EMA_results[0]]
            zipped = zip(columns, values)
            a_dictionary = dict(zipped)
            data.append(a_dictionary)

            walletName.__del__()

    dataframe = dataframe.append(data, True)
    GFG = pd.ExcelWriter(f'{filename}.xlsx')
    dataframe.to_excel(GFG, index=False)
    GFG.save()
    
    print(tabulate(dataframe, headers='keys', tablefmt='pretty'))



def main(strat, chart):
    with open('components\config.json', 'r') as json_file:
        settings = json.load(json_file)

    tickerSymbol = settings['tickerSymbol']
    df = fecthData(tickerSymbol, True)
    
    def graph_chart(chart):
        height = 800
        if strat.lower() == 'sma':

            df1 = df.copy()
            Wallet = wallet(settings['saldo'])
            SMA1, SMA2 = 20, 50

            SMA_result = SMAStrategy(Wallet, SMA1, SMA2, df1)
            df1 = SMA_result[1]

            if chart.lower() == 'candlestick':
                fig = go.Figure(data=[go.Candlestick(x = df.index, name=f'{tickerSymbol} Price', open=df1['Open'], 
                    high=df1['High'], low=df1['Low'], close=df1['Close'])])

            elif chart.lower() == 'line chart':
                fig = go.Figure()
                fig.add_trace(go.Scatter(x = df.index, y = df1['Adj Close'], mode='lines', name=f'{tickerSymbol} Price', 
                    line=dict(color='black', width=2)))

            fig.add_trace(go.Scatter(x = df.index, y=df1[f'SMA {SMA1}'], mode='lines', name= f'SMA {SMA1}'))
            fig.add_trace(go.Scatter(x = df.index, y=df1[f'SMA {SMA2}'], mode='lines', name= f'SMA {SMA2}'))
            fig.update_layout(height=height)

            return fig, SMA_result[0]

        if strat.lower() == 'ema':

            df2 = df.copy()
            Wallet = wallet(settings['saldo'])
            EMA1, EMA2 = 20, 50

            EMA_result = EMAStrategy(Wallet, EMA1, EMA2, df2)
            df2 = EMA_result[1]

            if chart.lower() == 'candlestick':
                fig = go.Figure(data=[go.Candlestick(x = df.index, name=f'{tickerSymbol} Price', open=df2['Open'], 
                    high=df2['High'], low=df2['Low'], close=df2['Close'])])
            elif chart.lower() == 'line chart':
                fig = go.Figure()
                fig.add_trace(go.Scatter(x = df.index, y=df2['Adj Close'], mode='lines', name=f'{tickerSymbol} Price', 
                    line=dict(color='black', width=2)))

            fig.add_trace(go.Scatter(x = df.index, y=df2[f'EMA {EMA1}'], mode='lines', name= f'EMA {EMA1}'))
            fig.add_trace(go.Scatter(x = df.index, y=df2[f'EMA {EMA2}'], mode='lines', name= f'EMA {EMA2}'))
            fig.update_layout(height=height)

            return fig, EMA_result[0]
        
    return graph_chart(chart)