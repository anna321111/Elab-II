import json
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer

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

def load_and_process_data(json_filename):
    # Define the directory containing the JSON file
    directory = 'Data'
    json_file_path = os.path.join(directory, json_filename)

    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    averaged_data = []
    for purchase_group in data:
        sum_second = 0
        sum_third = 0
        for purchase in purchase_group:
            if len(purchase) >= 3:
                sum_second += purchase[1]  # Sum the second element
                sum_third += purchase[2]  # Sum the third element

        if len(purchase_group) > 0:  # Avoid division by zero
            average_second = sum_second / len(purchase_group)
            average_third = sum_third / len(purchase_group)
            averaged_data.append([average_second, average_third])

    # Convert to numpy array and handle NaN values
    np_data = np.array(averaged_data)
    imputer = SimpleImputer(strategy='mean')
    cleaned_data = imputer.fit_transform(np_data)  # Impute any NaN values
    return cleaned_data

# Example usage
data = load_and_process_data('supermarketjsonnormal.json')  # Adjust filename as needed
print(data)
if data.size > 0:
    kmeans = KMeans(n_clusters=3, random_state=42).fit(data)
    plot_clusters(data, kmeans.labels_, kmeans.cluster_centers_)
else:
    print("No data to cluster.")

