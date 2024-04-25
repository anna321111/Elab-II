from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import os

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

def load_data(csv_filename):
    # Define the directory containing the CSV file
    directory = 'Data'
    csv_file_path = os.path.join(directory, csv_filename)

    # Read the CSV file using pandas
    data_df = pd.read_csv(csv_file_path, usecols=['timebetween', 'price'])

    # Convert the pandas DataFrame to a numpy array
    data_array = data_df.to_numpy()
    return data_array

# Example usage
data = load_data('supermarket_normalized_subset.csv')
kmeans = KMeans(n_clusters=3, random_state=42).fit(data)
plot_clusters(data, kmeans.labels_, kmeans.cluster_centers_)




