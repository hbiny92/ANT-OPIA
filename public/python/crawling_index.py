import sys
import requests
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding='utf-8')

# http get request
req = requests.get('https://finance.naver.com/sise/')
# html source / python str
html = req.text
# html source -> python
# html.parser -> (html source code , parser)
soup = BeautifulSoup(html, "html.parser")

kospi_index = soup.select('#KOSPI_now')
kospi_change = soup.select('#KOSPI_change')
kospi_state = soup.select('#KOSPI_change > span:nth-child(2)')

kosdaq_index = soup.select('#KOSDAQ_now')
kosdaq_change = soup.select('#KOSDAQ_change')
kosdaq_state = soup.select('#KOSDAQ_change > span:nth-child(2)')

kospi200_inex = soup.select('#KPI200_now')
kospi200_change = soup.select('#KPI200_change')
kospi200_state = soup.select('#KPI200_change > span:nth-child(2)')

file_data = [kospi_index[0].text, kospi_change[0].text.strip(), kospi_state[0].text,
             kosdaq_index[0].text, kosdaq_change[0].text.strip(), kosdaq_state[0].text,
             kospi200_inex[0].text, kospi200_change[0].text.strip(), kospi200_state[0].text
             ]



if __name__ == '__main__':
    print(file_data)

    # print(json.dumps(file_data, ensure_ascii=False, indent="\t"))
    # k_index 파일 생성
    # with open("json/k_index.json", 'w', encoding="utf-8") as make_file:
    #   json.dump(file_data, make_file, ensure_ascii=False, indent="\t")
