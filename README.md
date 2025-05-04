# CyberFlow

An end-to-end **MLOps pipeline for network intrusion detection** using **Airflow, Docker, and MLflow**. CyberFlow automates **data ingestion, drift detection, A/B model testing, and deployment**, ensuring real-time monitoring and high accuracy.

## Features

**Dual-Pipeline System**

- **One-Time Training Pipeline**: Trains the initial model.
- **Weekly Ingestion Pipeline**: Handles new data while maintaining **98.89% accuracy**.

  **Automated Drift Detection**

- Weekly drift detection with **detailed reports** and visualizations.
- Triggers model retraining if significant drift is detected.

  **A/B Testing & Deployment**

- Compares multiple models in production.
- Automatically deploys the best-performing model.

**Dashboard for Monitoring**

- Real-time performance visualization.
- Model metrics and drift detection reports.

## Visualization

**Streamlit Report**: [View Dashboard](https://network-weeklyreport.streamlit.app/)

![Airflow DAG Running](result_images_readme/Screenshot%202025-02-04%20at%208.51.36%E2%80%AFpm-1.png)

![Airflow DAG Running 2](result_images_readme/Screenshot%202025-02-04%20at%208.51.58%E2%80%AFpm.png)

## Tech Stack

- **Python**
- **Apache Airflow**
- **Docker**
- **MLflow**
- **Streamlit**
