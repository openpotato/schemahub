import json
import os
import requests
import argparse

def download_json_files(catalog_file_path, base_target_folder):
    # Read the JSON catalog file
    with open(catalog_file_path, 'r') as file:
        data = json.load(file)

    # Iterate through the schemas
    for schema in data['schemas']:
        relative_target_folder = schema['targetFolder']
        urls = schema['urls']

        # Create the full path to the target folder under the base folder
        full_target_folder = os.path.join(base_target_folder, relative_target_folder)

        # Create the target folder if it doesn't exist
        if not os.path.exists(full_target_folder):
            os.makedirs(full_target_folder)

        # Download each JSON file and save it to the target folder
        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                file_name = os.path.join(full_target_folder, url.split('/')[-1])
                with open(file_name, 'w', encoding='utf8') as json_file:
                    json_file.write(response.text)
                print(f"Downloaded and saved {url} to {file_name}")
            else:
                print(f"Failed to download {url}")

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Download JSON schemas and save them to specified folders.")
    parser.add_argument('catalog_file_path', type=str, help='Path to the input JSON file.')
    parser.add_argument('base_target_folder', type=str, help='Base folder where target folders will be created.')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the download function with the provided arguments
    download_json_files(args.catalog_file_path, args.base_target_folder)
