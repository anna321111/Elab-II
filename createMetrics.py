import json
import csv

# Read the JSON file
with open('Data/supermarketnew2.json') as f:
    data = json.load(f)

# Create a list to store dictionaries containing the sums
rows_data = []

# Iterate over each row in the JSON data
for row in data:
    # Calculate the sum of second values in the row (tour_time_sum)
    tour_time_sum = sum(t[1] for t in row if len(t) >= 2)  # Ensure tuple has at least 2 elements
    # Calculate the sum of third values in the row (tour_price_sum)
    tour_price_sum = sum(t[2] for t in row if len(t) >= 3)  # Ensure tuple has at least 3 elements

    # Store the sums in a dictionary
    row_data = {'Time': tour_time_sum, 'Price': tour_price_sum}
    rows_data.append(row_data)

# Write the data to a CSV file
with open('metrics.csv', 'w', newline='') as csvfile:
    fieldnames = ['Time', 'Price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write each row of data
    for row_data in rows_data:
        writer.writerow(row_data)