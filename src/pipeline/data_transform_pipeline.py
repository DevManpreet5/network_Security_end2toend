from src.config.configuration import ConfigurationManager
from src.component.data_transform_comp import DataTransformConfig

class DataTransformPipeline:
    def __init__(self):
        self.config_manager=ConfigurationManager()
    
    def run(self):
        config=self.config_manager.get_data_transform()
        data_ingestion=DataTransformConfig(config)
        data_ingestion.run()