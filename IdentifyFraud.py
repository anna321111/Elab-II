from FraudDetectionNetwork import FraudDetectionNetwork
from FraudDetectionSpending import FraudDetectionSpending
from FraudDetectionShopping import FraudDetectionShopping  # Assuming the code above is saved in a FraudDetectionShopping.py file
from FraudDetectionCommon import FraudDetectionCommon
from FraudDetectionDepartment import FraudDetectionDepartment

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import matthews_corrcoef

# Run 4-8 domjudge: Network only  Average Cases:30.4   Average Profit: 698.486 Relatively low variance
# Run 9-13 domjudge: Spending only Average Cases:25.4   Average Profit: 375.62 Very High Variance (highest 681)
# Run 14-18 domjudge: Shopping only Average Cases:17.8   Average Profit: 283.49 Relatively low variance
# Run 19-23 domjudge: Common only  Average Cases:23  Average Profit: 416.826 Relatively mid variance
# Run 24-28 domjudge: Common altered only Average Cases: 26  Average Profit: 499.326 Relatively low variance
# Run 49-53 domjudge: Department only Average Cases: 37  Average Profit: 667.418 Relatively low Variance

def get_suspicious_trip_numbers(predictions_df):
    # Identify trips where any detection method has flagged the trip as suspicious
    filtered_df = predictions_df[(predictions_df['Department'] >= 0.555)]
    return filtered_df['tripnumber'].unique().tolist()
def compute_phi_matrix(df):
    """Compute the Phi coefficient matrix for a binary DataFrame."""
    columns = df.columns
    phi_matrix = pd.DataFrame(index=columns, columns=columns, dtype=float)
    for col1 in columns:
        for col2 in columns:
            if col1 == col2:
                # The correlation of a variable with itself is always 1
                phi_matrix.at[col1, col2] = 1.0
            else:
                # Compute Matthews correlation coefficient, which is equivalent to the Phi coefficient
                phi_matrix.at[col1, col2] = matthews_corrcoef(df[col1], df[col2])
    return phi_matrix

def main():
    # Create a DataFrame as an example
    predictions_df = pd.DataFrame({'tripnumber': range(53000, 53999)})

    # Run the network-based fraud detection
    #network_detector = FraudDetectionNetwork('Data/supermarket_enhanced.csv', predictions_df, std_dev_multiplier=4.2)
    #predictions_df = network_detector.run()

    # Run the k-means-based fraud detection
    #spending_detector = FraudDetectionSpending('Data/supermarket_enhanced.csv', 'Data/TestFileFormatted.csv', predictions_df, n_clusters=3, fraud_threshold_percent=85)
    #predictions_df = spending_detector.run()

    # Run the shopping behavior-based fraud detection
    #shopping_detector = FraudDetectionShopping('Data/supermarket_enhanced.csv', 'Data/TestFileFormatted.csv', predictions_df, n_clusters=3, fraud_threshold_percent=84.9)
    #predictions_df = shopping_detector.run()

    # Run the common fraud detection method
    #common_detector = FraudDetectionCommon('Data/supermarket_enhanced.csv', 'Data/TestFileFormatted.csv', predictions_df, n_clusters=4, fraud_threshold_percent=84.9)
    #predictions_df = common_detector.run()

    # Run the department-based fraud detection
    department_detector = FraudDetectionDepartment(predictions_df, 'Data/TestFileFormatted.csv')
    predictions_df = department_detector.run()

    # Retrieve suspicious trip numbers that are flagged by any method
    suspicious_trips = get_suspicious_trip_numbers(predictions_df)
    print("Total number of suspicious trips across any method:", len(suspicious_trips))
    for trip in suspicious_trips[:150]:
        print(trip)

    # Calculate the Phi coefficient matrix for the binary DataFrame
    #phi_matrix = compute_phi_matrix(predictions_df[['Network']])

    # Generate a correlation heatmap using the Phi coefficient matrix
    #plt.figure(figsize=(10, 8))
    #sns.heatmap(phi_matrix, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1)
    #plt.title('Phi Coefficient Matrix of Fraud Detection Methods')
    #plt.show()

    # Save the updated predictions DataFrame to CSV
    predictions_df.to_csv('Data/predictions_output.csv', index=False)
    print("Predictions saved to 'Data/predictions_output.csv'.")

if __name__ == "__main__":
    main()
