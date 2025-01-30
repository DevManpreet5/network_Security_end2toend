from src.config.configuration import ConfigurationManager
from src.component.model_training_comp import ModelTrainingComp

class ModelTrainingPipeline:
    def __init__(self):
        self.config_manager=ConfigurationManager()
    
    def run(self):
        config=self.config_manager.get_model_training()
        model_training=ModelTrainingComp(config)
        model_training.startTraining()