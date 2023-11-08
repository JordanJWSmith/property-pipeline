import logging
from webscraper import Webscraper
from transformers import pipeline
from predict_image_classes import Classifier

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def property_pipeline():
    
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

    logging.info(f'\nInitialising image classification model...')
    pipe = pipeline("image-classification", model="andupets/real-estate-image-classification-30classes")

    scraped_filepaths = [f'{fp}.csv' for fp in Scraper.saved_filepaths]
    
    for fp in scraped_filepaths:

        ImagePredictor = Classifier(pipe, fp)
        ImagePredictor.classify()


if __name__ == "__main__":
    property_pipeline()
