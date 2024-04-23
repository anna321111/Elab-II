import csv
import os
import json
import numpy as np


def process_csv_to_json(input_filename, output_filename):
    # Define the directory containing the CSV files
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
                # Process each item by splitting on spaces and converting to numeric types
                elements = item.split()
                converted_elements = [float(element) if '.' in element else int(element) for element in elements]
                row_data.append(converted_elements)
            data.append(row_data)  # Append the whole list of lists for this row to data

    # Write the processed data to a JSON file
    with open(output_file_path, mode='w', newline='') as file:
        json.dump(data, file, indent=4)  # Use indent for better readability in the JSON file

def normalize_and_sample_json(input_filename, sample_size):
    directory = 'Data'
    json_file_path = os.path.join(directory, input_filename)

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Flatten the list of lists and remove empty sublists
    flattened_data = [item for sublist in data for item in sublist if item]

    # Convert to numpy array for easier manipulation
    data_array = np.array(flattened_data)

    # Normalize the data
    # Calculate mean and std along columns
    means = np.mean(data_array, axis=0)
    stds = np.std(data_array, axis=0)

    # Avoid division by zero in case of std deviation being zero
    stds[stds == 0] = 1

    normalized_data = (data_array - means) / stds

    # Select a random subset of 1000 rows if the dataset is large enough
    if len(normalized_data) > sample_size:
        sampled_indices = np.random.choice(len(normalized_data), size=sample_size, replace=False)
        sampled_data = normalized_data[sampled_indices]
    else:
        sampled_data = normalized_data

    # Save the sampled data back to JSON
    sampled_data_list = sampled_data.tolist()  # Convert numpy array back to list for JSON serialization
    output_filename = 'normalized_sampled.json'
    output_file_path = os.path.join(directory, output_filename)
    with open(output_file_path, 'w') as file:
        json.dump(sampled_data_list, file, indent=4)

    return sampled_data_list

# uncomment these lines to create a new json file from the csv file
# input_filename = 'supermarket.csv'
output_filename = 'supermarketnew2.json'
# process_csv_to_json(input_filename, output_filename)

normalized_sample = normalize_and_sample_json(output_filename, 1000)

