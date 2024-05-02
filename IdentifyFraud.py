from FraudDetectionNetwork import FraudDetectionNetwork
import pandas as pd

def get_suspicious_trip_numbers(predictions_df):
    # Filter DataFrame for tripnumbers with Network = 1.0
    suspicious_trips = predictions_df[predictions_df['Network'] == 1.0]['tripnumber'].tolist()
    return suspicious_trips


def main():
    # Create a DataFrame as an example, this would ideally come from your actual data processing
    predictions_df = pd.DataFrame({'tripnumber': range(1, 1001)})  # Example DataFrame initialization

    # Instantiate the FraudDetection class (assuming supermarket_enhanced.csv is your data file)
    detector = FraudDetectionNetwork('Data/supermarket_enhanced.csv', predictions_df)
    updated_predictions_df = detector.run()

    # Get suspicious trip numbers
    suspicious_trips = get_suspicious_trip_numbers(updated_predictions_df)

    # Print each trip number on a new line
    for trip_number in suspicious_trips[:150]:
        print(trip_number)


if __name__ == "__main__":
    main()