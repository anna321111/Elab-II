import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.stats import zscore

class FraudDetectionShopping:
    def __init__(self, train_file_path, test_file_path, predictions_df, n_clusters=3):
        self.train_file_path = train_file_path
        self.test_file_path = test_file_path
        self.predictions_df = predictions_df  # Now taken as an input parameter
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=0)

    def compute_features(self, df):
        items_per_trip = df.groupby('tripnumber').size().rename('items_per_trip')
        time_variability = df.groupby('tripnumber')['timebetween'].std().rename('time_variability')
        time_density = (items_per_trip / df.groupby('tripnumber')['timebetween'].sum()).rename('time_density')
        return pd.concat([items_per_trip, time_variability, time_density], axis=1).fillna(0).reset_index()

    def preprocess_data(self):
        df_train = pd.read_csv(self.train_file_path)
        df_test = pd.read_csv(self.test_file_path)

        df_train[['timebetween', 'price']] = self.scaler.fit_transform(df_train[['timebetween', 'price']])
        df_test[['timebetween', 'price']] = self.scaler.transform(df_test[['timebetween', 'price']])

        self.cluster_data_train = self.compute_features(df_train)
        self.cluster_data_test = self.compute_features(df_test)

    def fit(self):
        self.kmeans.fit(self.cluster_data_train[['items_per_trip', 'time_variability', 'time_density']])

    def predict(self):
        self.cluster_data_test['cluster'] = self.kmeans.predict(self.cluster_data_test[['items_per_trip', 'time_variability', 'time_density']])
        distances = self.kmeans.transform(self.cluster_data_test[['items_per_trip', 'time_variability', 'time_density']])
        min_distances = distances.min(axis=1)
        threshold = np.percentile(min_distances, 84.2)
        self.cluster_data_test['Shopping'] = (min_distances > threshold).astype(int)

        # Merge results back to the predictions dataframe
        self.predictions_df = self.predictions_df.merge(self.cluster_data_test[['tripnumber', 'Shopping']], on='tripnumber', how='left')
        self.predictions_df['Shopping'].fillna(0, inplace=True)

    def run(self):
        self.preprocess_data()
        self.fit()
        self.predict()
        return self.predictions_df

