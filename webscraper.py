import os
import json
import logging
import requests
import bson.json_util as json_util
from tqdm import tqdm
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient

load_dotenv()

