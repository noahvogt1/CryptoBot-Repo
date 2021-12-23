import numpy as np
import pandas as pd
from pandas.core.window.rolling import Window
import yfinance as yf
from plotly.subplots import make_subplots 
import plotly.graph_objs as go
import time

Done=False

def BollingerBands(data):
    data['Middle Band'] = data['Adj Close'].rolling(window=21).mean()
    data['Upper Band'] = data['Middle Band'] + 1.96*data['Adj Close'].rolling(window=21).std()
    data['Lower Band'] = data['Middle Band'] - 1.96*data['Adj Close'].rolling(window=21).std()

    return data

def EMA(data, period, smoothing=2):
    ema = []

    for price in data["Adj Close"][:period]:
        ema.append(np.nan)

    ema.append(sum(data["Adj Close"][:period]) / period)

    for price in data["Adj Close"][period:]:
        ema.append((price * (smoothing / (1 + period))) + ema[-1] * (1 - (smoothing / (1 + period))))

    ema.pop(0)

    data["EMA_" + str(period)] = ema
    return data


def SMA(data, period):
    data["SMA_" + str(period)] = data.rolling(window=period).mean()
    return data

def RSI(data, periods = 14, ema=True):
    close_delta = data['Adj Close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
	    # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    rsi = ma_up / ma_down
    data["RSI"] = 100 - (100/(1 + rsi))
    return data

while not Done:
    data = yf.download(tickers='BTC-USD', period='1d', interval='1m')

    data.drop("Close", axis=1)

    fig = make_subplots(rows=2, cols=1)

    data = RSI(data)
    fig.add_trace(go.Scatter(x=data.index, y= data["RSI"],line=dict(color='purple', width=1), name = "RSI"), row=2, col=1)



    # Calc Bollinger Bands
    data = BollingerBands(data)
    
    # Calc EMA and ad them to the graph
    emasUsed = [3, 50]
    for ema in emasUsed:
        data = EMA(data, ema)
        fig.add_trace(go.Scatter(x=data.index, y= data["EMA_" + str(ema)],line=dict(color='#17becf', width=1), name = 'EMA_'+str(ema)), row=1, col=1)


    fig.add_trace(go.Scatter(x=data.index, y= data["Middle Band"],line=dict(color='blue', width=.7), name = 'Middle Band'), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y= data["Upper Band"],line=dict(color='red', width=.3), name = 'Upper Band (Sell)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y= data["Lower Band"],line=dict(color='green', width=.3), name = 'Lower Band (Buy)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y= data['Close'],line=dict(color='black', width=.7), name = 'Price'), row=1, col=1)

   # Add titles
    fig.update_layout(
        title='Bitcoin live share price evolution',
        yaxis_title='Stock Price (USD per Shares)')


    #Show
    fig.show()
    
    time.sleep(20)