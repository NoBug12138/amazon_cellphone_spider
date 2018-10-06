# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import *


class AmazonPipeline(object):

    def open_spider(self, spider):
        client = MongoClient(host='127.0.0.1', port=27017)
        db = client.amazon
        self.items = db.items

    def process_item(self, item, spider):
        self.items.insert(dict(item))
        return item
