# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
import os

class ZillowImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # Get the zpid from the item (you must pass the item below for this to work)
        zpid = item.get('zpid', 'unknown_zpid')

        # Get image file name from the URL, zillow use checksum to name its image
        image_name = os.path.basename(urlparse(request.url).path)

        # Create path: zpid/image_name.jpg
        return f'{zpid}/{image_name}'