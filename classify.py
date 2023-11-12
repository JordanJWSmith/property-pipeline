import logging
from transformers import pipeline
from classifier import Classifier

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


def classify():

    pipe = pipeline("image-classification", model="andupets/real-estate-image-classification-30classes")
    filepath = 'data/08-11-2023_18-07-04/wandsworth_properties_08-11-2023_18-07-04.csv'

    ImagePredictor = Classifier(pipe, filepath)
    ImagePredictor.classify()


if __name__ == "__main__":
    classify()
