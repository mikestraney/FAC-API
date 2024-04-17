#!/usr/bin/env python3
import os
import sys
import argparse
import requests
import pandas as pd
import urllib.parse

# Constants for API URLs
API_URL_GENERAL = "https://api.fac.gov/general"
API_URL_FEDERAL_AWARDS = "https://api.fac.gov/federal_awards"

# Constants for file paths
KEY_FILE = '.key'
GENERAL_DATA_FILE = 'general_data.json'
FEDERAL_AWARDS_DATA_FILE = 'federal_awards_data.json'

def load_api_key(api_key_path):
    """
    Load the API key from a file.
    """
    with open(api_key_path, 'r') as file:
        return file.read().strip()

def fetch_data(api_key, base_url, params, limit=4999):
    """
    Fetches data from a specified API endpoint using pagination.
    """
    headers = {'Accept': 'application/json', 'X-Api-Key': api_key}
    offset = 0
    all_data = pd.DataFrame()

    while True:
        query_string = urllib.parse.urlencode(params) + f"&limit={limit}&offset={offset}"
        full_url = f"{base_url}?{query_string}"
        response = requests.get(full_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"API Request failed with URL {full_url}, status code {response.status_code}, and message: {response.text}")
        
        data = response.json()
        if not data:
            break
        all_data = pd.concat([all_data, pd.DataFrame(data)], ignore_index=True)
        offset += limit
        print(f"Fetched {limit} records from offset {offset}...")

    return all_data

def save_data(data, filename, format='json'):
    """
    Saves a DataFrame to a file in the specified format.
    """
    if format == 'json':
        data.to_json(filename, orient='records')
    elif format == 'csv':
        data.to_csv(filename, index=False)
    print(f"Data successfully saved to {filename} in {format} format.")

def process_data(api_key, force_refresh=False):
    """
    Process general and federal data, checking existing files or fetching new data if forced.
    """
    if not os.path.exists(GENERAL_DATA_FILE) or force_refresh:
        general_data = fetch_data(api_key, API_URL_GENERAL, params_general)
        save_data(general_data, GENERAL_DATA_FILE)
    else:
        print("General data file already exists. Skipping fetch.")
        general_data = pd.read_json(GENERAL_DATA_FILE)

    if not os.path.exists(FEDERAL_AWARDS_DATA_FILE) or force_refresh:
        federal_awards_data = fetch_data(api_key, API_URL_FEDERAL_AWARDS, params_federal)
        save_data(federal_awards_data, FEDERAL_AWARDS_DATA_FILE)
    else:
        print("Federal awards data file already exists. Skipping fetch.")
        federal_awards_data = pd.read_json(FEDERAL_AWARDS_DATA_FILE)

    return pd.merge(general_data, federal_awards_data, on='report_id', how='left', suffixes=('_gen', '_awd'))

def main():
    parser = argparse.ArgumentParser(description='Fetch and optionally export data from FAC API')
    parser.add_argument('--auditor_ein', type=str, help='Auditor EIN to filter data')
    parser.add_argument('--audit_year', type=str, help='Audit year to filter data')
    parser.add_argument('--export_csv', action='store_true', help='Export data to CSV if set')
    parser.add_argument('--export_json', action='store_true', help='Export data to JSON if set')
    parser.add_argument('--force_refresh', action='store_true', help='Force data refresh by refetching from the API')
    args = parser.parse_args()

    api_key = load_api_key(KEY_FILE)

    params_general = {}
    params_federal = {'is_major': 'eq.Y'}
    if args.auditor_ein:
        params_general['auditor_ein'] = f'eq.{args.auditor_ein}'
    if args.audit_year:
        params_federal['audit_year'] = f'eq.{args.audit_year}'

    combined_data = process_data(api_key, force_refresh=args.force_refresh)

    if args.export_csv:
        save_data(combined_data, 'output.csv', 'csv')
    if args.export_json:
        save_data(combined_data, 'output.json', 'json')

if __name__ == '__main__':
    main()
