from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    raw_zip_path: str
    zip_name: str
    raw_csv_path: str
    dataset_url: str
    raw_path: str
    file_name: str
    processed_path: str
    test_size: float
    evaluate_size: float
    random_state: str 
