import torch
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from nltk.tokenize import word_tokenize
from sklearn.preprocessing import StandardScaler


class Embedder:
    def __init__(self, df, folder_path):
        self.df = df
        self.folder_path = folder_path


    def generate_unique_df(self):
        return self.df.drop_duplicates(subset='_id')
    

    def generate_text_embeddings(self, df):
        df['tokenized_text'] = df['text'].apply(lambda x: word_tokenize(x.lower()))
        word2vec_model = Word2Vec(sentences=df['tokenized_text'], vector_size=100, window=5, min_count=1, workers=4)
        text_embeddings = df['tokenized_text'].apply(lambda tokens: np.mean([word2vec_model.wv[word] for word in tokens if word in word2vec_model.wv] or [np.zeros(100)], axis=0))
        text_embeddings = np.vstack(text_embeddings)

        return text_embeddings


    def generate_feature_embeddings(self, df):

        property_type_encoded = pd.get_dummies(df['property_type'], prefix='property_type')
        lease_type_encoded = pd.get_dummies(df['lease'], prefix='lease')

        numerical_features = df[['price', 'bedrooms', 'bathrooms']]
        scaler = StandardScaler()
        numerical_embeddings= scaler.fit_transform(numerical_features)

        location_data = df[['latitude', 'longitude']]
        pca = PCA(n_components=2)
        location_embeddings = pca.fit_transform(location_data)

        categorical_embeddings = np.hstack([property_type_encoded, lease_type_encoded])

        text_embeddings = self.generate_text_embeddings(df.copy())

        combined_embeddings = np.hstack((
        categorical_embeddings, 
        numerical_embeddings, 
        location_embeddings,
        text_embeddings
        ))

        return combined_embeddings
    

    def remove_null_embeddings(self, embeddings):
        nan_mask = torch.isnan(torch.from_numpy(embeddings))
        embeddings[nan_mask] = 0

        return embeddings
    

    def save_embeddings(self, embeddings, filepath):
        np.save(filepath, embeddings)

    
    def feature_embeddings(self):
        df = self.generate_unique_df()
        feature_embeddings = self.generate_feature_embeddings(df)
        feature_embeddings = self.remove_null_embeddings(feature_embeddings)
        self.save_path = f'{self.folder_path}/feature_embeddings.npy'
        self.save_embeddings(feature_embeddings, self.save_path)
        return feature_embeddings




