from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

DIRECTORY_PATH = "/usr/local/airflow/include/downloadsdags/"
def list_files():
    if os.path.exists(DIRECTORY_PATH):
        files = os.listdir(DIRECTORY_PATH)
        print(f"📂 Files in {DIRECTORY_PATH}:")
        for file in files:
            print(file)
    else:
        print(f"❌ Error: Directory {DIRECTORY_PATH} not found.")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 2, 3),
    'retries': 1,
}

with DAG('list_files_dag', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    list_files_task = PythonOperator(
        task_id='list_files',
        python_callable=list_files
    )

    list_files_task  

