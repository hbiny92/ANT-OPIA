import requests
from bs4 import BeautifulSoup
import datetime
import traceback
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib import style

path_dir = '../stock/python'
if not os.path.exists(path_dir):
    os.makedirs(path_dir)
path = os.path.join(path_dir, 'graph_data.csv')

date_from = datetime.datetime.strftime(datetime.datetime(year=2019, month=1, day=1), '%Y.%m.%d')
date_to = datetime.datetime.strftime(datetime.datetime.today(), '%Y.%m.%d')

code = '005930'
url = 'https://finance.naver.com/item/sise.nhn?code={code}'.format(code=code)
res = requests.get(url)
res.encoding = 'utf-8'
res.status_code


def parse_page(code, page):
    try:
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'.format(code=code, page=page)
        res = requests.get(url)
        _soap = BeautifulSoup(res.text, 'lxml')
        _df = pd.read_html(str(_soap.find("table")), header=0)[0]
        _df = _df.dropna()
        return _df
    except Exception as e:
        traceback.print_exc()
    return None


df = None
for page in range(1, 10):

    _df = parse_page(code, page)
    _df_filtered = _df[_df['날짜'] > date_from]

    if df is None:
        df = _df_filtered
    else:
        df = pd.concat([df, _df_filtered])
    if len(_df) > len(_df_filtered):
        break

if __name__ == '__main__':
    df.to_csv(path, index=False)
