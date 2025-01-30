from dataclasses import dataclass
@dataclass
class ModelevaluatingConfig:
  test_dir: str
  model_path: str
  model_name: str
  metrics_file: str
  tracking_uri: str