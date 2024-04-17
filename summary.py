#!/usr/bin/env python3
import pandas as pd
import json

def load_data(filename):
    """
    Load JSON data from a file into a pandas DataFrame.
    This function ensures that the JSON data is an array of objects,
    which directly maps to a DataFrame structure.
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)  # Load and parse the JSON data

        # Ensure the data is a list (an array of objects)
        if isinstance(data, list):
            return pd.DataFrame(data)
        else:
            print("JSON data is not an array of objects.")
            return pd.DataFrame()
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON from {filename}: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred loading {filename}: {e}")
        return pd.DataFrame()

def summarize_data(data):
    """
    Summarizes data to find the 500 most common federal programs and their statistics.
    """
    if data.empty:
        print("No data to summarize.")
        return pd.DataFrame()

    # Add a column to flag records with findings
    data['has_findings'] = data['findings_count'].apply(lambda x: 1 if x > 0 else 0)

    # Group data by relevant columns and perform required aggregations
    grouped = data.groupby(['federal_program_name', 'federal_agency_prefix', 'federal_award_extension']).agg(
        total_entries=pd.NamedAgg(column='federal_program_name', aggfunc='size'),
        findings_entries=pd.NamedAgg(column='has_findings', aggfunc='sum'),
        total_amount_expended=pd.NamedAgg(column='amount_expended', aggfunc='sum')
    ).reset_index()

    # Sort by the number of entries and get the top 500
    top_500 = grouped.sort_values(by='total_entries', ascending=False).head(500)
    return top_500

def save_data(data, filename):
    """
    Saves the DataFrame to a CSV file.
    """
    if data.empty:
        print("No data available to save.")
        return

    try:
        data.to_csv(filename, index=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Failed to save data to {filename}: {e}")

def main():
    # Load the data from federal_awards_data.json
    data = load_data('federal_awards_data.json')

    # Summarize the data if it was successfully loaded
    if not data.empty:
        summarized_data = summarize_data(data)
        # Save the summarized data to a new CSV file
        save_data(summarized_data, 'mostcommonprograms.csv')
    else:
        print("Data loading failed, no data to process.")

if __name__ == '__main__':
    main()
