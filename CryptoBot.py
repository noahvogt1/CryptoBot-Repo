import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import time

testvar = 0
shares = 0

var = "string"
var2 = 123
var3 = True
var4 = {1,2,3,4,5}

i=1
while i==1:
    data = yf.download(tickers='BTC-USD', period='1d', interval='1m')

    fig = go.Figure()

    data['Middle Band'] = data['Close'].rolling(window=21).mean()
    data['Upper Band'] = data['Middle Band'] + 1.96*data['Close'].rolling(window=21).std()
    data['Lower Band'] = data['Middle Band'] - 1.96*data['Close'].rolling(window=21).std()
    # timeNU = data["Upper Band"].iloc[-1:].to_dict()
    # timeNL = data["Lower Band"].iloc[-1:].to_dict()
    
    timeN = data.iloc[-1:]
    for date, item in timeN.iterrows():
        if item["Close"] < item["Lower Band"]:
            print("inside")
        elif item["Close"] > item["Upper Band"]:
            print("above")
        else:
            print("Inside")

    print(testvar)


    fig.add_trace(go.Scatter(x=data.index, y= data["Middle Band"],line=dict(color='blue', width=.7), name = 'Middle Band'))
    fig.add_trace(go.Scatter(x=data.index, y= data["Upper Band"],line=dict(color='red', width=.7), name = 'Upper Band (Sell)'))
    fig.add_trace(go.Scatter(x=data.index, y= data["Lower Band"],line=dict(color='green', width=.7), name = 'Lower Band (Buy)'))
    fig.add_trace(go.Scatter(x=data.index, y= data['Close'],line=dict(color='black', width=.7), name = 'Price'))

   # Add titles
    fig.update_layout(
        title='Bitcoin live share price evolution',
        yaxis_title='Stock Price (USD per Shares)')

    #Show
    fig.show()
    
    time.sleep(20)