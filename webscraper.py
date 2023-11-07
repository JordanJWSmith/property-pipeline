import os
import json
import logging
import requests
from tqdm import tqdm
from bson import json_util
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient

load_dotenv()

class Webscraper:
    def __init__(self, user_agent, location_codes, num_pages, mongo):
        self.user_agent = user_agent
        self.location_codes = location_codes
        self.num_pages = num_pages
        self.mongo = mongo
        if self.mongo:
            self.MONGO_USER = os.getenv('MONGO_USER')
            self.MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
            self.MONGO_CLUSTER = os.getenv('MONGO_CLUSTER')
            self.MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
            self.MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')


    def insert_many_to_mongo(self, properties):
        cluster = MongoClient(f"mongodb+srv://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_CLUSTER}/{self.MONGO_DB_NAME}")
        db = cluster[self.MONGO_DB_NAME]
        collection = db[self.MONGO_COLLECTION]

        existing_property_ids = [str(i) for i in collection.distinct('id')]
        properties_to_insert = [prop for prop in properties if prop['id'] not in existing_property_ids]
        if len(properties_to_insert):
            collection.insert_many(properties_to_insert)

        logging.info(f'{len(properties_to_insert)} new properties written to MongoDB \n')

        return len(properties_to_insert)


    def save_json(self, location, properties):
        timestring = datetime.strftime(datetime.now(), '%d-%m-%Y_%H-%M-%S')

        if not os.path.isdir("json_data"):
            os.mkdir('json_data')

        os.mkdir(f"json_data/{timestring}")

        with open(f'json_data/{timestring}/{location}_properties_{timestring}.json', 'w', encoding='utf-8') as f:
            f.write(json_util.dumps(properties))

        return timestring


    def scrape_location(self, location, location_code):
        location_properties = []
        for i in range(self.num_pages):
            logging.info(f"SCRAPING PAGE {i+1} OF {self.num_pages} in {location.upper()}")

            index = i*24
            search_url = f'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{location_code}&sortType=6&index={index}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords='
            html_page = requests.get(search_url, headers={'User-Agent': self.user_agent})
            soup = BeautifulSoup(html_page.content, 'html.parser')
            page_properties = self.process_search_page(soup, location)
            location_properties += (page_properties)
        
        return location_properties
        

    def process_search_page(self, soup, location):
        page_properties = []
        for s in soup.find_all('script'):
            if 'window.jsonModel = ' in s.text:
                str_dict = s.text.strip()[19:]
                properties_dict = json.loads(str_dict)['properties']

                for prop in tqdm(properties_dict):
                    property_url = prop['propertyUrl']
                    property_page = requests.get(f'https://www.rightmove.co.uk{property_url}', headers={'User-Agent': self.user_agent})
                    property_soup = BeautifulSoup(property_page.content, 'html.parser')

                    for t in property_soup.find_all('script'):
                        if 'window.PAGE_MODEL =' in t.text:
                            property_str_dict = t.text.strip()[20:]
                            property_page_dict = json.loads(property_str_dict)
                            property_page_data = property_page_dict['propertyData']
                            for key in property_page_data:
                                prop[key] = property_page_data[key]

                    # prop['_id'] = prop['id']
                    prop['location_area'] = location
                    page_properties.append(prop)
                    
        return page_properties

    
    def scrape(self):
        line_break = '*'*20
        prop_count = 0
        for location, code in self.location_codes.items():
            logging.info(f'{line_break} Beginning scraping from {location} {line_break}')

            location_properties = self.scrape_location(location, code)

            inserted_property_count = self.insert_many_to_mongo(location_properties) if self.mongo else len(location_properties)

            timestring = self.save_json(location, location_properties)

            prop_count += inserted_property_count

        log_suffix = "written to MongoDB in total" if self.mongo else f"written to json_data/{location}_properties_{timestring}.json"

        logging.info(f'{prop_count} property listings {log_suffix}')
