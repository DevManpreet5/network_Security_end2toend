from src.pipeline.model_evaluate_pipeline import ModelEvaluatingPipeline
from src.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.pipeline.data_transform_pipeline import DataTransformPipeline
from src.pipeline.model_training_pipeline import ModelTrainingPipeline
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
    pipelineING=DataIngestionPipeline()
    pipelineING.run()

    config = load_config('config.yaml')
    train_csv_path = os.path.join(config['data_transform']['file_path'], "train.csv")
    test_csv_path = os.path.join(config['data_transform']['file_path'], "test.csv")
    pipelineTRA = DataTransformPipeline()
    pipelineTRA.run(train_csv_path, test_csv_path)

    pipelineTraining=ModelTrainingPipeline()
    pipelineTraining.run()

    pipelineevaluate=ModelEvaluatingPipeline()
    pipelineevaluate.run()


with DAG(
    'one_time_dag',
    start_date=datetime(2025, 1, 31),
    schedule_interval=None,
    catchup=False,
) as dag:
    run_pipeline()
