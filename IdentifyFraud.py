from FraudDetectionNetwork import FraudDetectionNetwork
from FraudDetectionSpending import FraudDetectionSpending
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def get_suspicious_trip_numbers(predictions_df, method_column):
    # Filter DataFrame for tripnumbers with specified method column = 1.0
    suspicious_trips = predictions_df[predictions_df[method_column] == 1]['tripnumber'].tolist()
    return suspicious_trips

def main():
    # Create a DataFrame as an example, this would ideally come from your actual data processing
    predictions_df = pd.DataFrame({'tripnumber': range(1000, 1999)})

    # Instantiate and run the network-based fraud detection
    network_detector = FraudDetectionNetwork('Data/supermarket_enhanced.csv', predictions_df)
    predictions_df = network_detector.run()

    # Instantiate and run the k-means-based fraud detection
    k_means_detector = FraudDetectionSpending('Data/supermarket_enhanced.csv', 'Data/TestFileFormatted.csv', predictions_df)
    predictions_df = k_means_detector.run()

    # Get suspicious trip numbers from network-based detection
    suspicious_network_trips = get_suspicious_trip_numbers(predictions_df, 'Network')
    # Get suspicious trip numbers from k-means-based detection
    suspicious_kmeans_trips = get_suspicious_trip_numbers(predictions_df, 'KMeans')

    # Print each trip number on a new line
    print("Suspicious Trips from Network-Based Detection:")
    for trip_number in suspicious_network_trips[:150]:
        print(trip_number)

    print("\nSuspicious Trips from K-Means-Based Detection:")
    print(len(suspicious_kmeans_trips))
    for trip_number in suspicious_kmeans_trips[:150]:
        print(trip_number)

    # Generate a correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(predictions_df.corr(), annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Correlation Heatmap of Fraud Detection Methods')
    plt.show()

    predictions_df.to_csv('Data/predictions_output.csv', index=False)
    print("Predictions saved to 'Data/predictions_output.csv'.")

if __name__ == "__main__":
    main()
