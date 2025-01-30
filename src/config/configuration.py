import yaml 
from src.entity.data_ingestion_entity import DataIngestionConfig
from src.entity.data_transform_entity import DataTransformConfig
from src.entity.model_training import ModelTrainingConfig

class ConfigurationManager:
    def __init__ (self,config_path='config.yaml',params_path='params.yaml'):
        self.config=self.read_yaml(config_path)
        self.params=self.read_yaml(params_path)
    
    @staticmethod
    def read_yaml(path):
        with open(path,'r') as file:
            return yaml.safe_load(file)
    
    def get_data_ingestion(self):
        config=self.config['data_ingestion']
        params=self.params['data_ingestion']
        return DataIngestionConfig(
            raw_zip_path=config['raw_zip_path'],
            raw_csv_path=config['raw_csv_path'],
            zip_name=config['zip_name'],
            dataset_url=config['dataset_url'],
            raw_path=config['raw_path'],
            file_name=config['file_name'],
            processed_path=config['processed_path'],
            test_size=params['test_size'],
            evaluate_size=params['evaluate_size'],
            random_state=params['random_state']
        )

    def get_data_transform(self):
        config=self.config['data_transform']

        return DataTransformConfig(
            file_path= config['file_path'],
            transformed_path= config['transformed_path'],
            model_path= config['model_path'],
            target_col= config['target_col'],
            features_pkl_name = config['features_pkl_name']
        )

    def get_model_training(self):
        config=self.config['model_training']
        params=self.params['model_training']

        return ModelTrainingConfig(
            transformed_path=config['transformed_path'],
            target_col=config['target_col'],
            model_path=config['model_path'],
            test_size=params['test_size'],
            random_state=params['random_state']
        )