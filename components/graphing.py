import plotly.graph_objects as go
import pandas as pd
import json

from components.wallet import wallet
from components.algorithms.SmaAndEma import EMAStrategy, SMAStrategy


def graph_chart(chart, df):

    with open('components\config.json', 'r') as json_file:
        settings = json.load(json_file)

    tickerSymbol = settings['tickerSymbol']

    height = 1000
    Wallet = wallet(settings['saldo'])
    strat = settings['strat'].upper()

    if strat.lower() == 'sma':
        SMA1, SMA2 = 1, 52
        equity, df = SMAStrategy(Wallet, SMA1, SMA2, df)

    if strat.lower() == 'ema':
        SMA1, SMA2 = 1, 92
        equity, df = EMAStrategy(Wallet, SMA1, SMA2, df)

    if chart.lower() == 'candlestick':
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, name=f'{tickerSymbol} Price', open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])

    elif chart.lower() == 'line chart':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Adj Close'], mode='lines', name=f'{tickerSymbol} Price',
                                 line=dict(color='black', width=2)))

    fig.add_trace(go.Scatter(
        x=df.index, y=df[f'{strat} {SMA1}'], mode='lines', name=f'{strat} {SMA1}'))
    fig.add_trace(go.Scatter(
        x=df.index, y=df[f'{strat} {SMA2}'], mode='lines', name=f'{strat} {SMA2}'))

    fig.add_trace(go.Scatter(x=df.index, y=df['buy_signals'], mode="markers",
                             name='Buy signals', marker_symbol='triangle-up', marker_size=10, marker_color='green'))
    fig.add_trace(go.Scatter(x=df.index, y=df['sell_signals'], mode="markers",
                             name='Sell signals', marker_symbol='triangle-down', marker_size=10, marker_color='red'))

    fig.update_layout(height=height)

    return fig, df, equity
