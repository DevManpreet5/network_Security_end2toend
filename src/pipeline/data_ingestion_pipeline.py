from src.config.configuration import ConfigurationManager
from src.component.data_ingestion_comp import DataIngestionComponent

class DataIngestionPipeline:
    def __init__(self):
        self.config_manager=ConfigurationManager()
    
    def run(self):
        config=self.config_manager.get_data_ingestion()
        data_ingestion=DataIngestionComponent(config)
        data_ingestion.run()