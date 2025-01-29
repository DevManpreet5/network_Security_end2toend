from src.entity.data_ingestion_entity import DataIngestionConfig
import os
import subprocess
from sklearn.model_selection import train_test_split
import pandas as pd


class DataIngestionComponent:
    def __init__(self,config:DataIngestionConfig):
        self.config=config
        self.download_dir = self.config.raw_zip_path
        self.extract_path = self.config.raw_csv_path
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.extract_path, exist_ok=True)
        self.download_path = os.path.join(self.download_dir, self.config.zip_name)
    
    def download(self):
        curl_command = f"curl -L -o {self.download_path} {self.config.dataset_url}"
        subprocess.run(curl_command, shell=True, check=True)
    
    def unzip(self):
        self.download()
        unzip_command = f"unzip {self.download_path} -d {self.extract_path}"
        subprocess.run(unzip_command, shell=True, check=True)
        print("Download and extraction completed successfully!")

    def combine(self):
        self.unzip()
        directory_path = self.extract_path
        csv_files = [file for file in os.listdir(directory_path) if file.endswith(".csv")]
        df_list = [pd.read_csv(os.path.join(directory_path, file)) for file in csv_files]
        self.combined_df = pd.concat(df_list, ignore_index=True)
        self.combined_df.columns = self.combined_df.columns.str.strip()
        print('df merged successfully!')
    
    def savecsv(self):
        self.combine()
        os.makedirs(self.config.raw_path, exist_ok=True)
        csv_path=os.path.join(self.config.raw_path,self.config.file_name)
        self.combined_df.to_csv(csv_path,index=False)
        print('csv saved successfully!')
    
    


        
        
    def run(self):
        # self.savecsv()






