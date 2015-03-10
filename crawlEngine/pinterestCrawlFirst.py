# -*- coding: utf-8 -*-
__author__ = 'Deplax'

import urllib2
import time
import threading
from scrapy import Selector

#processing start
start_time = int(round(time.time() * 1000))

print "Pinterest Image Crawling --------------------------------------------------"

#검색 문자열을 받는다.
#중간에 띄어쓰기가 있을 경우 + 처리 필요
keyword = "tattoo+lion"

#받은 검색 문자열로 html덩어리를 가져온다.
url = "https://www.pinterest.com/search/pins/?q=" + keyword
user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36"
request = urllib2.Request(url)
request.add_header("User-agent", user_agent)
source = urllib2.urlopen(request).read()

url_list = []
img_url_list = []

#html덩어리에서 이미지 원본 주소만 추출해 리스트로 넣는다.
def extract_url(source):
    global  url_list
    res = Selector(text=source)
    imgString = u'//a[@class="pinImageWrapper"]/@href'
    imgurls = res.xpath(imgString).extract()
    for i in range(0, len(imgurls) - 1):
        url_list.append(imgurls[i])

extract_url(source)

def extract_img_url(source):
    global  img_url_list
    res = Selector(text=source)
    imgString = u'//img[@class="pinImage"]/@src'
    imgurls = res.xpath(imgString).extract()
    img_url_list.append(imgurls[0])

# def visit_page(url):
#     img_url = "https://www.pinterest.com/"
#     img_url = img_url + url
#     request = urllib2.Request(img_url)
#     try:
#         source = urllib2.urlopen(request).read()
#         extract_img_url(source)
#     except:
#         print "miss!!"

class visit_page(threading.Thread):

    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        img_url = "https://www.pinterest.com/"
        img_url = img_url + self.url
        request = urllib2.Request(img_url)
        try:
            source = urllib2.urlopen(request).read()
            extract_img_url(source)
        except:
            print "miss!!"

threads = []

def visit_pages(url_list):
    for i in range(0, len(url_list) - 1):
        thread = visit_page(url_list[i])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

visit_pages(url_list)

for i in range(0, len(img_url_list) - 1):
     print str(i) + " " + img_url_list[i]

#processing end
end_time = int(round(time.time() * 1000))
#print processing time
print str((end_time - start_time) / 1000.0) + " second"