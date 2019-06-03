import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sys
from pandas import DataFrame

sys.stdout.reconfigure(encoding='utf-8')

URL = "https://finance.naver.com/item/main.nhn?code=005930"

enterprise = requests.get(URL)
html = enterprise.text
soup = BeautifulSoup(html, 'html.parser')
finance_html = soup.select('div.section.cop_analysis div.sub_section')[0]

th_data = [item.get_text().strip() for item in finance_html.select('thead th')]
annual_date = th_data[3:7]
quarter_date = th_data[7:13]

finance_index = [item.get_text().strip() for item in finance_html.select('th.h_th2')][3:]
#실제데이터
finance_data = [item.get_text().strip() for item in finance_html.select('td')]

#5x4형태
#18.06 데이터
data11 = finance_data[5]
data12 = finance_data[15]
data13 = finance_data[25]
data14 = finance_data[35]

#18.09 데이터
data21 = finance_data[6]
data22 = finance_data[16]
data23 = finance_data[26]
data24 = finance_data[36]

#18.12 데이터
data31 = finance_data[7]
data32 = finance_data[17]
data33 = finance_data[27]
data34 = finance_data[37]

#19.03 데이터
data41 = finance_data[8]
data42 = finance_data[18]
data43 = finance_data[28]
data44 = finance_data[38]

#19.06 데이터
data51 = finance_data[9]
data52 = finance_data[19]
data53 = finance_data[29]
data54 = finance_data[39]

file_data = [data11, data12, data13, data14, data21, data22, data23, data24, data31, data32, data33, data34,
             data41, data42, data43, data44, data51, data52, data53, data54]



if __name__ == '__main__':
    print(file_data)







