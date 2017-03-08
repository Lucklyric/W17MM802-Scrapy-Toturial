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
