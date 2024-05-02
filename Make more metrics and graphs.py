import json
import pandas as pd

# Read the JSON file
with open('Data/supermarketjson.json') as f:
    data = json.load(f)

# Define department codes
department_codes = list(range(1, 19))

# Pre-allocate an empty matrix to store department totals
department_data_test = pd.DataFrame(0, index=department_codes, columns=['TotalPrice', 'NumItems', 'TotalTime', 'NumVisits'])

# Iterate over each row in the dataset
for row_index, row in enumerate(data):
    # Skip the first row if it contains data instead of column headers

    try:

        # Iterate over each tuple in the row
        for entry in row:
            department_code = entry[0]
            price = entry[2]
            time_since_last_scan = entry[3]

            # Update department totals for the current row
            if department_code in department_codes:
                department_data_test.at[department_code, 'TotalPrice'] += price
                department_data_test.at[department_code, 'NumItems'] += 1
                department_data_test.at[department_code, 'TotalTime'] += time_since_last_scan


    except IndexError:
        continue  # Skip the current row if IndexError occurs

# Calculate average price per item for each department
department_data_test['AvgPricePerItem'] = department_data_test['TotalPrice'] / department_data_test['NumItems']
department_data_test['AvgTimePerVisit'] = department_data_test['TotalTime'] / department_data_test['NumVisits']
department_data_test['AvgTimePerItem'] = department_data_test['TotalTime'] / department_data_test['NumItems']
department_data_test['Department'] = department_data_test.index


department_data_test.to_csv('department_metrics.csv', index=False)
