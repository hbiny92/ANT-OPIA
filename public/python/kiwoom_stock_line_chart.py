import plotly.offline as offline
from plotly import tools
import plotly.graph_objs as go
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import plotly
import plotly.graph_objs as go
from plotly.offline import *
import sys

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
1. 키움API를 활용한( CSV 처리로 미리 테스트 ) 주가차트 시각화
2. plotly를 활용
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

stock_df = pd.read_csv('./abcd.csv')
stock_df.head()

# print(stock_df)
# print(type(stock_df))

# stock_df 컬럼명 'Date'의 타입을 Date로 바꿔줌
stock_df['Date'] = pd.to_datetime(stock_df['Date'])

# stock_df 일자(Date)를 기준으로 오름차순 정렬
real_stock = stock_df.sort_values(by=['Date'], ascending=True)

print(real_stock)  # Date 오름차순 정렬완료
print(real_stock.Date)  # Date 컬럼 값 출력
print(real_stock.close)  # close 컬럼 값 출력
print(real_stock.iloc[0]['Date'])  # Date 컬럼의 0번째 인덱스 값 출력
print(real_stock.iloc[0]['close'])  # close 컬럼의 0번째 인덱스 값 출력

# Draw the line chart

stock_date = go.Scatter(
    x=real_stock.Date,
    y=real_stock['Date'],
    name="stock date")

print(stock_date)

line_chart = go.Scatter(
    mode='lines+markers',
    marker=dict(color='rgb(255,0,144)', size=8),  # 20, 20,255
    # 243, 112, 255  # 20, 20, 255
    line=dict(color='rgb(255,0,144)', width=3),
    x=real_stock.Date,
    y=real_stock['close'],
    name="line")

''' trace = go.Scatter(
    x=real_stock['Date'], y=real_stock['close'],
    name='주가 차트'
) '''


layout_s = go.Layout(
    width=915,
    height=640,
    title='주가 차트',
    paper_bgcolor='rgb(255,255,255)',  # 23, 32, 42 #0,0,0 블랙
    plot_bgcolor='rgb(255,255,255)',  # 23, 32, 42 #0,0,0 블랙
    font=dict(family='Tmon몬소리 Black',
                  size=22, color='dimgray'),

    xaxis=dict(
        gridcolor='rgb(241,241,241)',
        showgrid=True,
        tickcolor='rgb(220,220,220)'
    ),
    yaxis=dict(
        gridcolor='rgb(241,241,241)',
        tickcolor='rgb(220,220,220)'
    )
)

data_cur = [line_chart]

fig = go.Figure(data_cur, layout=layout_s)

plotly.offline.plot(fig, filename='stock-prices.html')
