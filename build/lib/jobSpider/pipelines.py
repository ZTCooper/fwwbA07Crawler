# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import pymysql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class A51jobspiderPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    # get info from settings.py
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings.get('MYSQL_HOST'),
            port=settings.get('MYSQL_PORT'),
            user=settings.get('MYSQL_USER'),
            passwd=settings.get('MYSQL_PASSWD'),
            db=settings.get('MYSQL_DBNAME'),
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    # called when spider starts
    def open_spider(self, spider):
        pass

    # called when spider closes
    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item['position_name'] and item['position_salary']:
            query = self.dbpool.runInteraction(self.insert_into_db, item)
            return item
        else:
            raise DropItem('Missing item in %s' % item)
    # without item['post_time'],  add it if need
    def insert_into_db(self, cur, item):
        sql = 'insert into 51job(position_name, keyword, position_salary, position_describe, company_name, company_location, company_type, company_size, company_describe, require_experience, require_education) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        params = (item['position_name'], item['keyword'], item['position_salary'], item['position_describe'], item['company_name'], item['company_location'],
                  item['company_type'], item['company_size'], item['company_describe'], item['require_experience'], item['require_education'])
        cur.execute(sql, params)
