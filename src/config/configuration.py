import yaml 
from src.entity.data_ingestion_entity import DataIngestionConfig

class ConfigurationManager:
    def __init__ (self,config_path='config.yaml',params_path='params.yaml'):
        self.config=read_yaml(config_path)
        self.params=read_yaml(params_path)
    
    @staticmethod
    def read_yaml(path):
        with open(path,'r') as file:
            return yaml.safe_load(file)
    
    def get_data_ingestion(self):
        config=self.config['data_ingestion']
        params=self.config['data_ingestion']
        return DataIngestionConfig(
            raw_zip_path=config['raw_zip_path'],
            raw_csv_path=config['raw_csv_path'],
            zip_name=config['zip_name'],
            raw_csv_path=config['raw_csv_path'],
            dataset_url=config['dataset_url'],
            raw_path=config['raw_path'],
            file_name=config['file_name'],
            processed_path=config['processed_path'],
            test_size=params['test_size'],
            evaluate_size=params['evaluate_size'],
            random_state=config['random_state']
        )
