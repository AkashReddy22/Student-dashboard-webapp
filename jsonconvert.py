import csv
import json

# Define the input and output file names
input_csv = 'MC2_Schedule.csv'
output_json = 'students.json'

# Initialize an empty list to store the converted JSON data
json_data = []

# Read the CSV file
with open(input_csv, mode='r', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=',')  # Tab-separated values
    for row in csvreader:
        # Construct the JSON structure for each row
        entry = {
            "email": row['Student_asu_email'].strip(),
            "first_name": row['Student_first_name'].strip(),
            "last_name": row['Student_last_name'].strip(),
            "asurite_id": row['Student_asurite_id'].split('@')[0].lower(),
        }
        json_data.append(entry)

# Write the JSON output
with open(output_json, 'w', encoding='utf-8') as jsonfile:
    json.dump(json_data, jsonfile, indent=4)

print(f'Converted data has been written to {output_json}')
