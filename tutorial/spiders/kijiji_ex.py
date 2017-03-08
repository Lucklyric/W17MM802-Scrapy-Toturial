from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class KijijiSpider_ex(CrawlSpider):
    name = "kijiji_ex"
    allowed_domain = ["www.kijiji.ca"]
    start_urls = ["http://www.kijiji.ca/b-laptops/edmonton/c773l1700203"]

    rules = {
        # For each item
        Rule(LinkExtractor(allow=(), restrict_xpath=('//a[@titiel="Next"]')))
        # For nect page
        # Rule(LinkExtractor(allow=(),restrict_xpath=('')))
    }

    def parse_item(self, response):
        pass

