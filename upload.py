import os
import csv
import time
import json
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Supabase configuration
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Batch size
BATCH_SIZE = 10000

# Base directory for CSV files
BASE_DIR = os.environ.get("BASE_DIR")

def read_table_info():
    with open('parsed_tables.json', 'r') as f:
        return json.load(f)

def read_csv_in_batches(file_path, batch_size, table_info):
    column_types = table_info.get('column_types', {})
    foreign_key_columns = [fk['column_name'] for fk in table_info.get('foreign_keys', [])]

    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        batch = []
        for row in reader:
            processed_row = {}
            for col, value in row.items():
                if value == '':
                    processed_row[col] = None
                else:
                    col_type = column_types.get(col, 'text')
                    processed_row[col] = process_value(value, col_type, col in foreign_key_columns)
            
            batch.append(processed_row)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

def process_value(value, col_type, is_foreign_key):
    if value is None:
        return None
    
    try:
        if col_type == 'integer' or col_type == 'bigint':
            return int(value)
        elif col_type == 'numeric' or col_type == 'double precision':
            return float(value)
        elif col_type == 'boolean':
            return value.lower() in ('true', 't', 'yes', 'y', '1')
        elif col_type == 'date':
            return value
        elif is_foreign_key:
            return value
        else:
            return value
    except ValueError:
        print(f"Warning: Invalid value '{value}' for type {col_type}. Setting to None.")
        return None

def upload_batch(table_name, batch):
    try:
        response = supabase.table(table_name).insert(batch).execute()
        if hasattr(response, 'data'):
            print(f"Successfully uploaded {len(response.data)} rows to {table_name}.")
        else:
            print(f"Upload successful to {table_name}, but no data returned.")
        return True
    except Exception as e:
        print(f"Error uploading batch to {table_name}: {str(e)}")
        return False

def process_table(table_info, release_date):
    table_name = table_info['table_name']
    filename = table_info['filename']

    file_path = os.path.join(BASE_DIR, release_date, 'csv', filename)
    total_rows = 0
    successful_rows = 0

    print(f"Processing table: {table_name}")
    print(f"File path: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    for batch in read_csv_in_batches(file_path, BATCH_SIZE, table_info):
        total_rows += len(batch)
        if upload_batch(table_name, batch):
            successful_rows += len(batch)
        time.sleep(1)  # Add a small delay to avoid rate limiting

    print(f"Upload complete for {table_name}. {successful_rows} out of {total_rows} rows uploaded successfully.")

def upload_dmd_data(release_date):
    print(f"Starting DMD data upload for release date: {release_date}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"BASE_DIR from environment: {BASE_DIR}")

    table_info_list = read_table_info()
    for table_info in table_info_list:
        process_table(table_info, release_date)

    print(f"DMD data upload completed for release date: {release_date}")
    return release_date

if __name__ == "__main__":
    # This section is for testing purposes
    test_release_date = "2024_09_02"
    upload_dmd_data(test_release_date)