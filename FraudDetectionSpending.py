import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

class FraudDetectionSpending:
    def __init__(self, train_file_path, test_file_path, predictions_df, n_clusters=3, fraud_threshold_percent=84.3):
        self.train_file_path = train_file_path
        self.test_file_path = test_file_path
        self.predictions_df = predictions_df
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        self.fraud_threshold_percent = fraud_threshold_percent  # New class variable for dynamic threshold setting

    def compute_features(self, df):
        total_spend = df.groupby('tripnumber')['price'].sum().rename('total_spend_per_trip')
        average_price = df.groupby('tripnumber')['price'].mean().rename('average_price_per_item')
        price_range = df.groupby('tripnumber')['price'].agg(lambda x: x.max() - x.min()).rename('price_range')
        return pd.concat([total_spend, average_price, price_range], axis=1).reset_index()

    def preprocess_data(self):
        df_train = pd.read_csv(self.train_file_path)
        df_test = pd.read_csv(self.test_file_path)

        # Normalize data
        df_train[['timebetween', 'price']] = self.scaler.fit_transform(df_train[['timebetween', 'price']])
        df_test[['timebetween', 'price']] = self.scaler.transform(df_test[['timebetween', 'price']])

        self.cluster_data_train = self.compute_features(df_train)
        self.cluster_data_test = self.compute_features(df_test)

    def fit(self):
        # Fit the model on the training data
        self.kmeans.fit(self.cluster_data_train[['total_spend_per_trip', 'average_price_per_item', 'price_range']])

    def predict(self):
        # Predict clusters and calculate distances for the test set
        self.cluster_data_test['cluster'] = self.kmeans.predict(self.cluster_data_test[['total_spend_per_trip', 'average_price_per_item', 'price_range']])
        distances = self.kmeans.transform(self.cluster_data_test[['total_spend_per_trip', 'average_price_per_item', 'price_range']])
        min_distances = distances.min(axis=1)

        # Set fraud threshold using the new class variable
        threshold = np.percentile(min_distances, self.fraud_threshold_percent)
        self.cluster_data_test['k-meansSpending'] = (min_distances > threshold).astype(int)

        # Update predictions_df
        self.predictions_df['KMeans'] = self.predictions_df['tripnumber'].map(self.cluster_data_test.set_index('tripnumber')['k-meansSpending']).fillna(0)

    def run(self):
        self.preprocess_data()
        self.fit()
        self.predict()
        return self.predictions_df




