import plotly.graph_objects as go
import json

from components.fetchData import fecthData
from components.graphing import graph_chart


def assembler():
    with open('components\config.json', 'r') as json_file:
        settings = json.load(json_file)

    df = fecthData(settings['tickerSymbol'], True)

    price_graph, df, equity = graph_chart(settings['chart'], df.copy())

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df.index, y=df['equity'], mode='lines', name=f'Equity',
                              line=dict(color='black', width=2)))
    fig1.update_layout(height=800)

    return price_graph, fig1, equity
