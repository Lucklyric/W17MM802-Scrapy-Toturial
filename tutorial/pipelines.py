# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
import json
import pymongo

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class CSStaffPipelineEx3(object):
    def __init__(self):
        log.msg('CSStaffPipelineEx3 Init')

    def open_spider(self, spider):
        self.file = open('cs_staff_ex3.json','wb')

    def close_spider(self,spider):
        log.msg('clos spider')
        self.file.close()

    def process_item(self,item,spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        log.msg("add"+item,level=log.DEBUG,spider=spider)
        return item


class CSStaffPipelineEx3Mongo(object):
    mongo_collection_name = "cs_staff"
    def __init__(self,mongo_server,mongo_port,mongo_db):
        self.mongo_server = mongo_server
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

        log.msg('CSStaffPipelineEx3Mongo Init')

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_server= crawler.settings.get('MONGODB_SERVER'),
            mongo_port= crawler.settings.get('MONGODB_PORT'),
            mongo_db = crawler.settings.get("MONGODB_DB")
        )


    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_server,
                                          self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        log.msg('close spider')
        self.client.close()

    def process_item(self,item,spider):
        self.db[self.mongo_collection_name].insert(dict(item))
        log.msg("add"+item,level=log.DEBUG,spider=spider)
        return item


