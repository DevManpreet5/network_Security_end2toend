from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import requests
FOLDER_NAME = os.path.join("/usr/local/airflow/include", "downloadsdags")
#/usr/local/airflow/dags/downloadsdags/nasa_apod.json
#FOLDER_NAME = os.path.join("include", "downloadsdags")
FILE_URL = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY" 
SAVE_PATH = os.path.join(FOLDER_NAME, "nasa_apod.json")

def download_file():
    os.makedirs(FOLDER_NAME, exist_ok=True) 
    
    response = requests.get(FILE_URL)
    if response.status_code == 200:
        with open(SAVE_PATH, "wb") as file:
            file.write(response.content)
        print(f"✅ File successfully downloaded to {SAVE_PATH}")
    else:
        raise Exception(f"❌ Failed to download file: {response.status_code}")

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 2, 1),
    "retries": 1,
}

with DAG(
    dag_id="astro_download_dag",
    default_args=default_args,
    schedule_interval="@daily",  
    catchup=False,
) as dag:

    create_folder = BashOperator(
        task_id="create_folder",
        bash_command=f"mkdir -p {FOLDER_NAME}",  
    )

    download_task = PythonOperator(
        task_id="download_file",
        python_callable=download_file,
    )
    
    create_folder >> download_task
