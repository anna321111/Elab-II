from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import json
import os

def plot_clusters(data, labels, centroids):
    # Generate unique colors using a colormap
    colors = plt.cm.get_cmap('viridis', max(labels) + 1)

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(data[:, 0], data[:, 1], c=labels, cmap=colors)
    plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='red', marker='*', edgecolors='black', label='Centroids')
    plt.title('Clusters and Centroids')
    plt.xlabel('Time spent')
    plt.ylabel('Price')
    plt.colorbar(scatter, spacing='proportional', ticks=range(max(labels) + 1), label='Cluster ID')
    plt.legend()
    plt.show()

def load_data(json_filename):
    # Define the directory containing the JSON file
    directory = 'data'
    json_file_path = os.path.join(directory, json_filename)

    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Assuming each sublist in data is a pair [time spent, price]
    # Flatten the data into a 2D array
    flattened_data = np.array(data).reshape(-1, 2)
    return flattened_data

# Example usage
data = load_data('normalized_sampled.json')
kmeans = KMeans(n_clusters=3, random_state=42).fit(data)
plot_clusters(data, kmeans.labels_, kmeans.cluster_centers_)




