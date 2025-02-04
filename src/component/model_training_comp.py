# import optuna
# from src.entity.model_training import ModelTrainingConfig
# import pandas as pd
# import os
# import joblib
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from lightgbm import LGBMClassifier
# import yaml
# from sklearn.metrics import accuracy_score

# class ModelTrainingComp:
#     def __init__(self, config: ModelTrainingConfig):

#         self.config = config
#         csv_path = os.path.join(config.transformed_path, "train_transformed.csv")
#         self.df = pd.read_csv(csv_path)

#     def objective(self, trial, X_train, y_train, X_test, y_test):
#         model_name = trial.suggest_categorical("model", ["RandomForest", "LightGBM"])
        
#         if model_name == "RandomForest":
#             params = {
#                 "n_estimators": trial.suggest_int("n_estimators", 100, 300, step=50),
#                 "max_depth": trial.suggest_int("max_depth", 10, 30, step=5),
#                 "min_samples_split": trial.suggest_int("min_samples_split", 2, 10)
#             }
#             model = RandomForestClassifier(**params, random_state=self.config.random_state)
#         else:  
#             params = {
#                 "n_estimators": trial.suggest_int("n_estimators", 100, 300, step=50),
#                 "max_depth": trial.suggest_int("max_depth", -1, 20, step=5),
#                 "learning_rate": trial.suggest_loguniform("learning_rate", 0.01, 0.3)
#             }
#             model = LGBMClassifier(**params, verbose=-1, random_state=self.config.random_state)
        
#         model.fit(X_train, y_train)
#         preds = model.predict(X_test)
#         return accuracy_score(y_test, preds)

#     def startTraining(self):
#         X = self.df.drop(columns=[self.config.target_col])  
#         y = self.df[self.config.target_col]
#         X_train, X_test, y_train, y_test = train_test_split(
#             X, y, test_size=self.config.test_size, random_state=self.config.random_state
#         )
#         print("training has started")
        
#         study = optuna.create_study(direction="maximize")
#         study.optimize(lambda trial: self.objective(trial, X_train, y_train, X_test, y_test), n_trials=30)
        
#         best_params = study.best_params
#         best_model_name = best_params.pop("model")
#         print(f"Best Model: {best_model_name} with params {best_params}")
        
#         if best_model_name == "RandomForest":
#             best_model = RandomForestClassifier(**best_params, random_state=self.config.random_state)
#         else:
#             best_model = LGBMClassifier(**best_params, verbose=-1, random_state=self.config.random_state)
        
#         best_model.fit(X_train, y_train)
#         test_preds = best_model.predict(X_test)
#         test_score = accuracy_score(y_test, test_preds)
#         print(f"Test Accuracy: {test_score:.4f}")
        
#         os.makedirs(self.config.model_path, exist_ok=True)
        

#         model_save_path = os.path.join(self.config.model_path, "best_model.pkl")
#         joblib.dump(best_model, model_save_path)
#         print(f"Best model saved to {model_save_path}")
        
#         config_save_path = os.path.join(self.config.model_path, "best_model_config.yaml")
#         best_model_config = {
#             "best_model": best_model_name,
#             "best_params": best_params,
#             "test_accuracy": test_score
#         }
        
#         with open(config_save_path, "w") as file:
#             yaml.dump(best_model_config, file)
        
#         print(f"Best model configuration saved to {config_save_path}")



import os
import joblib
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from src.entity.model_training import ModelTrainingConfig

class ModelTrainingComp:
    def __init__(self, config: ModelTrainingConfig):
        self.config = config
        csv_path = os.path.join(config.transformed_path, "train_transformed.csv")
        self.df = pd.read_csv(csv_path)

    def startTraining(self):
        X = self.df.drop(columns=[self.config.target_col])  
        y = self.df[self.config.target_col]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.config.test_size, random_state=self.config.random_state
        )
        print("Training has started")

        best_params = {
            "n_estimators": 300,
            "max_depth": 30,
            "min_samples_split": 10,
        }
        best_model = RandomForestClassifier(**best_params, random_state=self.config.random_state)

        best_model.fit(X_train, y_train)
        test_preds = best_model.predict(X_test)
        test_score = accuracy_score(y_test, test_preds)
        print(f"Test Accuracy: {test_score:.6f}")

        os.makedirs(self.config.model_path, exist_ok=True)
        
        model_save_path = os.path.join(self.config.model_path, "best_model.pkl")
        joblib.dump(best_model, model_save_path)
        print(f"Best model saved to {model_save_path}")
    
        config_save_path = os.path.join(self.config.model_path, "best_model_config.yaml")
        best_model_config = {
            "best_model": "RandomForest",
            "best_params": best_params,
            "test_accuracy": test_score
        }
        
        with open(config_save_path, "w") as file:
            yaml.dump(best_model_config, file)
        
        print(f"Best model configuration saved to {config_save_path}")
