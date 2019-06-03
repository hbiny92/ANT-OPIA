# -*- coding: utf-8 -*-
import pandas as pd
import re
from pandas import read_csv, concat
from ast import literal_eval
import csv


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
1. 크롤링한 csv 로드 후 , 데이터 형태소/품사 전처리
2. 명사용 / 형용사용 전처리를 위한 코드 분류 + REGEX로 정제
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def only_adj():
    adj_list = []
    f = open('news_word.csv', 'r')  # 파일명 명사용 or 형용사용으로 변경
    rdr = csv.reader(f)
    for line in rdr:
        adj_list.append(line[0])
    f.close()

    only_adj = []
    for A in adj_list:
        x = re.sub(
            '[a-zA-Z-=0-9+,''#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', A).strip()
        only_adj.append(x)
    only_adj.remove('')
    print(only_adj)

    # frequency list 저장
    freq_list = []
    f = open('news_adj.csv', 'r')
    rdr = csv.reader(f)
    for line in rdr:
        freq_list.append(line[1])
    f.close()

    only_freq = []
    for B in freq_list:
        y = re.sub(
            '[a-zA-Z-=+,''#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', B).strip()
        only_freq.append(y)
    only_freq.remove('')
    print(only_freq)

    # Data frame 지정
    adj_df = pd.DataFrame({"adj": only_adj,
                           "freq": only_freq})
    print(adj_df)

    # DataFrame csv로 저장하기
    # 반드시 쉼표 utf-8로 저장하기 , 형용사용 아웃풋
    adj_df.to_csv("only_adj_text.csv", index=False, sep=',',
                  encoding='utf-8-sig')  # utf-8-sig 로 넣기
    return 0


''' def only_noun():
    #adj_list = []
    f = open('news_adj.csv', 'r')  # 파일명 명사용 or 형용사용으로 변경
    rdr = csv.reader(f)
    for line in rdr:
        adj_list.append(line[0])
    f.close()

    #only_adj = []
    for A in adj_list:
        x = re.sub(
            '[a-zA-Z-=0-9+,''#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', A).strip()
        only_adj.append(x)
    only_adj.remove('')
    print(only_adj)

    # frequency list 저장
    freq_list = []
    f = open('news_adj.csv', 'r')
    rdr = csv.reader(f)
    for line in rdr:
        freq_list.append(line[1])
    f.close()

    only_freq = []
    for B in freq_list:
        y = re.sub(
            '[a-zA-Z-=+,''#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', B).strip()
        only_freq.append(y)
    only_freq.remove('')
    print(only_freq)

    # Data frame 지정
    adj_df = pd.DataFrame({"adj": only_adj,
                           "freq": only_freq})

    print(adj_df)


# 명사용 아웃풋
adj_df.to_csv("only_word_text.csv", index=False, sep=',',
              encoding='utf-8-sig')  # utf-8-sig 로 넣기 '''

only_adj()
