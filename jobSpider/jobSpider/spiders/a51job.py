# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class A51jobSpider(CrawlSpider):
    name = '51job'
    allowed_domains = ['51job.com']
    start_urls = [
        'http://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    ]

    rules = (
        Rule(LinkExtractor(allow=(u'.html\?s=01&t=0',)),
             follow=False,
             callback='parse_item'
             ),
    )

    def parse_start_url(self, response):
        next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
        if next_page:
            yield scrapy.Request(url=next_page[0])

    def parse_item(self, response):
        pass
