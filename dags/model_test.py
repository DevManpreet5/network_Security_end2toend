from src.pipeline.model_evaluate_pipeline import ModelEvaluatingPipeline
import yaml
import os
from airflow import DAG
from airflow.decorators import task
from datetime import datetime


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
