from flask import Flask
from prometheus_client import start_http_server, Gauge, generate_latest
import pandas as pd
import whylogs as wl
import numpy as np
from whylogs.viz.drift.column_drift_algorithms import calculate_drift_scores
from flask import Response

app = Flask(__name__)

drift_metric = Gauge("data_drift_score", "Data Drift Score", ["feature", "category"])

columns_to_keep = ["Max Packet Length", "Packet Length Variance", "Packet Length Std", "Destination Port"]

reference = pd.read_csv("artifact/data/processed/train.csv")[columns_to_keep]
current = pd.read_csv("artifact/data/processed/eval.csv")[columns_to_keep]

for df in [reference, current]:
    df.replace([np.inf, -np.inf], 0, inplace=True)
    df.fillna(0, inplace=True)

reference_profile_view = wl.log(reference).view()
current_profile_view = wl.log(current).view()

drift_scores = calculate_drift_scores(
    target_view=current_profile_view, 
    reference_view=reference_profile_view,
    with_thresholds=True
)

def get_drift_category(p_value):
    if p_value < 0.01:
        return "Drift"
    elif p_value < 0.05:
        return "Possible Drift"
    else:
        return "No Drift"

drift_results = []

for feature, score_data in drift_scores.items():
    drift_score = score_data.get("statistic", 0)
    p_value = score_data.get("p_value", 1)  
    category = get_drift_category(p_value)
    explanation = f"Feature {feature} has a drift score of {drift_score:.4f}. P-value: {p_value:.4f}. Category: {category}."
    
    drift_results.append({
        "feature": feature,
        "drift_score": drift_score,
        "p_value": p_value,
        "category": category,
        "explanation": explanation
    })
    
    drift_metric.labels(feature=feature, category=category).set(drift_score)

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype="text/plain")

@app.route('/drift_results')
def drift_results_route():
    return Response({"drift_results": drift_results}, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
