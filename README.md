![FourthWall](assets/fourthwall_banner.png)

# property-pipeline

This is a toolkit to display multimodal embeddings for live property listings on Rightmove. 

Work is still in progress, but its components will be:
1. Webscraper
2. Image classifier
3. Embedding generator
4. Visualise embeddings

## Deployment

Clone the repo, create your environment and run `pip install -r requirements.txt`. 

If you'd like to use the MongoDB functionality, you'll need to create an `.env` file and include the following information:

```
MONGO_USER=<your mongoDB username>
MONGO_PASSWORD=<your mongoDB password>
MONGO_CLUSTER=<the mongoDB cluster string>
MONGO_DB_NAME=<the mongoDB database name>
MONGO_COLLECTION=<the mongoDB collection>
```

For example, for the connection string `mongodb+srv://JordanSmith:<password>@cluster-test.fndbj.mongodb.net/myFirstDatabase`, your `.env` file would be as follows:

```
MONGO_USER="JordanSmith"
MONGO_PASSWORD=<password>
MONGO_CLUSTER="cluster-test.fndbj.mongodb.net"
MONGO_DB_NAME="myFirstDatabase"
MONGO_COLLECTION=<the mongoDB collection>
```

See [this article](https://medium.com/analytics-vidhya/connecting-to-mongodb-atlas-with-python-pymongo-5b25dab3ac53) for more guidance.

## Modules

### 1. Webscraper

Run `scrape.py` to run the webscraper. Property data will be scraped for each location code provided in `location_codes.json`. 

#### Arguments
- `-num_pages`: The number of Rightmove pages to scrape for each location (compulsory unless running `--test`)
- `--mongo`: If this is set, results will be stored in a MongoDB collection. See [deployment](#deployment). 
- `--test`: If this is set, the webscraper will run over one page from Wandsworth. 

#### Output

The webscraper retrieves a large amount of data per property in nested JSON format. Some elements are useful, some are not. Here is a non-exhaustive selection:

| Key      | Description | Type |
| ----------- | ----------- | ---- |
| _id         | Unique Rightmove property ID  (str)      | str |
| id          | Unique Rightmove property ID  (str)     | str |
| bedrooms   | Number of bedrooms (int)       | int |
| bathrooms   | Number of bathrooms (int)       | int |
| numberOfImages   | Number of images associated with property (int)       | int |
| numberofFloorplans   | Number of floorplan images associated with property (int)        | int |
| numberofFloorplans   | Number of floorplan images associated with property (int)        | int |
| summary   | Written summary of the property (str)       | str |
| displayAddress   | A truncated address, usually street and postcode (str)        | str |
| countryCode   | A code to indicate the country, i.e. "GB"        | str |
| location   | An object containing location information including latitude and longitude  | obj |
| propertyImages   | An object containing image URLs for each property image. Also separate objects for the main image and main map image.    | obj |
| propertySubType   | The type of property, i.e. "Apartment"    | str |
| listingUpdate   | Object containing the reason and date a property was reduced   | obj |
| premiumListing   | Whether or not the property is a premium listing.    | bool |
|  featuredProperty   | Whether or not the property is a featured listing.    | bool |
|  price   | An object containing the price, frequency and currencycode    | obj |
|  customer   | An object containing information on the estate agent listing the property, including name, address and branch   | obj | 
| distance | An object to signify distance | ? |
| transactionType | What type of transaction this is, i.e. "BUY", "LET" | str | 
| productLabel | An object describing a prdoduct label | obj | 
| commercial | Whether the property is suitable for commercial use | bool | 
| development | Whether the property is suitable for development | bool | 
| residential | Whether the property is residential | bool | 
| students | Whether the property is student accommodation | bool | 
| propertyUrl | The property's Rightmove URL slug | str|
| firstVisibleDate | The date the property was added to Rightmove | str |
| status | Whether the property is published or archived | obj |
| text | Various text elements including property description and page title | obj | 
| address | The property address | obj | 
| images | urls and resizedImageUrls for each image associated with the property | obj | 
| floorplans | urls for the property's floorplans | obj | 
| nearestStations | Station name, station type, distance and unit | obj |


...and many other fields.

### 2. Image Classifier

The image classifier currently uses a ViT model finetuned on real estate data, and is available [here](https://huggingface.co/andupets/real-estate-image-classification-30classes). 

It outputs 30 classes, some of which are a little niche for our use case. This model acts a placeholder, with the intention of replacing it with our own model finetuned on London real estate images. 

Run `classify.py` to run the image classifier. It takes the csv file from the previous step as an input, and saves it with an added column containing a prediction for each image. 


### 3. Embeddings Generator

In progress

### 4. Visualise Embeddings

In progress
