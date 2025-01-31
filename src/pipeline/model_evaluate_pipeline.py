from src.config.configuration import ConfigurationManager
from src.component.model_validation_comp import ModelEvaulatingComponent

class ModelEvaluatingPipeline:
    def __init__(self):
        self.config_manager=ConfigurationManager()
    
    def run(self):
        config=self.config_manager.get_model_training()
        model_training=ModelEvaulatingComponent(config)
        model_training.run()