#Scrapy Tutorial W17MM802
## Table of Contents
 * [Objective](#background)
 * [Introudction of Scrapy](#introduction-of-scrapy)
 * [Computing Science Faculty Example](#computing-science-faculty-example)
 * [Introduction of MongDB](#introduction-of-mongdb)
 * [Kijiji Example](#kijiji-example)

![alt text](https://github.com/Lucklyric/W17MM802-Scrapy-Tutorial/blob/master/Notes/images/scrapy.png)
## Objective
 The World Wide Web is a vast resources of Multimedia contents in varied formats. Crawling useful web pages and scraping the pages to trasform unstructured data to structured data (especially for multimeda content) into database become important and usefull. The extracted multimedia data could be used for further post processing and analysis. It can be treated as an early stage work to accelerate and benefits the Multimedia Data Mining Research, its outcome could be used for most of Multimedia Data Mining Project.

 **Web Crawling**: Crawl to the deepest and widest of the webpages.

 **Web Scraping**: Involves extrating and retrieving information from web.
 
## Introduction of Scrapy 
[Scrapy:](https://scrapy.org/)
 * "Scrapy is an application framework for crawling web sites and extracting structured data which can be used for a wide range of useful applications, like data mining, information processing or historical archival" 
 * [Twisted:](http://twistedmatrix.com/trac/) Python networking engine
 * [lxml:](http://lxml.de/) Python XML + HTML parser

###Installation
1. [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/)

 ```
 $ [sudo] pip install virtualenv # install the virtualenv
 ``` 

 ```
 $ virtualenv --no-site-packages [name e.g tutorial] # create virtualenv with completely separate and isolated Python environment
 ``` 

 ```
 $ source [virtualen name e.g tutorial]/bin/activate # activate the virtualenv
 ``` 

 ```
 (tutorial) $ deactivate # deactivate the virtualenv
 ``` 

2. [Scrapy](https://scrapy.readthedocs.io/en/latest/intro/install.html#installing-scrapy)
 ```
 $ pip install Scrapy
 ``` 

## Computing Science Faculty Example
###Creating a project
```
$ scrapy startproject [name e.g. tutorial]
```
The project content should have following contents:
```
tutorial/
    scrapy.cfg            # deploy configuration file

    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```

###First Spider for downloading a html page
```python
import scrapy

class CsSpider_ex1(scrapy.Spider):
    name = "cs_ex1"

    def start_requests(self):
        urls = [
            "https://www.ualberta.ca/computing-science/faculty-and-staff/faculty",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = "cs_faculty_Members_ex1.html"
        with open(filename,'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
```

###Run Spider
Go to the project's top level directory and run:
```
$ scrapy crawl [spider_name e.g. cs_ex1] 
```

###Extract Data
Using Scrapy shell for testing
```
$ scrapy shell [localfile or remote website e.g. ./cs_faculty_Members_ex1.html or https://www.ualberta.ca/computing-science/faculty-and-staff/faculty] 
```
Xpath: Scrapy selector [cheatsheet](http://ricostacruz.com/cheatsheets/xpath.html)
e.g
```
response.xpath(‘//tbody/tr’)[0].xpath(‘./td’)[0].xpath(‘./a/text()’)[0]
```

###Extract CS_Staff Data to Json

```python
import scrapy


class CsSpider_ex2(scrapy.Spider):
    name = "cs_ex2"

    def start_requests(self):
        urls = [
            "https://www.ualberta.ca/computing-science/faculty-and-staff/faculty",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for person in response.xpath('//tbody/tr'):
            person_item = {}
            rows = person.xpath('./td')
            first_row = rows[0].xpath('./a/text()').extract()
            person_item['name'] = first_row[0]
            person_item['position'] = first_row[1]
            person_item['department'] = rows[
                1].xpath('./text()').extract_first()
            area = rows[2].xpath('./text()').extract_first()
            person_item['area'] = area if area is not None else "N/A"
            phone = rows[3].xpath('./text()').extract_first()
            person_item['phone'] = phone if phone is not None else "N/A"
            person_item['email'] = rows[3].xpath('./a/text()').extract_first()
            yield person_item
```
Using CLI to output to JSON file
```
$ scrapy crawl cs_ex2 -o cs_staff.json # output to json file 
```

###Spider-Item-Pipeline structure
Define the item for cs_staff in items.py
```python
import scrapy

class CSStaff(scrapy.Item):
    name = scrapy.Field()
    position = scrapy.Field()
    department = scrapy.Field()
    area= scrapy.Field()
    phone= scrapy.Field()
    email= scrapy.Field()
```

Modify the spider file

```python
import scrapy
from tutorial.items import CSStaff

class CsSpider_ex3(scrapy.Spider):
    name = "cs_ex3"

    def start_requests(self):
        urls = [
            "https://www.ualberta.ca/computing-science/faculty-and-staff/faculty",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for person in response.xpath('//tbody/tr'):
            cs_staff_item = CSStaff()
            rows = person.xpath('./td')
            first_row = rows[0].xpath('./a/text()').extract()
            cs_staff_item['name']= first_row[0]
            cs_staff_item['position']= first_row[1]
            cs_staff_item['department']= rows[1].xpath('./text()').extract_first()
            area = rows[2].xpath('./text()').extract_first()
            cs_staff_item['area']= area if area is not None else "N/A"
            phone = rows[3].xpath('./text()').extract_first()
            cs_staff_item['phone'] = phone if phone is not None else "N/A"
            cs_staff_item['email'] = rows[3].xpath('./a/text()').extract_first()
            yield cs_staff_item
```

Define the pipeline in pipelines.py
```python
from scrapy import log
import json
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
```
Enable pipelines in setting.py
```python
ITEM_PIPELINES = {
   'tutorial.pipelines.CSStaffPipelineKijijiMongo': 100,#integer values is the determin the order in which they run from lower to higher
}

```
## Introduction of MongDB
Install MongoDB: [Link](https://docs.mongodb.com/master/tutorial/install-mongodb-on-ubuntu/?_ga=1.122977166.423304127.1488867109)

create a default db directory 
```
$ sudo mkdir /data/db
```

Start the MongoDB
```
sudo mongod --rest # --rest with html interface
```

CLI mongo Client
```
$ mongo
```

GUI mongoDB client:[robomongo](https://robomongo.org/)

Install pymongo
```
$ pip install pymongo
```

Add mongoDB configuration in settings.py
```python
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "w17mm802"
```

Add pipeplie for saving item to mongoDB
```python
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
```

## Kijiji Example
Get all laptop posts inforamtion from kijiji website:[link](http://www.kijiji.ca/b-laptops/edmonton/c773l1700203)

Define kijiji item in items.py
```python
class KijijiItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    date = scrapy.Field()
    brand = scrapy.Field()
```

Define spider with CrawlSpider
```python
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from tutorial.items import KijijiItem


class KijijiSpider_ex(CrawlSpider):
    name = "kijiji_ex"
    item_count = 0
    allowed_domain = ["www.kijiji.ca"]
    start_urls = ["http://www.kijiji.ca/b-laptops/edmonton/c773l1700203"]

    rules = {
        # For next page
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@title="Next"]'))),
        # For each item
        Rule(
            LinkExtractor(allow=(),
                          restrict_xpaths=(
                              '//div[@data-ad-id]//div[@class="title"]/a')
                          ),
            callback="parse_item",
            follow=False)
    }

    def parse_item(self, response):
        kijiji_item = KijijiItem()
        ad_info = response.xpath('//table[@class="ad-attributes"]//tr')
        kijiji_item["date"] = ad_info[0].xpath("./td/text()").extract_first()
        kijiji_item["price"] = ad_info[1].xpath(
            './/span[@itemprop="price"]/strong/text()').extract_first()
        kijiji_item["brand"] = ad_info.xpath(
            '//span[@itemprop="brand"]/text()').extract_first()
        kijiji_item["title"] = response.xpath(
            '//span[@itemprop="name"]/h1/text()').extract_first()
        self.item_count += 1
        if self.item_count > 1000:
                raise CloseSpider('item_exceeded')
        yield kijiji_item
```

Define a pipeline in pipelines.py
```python
class CSStaffPipelineKijijiMongo(object):
    mongo_collection_name = "kijiji_item"
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

```
_Dont't forget enable you pipeline in setting.py_
