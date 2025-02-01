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

st.set_page_config(page_title="Advanced Data Drift Dashboard", layout="wide")

st.sidebar.header("🔍 Filters & Reports")

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

json_files = sorted([f for f in os.listdir(REPORTS_DIR) if f.endswith(".json")], reverse=True)

if json_files:
    selected_json_file = st.sidebar.selectbox("Select Drift Report:", json_files, index=0)
    json_path = os.path.join(REPORTS_DIR, selected_json_file)

    drift_results = load_drift_scores(json_path)
    df = pd.DataFrame.from_dict(drift_results, orient="index")
    df.index.name = "Feature"
    df.reset_index(inplace=True)
    color_map = {"NO_DRIFT": "green", "POSSIBLE_DRIFT": "orange", "DRIFT": "red"}
    df["color"] = df["drift_category"].map(color_map)

    st.title("🚀 Advanced Data Drift Dashboard")


    drift_type = st.sidebar.radio("Filter by Drift Type:", ["ALL", "NO_DRIFT", "POSSIBLE_DRIFT", "DRIFT"], index=0)

    df_filtered = df if drift_type == "ALL" else df[df["drift_category"] == drift_type]

    st.header("📊 Drift Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Features Analyzed", len(df))
    col2.metric("Drift Detected", df[df["drift_category"] == "DRIFT"].shape[0], "⚠️")
    col3.metric("Possible Drift", df[df["drift_category"] == "POSSIBLE_DRIFT"].shape[0], "🔍")

    fig = px.bar(df, x="Feature", y="pvalue", color="drift_category", title="Feature Drift Analysis",
                 color_discrete_map=color_map, height=400)
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("📋 Feature Drift Details")
    st.dataframe(df_filtered.style.applymap(lambda x: f"background-color: {df.loc[df.index[df['drift_category'] == x], 'color'].values[0]}" if x in color_map else "", subset=['drift_category']))
else:
    st.sidebar.error("No reports available! Generate some reports first.")
