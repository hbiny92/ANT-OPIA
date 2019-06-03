import pandas
from collections import Counter
from konlpy.tag import Okt
import pandas as pd
from pandas import DataFrame, Series
import csv
import re

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
형태소/품사 및 빈도수 추출
+ REGEX로 형태소/품사 정제
+ CSV 저장
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def tag_nouns():
    f = open("C:/Users/User/Desktop/naver_news_crawling-master/NEWS_DATA.txt", "r")
    lines = f.read()
    nlpy = Okt()
    nouns = nlpy.nouns(lines)
    print(nouns)
    # print("\n---------------------------------")
    # print("     명사 총  {}개".format(len(tags)))
    # print("---------------------------------\n\n")


f = open("C:/Users/User/Desktop/naver_news_crawling-master/NEWS_DATA.txt",
         "r")  # txt저장 할 때 탭분리 .txt 형으로 저장
lines = f.read()
nlpy = Okt()
nouns = nlpy.nouns(lines)  # 명사 추출
# adj = nlpy.pos(lines, stem=True)  # 형용사 추출
count = Counter(nouns)  # 명사 카운팅
# count = Counter(adj)  # 형용사 카운팅
tag_count = []
tags = []

for n, c in count.most_common(2000):
    dics = {'tag': n, 'count': c}
    if len(dics['tag']) >= 1 and len(tags) <= 2000:
        tag_count.append(dics)
        tags.append(dics['tag'])
        # print(tags) #('단어','품사') 조합 출력


# for문 활용하여 그대로  CSV 파일쓰기

f_output = open('news_word.csv', 'w', newline='',
                encoding='utf-8-sig')  # 명사 저장
# f_output = open('news_adj.csv', 'w', newline='',encoding='utf-8-sig')  # 형용사 저장
csv_writer = csv.writer(f_output)
# csv_writer.writerow(['word', 'freq'])# 명사
csv_writer.writerow(['adj', 'freq'])  # 형용사

clean_adj = []

for tag in tag_count:
    tag_x = "{}".format(tag['tag'])  # 명사
    tag_y = "{}".format(tag['count'])
    # tag_x = " {}".format(tag['tag']) #형용사
    # tag_y = "{}".format(tag['count']) #형용사
    # print(tag_x)
    # tag_x_2 = re.sub('[(),-=.#/?:$}Adjective]', '', tag_x_1)
    csv_writer.writerow([tag_x, tag_y])

f_output.close()


""" for name in tags:
    for key in name:
        if key in ['Adjective']:
            for tag in tag_count:
                # tag_x = " {:<14}".format(tag['tag']) #명사
                # tag_y="{}".format(tag['count'])
                tag_x = " {}".format(tag['tag'])
                tag_y = "{}".format(tag['count'])
                csv_writer.writerow([tag_x, tag_y])

f_output.close() """
