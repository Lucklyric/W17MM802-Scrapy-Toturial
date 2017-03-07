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

