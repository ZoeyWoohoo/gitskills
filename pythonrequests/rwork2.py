# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

def know_more_about_it(what_you_want):
    #what_you_want = "百年孤独" #测试输入相应的书名，输出相应的信息
    what_you_want = what_you_want.decode('utf-8')
    for i in range(len(newpage)):
        if what_you_want==newpage[i]:
            geturl = newurl[i]
            geturl = "http://opac.ncu.edu.cn/opac/" + geturl #如果书名正确，得到相应的书籍详情链接地址
    newresponse = requests.get(geturl)
    contents = newresponse.content
    contents = BeautifulSoup(contents) #书籍详细内容bs解析后的源代码
    newcontents = str(contents)
    happy = re.search('ajax_douban.php(.*)[0-9]',newcontents) #正则抓取豆瓣简介链接地址
    dburl = happy.group()
    dburl = "http://opac.ncu.edu.cn/opac/" + dburl #完善地址名
    # print dburl
    for ul in contents.find_all('dl'):
	    main_new = ul.get_text()
	    print(main_new) #输出除豆瓣简介的其他详细内容

    dbjj = requests.get(dburl)
    dbjj = dbjj.content
    dbjq = str(dbjj) #豆瓣简介源码

    # print dbjj
    # print contents
    dbjq = re.search('\\\u(.*)\\\u\w\w\w\w',dbjq)
    dbjq = dbjq.group() #抓取出豆瓣简介正文内容
    # print type(dbjq)
    print dbjq.encode('utf-8')

index_url = 'http://210.35.251.243/opac/ajax_top_lend_shelf.php'
response = requests.get(index_url)
page = response.content
page = BeautifulSoup(page)
page = page.div.next_sibling.next_sibling
page = page.find_all('a')
#print type(page)
newpage = [x.get_text() for x in page] #抓取到的书名放入newpage列表
#print newpage
newurl = [url.get('href') for url in page] #抓取到每本图书的详情链接地址放入newurl列表
#print newurl
bookname = raw_input("Please input the name of the book you want:")
know_more_about_it(bookname.decode("cp936").encode("utf-8"))

