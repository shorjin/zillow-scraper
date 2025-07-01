import scrapy
import json
from datetime import datetime, timedelta
import os
import re

class ZilsoldspiderSpider(scrapy.Spider):
    name = "zilsoldspider"

    # url = "https://www.zillow.com/floral-park-ny/sold/"
    urls_pool = [
        "https://www.zillow.com/floral-park-ny/sold/",
        "https://www.zillow.com/mineola-ny/sold/",
        # "https://www.zillow.com/new-hyde-park-ny/sold/",
        # "https://www.zillow.com/franklin-square-ny/sold/",
        # "https://www.zillow.com/port-washington-ny/sold/",
        # "https://www.zillow.com/glen-oaks-queens-new-york-ny/sold/",
        # "https://www.zillow.com/bellerose-queens-new-york-ny/sold/",
        # "https://www.zillow.com/woodhaven-queens-new-york-ny/sold/"

    ]



    def start_requests(self):
        for url in self.urls_pool:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):


        next_data_script = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

        # change to json format

        data = json.loads(next_data_script)

        homes = data['props']['pageProps']['searchPageState']['cat1']['searchResults']['listResults']

        for home in homes:


            timestamp_ms  = float(home['hdpData']['homeInfo'].get('dateSold', None))

            sold_date = datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d')



        # zillow data structure for price  is $775,000
            sold_price_string =home.get('soldPrice', None)
            if not sold_price_string:  # covers None and empty string
                continue  # skip or handle missing price

            sold_price_string = sold_price_string.strip().replace('$', '').replace(',', '')
            if 'M' in sold_price_string:
                sold_price= int(float(sold_price_string.replace('M', '')) * 1000000)

            else:
                sold_price= int(sold_price_string)


            home_type = home['hdpData']['homeInfo'].get('homeType', None)

            if home_type not in ['SINGLE_FAMILY', 'MULTI_FAMILY']:
                continue










            home_data = {
                "zpid": home.get('zpid', None),
                "home_address_sold_Page": home.get('address', None),
                "sold_price": sold_price,
                "sold_date": sold_date,
                "daysOnZillow_soldPage":home['hdpData']['homeInfo'].get('daysOnZillow', None),

            }

            yield home_data

        search_list = data['props']['pageProps']['searchPageState']['cat1'].get('searchList')

        if search_list and search_list.get('pagination'):
            next_page_url = search_list['pagination'].get('nextUrl', None)
            # Stop crawling more than 3 pages
            if next_page_url:
                match = re.search(r'/(\d+)_p/', next_page_url)
                if match:
                    next_page_num = int(match.group(1))
                    if next_page_num > 3:
                        return  # Stop crawling more than 3 pages
                next_page_full_url = 'https://www.zillow.com' + next_page_url
                yield scrapy.Request(url=next_page_full_url, callback=self.parse)