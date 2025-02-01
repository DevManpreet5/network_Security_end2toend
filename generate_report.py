import os
import pandas as pd
import whylogs
import numpy as np
from datetime import datetime
from whylogs.viz import NotebookProfileVisualizer

columns_to_keep = [
    "Max Packet Length", "Packet Length Variance", "Packet Length Std", "Destination Port",
    "Avg Bwd Segment Size", "Total Length of Fwd Packets", "Average Packet Size",
    "Bwd Packet Length Max", "Subflow Fwd Bytes", "Total Length of Bwd Packets",
    "Fwd Packet Length Max", "Subflow Bwd Bytes", "Bwd Packet Length Std",
    "Init_Win_bytes_forward", "Packet Length Mean", "Fwd Packet Length Mean",
    "Bwd Packet Length Mean", "Init_Win_bytes_backward", "Total Fwd Packets",
    "Avg Fwd Segment Size", "Fwd Header Length.1", "Fwd IAT Max", "Bwd Header Length",
    "Fwd IAT Std", "Bwd Packets/s", "Fwd Header Length", "Flow Bytes/s", "Idle Mean",
    "Subflow Bwd Packets", "Total Backward Packets", "act_data_pkt_fwd", "ACK Flag Count",
    "Subflow Fwd Packets", "Label"
]

def load_and_sample_data(sample_fraction=0.1):
    reference = pd.read_csv('artifact/data/processed/train.csv')
    current = pd.read_csv('artifact/data/processed/eval.csv')
    reference = reference[columns_to_keep].sample(frac=sample_fraction, random_state=42)
    current = current[columns_to_keep].sample(frac=sample_fraction, random_state=42)
    reference.replace([np.inf, -np.inf], 0, inplace=True)
    reference.fillna(0, inplace=True)

    current.replace([np.inf, -np.inf], 0, inplace=True)
    current.fillna(0, inplace=True)

    return reference, current

def generate_drift_report(reference, current, save_path):
    reference_profile = whylogs.log(reference)
    current_profile = whylogs.log(current)
    
    reference_profile_view = reference_profile.view()
    current_profile_view = current_profile.view()
    
    visualization = NotebookProfileVisualizer()
    visualization.set_profiles(target_profile_view=current_profile_view, reference_profile_view=reference_profile_view)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    visualization.write(rendered_html=visualization.summary_drift_report(), html_file_name=save_path + f'/{timestamp}')

def main():
    save_path = os.path.join(os.getcwd(), "reports")
    os.makedirs(save_path, exist_ok=True)  

    for i in range(4):  
        reference, current = load_and_sample_data()
        generate_drift_report(reference, current, save_path)

if __name__ == "__main__":
    main()
