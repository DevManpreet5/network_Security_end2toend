from src.config.configuration import ConfigurationManager
from src.component.model_training_comp import ModelTrainingComp

class ModelTrainingPipeline:
    def __init__(self):
        self.config_manager=ConfigurationManager()
    
    def run(self):
        config=self.config_manager.get_model_training()
        data_ingestion=ModelTrainingComp(config)
        data_ingestion.run()