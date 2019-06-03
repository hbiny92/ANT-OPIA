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
1. 크롤링한 일봉데이터를 스토캐스틱 통계 기법을 적용
2. plotly를 활용한 라인 차트, 바 차트 시각화 
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# sys.stdout.reconfigure(encoding='utf-8')
code_df = pd.read_html(
    'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드']]

# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
code_df.head()


# 종목 이름을 입력하면 종목에 해당하는 코드를 불러와
# 네이버 금융(http://finance.naver.com)에 넣어줌


def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))[
        'code'].to_string(index=False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(
        code=code)

    print("요청 URL = {}".format(url))
    return url


# 특정 기업명의 일자데이터 url 가져오기
item_name = '삼성전자'
url = get_url(item_name, code_df)

# 일자 데이터를 담을 df라는 DataFrame 정의
df1 = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()

# 오늘날짜 기준 10일치의 실시간 일봉 데이터를 가져오기 위해 1p~2p만 불러오기
for page in range(1, 2):
    pg_url = '{url}&page={page}'.format(url=url, page=page)
    df1 = df1.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

# 이전 달 데이터 ~ 오늘날데이터(n)까지 약 30+n일치의 실시간 일봉 데이터를 가져오기 위해 2p~4p만 불러오기
for page in range(1, 4):
    pg_url = '{url}&page={page}'.format(url=url, page=page)
    df2 = df2.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

# 1분기 ~ 오늘날데이터(n)까지 약 90+n일치의 일봉 데이터를 가져오기 위해 1p~2p만 불러오기
for page in range(1, 11):
    pg_url = '{url}&page={page}'.format(url=url, page=page)
    df3 = df3.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)


# df1.dropna()를 이용해 결측값 있는 행 제거
df1 = df1.dropna()
df2 = df2.dropna()
df3 = df3.dropna()

# df1~df3 데이터 확인하기
# print(df1.tail())
# print(df2.tail())
# print(df3.tail())

# df1~df3의 한글로 된 컬럼명을 영어로 바꿔줌
df1 = df1.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff',
                          '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})
#
df2 = df2.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff',
                          '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})
#
df3 = df3.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff',
                          '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})

# df1~df3 데이터의 타입을 int형으로 바꿔줌
df1[['close', 'diff', 'open', 'high', 'low', 'volume']] \
    = df1[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
#
df2[['close', 'diff', 'open', 'high', 'low', 'volume']] \
    = df2[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
#
df3[['close', 'diff', 'open', 'high', 'low', 'volume']] \
    = df3[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)

# df1~df3 컬럼명 'date'의 타입을 date로 바꿔줌
df1['date'] = pd.to_datetime(df1['date'])
# print(df1['date'])
df2['date'] = pd.to_datetime(df2['date'])
df3['date'] = pd.to_datetime(df3['date'])

# df1~df3 일자(date)를 기준으로 오름차순 정렬
df1 = df1.sort_values(by=['date'], ascending=True)
df2 = df2.sort_values(by=['date'], ascending=True)
df3 = df3.sort_values(by=['date'], ascending=True)

# 일자(n,m,t)에 따른 Stochastic(KDJ)의 값을 구하기 위해 함수형태로 만듬


def get_stochastic(df, n=15, m=5, t=3):

    # 입력받은 값이 dataframe이라는 것을 정의해줌
    df = pd.DataFrame(df)

    # n일중 최고가
    ndays_high = df.high.rolling(window=n, min_periods=1).max()
    # n일중 최저가
    ndays_low = df.low.rolling(window=n, min_periods=1).min()

    # Stochastic fast %K calculate
    kdj_k = ((df.close - ndays_low) / (ndays_high - ndays_low))*100
    # Stochastic fast %D calculate
    kdj_d = kdj_k.ewm(span=m).mean()
    # Slow%D calculate
    kdj_j = kdj_d.ewm(span=t).mean()

    # dataframe에 컬럼 추가
    df = df.assign(kdj_k=kdj_k, kdj_d=kdj_d, kdj_j=kdj_j).dropna()

    return df


df1 = get_stochastic(df1)
df2 = get_stochastic(df2)
df3 = get_stochastic(df3)

# print(df1)
# print(df2)

# print(df1.head())
# df2.head()
# df3.head()

# jupyter notebook 에서 출력
# offline.init_notebook_mode(connected=True)


# df1 그래프 시각화

def get_graph(df):
    offline.init_notebook_mode(connected=True)

    # print(df)
    # print(type(df))

    kdj_k = go.Scatter(
        x=df.date,
        y=df['kdj_k'],
        name="Fast%K")

    kdj_d = go.Scatter(
        x=df.date,
        y=df['kdj_d'],
        name="Fast%D")
    print(kdj_d)

    kdj_d2 = go.Scatter(
        mode='lines+markers',
        marker=dict(color='rgb(20,20,255)', size=8),
        line=dict(color='rgb(20,20,255)', width=3),
        x=df.date,
        y=df['kdj_d'],
        name="Slow%K")

    kdj_j = go.Scatter(
        mode='lines+markers',
        marker=dict(color='rgb(255,10,10)', size=8),
        line=dict(color='rgb(255,10,10)', width=3),
        x=df.date,
        y=df['kdj_j'],
        name="Slow%D")

    trade_volume = go.Bar(
        marker=dict(
            color='rgba(153, 218, 205, 0.8)',
            line=dict(
                color='rgba(20, 143, 119, 1.0)',
                width=3),
        ),
        x=df.date,
        y=df['volume'],
        name="volume"
    )

    # data = [kdj_k, kdj_d]
    data1 = [kdj_d2, kdj_j]
    data2 = [trade_volume]

    # 레이아웃 1 설정 ( 매수/매도 포지션 라인 그래프 )
    layout_1 = go.Layout(
        width=1720,
        height=540,
        title='매수 / 매도 포지션 차트',
        # 23, 32, 42 #0,0,0 블랙
        paper_bgcolor='rgb(255,255,255)',
        # 23, 32, 42 #0,0,0 블랙
        plot_bgcolor='rgb(255,255,255)',
        font=dict(family='Tmon몬소리 Black',
                  size=30, color='dimgray'),
        showlegend=False,

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

    # 레이아웃 2 설정 ( 일일 총 거래량 )
    layout_2 = go.Layout(
        width=1720,
        height=540,
        title='일일 주식 총 거래량',
        paper_bgcolor='rgb(255,255,255)',  # 23, 32 ,42 , # 0, 0, 0(블랙)
        plot_bgcolor='rgb(255,255,255)',  # 23, 32 ,42, #0, 0, 0(블랙)
        font=dict(family='Tmon몬소리 Black',
                  size=22, color='dimgray'),
        xaxis=dict(
            gridcolor='rgb(241,241,241)',  # 33, 47, 60
            showgrid=True,
            tickcolor='rgb(220,220,220)'  # 52, 73, 94
        ),
        yaxis=dict(
            gridcolor='rgb(241,241,241)',  # 33, 47, 60
            tickcolor='rgb(220,220,220)'  # 52, 73, 94
        )
    )

    # data1 or data2 바꿔 적용하기
    data_cur = data2

    fig = tools.make_subplots(
        rows=2, cols=1, shared_xaxes=True)

    for trace in data1:
        fig.append_trace(trace, 1, 1)

    for trace in data2:
        fig.append_trace(trace, 2, 1)

    # 레이아웃 변경 1 or 2
    fig = go.Figure(data=data_cur, layout=layout_2)

    # offline.iplot(fig)
    return plotly.offline.plot(fig)


get_graph(df3)  # 함수 호출 & run
