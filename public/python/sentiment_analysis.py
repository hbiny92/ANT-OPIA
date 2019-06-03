# -*- coding: utf-8 -*-
from __future__ import division

import re
import matplotlib.pyplot as pyplot
import pandas as pd
from konlpy.tag import Kkma
from pandas import Series, DataFrame
import plotly.offline as offline
from plotly import tools
import plotly.graph_objs as go
import plotly
from plotly.offline import *
import plotly.plotly as py
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
import sys
import json
# sys.stdout.reconfigure(encoding='utf-8')

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
1. lexion 감성사전을 이용한 n-gram 형태소/품사 분석
2. news 기사에서 추출한 형태소의 긍/부정 지수 계산 및 출력
3. plotly를 활용한 긍/부정 지수 Pie chart 출력
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# 각 크롤링 결과 저장하기 위한 리스트 선언
title_text = []
link_text = []
source_text = []
date_text = []
contents_text = []
news_full_list = []
result = {}

# 엑셀로 저장하기 위한 변수
RESULT_PATH = 'C:/Users/User/Desktop/naver_news_crawling-master/'  # 결과 저장할 경로
now = datetime.now()  # 파일이름 현 시간으로 저장하기

# 날짜 정제화 함수


def date_cleansing(test):
    try:
        # 지난 뉴스
        # 머니투데이  10면1단  2018.11.05.  네이버뉴스   보내기
        pattern = '\d+.(\d+).(\d+).'  # 정규표현식

        r = re.compile(pattern)
        match = r.search(test).group(0)  # 2018.11.05.
        date_text.append(match)

    except AttributeError:
        # 최근 뉴스
        # 이데일리  1시간 전  네이버뉴스   보내기
        pattern = '\w* (\d\w*)'  # 정규표현식

        r = re.compile(pattern)
        match = r.search(test).group(1)
        # print(match)
        date_text.append(match)


# 내용 정제화 함수
def contents_cleansing(contents):
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '',
                                      str(contents)).strip()  # 앞에 필요없는 부분 제거
    # print(first_cleansing_contents)
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '',
                                       first_cleansing_contents).strip()  # 뒤에 필요없는 부분 제거 (새끼 기사)
    # print(second_cleansing_contents)
    third_cleansing_contents = re.sub(
        '<.+?>', '', second_cleansing_contents).strip()
    third_cleansing_contents = re.sub(
        '[a-zA-Z-=+,''#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'》◈]', '', second_cleansing_contents)
    # print(third_cleansing_contents)
    contents_text.append(third_cleansing_contents)
    # print(contents_text)
    # [a-zA-Z-=+,''#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]


def crawler(maxpage, query, sort, s_date, e_date):

    s_from = s_date.replace(".", "")
    e_to = e_date.replace(".", "")
    page = 1
    # 11= 2페이지 21=3페이지 31=4페이지  ...81=9페이지 , 91=10페이지, 101=11페이지
    maxpage_t = (int(maxpage)-1)*10+1

    while page <= maxpage_t:
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort="+sort+"&ds=" + \
            s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + \
            s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)

        response = requests.get(url)
        html = response.text

        # 뷰티풀소프의 인자값 지정
        soup = BeautifulSoup(html, 'html.parser')

        # <a>태그에서 제목과 링크주소 추출
        atags = soup.select('._sp_each_title')
        for atag in atags:
            # print(atag)
            x = re.sub(
                '[a-zA-Z-=+,”''#/\?:^$.@*\"※“~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', atag.text).strip()
            title_text.append(x)  # 제목
            # print(title_text)
            link_text.append(atag['href'])  # 링크주소
        # title_text.remove('')

        # 신문사 추출
        source_lists = soup.select('._sp_each_source')
        for source_list in source_lists:
            y = re.sub(
                '[a-zA-Z-=+,”''#/\?:^$.@*\"※“~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', source_list.text).strip()
            source_text.append(y)  # 신문사
        # source_text.remove('')

        # 날짜 추출
        date_lists = soup.select('.txt_inline')
        for date_list in date_lists:
            test = date_list.text
            date_cleansing(test)  # 날짜 정제 함수사용

        # 본문요약본
        contents_lists = soup.select('ul.type01 dl')
        for contents_list in contents_lists:
            # print('==='*40)
            # print(contents_list)
            contents_cleansing(contents_list)  # 본문요약 정제화

        # 모든 리스트 특수문자 제거
        #
        # print(title_text)

        # 모든 리스트 딕셔너리형태로 저장

        result = {"date": date_text, "title": title_text,
                  "source": source_text, "contents": contents_text, "link": link_text}

        # print(result)  # 딕셔너리 형태 출력

        # print(title_text)  # title_text ~ contents_text 까지 리스트형 출력
        # print(link_text)
        # print(source_text)
        # print(date_text)
        # print(contents_text)
        # print(page)

        df = pd.DataFrame(result)  # df로 변환
        page += 10
        print(page)

        # 빈도수, 명사 추출을위한 데이터프레임 설정
        df_count = df[["title", "contents"]]
        # 제목, 언론사, 시간, 프리뷰, 링크 추출을위한 데이터프레임 설정
        # df_count = df[["date", "title", "source", "contents", "link"]]
        page += 10
        df_count.iloc[: 0]


