from src.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.pipeline.data_transform_pipeline import DataTransformPipeline
from src.pipeline.model_training_pipeline import ModelTrainingPipeline
from src.pipeline.model_evaluate_pipeline import ModelEvaluatingPipeline
import yaml
import os
from airflow import DAG
from airflow.decorators import task
from datetime import datetime

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config

@task
def run_pipeline():
    pipeline = ModelEvaluatingPipeline()
    pipeline.run()

with DAG(
    'one_time_dag',
    start_date=datetime(2025, 1, 31),
    schedule_interval=None,
    catchup=False,
) as dag:
    run_pipeline()
