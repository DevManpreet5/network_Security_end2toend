import streamlit as st
import os
import streamlit.components.v1 as components  

REPORT_PATH = "templates/datadrift.html"  

st.set_page_config(page_title="Data Drift Report", layout="wide")  
st.title("📊 Weekly Data Drift Report")  
if os.path.exists(REPORT_PATH):  
    with open(REPORT_PATH, "r", encoding="utf-8") as f:  
        report_html = f.read()  
    components.html(report_html, height=800, scrolling=True)  
else:  
    st.error("No Data Drift Report Found! 🚨 Run the script to generate one.")  
