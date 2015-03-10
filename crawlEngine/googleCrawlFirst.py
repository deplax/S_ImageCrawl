# -*- coding: utf-8 -*-
__author__ = 'Deplax'

import urllib2
import time
from scrapy import Selector

#processing start
start_time = int(round(time.time() * 1000))

print "Google Image Crawling --------------------------------------------------"

#검색 문자열을 받는다.
#중간에 띄어쓰기가 있을 경우 + 처리 필요
keyword = "tattoo+lion"

#받은 검색 문자열로 html덩어리를 가져온다.
url = "https://www.google.com/search?q=" + keyword + "&tbm=isch"
user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36"
request = urllib2.Request(url)
request.add_header("User-agent", user_agent)
source = urllib2.urlopen(request).read()

url_list = []

#html덩어리에서 이미지 원본 주소만 추출해 리스트로 넣는다.
def extract_url(source):
    global  url_list
    res = Selector(text=source)
    imgString = u'//div[@class="rg_di rg_el"]/a/@href'
    imgurls = res.xpath(imgString).extract()
    for i in range(0, len(imgurls) - 1):
        url_list.append(imgurls[i].split('?imgurl=')[1].split('&imgrefurl=')[0])

extract_url(source)

for i in range(0, len(url_list) - 1):
    print str(i) + " " + url_list[i]

#processing end
end_time = int(round(time.time() * 1000))
#print processing time
print str((end_time - start_time) / 1000.0) + " second"