# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from bs4 import BeautifulSoup
from jobSpider.items import PositionItem


class A51jobSpider(CrawlSpider):
    name = '51job'
    allowed_domains = ['51job.com']
    start_urls = [
        'http://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    ]

    # 深入职位页面
    rules = (
        Rule(LinkExtractor(allow=(u'.html\?s=01&t=0',)),
             follow=False,
             callback='parse_item'
             ),
    )

    # 从初始页面找到下一页链接并发起request
    def parse_start_url(self, response):
        next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
        if next_page:
            yield scrapy.Request(url=next_page[0])

    # 解析职位信息页面
    def parse_item(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        if soup.select('.mt10 p + p'):
            keyword = soup.select(
                '.mt10 p + p')[0].get_text().replace('\n', ' ')
        else:
            keyword = None

        position_name = soup.select('h1')[0].get_text()
        position_salary = soup.select('h1 + span + strong')[0].get_text()

        position_describe = soup.select('h2 + div')[0].get_text()
        for word in ['\t', '\n', '\r', '职能类别：', '关键字：', '分享', '微信', '邮件']:
            position_describe = position_describe.replace(word, '')

        company_name = soup.select('.cname')[0].get_text().strip()
        company_location = soup.select('h1 + span')[0].get_text()
        company_type = soup.select('.i_house + p')[0].get_text().split()[0]
        company_size = soup.select('.i_house + p')[0].get_text().split()[2]
        company_describe = soup.select('.i_house + p')[0].get_text().split()[4]

        require_experience = soup.select('.sp4')[0].get_text()

        if soup.select('.sp4 .i2'):
            require_education = soup.select('.sp4')[1].get_text()
        else:
            require_education = None

        posItem = PositionItem(keyword=keyword,
                               position_name=position_name, position_salary=position_salary,
                               position_describe=position_describe,
                               company_name=company_name, company_location=company_location,
                               company_type=company_type, company_size=company_size,
                               company_describe=company_describe,
                               require_experience=require_experience, require_education=require_education)
        yield posItem
