import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

def load_drift_scores(json_filepath):
    with open(json_filepath, 'r') as json_file:
        scores = json.load(json_file)
    return scores

st.set_page_config(page_title="Data Drift Dashboard", layout="wide")

st.sidebar.header("🔍 Filters & Reports")

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

report_folders = sorted(
    [f for f in os.listdir(REPORTS_DIR) if os.path.isdir(os.path.join(REPORTS_DIR, f))], 
    reverse=True
)

st.sidebar.markdown(f"📂 **Total Reports:** {len(report_folders)}")
if not report_folders:
    st.sidebar.warning("No reports available! Generate some reports first.")
    st.stop()

selected_report = st.sidebar.selectbox("Select Drift Report:", report_folders, index=0)
report_path = os.path.join(REPORTS_DIR, selected_report)

json_file = f"{selected_report}.json"
html_file = f"{selected_report}.html"
json_path = os.path.join(report_path, json_file)
html_path = os.path.join(report_path, html_file)

if os.path.exists(json_path):
    drift_results = load_drift_scores(json_path)
    df = pd.DataFrame.from_dict(drift_results, orient="index")
    df.index.name = "Feature"
    df.reset_index(inplace=True)

    color_map = {"NO_DRIFT": "green", "POSSIBLE_DRIFT": "orange", "DRIFT": "red"}
    df["color"] = df["drift_category"].map(color_map)

    st.title("🚀 Data Drift Dashboard")
    st.header(f"📝 Report: {selected_report}")

    drift_type = st.sidebar.radio("Filter by Drift Type:", ["ALL", "NO_DRIFT", "POSSIBLE_DRIFT", "DRIFT"], index=0)
    df_filtered = df if drift_type == "ALL" else df[df["drift_category"] == drift_type]

    st.subheader("📊 Drift Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Features Analyzed", len(df))
    col2.metric("Drift Detected", df[df["drift_category"] == "DRIFT"].shape[0], "⚠️")
    col3.metric("Possible Drift", df[df["drift_category"] == "POSSIBLE_DRIFT"].shape[0], "🔍")

    fig = px.bar(df_filtered, x="Feature", y="pvalue", color="drift_category", title="Feature Drift Analysis",
                 color_discrete_map=color_map, height=400)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Feature Drift Details")
    st.dataframe(df_filtered.style.applymap(lambda x: f"background-color: {df.loc[df.index[df['drift_category'] == x], 'color'].values[0]}" if x in color_map else "", subset=['drift_category']))

    if os.path.exists(html_path):
        with open(html_path, "r") as file:
            html_content = file.read()
            st.components.v1.html(html_content, height=800, scrolling=True)
    else:
        st.warning("No HTML report found for this drift scores file.")
else:
    st.sidebar.error("No JSON report found in the selected folder!")
