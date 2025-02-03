from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import yaml
import os
from src.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.pipeline.data_transform_pipeline import DataTransformPipeline
from src.pipeline.model_training_pipeline import ModelTrainingPipeline
from src.pipeline.model_evaluate_pipeline import ModelEvaluatingPipeline
def load_config(config_path):
    with open(config_path, "r") as file:
        return yaml.load(file, Loader=yaml.FullLoader)

with DAG(
    "one_time_dag",
    start_date=datetime(2025, 1, 31),
    schedule_interval=None,
    catchup=False,
) as dag:

    @task
    def ingest_data():
        pipeline = DataIngestionPipeline()
        pipeline.run()

    # @task(do_xcom_push=False)
    # def transform_data():
    #     config = load_config("config.yaml")
    #     train_csv_path = os.path.join(config["data_transform"]["file_path"], "train.csv")
    #     test_csv_path = os.path.join(config["data_transform"]["file_path"], "test.csv")
    #     pipeline = DataTransformPipeline()
    #     pipeline.run(train_csv_path, test_csv_path)

    # @task
    # def train_model():
    #     pipeline = ModelTrainingPipeline()
    #     pipeline.run()

    # @task
    # def evaluate_model():
    #     pipeline = ModelEvaluatingPipeline()
    #     pipeline.run()
    ingest = ingest_data()
    # transform = transform_data()
    # train = train_model()
    #evaluate = evaluate_model()
    # ingest >> transform >> train >> evaluate
