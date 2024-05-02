import csv
import os
import numpy as np

def process_csv_to_enhanced_csv(input_filename, output_filename):
    directory = 'Data'
    input_file_path = os.path.join(directory, input_filename)
    output_file_path = os.path.join(directory, output_filename)

    with open(input_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        data = []

        # Initialize trip counter
        tripnumber = 1

        # Process each row
        for row in reader:
            purchasenumber = 1  # Initialize purchase counter for the row
            for item in row:
                # Split each item (which is a triple) and expand it with tripnumber and purchasenumber
                elements = item.split()
                if elements:
                    departmentnumber, timebetween, price = int(elements[0]), float(elements[1]), float(elements[2])
                    # Append the expanded data to a list
                    data.append([tripnumber, purchasenumber, departmentnumber, timebetween, price])
                    purchasenumber += 1
            tripnumber += 1  # Increment the trip counter after processing each row

    # Write the processed data back to a new CSV file
    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['tripnumber', 'purchasenumber', 'departmentnumber', 'timebetween', 'price'])
        # Write data
        writer.writerows(data)

def normalize_and_subset_csv(input_filename, output_filename, max_rows=10000):
    directory = 'Data'
    input_file_path = os.path.join(directory, input_filename)
    output_file_path = os.path.join(directory, output_filename)

    with open(input_file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        full_data = [row for row in reader]

    # Convert data to numpy array for easier manipulation
    data_array = np.array(full_data, dtype=float)

    # Normalize 'timebetween' and 'price' columns
    timebetween_col = 3
    price_col = 4
    means = np.mean(data_array[:, [timebetween_col, price_col]], axis=0)
    stds = np.std(data_array[:, [timebetween_col, price_col]], axis=0)
    data_array[:, [timebetween_col, price_col]] = (data_array[:, [timebetween_col, price_col]] - means) / stds

    # Subset data ensuring complete trips
    unique_trips = np.unique(data_array[:, 0])
    subset_data = []
    current_rows = 0

    for trip in unique_trips:
        trip_data = data_array[data_array[:, 0] == trip]
        if current_rows + len(trip_data) > max_rows:
            break
        subset_data.append(trip_data)
        current_rows += len(trip_data)

    # Flatten list of arrays to a single array
    subset_data = np.vstack(subset_data)

    # Write normalized and subset data back to a new CSV
    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['tripnumber', 'purchasenumber', 'departmentnumber', 'timebetween', 'price'])
        writer.writerows(subset_data)


def process_csv_to_enhanced_csv_v2(input_filename, output_filename):
    directory = 'Data'
    input_file_path = os.path.join(directory, input_filename)
    output_file_path = os.path.join(directory, output_filename)

    with open(input_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        data = []

        # Process each row
        for row in reader:
            if row:
                # First, isolate the first element to extract the trip number and its transaction
                first_transaction = row[0].split(':')
                tripnumber = int(first_transaction[0].replace('Transaction ', ''))
                # Include the first transaction part that comes after the trip number
                first_transaction_part = first_transaction[1].strip()

                # We start processing the first transaction separately
                all_transactions = [first_transaction_part] + row[1:]
                purchasenumber = 1  # Initialize purchase counter for each new row (trip)

                for item in all_transactions:
                    item = item.strip()
                    if item:  # Check if the item is not just whitespace
                        elements = item.split()
                        departmentnumber = int(elements[0])
                        timebetween = float(elements[1])
                        price = float(elements[2])
                        # Append the expanded data to a list
                        data.append([tripnumber, purchasenumber, departmentnumber, timebetween, price])
                        purchasenumber += 1  # Increment purchase number for next item in the same trip

    # Write the processed data back to a new CSV file
    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['tripnumber', 'purchasenumber', 'departmentnumber', 'timebetween', 'price'])
        # Write data
        writer.writerows(data)

input_filename = 'supermarket_fixed2.csv'
output_filename = 'supermarket_enhanced.csv'
process_csv_to_enhanced_csv(input_filename, output_filename)

input_filename = 'supermarket_enhanced.csv'
output_filename = 'supermarket_normalized_subset.csv'
normalize_and_subset_csv(input_filename, output_filename)

input_filename = 'TestFile.csv'
output_filename = 'TestFileFormatted.csv'
process_csv_to_enhanced_csv_v2(input_filename, output_filename)