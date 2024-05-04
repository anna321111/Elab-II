from FraudDetectionNetwork import FraudDetectionNetwork
from FraudDetectionSpending import FraudDetectionSpending
from FraudDetectionShopping import FraudDetectionShopping  # Assuming the code above is saved in a FraudDetectionShopping.py file
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# Assuming you've already defined FraudDetectionNetwork, FraudDetectionSpending, and FraudDetectionShopping classes.

def get_suspicious_trip_numbers(predictions_df, method_column):
    # This function now just returns a list of suspicious trip numbers
    return predictions_df[predictions_df[method_column] == 1]['tripnumber'].tolist()

def main():
    # Create a DataFrame as an example
    predictions_df = pd.DataFrame({'tripnumber': range(2000, 2999)})

    # Run the network-based fraud detection
    network_detector = FraudDetectionNetwork('Data/supermarket_enhanced.csv', predictions_df)
    predictions_df = network_detector.run()

    # Run the k-means-based fraud detection
    k_means_detector = FraudDetectionSpending('Data/supermarket_enhanced.csv', 'Data/TestFileFormatted.csv', predictions_df)
    predictions_df = k_means_detector.run()

    # Run the shopping behavior-based fraud detection
    shopping_detector = FraudDetectionShopping('Data/supermarket_enhanced.csv', 'Data/TestFileFormatted.csv', predictions_df)
    predictions_df = shopping_detector.run()

    # Retrieve suspicious trip numbers without altering the original DataFrame
    suspicious_network_trips = get_suspicious_trip_numbers(predictions_df, 'Network')
    suspicious_kmeans_trips = get_suspicious_trip_numbers(predictions_df, 'KMeans')
    suspicious_shopping_trips = get_suspicious_trip_numbers(predictions_df, 'Shopping')

    # Print suspicious trips for each method
    print("Suspicious Trips from Network-Based Detection:")
    for trip_number in suspicious_network_trips[:150]:
        print(trip_number)

    print("\nSuspicious Trips from K-Means-Based Detection:")
    print(len(suspicious_kmeans_trips))
    for trip_number in suspicious_kmeans_trips[:150]:
        print(trip_number)

    print("\nSuspicious Trips from Shopping-Based Detection:")
    print(len(suspicious_shopping_trips))
    for trip_number in suspicious_shopping_trips[:150]:
        print(trip_number)

    # Generate a correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(predictions_df.corr(), annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Correlation Heatmap of Fraud Detection Methods')
    plt.show()

    # Save the updated predictions DataFrame to CSV
    predictions_df.to_csv('Data/predictions_output.csv', index=False)
    print("Predictions saved to 'Data/predictions_output.csv'.")

if __name__ == "__main__":
    main()
