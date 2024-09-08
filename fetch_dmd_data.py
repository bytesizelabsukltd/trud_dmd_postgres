import os
import requests
import hashlib
from datetime import datetime
from zipfile import ZipFile
import glob
import shutil
from dotenv import load_dotenv
from parse_to_csv import parse_to_csv

# Load environment variables
load_dotenv()

def get_latest_release_info(api_key, item_number):
    url = f'https://isd.digital.nhs.uk/trud/api/v1/keys/{api_key}/items/{item_number}/releases?latest'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get('releases', [])[0]
    else:
        print(f"Failed to retrieve the latest release for item {item_number}. Status code: {response.status_code}")
        print(response.text)
        return None

def download_and_process_item(api_key, item_number, target_dir, is_dmdtool=False, is_bnf=False):
    latest_release = get_latest_release_info(api_key, item_number)
    
    if not latest_release:
        return

    archive_file_url = latest_release.get('archiveFileUrl')
    archive_file_sha256 = latest_release.get('archiveFileSha256')
    archive_file_name = latest_release.get('archiveFileName')
    
    if is_dmdtool:
        target_dir = os.path.join(target_dir, 'dmdTool')
    
    os.makedirs(target_dir, exist_ok=True)
    file_path = os.path.join(target_dir, archive_file_name)
    
    print(f"Downloading {archive_file_url}...")
    download_response = requests.get(archive_file_url)
    
    if download_response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(download_response.content)
        print(f"File downloaded and saved to {file_path}")
        
        with open(file_path, 'rb') as file:
            file_content = file.read()
            file_sha256 = hashlib.sha256(file_content).hexdigest().upper()
        
        if file_sha256 == archive_file_sha256:
            print("SHA-256 checksum matches.")
        else:
            print("SHA-256 checksum does NOT match.")
            print(f"Expected: {archive_file_sha256}")
            print(f"Calculated: {file_sha256}")
        
        with ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        print(f"File unzipped to {target_dir}")
        
        if is_dmdtool:
            process_dmdtool_files(target_dir)
        elif is_bnf:
            process_bnf_files(target_dir)
        else:
            process_dmd_files(target_dir)
        
        try:
            os.remove(file_path)
            print(f"Zip file deleted: {file_path}")
        except FileNotFoundError:
            print(f"Warning: Zip file not found for deletion: {file_path}")
        except PermissionError:
            print(f"Warning: Permission denied when trying to delete zip file: {file_path}")
        except Exception as e:
            print(f"Warning: Unable to delete zip file due to an unexpected error: {e}")
    else:
        print(f"Failed to download the file. Status code: {download_response.status_code}")
        print(download_response.text)

