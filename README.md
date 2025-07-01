# Zillow Property Scraper

This Scrapy project crawls Zillow listings for specified locations and extracts detailed property data. It filters homes by type and price.

## Project Purpose:

This project scrapes Zillow listings data to track housing market dynamics in near real-time. Since Zillow removes listings shortly after a house is sold, continuously collecting this data enables us to monitor price changes, time on market, and availability trends.
By analyzing this up-to-date and historical listing information, we can gain valuable insights into the short-term behavior of the housing market. This helps me to make informed, data-driven decisions when making offers.
## Features

    Scrapes multiple Zillow neighborhood URLs

    Filters homes by type (SINGLE_FAMILY and MULTI_FAMILY) and price (< $1,000,000)

    Extracts home details such as price, address, beds, baths, days on market, and more

    Downloads all carousel images for each property using Scrapy's ImagesPipeline

    Saves images organized by Zillow Property ID (zpid)

    Scrapes house sold data using a separate spider (zilsoldspider)

## Pipelines

- `ZillowImagesPipeline:` Saves images by zpid

- `AppendJsonPipeline:` Adds only new records to output.json (for zilspider only)

## Spiders
- `zilspider:` Scrapes active home listings (e.g., address, price, images)
- `zilsoldspider:`Scrapes recently sold home data (e.g., sold price, date sold, and listing duration)


## Usage
Scrape current listings:

    scrapy crawl zilspider

Scrape sold home data and export it to a JSON file:

    scrapy crawl zilsoldspider -O sold_homes.json


## Notes
- This project is for educational purposes only.
- Zillow’s website structure may change, which could break the scraper. Use responsibly.


