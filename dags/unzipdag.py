from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import zipfile

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 2, 3),
    'retries': 1,
}

def unzip_dataset():
    ZIP_PATH = "/usr/local/airflow/include/downloadsdags/dataset.zip"
    EXTRACT_PATH = "/usr/local/airflow/include/downloadsdags/"

    if os.path.exists(ZIP_PATH):
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_PATH)
        print(f"✅ Dataset extracted successfully at {EXTRACT_PATH}")
    else:
        print(f"❌ Error: File not found at {ZIP_PATH}")

with DAG('unzip_dataset_dag', default_args=default_args, schedule_interval=None) as dag:
    unzip_task = PythonOperator(
        task_id='unzip_dataset',
        python_callable=unzip_dataset
    )

    unzip_task
