# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
import json
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



