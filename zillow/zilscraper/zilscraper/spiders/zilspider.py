import scrapy
import json
from datetime import datetime, timedelta

class ZilspiderSpider(scrapy.Spider):
    name = "zilspider"

    # url = "https://www.zillow.com/floral-park-ny/"
    urls_pool = [
        "https://www.zillow.com/floral-park-ny/",
        "https://www.zillow.com/mineola-ny/",
        "https://www.zillow.com/new-hyde-park-ny/",
        "https://www.zillow.com/franklin-square-ny/",
        "https://www.zillow.com/port-washington-ny/"
        "https://www.zillow.com/glen-oaks-queens-new-york-ny/",
        "https://www.zillow.com/bellerose-queens-new-york-ny/",
        "https://www.zillow.com/woodhaven-queens-new-york-ny/"

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
            days = home['hdpData']['homeInfo'].get('daysOnZillow', None)
            if days is not None:
                posted = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
            else:
                posted = 'N/A'

            home_type = home['hdpData']['homeInfo'].get('homeType', None)

            if home_type not in ['SINGLE_FAMILY', 'MULTI_FAMILY']:
                continue

        # zillow data structure for price  is $775,000
            home_price_string =home.get('price', None)
            if not home_price_string:  # covers None and empty string
                continue  # skip or handle missing price

            home_price = int(home_price_string.replace("$", "").replace(",", ""))


            if home_price > 1000000:
                continue

            carousel = home.get('carouselPhotos', [])
            image_urls = [photo.get('url') for photo in carousel if photo.get('url')]



            home_data = {
                "zpid": home.get('zpid', None),
                "home_type": home_type,
                "posted": posted,
                "daysOnMarket":home['hdpData']['homeInfo'].get('daysOnZillow', None),
                "home_URL": home.get('detailUrl', None),
                "home_main_image": home.get('imgSrc', None),
                "home_status": home.get('statusType', None),
                "home_price": home_price,
                "home_address": home.get('address', None),
                "home_zipcode": home.get('addressZipcode', None),
                "num_beds": home.get('beds', None),
                "num_baths": home.get('baths', None),
                "home_area": home.get('area', None),
                "land_area": home['hdpData']['homeInfo'].get('lotAreaValue', None),
                "image_urls": image_urls,

            }

            yield home_data

        search_list = data['props']['pageProps']['searchPageState']['cat1'].get('searchList')

        if search_list and search_list.get('pagination'):
            next_page_url = search_list['pagination'].get('nextUrl', None)
            if next_page_url:
                next_page_full_url = 'https://www.zillow.com/homes/' + next_page_url
                yield scrapy.Request(url=next_page_full_url, callback=self.parse)