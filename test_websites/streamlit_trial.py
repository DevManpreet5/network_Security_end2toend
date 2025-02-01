# import streamlit as st
# import os
# import streamlit.components.v1 as components  
# import pandas as pd
# import whylogs
# import numpy as np
# import os
# from whylogs.viz import NotebookProfileVisualizer
# st.set_page_config(page_title="Data Drift Report", layout="wide")  
# st.title("📊 Weekly Data Drift Report") 
# columns_to_keep = [
#     "Max Packet Length", "Packet Length Variance", "Packet Length Std", "Destination Port",
#     "Avg Bwd Segment Size", "Total Length of Fwd Packets", "Average Packet Size",
#     "Bwd Packet Length Max", "Subflow Fwd Bytes", "Total Length of Bwd Packets",
#     "Fwd Packet Length Max", "Subflow Bwd Bytes", "Bwd Packet Length Std",
#     "Init_Win_bytes_forward", "Packet Length Mean", "Fwd Packet Length Mean",
#     "Bwd Packet Length Mean", "Init_Win_bytes_backward", "Total Fwd Packets",
#     "Avg Fwd Segment Size", "Fwd Header Length.1", "Fwd IAT Max", "Bwd Header Length",
#     "Fwd IAT Std", "Bwd Packets/s", "Fwd Header Length", "Flow Bytes/s", "Idle Mean",
#     "Subflow Bwd Packets", "Total Backward Packets", "act_data_pkt_fwd", "ACK Flag Count",
#     "Subflow Fwd Packets", "Label"
# ]

# def load_and_clean_data():
#     reference = pd.read_csv('artifact/data/processed/train.csv')
#     current = pd.read_csv('artifact/data/processed/eval.csv')

#     reference = reference[columns_to_keep]
#     current = current[columns_to_keep]
    
#     reference.replace([np.inf, -np.inf], 0, inplace=True)
#     reference.fillna(0, inplace=True)
    
#     current.replace([np.inf, -np.inf], 0, inplace=True)
#     current.fillna(0, inplace=True)

#     return reference, current

# def generate_drift_report(reference, current):
    
#     reference_profile = whylogs.log(reference)
#     current_profile = whylogs.log(current)
#     reference_profile_view = reference_profile.view()
#     current_profile_view = current_profile.view()
#     visualization = NotebookProfileVisualizer()
#     path=os.path.join(os.getcwd(),"templates")
#     visualization.set_profiles(target_profile_view=current_profile_view, reference_profile_view=reference_profile_view)
#     visualization.write(
#     rendered_html=visualization.summary_drift_report(),
#     html_file_name=path + "/datadrift",
# )
# path=os.path.join(os.getcwd(),"templates")
# html_file_name=os.path.join(path,'datadrift.html')

# REPORT_PATH = html_file_name
# reference, current = load_and_clean_data()
# generate_drift_report(reference, current)  
# if os.path.exists(REPORT_PATH):  
#     with open(REPORT_PATH, "r", encoding="utf-8") as f:  
#         report_html = f.read()  
#     components.html(report_html, height=800, scrolling=True)  
# else:  
#     st.error("No Data Drift Report Found! 🚨 Run the script to generate one.")  



import streamlit as st
import os
import streamlit.components.v1 as components  

st.set_page_config(page_title="Data Drift Report", layout="wide")  

st.title("📊 Weekly Data Drift Reports")
st.sidebar.header("Select Report")

REPORTS_DIR = "reports"

if not os.path.exists(REPORTS_DIR):
    st.error("No reports found! Generate some first.")
    st.stop()

report_files = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".html")]
report_names = [os.path.splitext(f)[0] for f in report_files]  

if not report_files:
    st.error("No reports available! Generate reports to see them here.")
    st.stop()

selected_name = st.sidebar.selectbox("Choose a report:", report_names)
selected_report = selected_name + ".html"

st.header(selected_name) 

report_path = os.path.join(REPORTS_DIR, selected_report)
if os.path.exists(report_path):
    with open(report_path, "r", encoding="utf-8") as f:
        report_html = f.read()
    components.html(report_html, height=800, scrolling=True)
else:
    st.error("Selected report not found! Try another one.")
