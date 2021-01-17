# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from DataScrapper.settings import IMAGES_STORE
import os

# basepath = os.path.dirname(__file__)
# filepath = os.path.join(basepath, "..", "Data/Scrapped")

class AstroPipeline:
    def process_item(self, item, spider):
        #print(ItemAdapter(item.key('img')))
        return item

class CustomImages(ImagesPipeline):


    # name information coming from the spider, in each item
    # add this information to Requests() for individual images downloads
    # through "meta" dictionary
    # def get_media_requests(self, item, info):
    #     print ("get_media_requests")
    #     return [Request(x, meta={'image_name': item["image_name"]})
    #             for x in item.get('image_urls', [])]
    # this is where the image is extracted from the HTTP response
    def get_media_requests(self, item, info):
        i = 1
        for image_url in item['image_urls']:
            site = item['site']
            product_name = item['product']
            filename = '{}_{}.jpg'.format(product_name, i)
            i += 1
            yield scrapy.Request(image_url, meta={'file_name': filename, 'site': site})


    def file_path(self, request, response=None, info=None, *, item=None):
        print("inside custom")
        folder = request.meta['site']
        img = request.meta['file_name']
        absolute = os.path.abspath(os.path.join('\\',IMAGES_STORE, f'{folder}', img))
        return absolute

    def item_completed(self, results, item, info):
        if self.IMAGES_RESULT_FIELD in item.fields:
            item[self.IMAGES_RESULT_FIELD] = [x for ok, x in results if ok]
        return item

    # def change_filename(self, key, response): << depreceated
    #     return "full/%s.jpg" % response.meta['image_name'][0]