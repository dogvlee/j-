# -*- coding: utf-8 -*-
import scrapy
import  re
from avtest.items import AvtestItem
class JavSpider(scrapy.Spider):
    name = 'jav'
    # allowed_domains = ['javlibrary.com/cn/']
    start_urls = ['http://www.javlibrary.com/cn/star_list.php?prefix=S']

    def parse(self, response):
        # starboxs=response.xpath("//div[@class='starbox']/div")

        # page_selector=response.xpath("//div[@class='page_selector']/a[last()]/@href").get()
        # number = re.search("(\d+)", page_selector)
        # last = int(number.group(1))
        #
        for x in range(42, 53):
            page = 'http://www.javlibrary.com/cn/star_list.php?prefix=S&page=' + str(x)  #修改字母
            yield scrapy.Request(url=page, callback=self.parse_star_list)


        # for starbox in starboxs:
        #     url=starbox.xpath(".//a/@href").get()
        #     star_url='http://www.javlibrary.com/cn/'+url
        #     yield scrapy.Request(url=star_url,callback=self.parse_star_url)


    def parse_star_list(self, response):#演员列表
        starboxs = response.xpath("//div[@class='starbox']/div")
        for starbox in starboxs:
            url = starbox.xpath(".//a/@href").get()
            star_url = 'http://www.javlibrary.com/cn/' + url
            yield scrapy.Request(url=star_url, callback=self.parse_star_url)


    def parse_star_url(self,response):  #解析演员界面
        name=response.xpath("//div[@class='boxtitle']/text()").get()
        videos=response.xpath("//div[@class='videos']//div[@class='video']/a")
        for video in videos:
            url=video.xpath(".//@href").get()
            url2=url.split("/")[-1]
            movie_url='http://www.javlibrary.com/cn/'+url2
            number=video.xpath(".//div[@class='id']/text()").get()
            title=video.xpath(".//div[@class='title']/text()").get()
            img=video.xpath(".//img/@src").get()
            img_url = re.sub('ps.jpg', 'pl.jpg', img)

            item=AvtestItem(movie_url=movie_url,number=number,title=title,img_url=img_url,name=name)
            yield item
        page_next = response.xpath("//a[@class='page next']/@href").get()
        if page_next: 
            yield scrapy.Request(url=response.urljoin(page_next),callback=self.parse_star_url)






        
