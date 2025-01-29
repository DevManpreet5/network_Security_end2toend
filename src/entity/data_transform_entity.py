from dataclasses import dataclass

@dataclass
class DataTransformConfig:
    file_path: str
    transformed_path: str
    model_path: str
    target_col: str
    features_pkl_name: str
    feature_threshold: float

