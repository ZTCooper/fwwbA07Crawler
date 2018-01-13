# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class A51jobSpider(CrawlSpider):
    name = '51job'
    allowed_domains = ['51job.com']
    start_urls = [
        'http://search.51job.com/jobsearch/search_result.php?fromJs=1&keyword=%E5%A4%A7%E6%95%B0%E6%8D%AE'
    ]

    rules = (
        # 主页面翻页
        Rule(LinkExtractor(allow=(
            'list/000000,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE,2,\d{1,}.html',)),
            follow=True,
        ),
        # 深入职位页面
        Rule(
            LinkExtractor(allow=('.html\?s=01&t=0',)),
            follow=False,
            callback='parse_item'
        ),
    )

    def parse_item(self, response):
        pass
