from pydoc import classname
from dash import Dash, dcc, html, Input, Output, State
from components.assembler import assembler
import json

app = Dash(__name__)

def updateJSON(id, value):
    json_file = open('components\config.json', 'r')
    Json_config = json.load(json_file)
    json_file.close()

    Json_config[f'{id}'] = value

    json_file = open('components\config.json', 'w')
    json.dump(Json_config, json_file)
    json_file.close()


interval_range = ['1m', '2m', '5m', '15m', '30m',
                  '60m', '90m', '1d', '5d', '1wk', '1mo', '3mo']

with open('components\config.json', 'r') as json_file:
    settings = json.load(json_file)

app.layout = html.Div(
    className='main_page',
    children=[

        html.H1(children='Data visualisering', style={'textAlign': 'center'}),
        html.Div(
            className='options-label',
            children=[
                html.H4(children='Ticker Symbol', style={'textAlign': 'center'}),
                html.H4(children='Saldo for account', style={'textAlign': 'center'}),
                html.H4(children='Time Period', style={'textAlign': 'center'}),
                html.H4(children='Interval for data point', style={'textAlign': 'center'}),
                html.H4(children='Strategy', style={'textAlign': 'center'}),
                html.H4(children='', style={'textAlign': 'center'}),
            ]),
        html.Div(
            className='options',
            children=[
                dcc.Input(id="tickerSymbol", type="text", placeholder="Ticker symbol",
                          value=settings['tickerSymbol'], debounce=True),
                dcc.Input(id="saldo", type="number", placeholder="Saldo",
                          value=settings['saldo'], debounce=True),
                dcc.Dropdown(['1d', '5d', '14d', '1mo', '3mo', '6mo', '1y', '2y',
                             '5y', '10y', 'ytd', 'max'], settings['period'], id="period"),
                dcc.Dropdown(interval_range,
                             settings['interval'], id="interval"),
                dcc.Dropdown(['Sma', 'Ema'], 'Sma', id='strat'),
                html.Button(id='button_update', n_clicks=0, children='Update graph')
            ]),
            html.Div(
            className='chart-options',
            children=[
                dcc.Dropdown(['Candlestick', 'line chart'], 'Candlestick', id='chart lines'),
            ]),
        html.H3(id='output-state', className='equity'),
        dcc.Graph(id='price-graph'),
        dcc.Graph(id='equity-graph')
    ])

@app.callback(
    Output('price-graph', 'figure'),
    Output('equity-graph', 'figure'),
    Output('output-state', 'children'),
    Input('button_update', 'n_clicks'),
    State('strat', 'value'),
    State('tickerSymbol', 'value'),
    State('saldo', 'value'),
    State('period', 'value'),
    State('interval', 'value'),
    State('chart lines', 'value')
)

def update_graph(n_clicks, strat, tickerSymbol, saldo, period, interval, chart):
    updateJSON('tickerSymbol', tickerSymbol)
    updateJSON('saldo', saldo)
    updateJSON('period', period)
    updateJSON('interval', interval)
    updateJSON('chart', chart)
    updateJSON('strat', strat)

    data = assembler()
    return data[0], data[1], f'''Your equity efter a period over {period} is: {round(data[2], 2)} USD, 
    your equity has increased by {round(100*((float(data[2])-float(saldo))/abs(float(saldo))))} %'''

if __name__ == '__main__':
    app.run_server(debug=True)