def process_dmd_files(target_dir):
    nested_zip_pattern = os.path.join(target_dir, "week*-GTIN.zip")
    nested_zip_files = glob.glob(nested_zip_pattern)
    
    if nested_zip_files:
        nested_zip_file = nested_zip_files[0]
        with ZipFile(nested_zip_file, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        print(f"Nested zip file extracted: {nested_zip_file}")
    
    xml_folder = os.path.join(target_dir, "xml")
    xsd_folder = os.path.join(target_dir, "xsd")
    os.makedirs(xml_folder, exist_ok=True)
    os.makedirs(xsd_folder, exist_ok=True)
    
    for file in os.listdir(target_dir):
        if file.endswith(".xml"):
            os.rename(os.path.join(target_dir, file), os.path.join(xml_folder, file))
        elif file.endswith(".xsd"):
            os.rename(os.path.join(target_dir, file), os.path.join(xsd_folder, file))
    
    print("Files sorted into xml and xsd folders.")
    
    if nested_zip_files:
        os.remove(nested_zip_file)
        print("Nested zip file deleted.")

def process_bnf_files(target_dir):
    nested_zip_pattern = os.path.join(target_dir, "week*-BNF.zip")
    nested_zip_files = glob.glob(nested_zip_pattern)
    
    if nested_zip_files:
        nested_zip_file = nested_zip_files[0]
        with ZipFile(nested_zip_file, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        print(f"Nested BNF zip file extracted: {nested_zip_file}")
    
    xml_folder = os.path.join(target_dir, "xml")
    xsd_folder = os.path.join(target_dir, "xsd")
    os.makedirs(xml_folder, exist_ok=True)
    os.makedirs(xsd_folder, exist_ok=True)
    
    for file in os.listdir(target_dir):
        if file.endswith(".xml"):
            os.rename(os.path.join(target_dir, file), os.path.join(xml_folder, file))
        elif file.endswith(".xsd"):
            os.rename(os.path.join(target_dir, file), os.path.join(xsd_folder, file))
    
    print("BNF files sorted into xml and xsd folders.")
    
    if nested_zip_files:
        os.remove(nested_zip_file)
        print("Nested BNF zip file deleted.")

def process_dmdtool_files(target_dir):
    dmd_extract_tool_dir = os.path.join(target_dir, "dmd_extract_tool")
    xsl_source_dir = os.path.join(dmd_extract_tool_dir, "xsl")
    dmd_xsl_dir = os.path.join(os.path.dirname(target_dir), "dmd_xsl")
    
    # Copy XSL files
    if os.path.exists(xsl_source_dir):
        shutil.copytree(xsl_source_dir, dmd_xsl_dir, dirs_exist_ok=True)
        print(f"XSL files copied to {dmd_xsl_dir}")
    else:
        print(f"XSL source directory not found: {xsl_source_dir}")
    
    # Delete everything except 'docs' folder
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        if item != 'docs' and os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Deleted directory: {item_path}")
        elif item != 'docs' and os.path.isfile(item_path):
            os.remove(item_path)
            print(f"Deleted file: {item_path}")

def verify_directory_structure(base_dir):
    expected_dirs = ['xml', 'xsd', 'dmd_xsl', 'docs']
    for dir_name in expected_dirs:
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"Verified: {dir_name} directory exists")
            if dir_name == 'dmd_xsl':
                xsl_files = glob.glob(os.path.join(dir_path, '*.xsl'))
                print(f"Number of XSL files in dmd_xsl: {len(xsl_files)}")
        else:
            print(f"Warning: {dir_name} directory is missing")

def remove_dmdtool_folder(base_dir):
    dmdtool_dir = os.path.join(base_dir, 'dmdTool')
    if os.path.exists(dmdtool_dir):
        try:
            shutil.rmtree(dmdtool_dir)
            print(f"Removed dmdTool directory: {dmdtool_dir}")
        except Exception as e:
            print(f"Error removing dmdTool directory: {e}")
    else:
        print("dmdTool directory not found, no need to remove.")

def remove_historic_codes_folder(base_dir):
    historic_codes_dir = os.path.join(base_dir, 'HISTORIC_CODES')
    if os.path.exists(historic_codes_dir):
        try:
            shutil.rmtree(historic_codes_dir)
            print(f"Removed HISTORIC_CODES directory: {historic_codes_dir}")
        except Exception as e:
            print(f"Error removing HISTORIC_CODES directory: {e}")
    else:
        print("HISTORIC_CODES directory not found, no need to remove.")

def process_dmd_data():
    """
    Main function to process DMD data.
    
    Returns:
    str: The formatted release date (YYYY_MM_DD) if successful, None otherwise.
    """
    api_key = os.getenv('TRUD_API_KEY')
    base_dir = os.getenv('BASE_DIR')

    # Get DMD release info first to determine the dated folder
    dmd_release = get_latest_release_info(api_key, '24')
    if dmd_release:
        release_date = dmd_release.get('releaseDate')
        release_date_formatted = datetime.strptime(release_date, "%Y-%m-%d").strftime("%Y_%m_%d")
        dated_dir = os.path.join(base_dir, release_date_formatted)

        if os.path.exists(dated_dir):
            print(f"Directory for {release_date_formatted} already exists. We've already fetched the latest data.")
        else:
            # Process item 24 (DMD)
            download_and_process_item(api_key, '24', dated_dir)

            # Process item 25 (BNF)
            download_and_process_item(api_key, '25', dated_dir, is_bnf=True)

            # Process item 239 (DMDTool)
            download_and_process_item(api_key, '239', dated_dir, is_dmdtool=True)

            # Remove dmdTool folder
            remove_dmdtool_folder(dated_dir)

            # Remove HISTORIC_CODES folder
            remove_historic_codes_folder(dated_dir)

            # Verify the final directory structure
            verify_directory_structure(dated_dir)

            print("Processing complete for DMD, BNF, and DMDTool.")
        
            # Call parse_to_csv function with the release date
            parse_to_csv(release_date_formatted)
            print(f"Parsing to CSV completed for release date: {release_date_formatted}")
        
        return release_date_formatted
    else:
        print("Failed to retrieve DMD release information. Aborting process.")
        return None

if __name__ == "__main__":
    release_date = process_dmd_data()
    if release_date:
        print(f"DMD data processed successfully. Release date: {release_date}")
    else:
        print("DMD data processing failed.")