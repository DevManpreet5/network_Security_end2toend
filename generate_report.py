import os
import json
import pandas as pd
import whylogs
import numpy as np
from datetime import datetime
from whylogs.viz import NotebookProfileVisualizer
from whylogs.viz.drift.column_drift_algorithms import calculate_drift_scores

def load_and_sample_data(sample_fraction=0.1):
    reference = pd.read_csv('artifact/data/processed/train.csv')
    current = pd.read_csv('artifact/data/processed/eval.csv')
    reference = reference.sample(frac=sample_fraction, random_state=42)
    current = current.sample(frac=sample_fraction, random_state=42)
    reference.replace([np.inf, -np.inf], 0, inplace=True)
    reference.fillna(0, inplace=True)
    current.replace([np.inf, -np.inf], 0, inplace=True)
    current.fillna(0, inplace=True)
    return reference, current

def generate_drift_report(reference, current, base_save_path):
    reference_profile = whylogs.log(reference)
    current_profile = whylogs.log(current)
    reference_profile_view = reference_profile.view()
    current_profile_view = current_profile.view()
    
    visualization = NotebookProfileVisualizer()
    visualization.set_profiles(target_profile_view=current_profile_view, reference_profile_view=reference_profile_view)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_folder = os.path.join(base_save_path, timestamp)
    os.makedirs(report_folder, exist_ok=True)
    json_filename = os.path.join(report_folder, f"{timestamp}.json")
    visualization.write(rendered_html=visualization.summary_drift_report(), html_file_name=report_folder +f"/{timestamp}")
    
    scores = calculate_drift_scores(target_view=current_profile_view, reference_view=reference_profile_view, with_thresholds=True)
    with open(json_filename, 'w') as json_file:
        json.dump(scores, json_file, indent=4, default=str)

def main():
    save_path = os.path.join(os.getcwd(), "reports")
    os.makedirs(save_path, exist_ok=True)
    
    for i in range(4):  
        reference, current = load_and_sample_data()
        generate_drift_report(reference, current, save_path)

if __name__ == "__main__":
    main()
