import sys
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

# http get request
req = requests.get('https://finance.naver.com/marketindex/')
# html source / python str
html = req.text
# html source -> python
# html.parser -> (html source code , parser)
soup = BeautifulSoup(html, "html.parser")

dollar = soup.select('.usd > div:nth-child(2) > span:nth-child(1)')
dollar_change = soup.select('.usd > div:nth-child(2) > span:nth-child(3)')
dollar_state = soup.select('.usd > div:nth-child(2) > span:nth-child(4)')

jpy = soup.select('.jpy > div:nth-child(2) > span:nth-child(1)')
jpy_change = soup.select('.jpy > div:nth-child(2) > span:nth-child(3)')
jpy_state = soup.select('.jpy > div:nth-child(2) > span:nth-child(4)')

euro = soup.select('.eur > div:nth-child(2) > span:nth-child(1)')
euro_change = soup.select('.eur > div:nth-child(2) > span:nth-child(3)')
euro_state = soup.select('.eur > div:nth-child(2) > span:nth-child(4)')

file_data = [dollar[0].text, dollar_change[0].text, dollar_state[0].text,
             jpy[0].text, jpy_change[0].text, jpy_state[0].text,
             euro[0].text, euro_change[0].text, euro_state[0].text,
             ]

if __name__ == '__main__':
    print(file_data)
