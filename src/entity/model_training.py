from dataclasses import dataclass

@dataclass
class ModelTrainingConfig:
    transformed_path: str
    target_col: str
    model_path: str
    test_size: float
    random_state: int