def main(v1, v2, v3, v4, v5):
    maxpage = v1  # 크롤링 페이지 수
    query = v2  # 검색어 입력
    sort = v3  # 관련도순=0 , 최신순=1, 오래된순=2
    s_date = v4  # 시작 날짜 입력 20xx.xx.xx
    e_date = v5  # 끝날짜 입력 20yy.yy.yy
    crawler(maxpage, query, sort, s_date, e_date)


main("1200", "삼성전자", "0", "2019.05.20", "2019.06.01")  # direct input 설정
######################################################################################################

news_full_list.extend(title_text)
news_full_list.extend(contents_text)
print(news_full_list)


def preprocessor(text):
    text = text.rstrip().lstrip()
    # remove special chars
    return re.sub('[/[\{\}\[\]\/?|\)*~`!\-_+<>@\#$%&\\\=\(\'\"]+', '', text)


def scores_to_percentiles(scores):
    sum_of_scores = sum(scores.values())

    for category in scores:
        scores[category] = scores[category] / sum_of_scores

    return scores


def analyze_sentences_into_chunks(sentences):
    kkma = Kkma()
    analyzed_words = []

    for s in sentences:
        s = preprocessor(s)
        analyzed_in_dicts = kkma.pos(s)
        tmp = []

        for word in analyzed_in_dicts:
            tmp.append("/".join(word))
        analyzed_words.append(";".join(tmp))

    return analyzed_words


def categorize_word_chunks(chunks, lexicons):
    scores = {'POS': 0, 'NEG': 0, 'NEUT': 0, 'COMP': 0, 'None': 0}
    for chunk in chunks:
        for index, row in lexicons.iterrows():
            if row['ngram'] in chunk:
                scores[row['max.value']] += row['max.prop']

    return scores_to_percentiles(scores)


# Get data and Read files
raw_data = news_full_list

print(raw_data)

# raw_data = open('resources/example.txt', encoding='utf-8')
sentiment_data_frame = pd.read_csv(
    'C:/Users/User/Desktop/KoreanSentimentAnalysis-master/lexicon/polarity.csv')
# Split sentences to chunks
word_chunks = analyze_sentences_into_chunks(raw_data)
# Analyze sentiments from chunks and polarity data frame
categorized_scores = categorize_word_chunks(word_chunks, sentiment_data_frame)
print(categorized_scores)

# Draw pie chart using plotly
newdf = pd.DataFrame.from_dict(categorized_scores, orient='index')
newdf.reset_index(inplace=True)
newdf.columns = ['sentiment', 'score']
# print(newdf, '\n')
# print(newdf[:1], '\n')
# print(newdf.sentiment, '\n')  # 감성표현 열 출력
# print(newdf.score, '\n')  # 스코어 열 출력
# print(newdf.iloc[0]['score']) # 특정 데이 불러오기

fig = {
    "data": [
      {
          "values": [newdf.iloc[0]['score'],
                     newdf.iloc[1]['score'],
                     newdf.iloc[2]['score'],
                     newdf.iloc[3]['score'],
                     newdf.iloc[4]['score']],
          "labels": [
              "Postive", "Negative", "Neutral", "Composite", "None"
          ],


          "domain": {"x": [0.7, .3], "y": [0.5, .6]},  # 75FFDA
          "marker": {'colors': ['#6AFFE4', '#FF7CB5', '#9CBFFF',
                                '#ffac17', '#E7B2FF']},  # FFBB73
          "hoverinfo": "label+percent",
          "textposition": "outside",
          "textfont": {
              "color": ["#38B2BC", "#FF549E", "#5994FF", "#ffac17", "#CE62FF"],
              "family": ["Tmon몬소리 Black", "Tmon몬소리 Black", "Tmon몬소리 Black", "Tmon몬소리 Black", "Tmon몬소리 Black"],
              "size": [30, 30, 30, 30, 30]
          },
          "hole": .4,
          "type": "pie"
      }],
    "layout": {
        "width": 639,
        "height": 545,
        "legend": {
            "orientation": "h",
            "xanchor": "auto",
            "x": 0.5,
            "y": 0.20
        },
        "showlegend": True,
        "annotations": [
            {
                "align": "center",
                "font": {
                    "size": 21,
                    "color": '#ff1493',
                    "family": 'Tmon몬소리 Black'
                },

                "showarrow": False,
                "text": "감성지수",
                "x": 0.5,
                "y": 0.55
            },

        ]
    }
}
plotly.offline.plot(fig)
