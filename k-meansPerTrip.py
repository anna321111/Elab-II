import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer

def plot_clusters(data, labels, centroids, output_file='Plots/clusters.png'):
    colors = plt.cm.get_cmap('viridis', max(labels) + 1)
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(data[:, 0], data[:, 1], c=labels, cmap=colors)
    plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='red', marker='*', edgecolors='black', label='Centroids')
    plt.title('Clusters and Centroids')
    plt.xlabel('Normalized Time Spent')
    plt.ylabel('Normalized Price')
    plt.colorbar(scatter, spacing='proportional', ticks=range(max(labels) + 1), label='Cluster ID')
    plt.legend()
    plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
    plt.show()

def load_and_process_data(csv_filename):
    directory = 'Data'
    csv_file_path = os.path.join(directory, csv_filename)
    df = pd.read_csv(csv_file_path)
    grouped_df = df.groupby('tripnumber')[['timebetween', 'price']].mean().reset_index(drop=True)
    np_data = grouped_df.to_numpy()
    imputer = SimpleImputer(strategy='mean')
    cleaned_data = imputer.fit_transform(np_data)
    return cleaned_data

def plot_elbow_method(data, output_file='Plots/elbow.png'):
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, random_state=42)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), wcss, marker='o')
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.xticks(range(1, 11))
    plt.grid(True)
    plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
    plt.show()

# Example usage
data = load_and_process_data('supermarket_normalized_subset.csv')
if data.size > 0:
    plot_elbow_method(data, 'Plots/elbow_plot.png')  # Plotting and saving the elbow curve
    kmeans = KMeans(n_clusters=3, random_state=42).fit(data)  # Example with 3 clusters, adjust based on elbow plot
    plot_clusters(data, kmeans.labels_, kmeans.cluster_centers_, 'Plots/cluster_plot.png')  # Plotting and saving the clusters
else:
    print("No data to cluster.")
