# Zillow Property Scraper

This Scrapy project crawls Zillow listings for specified locations and extracts detailed property data. It filters homes by type and price.
## Features

    Scrapes multiple Zillow neighborhood URLs

    Filters homes by type (SINGLE_FAMILY and MULTI_FAMILY) and price (< $1,000,000)

    Extracts home details such as price, address, beds, baths, days on market, and more


## Usage
Run the spider and save output to JSON:

    scrapy crawl zilspider -O output.json


## Notes
- This project is for educational purposes only.
- Zillow’s website structure may change, which could break the scraper. Use responsibly.
