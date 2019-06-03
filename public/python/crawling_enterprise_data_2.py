import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

URL = "https://finance.naver.com/item/sise.nhn?code=005930"

enterprise = requests.get(URL)
html = enterprise.text
soup = BeautifulSoup(html, 'html.parser')

# 현재가 시가 전일대비 등락률 거래량 시가총액 고가 저가 PER EPS
data1 = soup.select('#_nowVal')[0].text.replace('\n', '')
data1 = data1.replace('\t', '')

# 시가
data2 = soup.select('#_diff > span')[0].text.replace('\n', '')
data2 = data2.replace('\t', '')
# 전일대비
data3 = soup.select('#_rate > span')[0].text.replace('\n', '')
data3 = data3.replace('\t', '')
# 등락률
data4 = soup.select('#_rate > span')[0].text.replace('\n', '')
data4 = data4.replace('\t', '')
# 거래량
data5 = soup.select('#_quant')[0].text.replace('\n', '')
data5 = data5.replace('\t', '')

# 시가총액
data6 = soup.select('#_market_sum')[0].text.replace('\n', '')
data6 = data6.replace('\t', '')

# 고가
data7 = soup.select('#_high')[0].text.replace('\n', '')
data7 = data7.replace('\t', '')

# 저가
data8 = soup.select('#_low')[0].text.replace('\n', '')
data8 = data8.replace('\t', '')

# PER
data9 = soup.select('#_sise_per')[0].text.replace('\n', '')
data9 = data9.replace('\t', '')

# EPS
data10 = soup.select('#_sise_eps')[0].text.replace('\n', '')
data10 = data10.replace('\t', '')

file_data = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10]

if __name__ == '__main__':
    print(file_data)
