from src.config.configuration import ConfigurationManager
from src.component.data_transform_comp import DataTransformer

class DataTransformPipeline:
    def __init__(self):
        self.config_manager=ConfigurationManager()
    
    def run(self, train_csv_path, test_csv_path):
        config=self.config_manager.get_data_transform()
        data_transform = DataTransformer(train_csv_path, test_csv_path, config)
        data_transform.run()
