import pandas as pd
import whylogs
import numpy as np
import os
from flask import Flask, render_template, send_file
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
    reference = pd.read_csv('artifact/data/processed/train.csv')
    current = pd.read_csv('artifact/data/processed/eval.csv')

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
    path=os.path.join(os.getcwd(),"templates")
    visualization.set_profiles(target_profile_view=current_profile_view, reference_profile_view=reference_profile_view)
    visualization.write(
    rendered_html=visualization.summary_drift_report(),
    html_file_name=path + "/datadrift",
)

@app.route('/')
def index():
    #reference, current = load_and_clean_data()
    # generate_drift_report(reference, current)  
     return send_file("templates/datadrift.html")
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
