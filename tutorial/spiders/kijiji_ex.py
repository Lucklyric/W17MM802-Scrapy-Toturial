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
        # For each item
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@title="Next"]'))),
        # For nect page
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
