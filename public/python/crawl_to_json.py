# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re
import sys
import json
# sys.stdout.reconfigure(encoding='utf-8')

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
네이버 뉴스 크롤링 딕셔너리  -> JSON 변환 코드
+ 정규표현식을 이용한 텍스트 전처리
+ 크롤링 인자는 v1~v5에서 처리
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# 각 크롤링 결과 저장하기 위한 리스트 선언
title_text = []
link_text = []
source_text = []
date_text = []
contents_text = []
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
        # print(date_text)

    except AttributeError:
        # 최근 뉴스
        # 이데일리  1시간 전  네이버뉴스   보내기
        pattern = '\w* (\d\w*)'  # 정규표현식

        r = re.compile(pattern)
        match = r.search(test).group(1)

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
            # print(date_text)

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

        # 빈도수, 명사 추출을위한 데이터프레임 설정
        # df_count = df[["title", "contents"]]
        # 제목, 언론사, 시간, 프리뷰, 링크 추출을위한 데이터프레임 설정
        df_count = df[["date", "title", "source", "contents", "link"]]
        page += 10
        df_count.iloc[: 0]
######################################################################################################
        news_full_list = []
        news_full_list.extend(title_text)
        news_full_list.extend(contents_text)

        # print(news_full_list)


        # Encoding -> PYTHON to JSON
        # def toJson(result):
        # with open('JSON_NEWS_DB.json', 'w', encoding='utf-8-sig') as file:
        #    json.dump(result, file, ensure_ascii=False, indent='\t')
print('##############  complete Python to JSON  #############')


def main(v1, v2, v3, v4, v5):
    maxpage = v1  # 크롤링 페이지 수
    query = v2  # 검색어 입력
    sort = v3  # 관련도순=0 , 최신순=1, 오래된순=2
    s_date = v4  # 시작 날짜 입력 20xx.xx.xx
    e_date = v5  # 끝날짜 입력 20yy.yy.yy
    crawler(maxpage, query, sort, s_date, e_date)


main("1", "삼성전자", "0", "2019.05.23", "2019.05.24")  # direct input 설정
