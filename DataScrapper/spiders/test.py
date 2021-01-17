import scrapy
from scrapy_selenium import SeleniumRequest as sr
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from scrapy.crawler import CrawlerProcess


class Spider(scrapy.Spider):

    name = "test"
    url = []

    def start_requests(self):  # creates request object per url, sends it to engine
        for url in self.url:
            try:
                yield sr(url=url, wait_time=30, wait_until = EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/main/div[3]/div/div[2]/div/div[2]/div[2]/div[1]/div[3]/div/img')
                ), dont_filter=True, callback=self.parse)
            except:
                print(str(Exception))

    def parse(self, response, **kwargs):  # parsing logic, received from downloader via engine
        spec = response.xpath('/html/body/div/main/div[3]/div/div[1]/div[1]/div/div[2]/div/div[4]/div/div').get()
        imagepath = response.xpath('/html/body/div[1]/main/div[3]/div/div[2]/div/div[2]/div[2]/div[1]/div[3]/div/img')
        for i in imagepath:
            image = i.xpath('@src').extract_first()
            print(image)
        for i in range(10):
            print('\n')
        print(spec)
        print(image)

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl('test', url=['https://www.astrotools.com/1-heavy-duty-air-impact-wrench-with-2-anvil.html'])
    process.start()



