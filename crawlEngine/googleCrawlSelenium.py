# -*- coding: utf-8 -*-
__author__ = 'Deplax'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import time
from scrapy import Selector

#processing start
start_time = int(round(time.time() * 1000))

#한글을 처리해요
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#main logic
keyword = u"아이유"
url = u"https://www.google.co.kr/imghp"
#url = u"https://www.google.co.kr/search?q=" + keyword + u"&tbm=isch"

user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)
referer = {
    "referer" : "https://www.google.co.kr/"
}

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = user_agent
dcap["phantomjs.page.customHeaders"] = referer
#phantomjs_path = u"D:/Download/phantomjs-2.0.0-windows/bin/phantomjs.exe"
phantomjs_path = u"/Users/Deplax/project/Crawl/ImageCrawling/Selenium/phantomjs-2.0.0-macosx/bin/phantomjs"
driver = webdriver.PhantomJS(executable_path=phantomjs_path, desired_capabilities=dcap)
driver.set_window_size(1920, 1080)

driver.get(url)
search_box = driver.find_element_by_id("lst-ib")
search_box.send_keys(keyword, Keys.ENTER)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'hdtb_tls')))

url_list = []
#-------------------------------------------------
def make_request_xhr(string):
    xhr_url = string.split('url=')[1].split('" http-equiv=')[0]
    xhr_url = xhr_url.replace(u"&amp;", u"&")
    xhr_url = xhr_url.replace(u"sei=", u"ei=")
    return xhr_url

def extract_xhr(source):
    res = Selector(text=source)
    xhr_string = '//*[@id="gsr"]/noscript[2]/text()'
    xhr = res.xpath(xhr_string).extract()
    xhr = make_request_xhr(xhr[0])
    return xhr

def extract_url(source):
    global  url_list
    res = Selector(text=source)
    imgString = u'//div[@class="rg_di rg_el"]/a/@href'
    imgurls = res.xpath(imgString).extract()
    for i in range(0, len(imgurls) - 1):
        url_list.append(imgurls[i].split('?imgurl=')[1].split('&imgrefurl=')[0])

page_source = driver.page_source

def extract_append_url(source):
    xhr = extract_xhr(source)
    html = ""
    for i in range(1, 10):
        append_image = "https://www.google.co.kr" + xhr + u"&ijn=" + str(i) + u"&start=" + str(i * 100)
        response = requests.get(append_image)
        html = html + response.text
        print html
    extract_url(html)

extract_url(page_source)
extract_append_url(page_source)

for i in range(0, len(url_list) - 1):
    print str(i) + ':' + url_list[i]

driver.close()

#processing end
end_time = int(round(time.time() * 1000))
#print processing time
print str((end_time - start_time) / 1000.0) + " second"
