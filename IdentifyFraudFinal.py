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



def update_detection_results(df, column, positive_value, negative_value):
    df[column] = df[column].apply(lambda x: positive_value if x == 1 else negative_value)

def main():
    predictions_df = pd.DataFrame({'tripnumber': range(48000, 48999)})
    # Run the network-based fraud detection
    #network_detector = FraudDetectionNetwork('Data/supermarket_enhanced.csv', predictions_df, std_dev_multiplier=4.2)
    #predictions_df = network_detector.run()

    # Run the k-means-based fraud detection
    #spending_detector = FraudDetectionSpending('Data/supermarket_enhanced.csv', 'Data/TestFileFormatted.csv', predictions_df, n_clusters=3, fraud_threshold_percent=98.7)
    #predictions_df = spending_detector.run()

    # Run the shopping behavior-based fraud detection
    #shopping_detector = FraudDetectionShopping('Data/supermarket_enhanced.csv', 'Data/TestFileFormatted.csv', predictions_df, n_clusters=3, fraud_threshold_percent= 95)
    #predictions_df = shopping_detector.run()

    # Run the common fraud detection method
    #common_detector = FraudDetectionCommon('Data/supermarket_enhanced.csv', 'Data/TestFileFormatted.csv', predictions_df, n_clusters=4, fraud_threshold_percent=98.7)
    #predictions_df = common_detector.run()

    department_detector = FraudDetectionDepartment(predictions_df, 'Data/TestFileFormatted.csv')
    predictions_df = department_detector.run()


    # Update results after each detection method
    #update_detection_results(predictions_df, 'Network', 0.5, -0.1)
    #update_detection_results(predictions_df, 'Shopping', 0.3, -0.05)
    #update_detection_results(predictions_df, 'Spending', 0.2, -0.02)
    #update_detection_results(predictions_df, 'Common', 0.4, -0.1)
    predictions_df['Department'] = predictions_df['Department']

    predictions_df['Score'] = predictions_df['Department']
    # Iterating through rows to print trip numbers where Score > 0.4
    for index, row in predictions_df.iterrows():
        if row['Score'] > 0.565:
            print(int(row['tripnumber']))

    # Counting the number of rows where Score > 0.4
    count_scores_above_0_4 = (predictions_df['Score'] > 0.565).sum()
    print(count_scores_above_0_4)

    # Save the updated predictions DataFrame to CSV
    predictions_df.to_csv('Data/predictions_output.csv', index=False)
    print("Predictions saved to 'Data/predictions_output.csv'.")

if __name__ == "__main__":
    main()
