from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import requests

# Define folder path
FOLDER_NAME = "downloads"



os.makedirs(FOLDER_NAME)
FILE_URL = "https://api.nasa.gov/planetary/apod?api_key=TLnQfhbikfGL2U1eL6NM6EiAHm1TUT2DfJF2MU1u"
SAVE_PATH = os.path.join(FOLDER_NAME, "free-programming-books.md")

# Function to download content
def download_file():
    response = requests.get(FILE_URL)
    
    if response.status_code == 200:
        with open(SAVE_PATH, "wb") as file:
            file.write(response.content)
        print(f"File downloaded to {SAVE_PATH}")
    else:
        raise Exception(f"Failed to download file: {response.status_code}")

# Define the DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 2, 1),
    "retries": 1,
}

with DAG(
    dag_id="astro_download_dag",
    default_args=default_args,
    schedule_interval="@daily",  # Runs daily
    catchup=False,
) as dag:

    

    download_task = PythonOperator(
        task_id="download_file",
        python_callable=download_file,
    )

