import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sys

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
finance_data = [item.get_text().strip() for item in finance_html.select('td')]

finance_data = np.array(finance_data)
finance_data.resize(len(finance_index), 10)

finance_date = annual_date + quarter_date
finance = pd.DataFrame(data=finance_data[0:, 0:], index=finance_index, columns=finance_date)

#연간 / 분기간

annual_finance = finance.iloc[:, :4]
quarter_finance = finance.iloc[:, 4:]


if __name__ == '__main__':
    print(annual_finance)






