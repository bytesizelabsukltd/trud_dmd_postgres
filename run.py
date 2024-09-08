import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
from fetch_dmd_data import process_dmd_data
from upload import upload_dmd_data
from create_tables import create_supabase_tables

# Load environment variables
load_dotenv()

# Initialize Supabase client with regular key
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Initialize Supabase client with service key
supabase_service: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

def run_pipeline():
    print("Starting the pipeline...")

    # Create Supabase tables first
    print("Creating Supabase tables...")
    create_supabase_tables('supabase_tables.sql')
    print("Supabase tables created or verified.")

    # DMD Processing
    print("Processing DMD data...")
    release_date = process_dmd_data()

    if release_date:
        print(f"DMD data processed successfully. Release date: {release_date}")
        
        # Call the deleteDMDData function using the service client
        print("Deleting existing DMD data...")
        try:
            data, error = supabase_service.rpc('deleteDMDData').execute()
            if error:
                print(f"Error deleting DMD data: {error}")
            else:
                print("Existing DMD data deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting DMD data: {str(e)}")

        # Upload new DMD data
        upload_result = upload_dmd_data(release_date)
        if upload_result:
            print(f"DMD data uploaded successfully for release date: {upload_result}")
        else:
            print("DMD data upload failed.")
    else:
        print("DMD data processing failed.")

    print("Pipeline completed.")

if __name__ == "__main__":
    run_pipeline()