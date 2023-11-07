import logging
from transformers import pipeline
from predict_image_classes import Classifier

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


def classify():

    pipe = pipeline("image-classification", model="andupets/real-estate-image-classification-30classes")
    filepath = 'sample_data/csv_file/wandsworth_properties_07-11-2023_17-52-04.csv'

    ImagePredictor = Classifier(pipe, filepath)
    ImagePredictor.classify()


if __name__ == "__main__":
    classify()
