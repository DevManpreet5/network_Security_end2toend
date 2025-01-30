from src.entity.data_transform_entity import DataTransformConfig
import os
import pandas as pd
import numpy as np
import joblib
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class DataTransformer:
    def __init__(self, train_csv_path, test_csv_path,config:DataTransformConfig):
        self.config = config
        self.train_df = pd.read_csv(train_csv_path)
        self.test_df = pd.read_csv(test_csv_path)
        os.makedirs(self.config.model_path, exist_ok=True)
        os.makedirs(self.config.transformed_path, exist_ok=True)

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

    def HandleInfinityNull(self):
        for df in [self.train_df, self.test_df]:
            df.replace([np.inf, -np.inf], 0, inplace=True)
            df.fillna(0, inplace=True)

    def LabelEncode(self):
        self.encoder = LabelEncoder()
        self.train_df[self.config.target_col] = self.encoder.fit_transform(self.train_df[self.config.target_col])
        self.test_df[self.config.target_col] = self.encoder.transform(self.test_df[self.config.target_col])
        joblib.dump(self.encoder, os.path.join(self.config.model_path, "label_encoder.joblib"))

    def ScaleAndImpute(self):
        X_train = self.train_df.drop(columns=[self.config.target_col])
        X_test = self.test_df.drop(columns=[self.config.target_col])

        self.imputer = SimpleImputer(strategy="constant", fill_value=0)
        X_train = self.imputer.fit_transform(X_train)
        X_test = self.imputer.transform(X_test)
        joblib.dump(self.imputer, os.path.join(self.config.model_path, "imputer.joblib"))

        self.scaler = StandardScaler()
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)
        joblib.dump(self.scaler, os.path.join(self.config.model_path, "scaler.joblib"))

        self.train_df.iloc[:, :-1] = X_train.astype(float)
        self.test_df.iloc[:, :-1] = X_test.astype(float)


    def SaveTransformedData(self):
        selected_features_path = os.path.join(self.config.model_path, "selected_features.joblib")
    
        if os.path.exists(selected_features_path):
            best_features = joblib.load(selected_features_path)
            best_features.append(self.config.target_col)
            self.train_df = self.train_df[best_features]
            self.test_df = self.test_df[best_features]
    
        self.train_df.to_csv(os.path.join(self.config.transformed_path, "train_transformed.csv"), index=False)
        self.test_df.to_csv(os.path.join(self.config.transformed_path, "test_transformed.csv"), index=False)


    def FeatureSelectionBinarySearch(self):
        sample_df = self.train_df.sample(frac=0.1, random_state=42)
        X_sample = sample_df.drop(columns=[self.config.target_col])
        y_sample = sample_df[self.config.target_col]

        rf = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
        rf.fit(X_sample, y_sample)

        feature_importances = pd.DataFrame({
            'Feature': X_sample.columns,
            'Importance': rf.feature_importances_
        }).sort_values(by='Importance', ascending=False)

        max_importance = feature_importances['Importance'].max()
        feature_importances['Normalized_Importance'] = feature_importances['Importance'] / max_importance

        low, high = 0.05, 0.5
        best_threshold, best_score, best_features = None, -np.inf, None

        while high - low > 0.01:
            threshold = (low + high) / 2
            selected_features = feature_importances[feature_importances['Normalized_Importance'] >= threshold]['Feature']

            if len(selected_features) == 0:
                high = threshold
                continue

            X_selected = sample_df[selected_features]
            X_train, X_test, y_train, y_test = train_test_split(X_selected, y_sample, test_size=0.3, random_state=42)

            model = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
            model.fit(X_train, y_train)
            cv_score = np.mean(cross_val_score(model, X_train, y_train, cv=3, scoring='accuracy'))

            if cv_score > best_score:
                best_score = cv_score
                best_threshold = threshold
                best_features = selected_features

            if cv_score > best_score:
                low = threshold
            else:
                high = threshold

        joblib.dump(best_features.tolist(), os.path.join(self.config.model_path, "selected_features.joblib"))

    def run(self):
        self.FeatureEncode()
        self.HandleInfinityNull()
        self.LabelEncode()
        self.ScaleAndImpute()
        self.FeatureSelectionBinarySearch()
        self.SaveTransformedData()
