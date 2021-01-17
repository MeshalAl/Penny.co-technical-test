import scrapy
import scrapy_selenium


class Spider(scrapy.Spider):

    name = "Knipex"
    allowed_domains = []

    def __init__(self, **kwargs):
        super(Spider, self).__init__(**kwargs)

        self.url = kwargs.get(
            'url')  # or kwargs.get('domain')  # gets a list of urls supplied by main todo fix abiguation by supplying domain from main

        if 'idx' in kwargs:
            self.idx = kwargs.get('idx')

        # todo rest of logic and handling

    def start_requests(self):  # creates request object per url, sends it to engine
        for url in self.url:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):  # parsing logic, received from downloader via engine
        page = response.url
        file = 'test.txt'
        with open(file, 'wb') as f:
            f.write(response.body)



