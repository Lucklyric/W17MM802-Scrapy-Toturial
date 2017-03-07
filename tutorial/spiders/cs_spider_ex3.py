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
