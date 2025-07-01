# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
import os
import json

class ZillowImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if info.spider.name != 'zilspider':
            return []  # Don't download images for other spiders
        return super().get_media_requests(item, info)


    def file_path(self, request, response=None, info=None, *, item=None):
        # Get the zpid from the item (you must pass the item below for this to work)

        zpid = item.get('zpid', 'unknown_zpid')

        # Get image file name from the URL, zillow use checksum to name its image
        image_name = os.path.basename(urlparse(request.url).path)

        # Create path: zpid/image_name.jpg
        return f'{zpid}/{image_name}'



class AppendJsonPipeline:
    def open_spider(self, spider):
        self.file_path = 'output.json'
        self.existing_data = []
        self.new_records_count = 0  # Track new records added

        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                try:
                    self.existing_data = json.load(f)
                except json.JSONDecodeError:
                    self.existing_data = []

        self.existing_zpids = {str(item.get('zpid')) for item in self.existing_data if item.get('zpid')}

    def process_item(self, item, spider):
        if 'images' in item:
            item.pop('images')
        if spider.name != 'zilspider':
            return item
        zpid = item.get('zpid')
        if zpid is None:
            return item
        zpid = str(zpid)
        if zpid not in self.existing_zpids:
            self.existing_data.append(dict(item))
            self.existing_zpids.add(zpid)
            self.new_records_count += 1  # Increment counter for new record
        return item

    def close_spider(self, spider):
        if spider.name != 'zilspider':
            return
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.existing_data, f, ensure_ascii=False, indent=2)

        print(f"[AppendJsonPipeline] Added {self.new_records_count} new record(s) to {self.file_path}")
        print(f"[AppendJsonPipeline] Total records in {self.file_path}: {len(self.existing_data)}")



