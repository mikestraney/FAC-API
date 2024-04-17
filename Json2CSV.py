#!/usr/bin/env python3
import pandas as pd

def convert_json_to_csv(json_filename, csv_filename):
    """
    Converts a JSON file to a CSV file.

    Args:
        json_filename (str): The path to the source JSON file.
        csv_filename (str): The path for the output CSV file.
    """
    try:
        # Load the JSON data into a DataFrame
        data = pd.read_json(json_filename)
        
        # Save the DataFrame to a CSV file
        data.to_csv(csv_filename, index=False)
        print(f"Successfully converted {json_filename} to {csv_filename}.")
    except Exception as e:
        print(f"Failed to convert {json_filename} to {csv_filename}: {e}")

def main():
    # Convert federal awards data from JSON to CSV
    convert_json_to_csv('federal_awards_data.json', 'federal_awards_data.csv')
    
    # Convert general data from JSON to CSV
    convert_json_to_csv('general_data.json', 'general_data.csv')

if __name__ == '__main__':
    main()
