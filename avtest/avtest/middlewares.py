# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http.response.html import HtmlResponse
import time
import re
class AvtestSpiderMiddleware(object):
    def __init__(self):
        self.chrome_opt = webdriver.ChromeOptions()
        self.prefs = {'profile.managed_default_content_settings.images': 2}
        self.chrome_opt.add_experimental_option('prefs', self.prefs)
        self.driver = webdriver.Chrome(chrome_options=self.chrome_opt)
        self.i=0
    def process_request(self, request, spider):
        self.i=self.i+1
        # frist_url=re.match('^http://www.javlibrary.com/cn/star_list.php\?prefix=B',request.url)
        if  self.i==1:
            self.driver.get(request.url)
            time.sleep(5)
            showMore = self.driver.find_element_by_xpath("//input[@class='largebutton btnAdultAgree']")
            showMore.click()
            source = self.driver.page_source
            response = HtmlResponse(url=self.driver.current_url, body=source, request=request, encoding='utf-8')
            return response
        else:
            self.driver.get(request.url)
            source = self.driver.page_source
            response = HtmlResponse(url=self.driver.current_url, body=source, request=request, encoding='utf-8')
            return response
