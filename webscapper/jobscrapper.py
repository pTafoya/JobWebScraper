import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import xlwt
import re

url = "https://www.bloomberg.com/news/photo-essays/2011-05-17/50-top-employers-for-college-grads"
response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')

m_companies = html_soup.find_all('div', class_ = 'slideshow__title photo-essay__title')

book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet("Initial Company Listing")
count = 0;

for company in m_companies:
	cname = company.text.split(' ', 1)
	tmp_sub = cname[1].replace(" ","").lower()
	clean_name = re.sub('[^A-Za-z0-9]+', '', tmp_sub)
	curl_1 = "https://careers.{}.com/".format(clean_name)
	curl_2 = "http://www.{}.com/careers".format(clean_name)
	sheet1.write(count, 0, cname)
	sheet1.write(count, 1,curl_1)
	sheet1.write(count, 2, curl_2)
	count += 1
	
book.save("JobSearch.xls")