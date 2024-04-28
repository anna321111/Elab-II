from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import os
from yellowbrick.cluster import SilhouetteVisualizer
from sklearn.metrics import silhouette_score

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

def plot_elbow_method(data):
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, random_state=42)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), wcss, marker='o')
    plt.title('Elbow Method')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
    plt.xticks(range(1, 11))
    plt.grid(True)
    plt.show()


def plot_silhouette_method(data):
    fig, ax = plt.subplots(3, 2, figsize=(15, 15))
    avg_scores = []
    for i, n_clusters in enumerate([2, 3, 4, 5, 6, 7]):
        km = KMeans(n_clusters=n_clusters, init='k-means++', n_init=10, max_iter=100, random_state=42)
        q, mod = divmod(i, 2)
        visualizer = SilhouetteVisualizer(km, colors='yellowbrick', ax=ax[q][mod])
        visualizer.fit(data)

        # Calculate silhouette score
        score = silhouette_score(data, km.labels_)
        avg_scores.append(score)

    # Output average silhouette scores
    for i, score in enumerate(avg_scores):
        print(f"Average silhouette score for {i + 2} clusters: {score}")


# Example usage
data = load_data('supermarket_normalized_subset.csv')
if data.size > 0:
    plot_elbow_method(data)  # Plotting the elbow curve to find optimal number of clusters
    plot_silhouette_method(data)  # Plotting silhouette scores for different cluster sizes
    optimal_clusters = 5  # Replace this with the number from the elbow plot if different
    kmeans = KMeans(n_clusters=optimal_clusters, random_state=42).fit(data)
    plot_clusters(data, kmeans.labels_, kmeans.cluster_centers_)
else:
    print("No data to cluster.")


