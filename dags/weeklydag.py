from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import zipfile
import requests

# Define paths
data_dir = "/opt/airflow/data/network_intrusion"
zip_path = f"{data_dir}/dataset.zip"
kaggle_url = "https://www.kaggle.com/datasets/chethuhn/network-intrusion-dataset/download"

# Ensure directory exists
def ensure_data_dir():
    os.makedirs(data_dir, exist_ok=True)

# Download ZIP file
def download_dataset():
    response = requests.get(kaggle_url, stream=True)
    with open(zip_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

# Extract ZIP file
def extract_zip():
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(data_dir)

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 6),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'download_kaggle_dataset',
    default_args=default_args,
    description='Download and extract dataset from Kaggle without API',
    schedule_interval='@daily',
    catchup=False,
)

# Ensure the data directory exists
task_create_dir = PythonOperator(
    task_id='create_data_directory',
    python_callable=ensure_data_dir,
    dag=dag,
)

# Download dataset from Kaggle without API
task_download = PythonOperator(
    task_id='download_dataset',
    python_callable=download_dataset,
    dag=dag,
)

# Extract dataset
task_extract = PythonOperator(
    task_id='extract_dataset',
    python_callable=extract_zip,
    dag=dag,
)

# Task dependencies
task_create_dir >> task_download >> task_extract
