# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

keyword = u"아이유"

driver = webdriver.Chrome(executable_path="C:\Users\Administrator\PycharmProjects\pyTest\chromedriver.exe")
driver.get("http://www.google.com")
serchbox = driver.find_element_by_id("lst-ib")
serchbox.send_keys(keyword, Keys.ENTER)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="hdtb-msb"]/div[2]/a')))
driver.find_element_by_xpath('//*[@id="hdtb-msb"]/div[2]/a').click()

try:
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable, '//*[@id="smb"]')
except:
    driver.find_element_by_name("mngb").send_keys(Keys.END)

flag = 1
stack = 1
while flag:
    try:
        more = driver.find_element_by_xpath('//*[@id="smb"]')
        more.click()
        stack = 0
    except:
        driver.execute_script("window.scrollTo(30, document.body.scrollHeight);")
        stack = stack + 1
        if stack == 300:
            flag = 0


txt = unicode(driver.page_source)

print "Exit"

with open("all.html", 'wb') as f:
    f.write(txt)

driver.close()

#================================================================================================================

# # -*- coding: utf-8 -*-
# __author__ = 'Administrator'
#
import urllib2
import sys
import os
from scrapy import Selector

print "Google Image Crawling --------------------------------------------------"

#html덩어리에서 이미지 원본 주소만 추출해 리스트로 넣는다.
res = Selector(text=txt)
titleString = u'//div/a/img/@name'
# u'//*[@id="rg_s"]/div/a/@href'
imgString = u'//*[@id="rg_s"]/div/a/@href'
title = res.xpath(titleString).extract()
imgurls = res.xpath(imgString).extract()

print imgurls

#저장할 곳을 만든다.
#한글문제 처리

if not os.path.isdir(keyword):
    os.mkdir(unicode(keyword))

print "count" + str(len(title))

#리스트를 순회하면서 파일을 저장한다.
for i in range(0, len(title) - 1):
    imgurltrim = imgurls[i].split('?imgurl=')[1].split('&imgrefurl=')[0]
    print str(i) + ' : ' + imgurltrim

    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    try:
        req = urllib2.Request(imgurltrim, headers=hdr)
        imgurl = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()
    except:
        print "??"

    if imgurltrim[-1: -5].find('.') == -1:
        imgurltrim = imgurltrim + ".jpg"
    filename = title[i][0:-1] + '.' + imgurltrim.split('.')[-1]
    if filename.find('/') != -1:
        filename = filename.split('/')[0]
    print filename

    text = imgurl.read()
    if text:
        output = open("./" + keyword + "/" + str(i) + "." + filename, 'wb')
        output.write(text)
        output.close()

#저장한 갯수와 통계를 보여주고 종료한다.