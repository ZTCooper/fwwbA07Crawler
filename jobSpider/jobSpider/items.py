# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PositionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    position_name = scrapy.Field()
    position_salary = scrapy.Field()
    position_descibe = scrapy.Field()


class CompanyItem(scrapy.Item):
    company_name = scrapy.Field()
    company_location = scrapy.Field()
    company_type = scrapy.Field()
    company_size = scrapy.Field()
    company_describe = scrapy.Field()


class RequireItem(scrapy.Item):
    aquire_experience = scrapy.Field()
    aquire_education = scrapy.Field()
