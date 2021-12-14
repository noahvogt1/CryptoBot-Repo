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
    timeN = data[-1]

    fig = go.Figure()

    mid = data['Middle Band'] = data['Close'].rolling(window=21).mean()
    upper = data['Upper Band'] = data['Middle Band'] + 1.96*data['Close'].rolling(window=21).std()
    lower = data['Lower Band'] = data['Middle Band'] - 1.96*data['Close'].rolling(window=21).std()
    timeNU = upper[-1]
    timeNL = lower[-1]

    if timeN < timeNL:
        testvar = testvar + timeN
    if timeN > timeNU:
        if shares > 0:
            testvar = testvar - timeN
        else:
            0

    print(testvar)


    fig.add_trace(go.Scatter(x=data.index, y= mid,line=dict(color='blue', width=.7), name = 'Middle Band'))
    fig.add_trace(go.Scatter(x=data.index, y= upper,line=dict(color='red', width=.7), name = 'Upper Band (Sell)'))
    fig.add_trace(go.Scatter(x=data.index, y= lower,line=dict(color='green', width=.7), name = 'Lower Band (Buy)'))
    fig.add_trace(go.Scatter(x=data.index, y= data['Close'],line=dict(color='black', width=.7), name = 'Price'))

   # Add titles
    fig.update_layout(
        title='Bitcoin live share price evolution',
        yaxis_title='Stock Price (USD per Shares)')

    #Show
    fig.show()
    
    time.sleep(20)