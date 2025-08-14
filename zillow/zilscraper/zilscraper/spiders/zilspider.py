import scrapy
import json
from datetime import datetime, timedelta
import os

class ZilspiderSpider(scrapy.Spider):
    name = "zilspider"
    custom_settings = {
        'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        'COOKIES_ENABLED': True,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
        },
        'DOWNLOAD_DELAY': 3,
        'RANDOMIZE_DOWNLOAD_DELAY': True
    }

    # url = "https://www.zillow.com/floral-park-ny/"
    urls_pool = [
        "https://www.zillow.com/floral-park-ny/",
        "https://www.zillow.com/mineola-ny/",
        "https://www.zillow.com/new-hyde-park-ny/",
        "https://www.zillow.com/franklin-square-ny/",
        "https://www.zillow.com/port-washington-ny/",
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

            # home_price = int(home_price_string.replace("$", "").replace(",", ""))
            home_price_str = home_price_string.replace("$", "").replace(",", "").strip().upper()

            try:
                if "K" in home_price_str:
                    home_price = int(float(home_price_str.replace("K", "")) * 1_000)
                elif "M" in home_price_str:
                    home_price = int(float(home_price_str.replace("M", "")) * 1_000_000)
                else:
                    home_price = int(home_price_str)
            except ValueError:
                continue  # skip invalid price formats like "—" or "Contact for price"


            if home_price > 1000000:
                continue
#  old zillow data structure for images
            # carousel = home.get('carouselPhotos', [])
            # image_urls = [photo.get('url') for photo in carousel if photo.get('url')]


            carousel = home.get('carouselPhotosComposable', {})
            base_url = carousel.get('baseUrl')
            photo_data = carousel.get('photoData', [])

            image_urls = []
            if base_url and photo_data:
                for photo in photo_data:
                    key = photo.get('photoKey')
                    if key:
                        image_urls.append(base_url.replace("{photoKey}", key))



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