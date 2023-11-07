import json
import logging
from webscraper import Webscraper

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def main():
    
    user_agent = 'Mozilla/5.0 (Linux; Android 10; SM-A205U) ' \
                    'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                    'Chrome/106.0.5249.126 Mobile Safari/537.36'

    with open('location_codes.json', 'r') as f:
        location_codes = json.load(f)
    
    # num_pages = 999 // 24  # Number of pages to scrape per location (24 properties per page)

    # test settings
    num_pages = 1
    location_codes = {'wandsworth': "5E93977"}

    TestClass = Webscraper(user_agent, location_codes, num_pages, mongo=False)
    TestClass.scrape()


if __name__ == "__main__":
    main()
