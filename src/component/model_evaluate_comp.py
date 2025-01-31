from src.entity.model_evaluate import ModelevaluatingConfig
import mlflow 
import os
from dotenv import load_dotenv
import json
import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score , classification_report , confusion_matrix

load_dotenv()

class ModelEvaulatingComponent:
    def __init__(self, config: ModelevaluatingConfig):
        self.config = config
        mlflow_tracking_uri = self.config.tracking_uri
        mlflow_tracking_username = os.getenv("MLFLOW_TRACKING_USERNAME")
        mlflow_tracking_password = os.getenv("MLFLOW_TRACKING_PASSWORD")
        os.environ['MLFLOW_TRACKING_URI'] = mlflow_tracking_uri
        os.environ['MLFLOW_TRACKING_USERNAME'] = mlflow_tracking_username
        os.environ['MLFLOW_TRACKING_PASSWORD'] = mlflow_tracking_password

    
    def modeltest(self):
        data=pd.read_csv(self.config.test_dir)
        X=data.drop(columns=[self.config.target_col])
        y=data[self.config.target_col]

        mlflow.set_tracking_uri(self.config.tracking_uri)
        mlflow.set_experiment("evaluating wine model")


        with mlflow.start_run():
      
            print("testing started")
            model_path=os.path.join(self.config.model_path,self.config.model_name)
            best_model = joblib.load(model_path)
            y_pred=best_model.predict(X)
            r2score=r2_score(y_pred,y)
            mlflow.log_metric("r2_score",r2score)
            mae=mean_absolute_error(y_pred,y)
            mse=mean_squared_error(y_pred,y)
            mlflow.log_metric("mae",mae)
            mlflow.log_metric("mse",mse)

            cm=confusion_matrix(y,y_pred)
            cr=classification_report(y,y_pred)
            mlflow.log_text(str(cm),"confusion_matrix.txt")
            mlflow.log_text(cr,"classification_report.txt")

            metrics={
                "r2_score": r2score,
                "mae": mae,
                "mse":mse,
                "confusion_matrix": cm.tolist(),
                "classification_report": cr
            }
            metric_path=os.path.join(self.config.model_path,self.config.metrics_file)
            with open(metric_path, "w") as json_file:
                json.dump(metrics, json_file, indent=4)
                print("saved metrics in file")

  
        
    def run(self):
        self.modeltest()
        print("evaluating done")