from src.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.pipeline.data_transform_pipeline import DataTransformPipeline
from src.pipeline.model_training_pipeline import ModelTrainingPipeline
import yaml
import os

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config

if __name__=="__main__":
    #pipelineING=DataIngestionPipeline()
    #pipelineING.run()

    # config = load_config('config.yaml')
    # train_csv_path = os.path.join(config['data_transform']['file_path'], "train.csv")
    # test_csv_path = os.path.join(config['data_transform']['file_path'], "test.csv")
    # pipeline = DataTransformPipeline()
    # pipeline.run(train_csv_path, test_csv_path)

    pipeline=ModelTrainingPipeline()
    pipeline.run()


