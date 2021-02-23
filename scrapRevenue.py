import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

BASE_URL = 'https://finance.naver.com'

def crawl(code):
	req = requests.get(BASE_URL + '/item/main.nhn?code='+code)
	page_soup = BeautifulSoup(req.text, 'lxml')
	finance_html = page_soup.select_one('div.cop_analysis')
	th_data = [item.get_text().strip() for item in finance_html.select('thead th')]

	annual_date = th_data[3:7] #['2018.12',~~~, 2019.12(E)]
	quarter_date = th_data[7:13] 

	finance_index = [item.get_text().strip() for item in finance_html.select('th.h_th2')][3:] #['주요재무정보','최근연간실적','최근분기실적',...]
	finance_data = [item.get_text().strip() for item in finance_html.select('td')]

	finance_data = np.array(finance_data)
	finance_data.resize(len(finance_index), 10)

	finance_date = annual_date + quarter_date
	finance = pd.DataFrame(data = finance_data[0:, 0:], index=finance_index, columns = finance_date)

	annual_finance = finance.iloc[:, :4]
	quarter_finance = finance.iloc[:, 4:]

	return finance, annual_finance, quarter_finance

finance, annual, quarter = crawl('005930')

print(annual.iloc[0]) # 매출액
print(annual.iloc[1]) # 영업이익
print(annual.iloc[2]) # 당기순이익
print(annual.iloc[5]) # ROE
print(annual.iloc[6]) # 부채비율
print(annual.iloc[8]) # 유보율

print(quarter.iloc[0]) # 매출액
print(quarter.iloc[1]) # 영업이익
print(quarter.iloc[2]) # 당기순이익
print(quarter.iloc[5]) # ROE
print(quarter.iloc[6]) # 부채비율
print(quarter.iloc[8]) # 유보율
