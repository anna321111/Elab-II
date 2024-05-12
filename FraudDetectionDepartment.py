import pandas as pd
import numpy as np


class FraudDetectionDepartment:
    def __init__(self, predictions_df, test_file_path):
        self.predictions_df = predictions_df
        self.test_file_path = test_file_path
        self.department_weights = {
            1: 428.41, 2: 447.51, 3: 182.34, 4: 442.55, 5: 184.25, 6: 219.51,
            7: 223.71, 8: 315.31, 9: 377.4, 10: 298.38, 11: 408.03, 12: 275.62,
            13: 529.91, 14: 435.96, 15: 429.31, 16: 312.08, 17: 230.87, 18: 284.15
        }
        self.scale_weights()

    def scale_weights(self):
        min_weight = min(self.department_weights.values())
        max_weight = max(self.department_weights.values())
        range_weight = max_weight - min_weight
        self.department_weights = {dept: (weight - min_weight) / range_weight
                                   for dept, weight in self.department_weights.items()}

    def classify_purchases(self):
        df = pd.read_csv(self.test_file_path)
        df['Score'] = df['departmentnumber'].map(self.department_weights)

        # Replace NaN scores for departments not in the weight list with zero
        df['Score'].fillna(0, inplace=True)
        print(df['Score'])
        trip_scores = df.groupby('tripnumber')['Score'].mean().reset_index()
        trip_scores.rename(columns={'Score': 'Department'}, inplace=True)

        # Map the scores to the predictions dataframe
        self.predictions_df = self.predictions_df.merge(trip_scores, on='tripnumber', how='left')
        return self.predictions_df

    def run(self):
        updated_predictions_df = self.classify_purchases()
        updated_predictions_df.to_csv('Data/predictions_with_department_scores.csv', index=False)
        return updated_predictions_df
