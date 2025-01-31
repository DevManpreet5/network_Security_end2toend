import pandas as pd
import whylogs
import numpy as np
import os
from flask import Flask, render_template_string, jsonify
from whylogs.viz import NotebookProfileVisualizer

app = Flask(__name__)

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

def load_and_clean_data():
    reference = pd.read_csv(r'/Users/s/Desktop/mlops/network_Security_end2end/artifact/data/processed/train.csv')
    current = pd.read_csv(r'/Users/s/Desktop/mlops/network_Security_end2end/artifact/data/processed/eval.csv')

    reference = reference[columns_to_keep]
    current = current[columns_to_keep]
    
    reference.replace([np.inf, -np.inf], 0, inplace=True)
    reference.fillna(0, inplace=True)
    
    current.replace([np.inf, -np.inf], 0, inplace=True)
    current.fillna(0, inplace=True)

    return reference, current

def generate_drift_report(reference, current):
    reference_profile = whylogs.log(reference)
    current_profile = whylogs.log(current)
    
    reference_profile_view = reference_profile.view()
    current_profile_view = current_profile.view()

    visualization = NotebookProfileVisualizer()
    visualization.set_profiles(target_profile_view=current_profile_view, reference_profile_view=reference_profile_view)
    output_dir = os.path.dirname(__file__)  
    output_file_path = os.path.join(output_dir, "flask_report", "datadrift_report.html")
    
    visualization.write(
        rendered_html=visualization.summary_drift_report(),
        html_file_name=output_file_path
    )
    
    return output_file_path

@app.route('/')
def index():
    reference, current = load_and_clean_data()
    drift_report_path = generate_drift_report(reference, current)
    
    with open(drift_report_path, 'r') as file:
        report_html = file.read()

    return render_template_string(report_html)

@app.route('/api/drift')
def api_drift():
    reference, current = load_and_clean_data()
    reference_profile = whylogs.log(reference)
    current_profile = whylogs.log(current)

    reference_profile_view = reference_profile.view()
    current_profile_view = current_profile.view()

    visualization = NotebookProfileVisualizer()
    visualization.set_profiles(target_profile_view=current_profile_view, reference_profile_view=reference_profile_view)
    drift_summary = visualization.summary_drift_report()

    return jsonify({"drift_summary": drift_summary})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
