import json
import csv
from collections import Counter
import pandas as pd

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





# Read the original CSV file without header and skipping the first row
original_df = pd.read_csv('Data/supermarket_enhanced.csv', header=None, skiprows=1)

# Group the DataFrame by the trip number (1st column) and concatenate the values in the 3rd column
all_paths = original_df.groupby(0)[2].apply(tuple).tolist()

# Count the occurrences of each path
path_counts = Counter(all_paths)

# Filter out paths with counter less than 6
filtered_paths = {path: count for path, count in path_counts.items() }

# Convert the filtered paths to a DataFrame
path_counts_df = pd.DataFrame(list(filtered_paths.items()), columns=['Path', 'Count'])

# Sort path_counts_df by count in descending order
path_counts_df = path_counts_df.sort_values(by='Count', ascending=False)

# Write the result to a new CSV file
path_counts_df.to_csv('Data/common_paths.csv', index=False)


# Read the CSV file into a pandas DataFrame
df = pd.read_csv('Data/supermarket_enhanced.csv', header=None, skiprows=1)

# Rename columns for clarity
df.columns = ['Identifier', 'Column2', 'Integer', 'Column4', 'Column5']

# Group by 'Identifier' and count unique values in 'Integer' column
unique_counts = df.groupby('Identifier')['Integer'].nunique().reset_index()

# Create a dictionary to store the counts for each identifier
counts_dict = dict(zip(unique_counts['Identifier'], unique_counts['Integer']))

# Read existing data from the CSV file
existing_data = []
with open('Data/metrics.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        existing_data.append(row)

# Modify the existing rows to include the new data
for row_number, row in enumerate(existing_data, start=1):
    identifier = row_number
    count = counts_dict.get(identifier, 0)
    row['UItems'] = count


# Write the modified data back to the CSV file
with open('Data/metrics.csv', 'w', newline='') as csvfile:
    fieldnames = ['Time', 'Price', 'Items', 'MCFU', 'UItems']  # Adding 'Identifier' as a fieldname
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write each modified row
    for row in existing_data:
        writer.writerow(row)


# Read existing data from the CSV file
existing_data = []
with open('Data/metrics.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        existing_data.append(row)

# Iterate through each row and add a new column for the division of "MCFU" and "UItems"
for row in existing_data:
    division_result = int(row['MCFU']) / int(row['UItems'])
    row['Division'] = division_result

# Write the modified data back to the CSV file
with open('Data/metrics.csv', 'w', newline='') as csvfile:
    fieldnames = ['Time', 'Price', 'Items', 'MCFU', 'UItems', 'Division']  # Adding 'Division' as a fieldname
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write each modified row
    for row in existing_data:
        writer.writerow(row)