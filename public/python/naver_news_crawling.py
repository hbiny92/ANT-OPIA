# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re
import sys
import csv
# sys.stdout.reconfigure(encoding='utf-8')

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Naver 뉴스 크롤링 Beautifulsoup 사용
+ 뉴스 제목/내용 크롤링 or 날짜/언론사/제목/뉴스내용
+ 날짜,내용요약은 REGEX로 정제 작업
+ CSV로 저장
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# 각 크롤링 결과 저장하기 위한 리스트 선언
title_text = []
link_text = []
source_text = []
date_text = []
contents_text = []
result = {}

# CSV 저장을 위한 경로
RESULT_PATH = 'C:/Users/User/Desktop/naver_news_crawling-master/'  # 결과 저장할 경로
now = datetime.now()  # 파일이름 현 시간으로 저장하기

# Date 정제


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


# Contents 정제
def contents_cleansing(contents):
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '',
                                      str(contents)).strip()  # 앞에 필요없는 부분 제거
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '',
                                       first_cleansing_contents).strip()  # 뒤에 필요없는 부분 제거 (새끼 기사)
    third_cleansing_contents = re.sub(
        '<.+?>', '', second_cleansing_contents).strip()
    contents_text.append(third_cleansing_contents)
    # print(contents_text)


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

        # Beautifulsoup 인자 설정
        soup = BeautifulSoup(html, 'html.parser')

        # <a>태그에서 제목, 링크주소 추출
        atags = soup.select('._sp_each_title')
        for atag in atags:
            title_text.append(atag.text)  # 제목
            link_text.append(atag['href'])  # 링크주소

        # 언론사 추출
        source_lists = soup.select('._sp_each_source')
        for source_list in source_lists:
            source_text.append(source_list.text)  # 신문사

        # 날짜 추출
        date_lists = soup.select('.txt_inline')
        for date_list in date_lists:
            test = date_list.text
            date_cleansing(test)  # 날짜 정제 함수사용
            # print(test)

        # 본문요약본
        contents_lists = soup.select('ul.type01 dl')
        for contents_list in contents_lists:
            # print('==='*40)
            # print(contents_list)
            contents_cleansing(contents_list)  # 본문요약 정제화

            # 모든 리스트 딕셔너리형태로 저장
        result = {"date": date_text, "title": title_text,
                  "source": source_text, "contents": contents_text, "link": link_text}
        print(page)

        df = pd.DataFrame(result)  # df로 변환
        page += 10

        # 빈도수, 명사 추출을위한 데이터프레임 설정
        df_count = df[["title", "contents"]]
        # 제목, 언론사, 시간, 프리뷰, 링크 추출을위한 데이터프레임 설정
        #df_count = df[["date", "title", "source", "contents", "link"]]
        page += 10
        df_count.iloc[: 0]

    # 새로 만들 파일이름 지정
    # 파일명 '%s-%s-%s  %s시 %s분 %s초 merging.csv'
    #outputFileName = "NEWS_DATA.csv"
    # header 없애고싶으면 header=False 옵션 추가
    # 반드시 쉼표구분 utf-8로 다른이름저장해주기  , 인코딩 utf-8-sig 로 넣기
    df_count.to_csv("NEWS_DATA.csv", index=False, sep=',',
                    encoding='utf-8-sig')

# def main():
#    info_main = input("="*50+"\n"+"입력 형식에 맞게 입력해주세요."+"\n" +
#                     " 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
#
#    maxpage = input("최대 크롤링할 페이지 수 입력하시오: ")
#    query = input("검색어 입력: ")
#    # 관련도순=0  최신순=1  오래된순=2
#    sort = input("뉴스 검색 방식 입력(관련도순=0  최신순=1  오래된순=2): ")
#    s_date = input("시작날짜 입력(20XX.XX.XX):")  # 2019.01.04
#    e_date = input("끝날짜 입력(20YY.YY.YY):")  # 2019.01.05

#    crawler(maxpage, query, sort, s_date, e_date)


# main()


def main(v1, v2, v3, v4, v5):
    maxpage = v1  # 크롤링 페이지 수
    query = v2  # 검색어 입력
    sort = v3  # 관련도순=0 , 최신순=1, 오래된순=2
    s_date = v4  # 시작 날짜 입력 20xx.xx.xx
    e_date = v5  # 끝날짜 입력 20yy.yy.yy
    crawler(maxpage, query, sort, s_date, e_date)


main("1300", "삼성전자", "0", "2019.05.20", "2019.06.02")  # direct input 설정
