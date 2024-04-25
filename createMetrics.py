import json
import csv
from collections import Counter
from collections import defaultdict

# Read the JSON file
with open('Data/supermarketjson.json') as f:
    data = json.load(f)

# Create a list to store dictionaries containing the sums and counts
rows_data = []

# Iterate over each row in the JSON data
for row in data:
    # Calculate the sum of second values in the row (tour_time_sum)
    tour_time_sum = sum(t[1] for t in row if len(t) >= 2)  # Ensure tuple has at least 2 elements
    # Calculate the sum of third values in the row (tour_price_sum)
    tour_price_sum = sum(t[2] for t in row if len(t) >= 3)  # Ensure tuple has at least 3 elements

    # Count the number of tuples in the row
    num_items = len(row)

    # Store the sums and counts in a dictionary
    row_data = {'Time': tour_time_sum, 'Price': tour_price_sum, 'Items': num_items}
    rows_data.append(row_data)

# Write the data to a CSV file
with open('Data/metrics.csv', 'w', newline='') as csvfile:
    fieldnames = ['Time', 'Price', 'Items']  # Add 'Items' to the fieldnames
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write each row of data
    for row_data in rows_data:
        writer.writerow(row_data)


# Function to find the most common follow-up for each identifier
def find_most_common_follow_up(data):
    follow_ups = {i: Counter() for i in range(1, 19)}

    # Iterate over each row in the JSON data
    for row in data:
        for i in range(len(row) - 1):
            if row[i] and row[i + 1]:
                current_id = row[i][0]
                follow_up_id = row[i + 1][0]
                if current_id != follow_up_id:
                    follow_ups[current_id][follow_up_id] += 1

    most_common_follow_up = {}
    # Find the most common follow-up for each identifier
    for identifier, follow_up_counter in follow_ups.items():
        if follow_up_counter:
            most_common_follow_up[identifier] = follow_up_counter.most_common(1)[0][0]
        else:
            most_common_follow_up[identifier] = None
    return most_common_follow_up

# Dictionary to store the most common follow-up for each identifier
most_common_follow_up = find_most_common_follow_up(data)

# List to store the counts of most common follow-ups for each row
row_follow_up_counts = []

# Iterate over each row in the JSON data
for row in data:
    row_follow_up_count = 0
    for i in range(len(row) - 1):
        current_id = row[i][0]
        # Check if follow-up tuple exists and the row is not empty
        if i + 1 < len(row) and len(row[i + 1]) > 0:
            follow_up_id = row[i + 1][0]
            # Check if the follow-up is the most common follow-up of the current identifier
            if most_common_follow_up[current_id] == follow_up_id:
                row_follow_up_count += 1
    row_follow_up_counts.append(row_follow_up_count)

# Print the counts of most common follow-ups for each row
print("Counts of Most Common Follow-ups for Each Row")
print("----------------------------------------------")
for identifier, common_follow_up in most_common_follow_up.items():
    print(f"{identifier:<12} {common_follow_up}")


# Read existing data from the CSV file
existing_data = []
with open('Data/metrics.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        existing_data.append(row)

# Modify the existing rows to include the new data
for row, count in zip(existing_data, row_follow_up_counts):
    row['MCFU'] = count

# Write the modified data back to the CSV file
with open('Data/metrics.csv', 'w', newline='') as csvfile:
    fieldnames = ['Time', 'Price', 'Items', 'MCFU']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write each modified row
    for row in existing_data:
        writer.writerow(row)

