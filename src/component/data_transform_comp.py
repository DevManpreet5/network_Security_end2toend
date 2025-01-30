from src.entity.data_transform_entity import DataTransformConfig
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
import numpy as np


class DataIngestionComponent:
    def __init__(self, config: DataTransformConfig):
        self.config = config
        train_path = os.path.join(self.config.file_path, "train.csv")
        test_path = os.path.join(self.config.file_path, "test.csv")
        self.train_df = pd.read_csv(train_path)
        self.test_df = pd.read_csv(test_path)

    def FeatureEncode(self):
        group_mapping = {
            'BENIGN': 'Normal Traffic',
            'DoS Hulk': 'DoS',
            'DDoS': 'DDoS',
            'PortScan': 'Port Scanning',
            'DoS GoldenEye': 'DoS',
            'FTP-Patator': 'Brute Force',
            'DoS slowloris': 'DoS',
            'DoS Slowhttptest': 'DoS',
            'SSH-Patator': 'Brute Force',
            'Bot': 'Bots',
            'Web Attack � Brute Force': 'Web Attacks',
            'Web Attack � XSS': 'Web Attacks',
            'Infiltration': 'Infiltration',
            'Web Attack � Sql Injection': 'Web Attacks',
            'Heartbleed': 'Miscellaneous'
        }

        self.train_df[self.config.target_col] = self.train_df[self.config.target_col].map(group_mapping)
        self.test_df[self.config.target_col] = self.test_df[self.config.target_col].map(group_mapping)

        le = LabelEncoder()
        self.train_df[self.config.target_col] = le.fit_transform(self.train_df[self.config.target_col])
        self.test_df[self.config.target_col] = le.transform(self.test_df[self.config.target_col])

        label_path = os.path.join(self.config.model_path, "label_encoder.joblib")
        joblib.dump(le, label_path)

        self.X_train = self.train_df.drop(columns=[self.config.target_col])
        self.y_train = self.train_df[self.config.target_col]

        self.X_test = self.test_df.drop(columns=[self.config.target_col])
        self.y_test = self.test_df[self.config.target_col]

    def featureimp(self):
        self.X_train = self.X_train.fillna(0)
        self.X_test = self.X_test.fillna(0)

        self.X_train = np.where(np.isinf(self.X_train), 0, self.X_train)
        self.X_test = np.where(np.isinf(self.X_test), 0, self.X_test)
        imputer = SimpleImputer(strategy='constant', fill_value=0)
        self.X_train = imputer.fit_transform(self.X_train)
        self.X_test = imputer.transform(self.X_test)

        imputer_path = os.path.join(self.config.model_path, "imputer.joblib")
        joblib.dump(imputer, imputer_path)
        scaler = StandardScaler()
        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.transform(self.X_test)  

        scaler_path = os.path.join(self.config.model_path, "scaler.joblib")
        joblib.dump(scaler, scaler_path)
        X_scaled_df = pd.DataFrame(self.X_train, columns=[f"Feature_{i}" for i in range(self.X_train.shape[1])])

        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X_scaled_df, self.y_train)

        feature_importances = pd.DataFrame({'Feature': X_scaled_df.columns, 'Importance': rf.feature_importances_})
        feature_importances = feature_importances.sort_values(by='Importance', ascending=False)

        max_importance = feature_importances['Importance'].max()
        feature_importances['Normalized_Importance'] = feature_importances['Importance'] / max_importance

        thresholds = np.linspace(0.05, 0.5, 10)
        best_score = -np.inf
        best_threshold = None
        best_model = None
        best_features = None

        for threshold in thresholds:
            threshold_value = threshold * max_importance
            selected_features = feature_importances[feature_importances['Importance'] >= threshold_value]['Feature']
            
            X_selected = X_scaled_df[selected_features]

            X_train, X_test, y_train, y_test = train_test_split(X_selected, self.y_train, test_size=0.3, random_state=42)
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            cv_score = np.mean(cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy'))

            if cv_score > best_score:
                best_score = cv_score
                best_threshold = threshold
                best_model = model
                best_features = selected_features

            print(f"Threshold: {threshold:.2f}, CV Score: {cv_score:.4f}")

        print(f"\nBest Threshold: {best_threshold:.2f}")
        print(f"Best CV Score: {best_score:.4f}")
        print(f"Selected Features: {best_features.tolist()}")

        feature_path = os.path.join(self.config.model_path, "selected_features.joblib")
        joblib.dump(best_features.tolist(), feature_path)

    def run(self):
        self.FeatureEncode()
        self.featureimp()
