# Zillow Property Scraper

A Scrapy-based project to scrape Zillow real estate data for multiple neighborhoods, including both active listings and sold home details. It also downloads property images and merges data for comprehensive analysis.

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

    Supports incremental JSON output with a custom pipeline that appends new records to existing JSON files without duplication

    Provides utilities for cleaning, merging, and analyzing scraped data using pandas, including handling missing values and date conversions

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


