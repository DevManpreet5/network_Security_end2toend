from src.entity.model_training import ModelTrainingConfig
import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import yaml
#from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, classification_report

class ModelTrainingComp:
    def __init__(self,config:ModelTrainingConfig):
        self.config=config
        csv_path=os.path.join(config.transformed_path,"train.csv")
        self.df=pd.read_csv(csv_path)
    
    def startTraining(self):
        X = self.df.drop(columns=[self.config.target_col])  
        y = self.df[self.config.target_col]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.config.test_size, random_state=self.config.random_state)
        models = {
    "RandomForest": (RandomForestClassifier(), {
        "n_estimators": [100, 200],
        "max_depth": [10, 20],
        "min_samples_split": [2, 5]
    }),
    "XGBoost": (XGBClassifier(use_label_encoder=False, eval_metric='logloss'), {
        "n_estimators": [100, 200],
        "max_depth": [6, 10],
        "learning_rate": [0.01, 0.1]
    }),
    "LightGBM": (LGBMClassifier(), {
        "n_estimators": [100, 200],
        "max_depth": [-1, 10],
        "learning_rate": [0.01, 0.1]
    })
}

        best_model = None
        best_score = 0
        best_name = ""
        best_params = {}

        for name, (model, params) in models.items():
            print(f"Training {name} with GridSearchCV...")
            grid_search = GridSearchCV(model, params, cv=3, scoring='accuracy', n_jobs=-1)
            grid_search.fit(X_train, y_train)
    
            print(f"Best Params for {name}: {grid_search.best_params_}")
    

        test_preds = grid_search.best_estimator_.predict(X_test)
        test_score = accuracy_score(y_test, test_preds)
        print(f"{name} Test Accuracy: {test_score:.4f}")
    
        if test_score > best_score:
            best_score = test_score
            best_model = grid_search.best_estimator_
            best_name = name
            best_params = grid_search.best_params_


        print("\nBest Model:", best_name)
        print("Test Accuracy:", best_score)


        os.makedirs(self.config.model_path, exist_ok=True)


        model_save_path = os.path.join(self.config.model_path,"best_model.pkl")
        joblib.dump(best_model, model_save_path)
        print(f"Best model saved to {model_save_path}")


        config_save_path = os.path.join(self.config.model_path,"best_model_config.yaml")
        best_model_config = {
            "best_model": best_name,
            "best_params": best_params      }

        with open(config_save_path, "w") as file:
            yaml.dump(best_model_config, file)

        print(f"Best model configuration saved to {config_save_path}")
        



    