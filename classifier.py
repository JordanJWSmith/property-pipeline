import logging
import pandas as pd
import numpy as np
from tqdm import tqdm
from PIL import UnidentifiedImageError

class Classifier:
    def __init__(self, pipe, csv_path):
        self.pipe = pipe
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)


    def generate_predictions(self, df, pipe):
        image_labels = []
        line_break = '*'*20
        logging.info(f'\n{line_break} Generating predictions for {df.shape[0]} images {line_break}')
        for image_url in tqdm(self.df['image_url']):
            try:
                result = pipe(image_url, top_k=1)
                label = result[0]['label']
            except UnidentifiedImageError:
                label = np.nan

            image_labels.append(label)

        df['image_prediction'] = image_labels
        return df
    

    def classify(self):
        cont = True

        if 'image_prediction' in self.df.columns:
            cont = input('Overwrite existing predictions? \n* [Y] to proceed \n* Any other key to cancel\n').lower() == 'y'

        if cont:
            df = self.generate_predictions(self.df, self.pipe)
            df.to_csv(self.csv_path)
            logging.info(f"`image_prediction` column added to {self.csv_path}")
            return df

        else:
            logging.info("Classifier cancelled")
            return None
    