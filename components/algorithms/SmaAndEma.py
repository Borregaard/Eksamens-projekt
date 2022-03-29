import pandas as pd


def SMAStrategy(wallet, SMA_1, SMA_2, df):

    df[f'SMA {SMA_1}'] = df['Adj Close'].rolling(SMA_1).mean()
    df[f'SMA {SMA_2}'] = df['Adj Close'].rolling(SMA_2).mean()

    buy_signals = []
    sell_signals = []
    equity = []

    for x in range(len(df)):
        if df[f'SMA {SMA_1}'].iloc[x] > df[f'SMA {SMA_2}'].iloc[x] and wallet.trigger != 1:
            sell_signals.append(float('nan'))
            buy_signals.append(df[f'SMA {SMA_2}'].iloc[x])

            wallet.buyOrder(df['Adj Close'].iloc[x])
            wallet.trigger = 1

        elif df[f'SMA {SMA_1}'].iloc[x] < df[f'SMA {SMA_2}'].iloc[x] and wallet.trigger != -1:
            buy_signals.append(float('nan'))
            sell_signals.append(df[f'SMA {SMA_2}'].iloc[x])

            wallet.sellOrder(df['Adj Close'].iloc[x])
            wallet.trigger = -1

        else:
            buy_signals.append(float('nan'))
            sell_signals.append(float('nan'))

        equity.append(wallet.equity(df['Adj Close'].iloc[x]))

    df['equity'] = equity
    df['buy_signals'] = buy_signals
    df['sell_signals'] = sell_signals

    return wallet.equity(df['Adj Close'].iloc[-1]), df


def EMAStrategy(wallet, SMA_1, SMA_2, df):

    df[f'SMA {SMA_1}'] = df['Adj Close'].rolling(SMA_1).mean()
    df[f'SMA {SMA_2}'] = df['Adj Close'].rolling(SMA_2).mean()

    df[f'EMA {SMA_1}'] = df['Adj Close'].ewm(span=SMA_1, adjust=False).mean()
    df[f'EMA {SMA_2}'] = df['Adj Close'].ewm(span=SMA_2, adjust=False).mean()

    buy_signals = []
    sell_signals = []
    equity = []

    for x in range(len(df)):
        if df[f'EMA {SMA_1}'].iloc[x] > df[f'EMA {SMA_2}'].iloc[x] and wallet.trigger != 1:
            sell_signals.append(float('nan'))
            buy_signals.append(df[f'EMA {SMA_2}'].iloc[x])

            wallet.buyOrder(df['Adj Close'].iloc[x])
            wallet.trigger = 1

        elif df[f'EMA {SMA_1}'].iloc[x] < df[f'EMA {SMA_2}'].iloc[x] and wallet.trigger != -1:
            buy_signals.append(float('nan'))
            sell_signals.append(df[f'EMA {SMA_2}'].iloc[x])

            wallet.sellOrder(df['Adj Close'].iloc[x])
            wallet.trigger = -1

        else:
            buy_signals.append(float('nan'))
            sell_signals.append(float('nan'))

        equity.append(wallet.equity(df['Adj Close'].iloc[x]))

    df['equity'] = equity
    df['buy_signals'] = buy_signals
    df['sell_signals'] = sell_signals

    return wallet.equity(df['Adj Close'].iloc[-1]), df
