import csv
import os
import json


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


# Example usage
input_filename = 'supermarket.csv'
output_filename = 'supermarketnew2.json'
process_csv_to_json(input_filename, output_filename)
