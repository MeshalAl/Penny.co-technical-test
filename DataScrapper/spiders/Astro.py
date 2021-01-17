import scrapy
from scrapy_selenium import SeleniumRequest
import w3lib.html as w3
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from DataScrapper.items import AstroItem
import re

class AstroSpider(scrapy.Spider):
    name = 'Astro'
    url = []
    count = 1
    def __init__(self, **kwargs):
        super(AstroSpider, self).__init__(**kwargs)
        self.url = kwargs.get('url')  # # gets a list of urls supplied by main

    def start_requests(self):  # creates request object per url, sends it to engine

        for url in self.url:
            try:
                yield SeleniumRequest(url=url, wait_time=5, wait_until=EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/main/div[3]/div/div[2]/div/div[2]/div[2]/div[1]/div[3]/div/img'
                     )
                ), dont_filter=True, callback=self.parseinfo, errback=self.parseerr)
            except:
                print(str(Exception))

    def parseinfo(self, response, **kwargs):  # parsing logic
        item = AstroItem()
        item['site'] = 'Astro'
        item['url'] = response.request.url
        product_name = item['url']
        item['product'] = re.search('.*/(.+?).html', product_name).group(1)
        x = response.xpath('/html/body/div/main/div[3]/div/div[1]/div[1]/div/div[2]/div/div[4]/div/div').get()
        cleaned = w3.remove_tags(x)
        further = re.sub("\'\s*", '', cleaned)
        ready = re.sub("\\n", '|', further)
        spec = ready.split('|')
        item['spec'] = spec
        item['image_urls'] = response.xpath('/html/body/div[1]/main/div[3]/div/div[2]/div/div[2]/div[2]/div[1]/div[3]/div/img/@src').extract()
        item['counter'] = self.count
        self.count += 1

        # loader = ItemLoader(item=item, selector=i)
        # for i in item['image_urls']:
        #     item.['image'].append

        yield item

    def parseerr(self, response, **kwargs):
        item = AstroItem()
        item['site'] = 'Astro'
        item['url'] = ''
        item['product'] = ''
        item['spec'] = ''
        item['image_urls'] = ''
        item['counter'] = self.count
        self.count += 1
        yield item

