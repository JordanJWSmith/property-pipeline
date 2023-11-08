import logging
from webscraper import Webscraper
from predict_image_classes import Classifier

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def pipeline():
    
    user_agent = 'Mozilla/5.0 (Linux; Android 10; SM-A205U) ' \
                    'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                    'Chrome/106.0.5249.126 Mobile Safari/537.36'
    
    location_codes = {
        "wandsworth": "5E93977",
        "kensington_and_chelsea": "5E61229"
    }
    num_pages = 1

    Scraper = Webscraper(user_agent, location_codes, num_pages, mongo=False)
    Scraper.scrape()

    scraped_filepaths = [f'{fp}.csv' for fp in Scraper.saved_filepaths]
    print(scraped_filepaths)


if __name__ == "__main__":
    pipeline()
