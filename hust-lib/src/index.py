#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-20 15:32:45
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import re
import requests
from bs4 import BeautifulSoup as Soup


headers = {
	'Host': 'ftp.lib.hust.edu.cn',
	'Referer': 'http://www.lib.hust.edu.cn/',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}

r = requests.get('http://ftp.lib.hust.edu.cn/search*chx/X?SEARCH=%E6%95%B0%E6%8D%AE%E5%BA%93', headers = headers)

soup = Soup(r.text, 'html5lib')

table = soup.find('table', {'calss', 'browseScreen'})

pages = table.find('tr', {'class', 'browsePager'})

last_page = pages.find_all('a')[-2]

link = last_page['href'] 
num = last_page.text
pre, suf = re.findall(r'(.*?SUBKEY=.*?)/\d+(%2C.*?/browse)', link)[0]
print(pre, suf)

# 'http://ftp.lib.hust.edu.cn' + pre + '/' page*50+1 + suf

books = table.find_all('td', {'class', 'briefCitRow'})

for x in books:
	title = x.find('span', {'class', 'briefcitTitle'}).a.text
	detail = x.find('span', {'class', 'briefcitDetail'}).text.replace('\n\n', '')
	print(title, detail)
	print('====')