# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from airflow.operators.python import PythonOperator
# from datetime import datetime
# import os
# import requests
# FOLDER_NAME = os.path.join("/usr/local/airflow/include", "downloadsdags")
# #/usr/local/airflow/dags/downloadsdags/nasa_apod.json
# #FOLDER_NAME = os.path.join("include", "downloadsdags")
# FILE_URL = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY" 
# SAVE_PATH = os.path.join(FOLDER_NAME, "nasa_apod.json")

# def download_file():
#     os.makedirs(FOLDER_NAME, exist_ok=True) 
    
#     response = requests.get(FILE_URL)
#     if response.status_code == 200:
#         with open(SAVE_PATH, "wb") as file:
#             file.write(response.content)
#         print(f"✅ File successfully downloaded to {SAVE_PATH}")
#     else:
#         raise Exception(f"❌ Failed to download file: {response.status_code}")

# default_args = {
#     "owner": "airflow",
#     "start_date": datetime(2024, 2, 1),
#     "retries": 1,
# }

# with DAG(
#     dag_id="astro_download_dag",
#     default_args=default_args,
#     schedule_interval="@daily",  
#     catchup=False,
# ) as dag:

#     create_folder = BashOperator(
#         task_id="create_folder",
#         bash_command=f"mkdir -p {FOLDER_NAME}",  
#     )

#     download_task = PythonOperator(
#         task_id="download_file",
#         python_callable=download_file,
#     )
    
#     create_folder >> download_task



# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from airflow.operators.python import PythonOperator
# from datetime import datetime
# import os
# import subprocess
# import pandas as pd
# from sklearn.model_selection import train_test_split

# # Paths inside Airflow
# BASE_DIR = "/usr/local/airflow/include/downloadsdags"
# EXTRACT_DIR = os.path.join(BASE_DIR, "extracted")
# PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
# ZIP_PATH = os.path.join(BASE_DIR, "dataset.zip")

# # Kaggle dataset URL (must be a direct public link)
# DATASET_URL = "https://www.kaggle.com/datasets/uciml/iris/download?datasetVersionNumber=1"

# # Function to download dataset
# def download_dataset():
#     os.makedirs(BASE_DIR, exist_ok=True)
#     curl_command = f"curl -L -o {ZIP_PATH} '{DATASET_URL}'"
#     subprocess.run(curl_command, shell=True, check=True)
#     print(f"✅ Dataset downloaded: {ZIP_PATH}")

# # Function to extract dataset
# def extract_dataset():
#     os.makedirs(EXTRACT_DIR, exist_ok=True)
#     unzip_command = f"unzip -o {ZIP_PATH} -d {EXTRACT_DIR}"
#     subprocess.run(unzip_command, shell=True, check=True)
#     print(f"✅ Dataset extracted: {EXTRACT_DIR}")

# # Function to process dataset
# def process_dataset():
#     os.makedirs(PROCESSED_DIR, exist_ok=True)

#     # Read all CSV files in extracted folder
#     csv_files = [file for file in os.listdir(EXTRACT_DIR) if file.endswith(".csv")]
#     if not csv_files:
#         raise Exception("❌ No CSV files found in extracted folder!")

#     df_list = [pd.read_csv(os.path.join(EXTRACT_DIR, file)) for file in csv_files]
#     combined_df = pd.concat(df_list, ignore_index=True)
#     combined_df.columns = combined_df.columns.str.strip()  # Remove extra spaces
#     print("✅ Data merged successfully!")

#     # Splitting dataset
#     X = combined_df.drop(columns=['Label'])
#     y = combined_df['Label']
#     X_build, X_eval, y_build, y_eval = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
#     X_train, X_test, y_train, y_test = train_test_split(X_build, y_build, test_size=0.25, random_state=42, stratify=y_build)

#     # Create train, test, eval dataframes
#     train_df = X_train.copy()
#     train_df['Label'] = y_train

#     test_df = X_test.copy()
#     test_df['Label'] = y_test

#     eval_df = X_eval.copy()
#     eval_df['Label'] = y_eval

#     # Save datasets
#     train_df.to_csv(os.path.join(PROCESSED_DIR, "train.csv"), index=False)
#     test_df.to_csv(os.path.join(PROCESSED_DIR, "test.csv"), index=False)
#     eval_df.to_csv(os.path.join(PROCESSED_DIR, "eval.csv"), index=False)

#     print("✅ Processed datasets saved in:", PROCESSED_DIR)

# # Define DAG
# default_args = {
#     "owner": "airflow",
#     "start_date": datetime(2024, 2, 1),
#     "retries": 1,
# }

# with DAG(
#     dag_id="kaggle_download_dag",
#     default_args=default_args,
#     schedule_interval="@daily",
#     catchup=False,
# ) as dag:

#     create_folder = BashOperator(
#         task_id="create_folders",
#         bash_command=f"mkdir -p {BASE_DIR} {EXTRACT_DIR} {PROCESSED_DIR}",
#     )

#     download_task = PythonOperator(
#         task_id="download_dataset",
#         python_callable=download_dataset,
#     )

#     extract_task = PythonOperator(
#         task_id="extract_dataset",
#         python_callable=extract_dataset,
#     )

#     process_task = PythonOperator(
#         task_id="process_dataset",
#         python_callable=process_dataset,
#     )

#     # Task dependencies
#     create_folder >> download_task >> extract_task >> process_task


from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import zipfile
import subprocess

# Define paths
DOWNLOAD_DIR = "/usr/local/airflow/include/downloadsdags"
ZIP_PATH = os.path.join(DOWNLOAD_DIR, "dataset.zip")
EXTRACT_PATH = os.path.join(DOWNLOAD_DIR, "extracted")

# Ensure directories exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACT_PATH, exist_ok=True)

def download_dataset():
    dataset_url = "https://www.kaggle.com/datasets/uciml/iris/download?datasetVersionNumber=1"
    curl_command = f"curl -L -o {ZIP_PATH} {dataset_url}"
    subprocess.run(curl_command, shell=True, check=True)
    print(f"✅ Dataset downloaded successfully! {ZIP_PATH}")
    def debug_path():
        print(f"Dataset exists: {os.path.exists('/usr/local/airflow/include/downloadsdags/dataset.zip')}")
        print(f"Current working directory: {os.getcwd()}")
    debug_path()


def extract_dataset():
    if not os.path.exists(ZIP_PATH):
        raise FileNotFoundError("Dataset ZIP file not found!")
    
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_PATH)
    print("✅ Dataset extracted successfully!")

def process_dataset():
    csv_files = [f for f in os.listdir(EXTRACT_PATH) if f.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError("No CSV files found in extracted dataset!")
    print(f"✅ Found {len(csv_files)} CSV files for processing.")

# Define DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 2, 3),
    'retries': 1,
}

dag = DAG(
    'kaggle_download_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)

download_task = PythonOperator(
    task_id='download_dataset',
    python_callable=download_dataset,
    dag=dag,
)

extract_task = PythonOperator(
    task_id='extract_dataset',
    python_callable=extract_dataset,
    dag=dag,
)

process_task = PythonOperator(
    task_id='process_dataset',
    python_callable=process_dataset,
    dag=dag,
)

download_task >> extract_task >> process_task
