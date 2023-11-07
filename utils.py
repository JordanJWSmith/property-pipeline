import json
import pandas as pd
from tqdm import tqdm


def json_to_csv(filepath):

    with open(filepath) as f:
        json_file = json.load(f)
    
    ITEMS = []
    for listing in tqdm(json_file):
        _id = listing['id']
        price = listing['price']['amount']
        bedrooms = listing['bedrooms']
        bathrooms = listing['bathrooms']
        summary = listing['summary']
        text = listing['text']['description']
        latitude = listing['location']['latitude']
        longitude = listing['location']['longitude']
        property_type = listing['propertySubType']
        lease = listing['tenure']['tenureType']

        for image in listing['images']:
            image_url = image['url']

            ITEMS.append([_id, price, bedrooms, bathrooms, summary, text, latitude, longitude, property_type, lease, image_url])

    df = pd.DataFrame(ITEMS)
    df.columns = ['_id', 'price', 'bedrooms', 'bathrooms', 'summary', 'text', 'latitude', 'longitude', 'property_type', 'lease', 'image_url']

    return df
