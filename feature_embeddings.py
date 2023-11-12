import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def generate_unique_df(df):
    return df.drop_duplicates(subset='_id')

def generate_feature_embeddings(df):

    property_type_encoded = pd.get_dummies(df['property_type'], prefix='property_type')
    lease_type_encoded = pd.get_dummies(df['lease'], prefix='lease')

    numerical_features = df[['price', 'bedrooms', 'bathrooms']]
    scaler = StandardScaler()
    numerical_embeddings= scaler.fit_transform(numerical_features)

    location_data = df[['latitude', 'longitude']]
    pca = PCA(n_components=2)
    location_embeddings = pca.fit_transform(location_data)

    categorical_embeddings = np.hstack([property_type_encoded, lease_type_encoded])

    combined_embeddings = np.hstack((
    categorical_embeddings, 
    numerical_embeddings, 
    location_embeddings
    ))

    return combined_embeddings

generate_feature_embeddings('data/08-11-2023_18-53-01/kensington_and_chelsea/kensington_and_chelsea_properties_08-11-2023_18-53-01.csv')