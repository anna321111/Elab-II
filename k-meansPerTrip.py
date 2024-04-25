import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer

def plot_clusters(data, labels, centroids):
    # Generate unique colors using a colormap
    colors = plt.cm.get_cmap('viridis', max(labels) + 1)
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(data[:, 0], data[:, 1], c=labels, cmap=colors)
    plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='red', marker='*', edgecolors='black', label='Centroids')
    plt.title('Clusters and Centroids')
    plt.xlabel('Normalized Time Spent')
    plt.ylabel('Normalized Price')
    plt.colorbar(scatter, spacing='proportional', ticks=range(max(labels) + 1), label='Cluster ID')
    plt.legend()
    plt.show()

def load_and_process_data(csv_filename):
    # Define the directory containing the CSV file
    directory = 'Data'
    csv_file_path = os.path.join(directory, csv_filename)

    # Read the CSV file using pandas
    df = pd.read_csv(csv_file_path)

    # Group by 'tripnumber' and compute the mean of 'timebetween' and 'price'
    # Correcting from tuple to list for column names
    grouped_df = df.groupby('tripnumber')[['timebetween', 'price']].mean().reset_index(drop=True)

    # Convert the grouped DataFrame to a numpy array and handle NaN values
    np_data = grouped_df.to_numpy()
    imputer = SimpleImputer(strategy='mean')
    cleaned_data = imputer.fit_transform(np_data)  # Impute any NaN values if present
    return cleaned_data

# Example usage
data = load_and_process_data('supermarket_normalized_subset.csv')  # Ensure you provide the correct filename
print(data)
if data.size > 0:
    kmeans = KMeans(n_clusters=2, random_state=42).fit(data)
    plot_clusters(data, kmeans.labels_, kmeans.cluster_centers_)
else:
    print("No data to cluster.")
