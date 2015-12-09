# -*- coding:utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

index_url = 'http://210.35.251.243/opac/ajax_top_lend_shelf.php'
response = requests.get(index_url)

# wtf = open('pyrequests.html','w+')
# wtf.write(response.content)
# wtf.close()

page = response.content
page = BeautifulSoup(page)
# print type(page)
# page = page.decode('utf-8')
# page = page.encode('gbk')
# print page
page = page.div.next_sibling.next_sibling
for spancontents in page.find_all('span'):
	print(spancontents.get_text())


