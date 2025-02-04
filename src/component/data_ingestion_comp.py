from src.entity.data_ingestion_entity import DataIngestionConfig
import os
import subprocess
from sklearn.model_selection import train_test_split
import pandas as pd
import zipfile

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
    
        if not os.path.exists(self.download_path):
            raise FileNotFoundError(f"Zip file not found: {self.download_path}")

        with zipfile.ZipFile(self.download_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_path)

        print("Download and extraction completed successfully!")


    def combine(self):
        self.unzip()
        directory_path = self.extract_path
        csv_files = [file for file in os.listdir(directory_path) if file.endswith(".csv")]
        chunk_size = 10000
        df_list = []
        i=1
        for file in csv_files:
            file_path = os.path.join(directory_path, file)
            chunks = pd.read_csv(file_path, chunksize=chunk_size)  
            df_list.extend(chunks) 
            print(f'chunk {i} done')
            i=i+1

        self.combined_df = pd.concat(df_list, ignore_index=True)
        self.combined_df.columns = self.combined_df.columns.str.strip()
        print('df merged successfully!')

    
    def savecsv(self):
        self.combine()
        os.makedirs(self.config.raw_path, exist_ok=True)
        csv_path=os.path.join(self.config.raw_path,self.config.file_name)
        self.combined_df.to_csv(csv_path,index=False)
        print('csv saved successfully!')
    
    def split(self):
        self.savecsv()  
        
        csv_path = os.path.join(self.config.raw_path, self.config.file_name)
        
        
        chunk_size = 100000  
        
        train_df = pd.DataFrame()
        test_df = pd.DataFrame()
        eval_df = pd.DataFrame()

        chunks = pd.read_csv(csv_path, chunksize=chunk_size)

        for chunk in chunks:
            
            X = chunk.drop(columns=['Label'])
            y = chunk['Label']
            
    
            X_build, X_eval, y_build, y_eval = train_test_split(
                X, y, test_size=self.config.evaluate_size, random_state=self.config.random_state, stratify=y
            )
            X_train, X_test, y_train, y_test = train_test_split(
                X_build, y_build, test_size=self.config.test_size, random_state=self.config.random_state, stratify=y_build
            )
            
        
            chunk_train_df = X_train.copy()
            chunk_train_df['Label'] = y_train

            chunk_test_df = X_test.copy()
            chunk_test_df['Label'] = y_test

            chunk_eval_df = X_eval.copy()
            chunk_eval_df['Label'] = y_eval


            train_df = pd.concat([train_df, chunk_train_df], ignore_index=True)
            test_df = pd.concat([test_df, chunk_test_df], ignore_index=True)
            eval_df = pd.concat([eval_df, chunk_eval_df], ignore_index=True)


        os.makedirs(self.config.processed_path, exist_ok=True)


        train_df.to_csv(os.path.join(self.config.processed_path, "train.csv"), index=False)
        test_df.to_csv(os.path.join(self.config.processed_path, "test.csv"), index=False)
        eval_df.to_csv(os.path.join(self.config.processed_path, "eval.csv"), index=False)

        print("Datasets saved successfully in:", self.config.processed_path)

    def run(self):
        self.split()