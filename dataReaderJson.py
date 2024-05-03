import csv
import os
import json
import numpy as np

def process_csv_to_json(input_filename, output_filename):
    directory = 'Data'
    input_file_path = os.path.join(directory, input_filename)
    output_file_path = os.path.join(directory, output_filename)

    # Open the input CSV file
    with open(input_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        data = []

        # Process each row
        for row in reader:
            row_data = []  # List to hold processed data for the current row
            for item in row:
                # Process each item by splitting on spaces and converting to numeric types if needed
                elements = item.split()
                converted_elements = [float(element) if '.' in element else int(element) for element in elements]
                row_data.append(converted_elements)
            data.append(row_data)  # Append the whole list of lists for this row to data

    # Write the processed data to a JSON file
    with open(output_file_path, mode='w', newline='') as file:
        json.dump(data, file, indent=4)  # Use indent for better readability in the JSON file


def normalize_and_sample_json(input_filename, output_filename, sample_size):
    directory = 'Data'
    json_file_path = os.path.join(directory, input_filename)
    output_file_path = os.path.join(directory, output_filename)

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    normalized_data = []
    for trip in data:
        if trip:  # Check if the trip list is not empty
            # Ensure all sublists in the trip have the same length by padding shorter ones
            max_len = max(len(item) for item in trip if item)  # Find the maximum length of sublists
            padded_trip = [item + [0]*(max_len - len(item)) for item in trip if item]  # Pad shorter lists

            # Convert the trip data to numpy array
            trip_array = np.array(padded_trip)

            # Normalize the data: mean=0, std=1
            means = np.mean(trip_array, axis=0)
            stds = np.std(trip_array, axis=0)
            normalized_trip = (trip_array - means) / stds

            # Append the normalized trip to normalized_data if it's not empty
            if normalized_trip.size > 0:
                normalized_data.append(normalized_trip.tolist())

    # Sample from the normalized data
    sampled_data_list = []
    if len(normalized_data) > sample_size:
        indices = np.random.choice(len(normalized_data), size=sample_size, replace=False)
        sampled_data_list = [normalized_data[index] for index in indices if len(normalized_data[index]) > 0]
    else:
        sampled_data_list = [trip for trip in normalized_data if len(trip) > 0]

    # Save the sampled data to a JSON file
    with open(output_file_path, mode='w') as file:
        json.dump(sampled_data_list, file, indent=4)

    return sampled_data_list


# Uncomment these lines to execute the processing and normalization steps
input_filename = 'supermarket_fixed2.csv'
output_filename1 = 'supermarketjson.json'
output_filename2 = 'supermarketjsonnormal.json'
process_csv_to_json(input_filename, output_filename1)
normalized_sample = normalize_and_sample_json(output_filename1, output_filename2, 1000)
print(normalized_sample)

