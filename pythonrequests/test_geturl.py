# -*- coding:utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

geturl="http://opac.ncu.edu.cn/opac/item.php?marc_no=0000431036"
newresponse = requests.get(geturl)
contents = newresponse.content
contents = BeautifulSoup(contents)
#happy = re.search('^ajax_douban.php?is(\w)+=(\d)+',contents）
newcontents = str(contents)
happy = re.search('ajax_douban.php(.*)[0-9]',newcontents)
print happy.group()