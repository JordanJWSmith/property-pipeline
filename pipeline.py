import logging
import argparse
import pandas as pd
from transformers import pipeline

from webscraper import Webscraper
from classifier import Classifier
from embedder import Embedder

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def property_pipeline():

    parser = argparse.ArgumentParser(description='Web Scraper Script')
    parser.add_argument('--images', action='store_true', help='Include image classification and embeddings')
    args = parser.parse_args()

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

    if args.images:
        logging.info(f'Initialising image classification model...')
        pipe = pipeline("image-classification", model="andupets/real-estate-image-classification-30classes")

        for fp in scraped_filepaths:
            ImagePredictor = Classifier(pipe, fp)
            ImagePredictor.classify()
    
    df = pd.concat([pd.read_csv(fp) for fp in scraped_filepaths])
    folder_path = f'data/{Scraper.timestring}/'
    df.to_csv(f'{folder_path}/combined_locations.csv')

    PropertyEmbedder = Embedder(df, folder_path)
    PropertyEmbedder.feature_embeddings()


if __name__ == "__main__":
    property_pipeline()
