from src.entity.data_ingestion_entity import DataIngestionConfig
import os
import subprocess


class DataIngestionComponent:
    def __init__(self,config:DataIngestionConfig):
        self.config=config
        self.download_dir = self.config['raw_zip_path']
        self.extract_path = self.config['raw_csv_path']
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.extract_path, exist_ok=True)
        self.download_path = os.path.join(self.download_dir, self.config['zip_name'])
    
    def download(self):
        curl_command = f"curl -L -o {self.download_path} {self.config['dataset_url']}"
        subprocess.run(curl_command, shell=True, check=True)
    
    def unzip(self):
        unzip_command = f"unzip {self.download_path} -d {self.extract_path}"
        subprocess.run(unzip_command, shell=True, check=True)
        print("Download and extraction completed successfully!")

