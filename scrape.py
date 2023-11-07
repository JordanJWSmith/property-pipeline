import json
import logging
import argparse
from webscraper import Webscraper

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def main():

    parser = argparse.ArgumentParser(description='Web Scraper Script')
    parser.add_argument('-num_pages', type=int, default=None, help='Number of pages to scrape per location (24 listings per page)')
    parser.add_argument('--test', action='store_true', help='Set to true to run in test mode')
    parser.add_argument('--mongo', action='store_true', help='Save results in mongoDB (assumes .env file)')
    args = parser.parse_args()

    
    user_agent = 'Mozilla/5.0 (Linux; Android 10; SM-A205U) ' \
                    'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                    'Chrome/106.0.5249.126 Mobile Safari/537.36'
    
    if args.test:
        logging.info("Running in test mode. Scraping 1 page from Wandsworth.")
        num_pages = 1
        location_codes = {'wandsworth': "5E93977"}

    else:
        if args.num_pages is None:
            parser.error("value for -num_pages is required, e.g. `python3 scrape.py -num_pages 10`")

        with open('location_codes.json', 'r') as f:
            location_codes = json.load(f)
        
        num_pages = args.num_pages  # Number of pages to scrape per location (24 properties per page)
        
    mongo = args.mongo

    TestClass = Webscraper(user_agent, location_codes, num_pages, mongo)
    TestClass.scrape()


if __name__ == "__main__":
    main()
