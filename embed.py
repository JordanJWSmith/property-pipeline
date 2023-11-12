import logging
import pandas as pd
from embedder import Embedder

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def embed():

    timestring = '12-11-2023_16-01-50'
    folder_path = f'data/{timestring}/'
    df = pd.read_csv(f'{folder_path}/combined_locations.csv')
    PropertyEmbedder = Embedder(df, folder_path)
    feature_embeddings = PropertyEmbedder.feature_embeddings()
    print(feature_embeddings.shape)

if __name__ == "__main__":
    embed()
