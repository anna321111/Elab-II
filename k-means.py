import numpy as np
import matplotlib.pyplot as plt
import random
import json
import os


def k_means(data, k, max_iterations=100):
    # Step 1: Initialize centroids randomly from the data points
    centroids = random.sample(data, k)
    centroids_old = np.zeros_like(centroids)

    # To store the centroids' assignments
    clusters = np.zeros(len(data))

    # Measure of the movement of centroids
    movement = np.linalg.norm(np.array(centroids) - np.array(centroids_old), axis=1)

    iteration = 0
    while np.any(movement > 0.01) and iteration < max_iterations:
        print(iteration)
        iteration += 1

        # Step 2: Assign each point to the nearest centroid
        for i, point in enumerate(data):
            distances = np.linalg.norm(point - np.array(centroids), axis=1)
            cluster = np.argmin(distances)
            clusters[i] = cluster

        # Store old centroid values
        centroids_old = np.copy(centroids)

        # Step 3: Update the centroids to the mean of the points assigned to them
        for i in range(k):
            points_in_cluster = [data[j] for j in range(len(data)) if clusters[j] == i]
            if points_in_cluster:
                centroids[i] = np.mean(points_in_cluster, axis=0)

        movement = np.linalg.norm(np.array(centroids) - np.array(centroids_old), axis=1)

    return centroids, clusters


def plot_clusters(data, centroids, clusters):
    print('start plotting')
    # Visualizing the results
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'orange', 'purple', 'pink', 'lime', 'teal']

    for i in range(len(centroids)):
        points = [data[j] for j in range(len(data)) if clusters[j] == i]
        if points:
            points = np.array(points)  # Convert to numpy array for easier indexing
            plt.scatter(points[:, 0], points[:, 1], s=30, c=colors[i], label=f'Cluster {i}')

    # Convert centroids to numpy array for easier plotting
    centroids = np.array(centroids)
    plt.scatter(centroids[:, 0], centroids[:, 1], s=300, marker='*', c='black', label='Centroids')
    plt.title('Clusters and Centroids')
    plt.xlabel('Time spent')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

def load_data(json_filename):
    # Define the directory containing the JSON file
    directory = 'data'
    json_file_path = os.path.join(directory, json_filename)

    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Flatten the data to extract only the department number and time spent
    flattened_data = []
    for trip in data[:400]:
        for purchase in trip:
            if len(purchase) == 3:  # Ensure the purchase has exactly three elements
                flattened_data.append([purchase[1], purchase[2]])  # department, time
    print('data ready')
    return flattened_data

# Example usage
data = load_data('supermarketnew2.json')
centroids, clusters = k_means(data, k=8)  # k is the number of clusters
plot_clusters(data, centroids, clusters)