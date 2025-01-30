# Required Libraries
try:
    import evidently
except:
    !pip install git+https://github.com/evidentlyai/evidently.git
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, RegressionPreset
from evidently import ColumnMapping
from evidently.report import Report

reference = pd.read_csv('artifact/data/transformed/train_transformed.csv')
current = pd.read_csv('artifact/data/transformed/test_transformed.csv')

target = "Label"

numerical_features = [
    "Max Packet Length", "Packet Length Variance", "Packet Length Std", "Destination Port", 
    "Avg Bwd Segment Size", "Total Length of Fwd Packets", "Average Packet Size", 
    "Bwd Packet Length Max", "Subflow Fwd Bytes", "Total Length of Bwd Packets", 
    "Fwd Packet Length Max", "Subflow Bwd Bytes", "Bwd Packet Length Std", 
    "Init_Win_bytes_forward", "Packet Length Mean", "Fwd Packet Length Mean", 
    "Bwd Packet Length Mean", "Init_Win_bytes_backward", "Total Fwd Packets", 
    "Avg Fwd Segment Size", "Fwd Header Length.1", "Fwd IAT Max", "Bwd Header Length", 
    "Fwd IAT Std", "Bwd Packets/s", "Fwd Header Length", "Flow Bytes/s", 
    "Idle Mean", "Subflow Bwd Packets", "Total Backward Packets", "act_data_pkt_fwd", 
    "ACK Flag Count", "Subflow Fwd Packets"
]

classifier = RandomForestClassifier(random_state=0, n_estimators=50)
classifier.fit(reference[numerical_features], reference[target])

reference["prediction"] = classifier.predict(reference[numerical_features])
current["prediction"] = classifier.predict(current[numerical_features])

column_mapping = ColumnMapping()
column_mapping.target = target
column_mapping.prediction = "prediction"
column_mapping.numerical_features = numerical_features

data_drift = Report(metrics=[DataDriftPreset()])
data_drift.run(current_data=current,
               reference_data=reference,
               column_mapping=None)

data_drift.show()
data_drift.save_html("data_drift_report.html")
print("Report saved as 'data_drift_report.html'")