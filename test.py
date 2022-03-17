import pandas as pd
from tabulate import tabulate
from tqdm import tqdm
import plotly.graph_objects as go

from components.wallet import wallet
from components.algo import EMAStrategy, SMAStrategy

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

            SMA_results = SMAStrategy(walletName, sma1, sma2, df.copy())
            EMA_results = EMAStrategy(walletName, sma1, sma2, df.copy())

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