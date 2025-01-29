import yaml
import os
import subprocess


with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

config = config['data_ingestion']

download_path = config['raw_zip_path']
extract_path = config['raw_csv_path']


os.makedirs(download_path, exist_ok=True)
os.makedirs(extract_path, exist_ok=True)


download_path = os.path.join(download_path, config['zip_name'])


curl_command = f"curl -L -o {download_path} {config['dataset_url']}"
subprocess.run(curl_command, shell=True, check=True)


unzip_command = f"unzip {download_path} -d {extract_path}"
subprocess.run(unzip_command, shell=True, check=True)

print("Download and extraction completed successfully!")
