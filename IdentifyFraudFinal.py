import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import matthews_corrcoef


from FraudDetectionNetwork import FraudDetectionNetwork
from FraudDetectionSpending import FraudDetectionSpending
from FraudDetectionShopping import FraudDetectionShopping
from FraudDetectionCommon import FraudDetectionCommon
from FraudDetectionDepartment import FraudDetectionDepartment


def get_suspicious_trip_numbers(predictions_df):
    # Identify trips where any detection method has flagged the trip as suspicious
    filtered_df = predictions_df[(predictions_df['Network'] == 1)]
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

def update_detection_results(df, column, positive_value, negative_value):
    df[column] = df[column].apply(lambda x: positive_value if x == 1 else negative_value)

def main():
    predictions_df = pd.DataFrame({'tripnumber': range(7000, 7999)})
    # Run the network-based fraud detection
    network_detector = FraudDetectionNetwork('Data/supermarket_enhanced.csv', predictions_df, std_dev_multiplier=4.2)
    predictions_df = network_detector.run()

    # Run the k-means-based fraud detection
    spending_detector = FraudDetectionSpending('Data/supermarket_enhanced.csv', 'Data/TestFileFormatted.csv', predictions_df, n_clusters=3, fraud_threshold_percent=98.7)
    predictions_df = spending_detector.run()

    # Run the shopping behavior-based fraud detection
    shopping_detector = FraudDetectionShopping('Data/supermarket_enhanced.csv', 'Data/TestFileFormatted.csv', predictions_df, n_clusters=3, fraud_threshold_percent= 95)
    predictions_df = shopping_detector.run()

    # Run the common fraud detection method
    common_detector = FraudDetectionCommon('Data/supermarket_enhanced.csv', 'Data/TestFileFormatted.csv', predictions_df, n_clusters=4, fraud_threshold_percent=98.7)
    predictions_df = common_detector.run()

    department_detector = FraudDetectionDepartment('Data/supermarket_enhanced.csv', 'Data/TestFileFormatted.csv', predictions_df)
    predictions_df = department_detector.run()

    # Calculate the Phi coefficient matrix for the binary DataFrame
    phi_matrix = compute_phi_matrix(predictions_df[['Network', 'Shopping', 'Spending', 'Common']])

    # Generate a correlation heatmap using the Phi coefficient matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(phi_matrix, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Phi Coefficient Matrix of Fraud Detection Methods')
    plt.show()

    # Update results after each detection method
    update_detection_results(predictions_df, 'Network', 0.5, -0.2)
    update_detection_results(predictions_df, 'Shopping', 0.3, -0.1)
    update_detection_results(predictions_df, 'Spending', 0.2, -0.05)
    update_detection_results(predictions_df, 'Common', 0.4, -0.2)
    update_detection_results(predictions_df, 'Department', 0.2, -0.1)

    predictions_df['Score'] = predictions_df['Network'] + predictions_df['Shopping'] + predictions_df['Spending'] + predictions_df['Common'] + predictions_df['Department']

    for value in predictions_df['Score']:
        if value > 0.6:
            print(value)


    # Save the updated predictions DataFrame to CSV
    predictions_df.to_csv('Data/predictions_output.csv', index=False)
    print("Predictions saved to 'Data/predictions_output.csv'.")

if __name__ == "__main__":
    main()
