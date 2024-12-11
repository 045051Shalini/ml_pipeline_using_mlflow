import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
import mlflow
from mlflow.tracking import MlflowClient
import mlflow.sklearn
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from datetime import datetime
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import ml_monitor  # Real-time monitoring

# Enable system metrics logging
mlflow.enable_system_metrics_logging()

# Set a very short sampling interval, e.g., 1 second
mlflow.set_system_metrics_sampling_interval(1)

# Set the number of samples before logging to 1 to log after each sample
mlflow.set_system_metrics_samples_before_logging(1)

# Function to evaluate drift and generate an HTML artifact for the Evidently report
def eval_drift(reference, production, column_mapping, artifact_path):
    data_drift_report = Report(metrics=[DataDriftPreset()])
    data_drift_report.run(reference_data=reference, current_data=production, column_mapping=column_mapping)

    report_path = os.path.join(artifact_path, "data_drift_report.html")
    data_drift_report.save_html(report_path)

    report_dict = data_drift_report.as_dict()
    drifts = {}
    try:
        for feature in column_mapping.numerical_features + column_mapping.categorical_features:
            drift_score = report_dict.get("metrics", [])[1].get("result", {}).get("drift_by_columns", {}).get(feature, {}).get("drift_score", 'N/A')
            drifts[feature] = drift_score
    except KeyError as e:
        print(f"KeyError while extracting drift metrics: {e}")
        drifts = {}

    return drifts, report_path

# Function to evaluate target drift and generate an HTML artifact
def eval_target_drift(reference, production, target, artifact_path):
    target_drift_report = Report(metrics=[TargetDriftPreset()])
    target_drift_report.run(reference_data=reference, current_data=production, column_mapping=ColumnMapping(target=target))

    report_path = os.path.join(artifact_path, "target_drift_report.html")
    target_drift_report.save_html(report_path)

    report_dict = target_drift_report.as_dict()
    drift_score = report_dict.get("metrics", [])[0].get("result", {}).get("drift_score", 'N/A')
    return drift_score, report_path

# Function to push all metrics to Pushgateway for Prometheus
def push_metrics_to_gateway(mse, r2_score_value, accuracy, feature_drifts, target_drift):
    registry = CollectorRegistry()

    # General model metrics
    mse_gauge = Gauge('model_mse', 'Mean Squared Error of the model', registry=registry)
    r2_gauge = Gauge('model_r2_score', 'R^2 Score of the model', registry=registry)
    accuracy_gauge = Gauge('mlflow_prediction_accuracy', 'Prediction Accuracy %', registry=registry)
    
    mse_gauge.set(mse)
    r2_gauge.set(r2_score_value)
    accuracy_gauge.set(accuracy * 100)  # Convert to percentage

    # Log feature drifts
    feature_drift_gauge = Gauge('mlflow_feature_drift_over_time', 'Feature Drift Over Time', ['feature'], registry=registry)
    for feature, drift in feature_drifts.items():
        feature_drift_gauge.labels(feature=feature).set(drift)

    # Log target drift
    target_drift_gauge = Gauge('mlflow_target_drift_over_time', 'Target Drift Over Time', registry=registry)
    target_drift_gauge.set(target_drift)

    # Push metrics
    push_to_gateway('localhost:9091', job='model_metrics', registry=registry)

def main():
    # Start MLMonitor
    monitor = ml_monitor.Monitor(config_file="ml_monitor/config.yml", log_level="debug")
    monitor.start()

    # Set up MLflow Tracking Client and Experiment
    tracking_uri = "http://localhost:5000"
    mlflow.set_tracking_uri(tracking_uri)
    experiment_name = "lrgn_model"
    mlflow.set_experiment(experiment_name)
    client = MlflowClient(tracking_uri)

    # Load reference and production data from separate CSV files
    reference_data = pd.read_csv('/home/user/project/reference_data.csv')
    production_data = pd.read_csv('/home/user/project/current_data.csv')

    cat_features = ['conds', 'wdird', 'wdire']
    num_features = ['dewptm', 'hum', 'pressurem']
    target = 'tempm'

    # Preprocessing pipelines
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy="median")),
        ('scaler', StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy="most_frequent")),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))  # Ensure dense matrix output
    ])

    preprocessor = ColumnTransformer([
        ('num', num_pipeline, num_features),
        ('cat', cat_pipeline, cat_features)
    ])

    # Preprocess reference and production data
    X_reference = reference_data.drop(columns=[target, 'datetimeutc'])
    y_reference = reference_data[target]
    X_production = production_data.drop(columns=[target, 'datetimeutc'])
    y_production = production_data[target]

    # Split data for training and evaluation
    X_train, X_test, y_train, y_test = train_test_split(X_reference, y_reference, test_size=0.2, random_state=42)

    # Apply preprocessing to data
    X_train_preprocessed = preprocessor.fit_transform(X_train)
    X_test_preprocessed = preprocessor.transform(X_test)
    X_production_preprocessed = preprocessor.transform(X_production)

    # Initialize and train model
    model = LinearRegression()
    model.fit(X_train_preprocessed, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test_preprocessed)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Calculate prediction accuracy
    accuracy = 1 - (np.abs(y_test - y_pred).sum() / len(y_test))

    # Set up column mapping for Evidently
    column_mapping = ColumnMapping()
    column_mapping.numerical_features = num_features
    column_mapping.categorical_features = cat_features

    artifact_path = "./artifacts"
    os.makedirs(artifact_path, exist_ok=True)

    # Evaluate data drift using Evidently
    drift_metrics, data_drift_report_path = eval_drift(X_reference, X_production, column_mapping, artifact_path)

    # Evaluate target drift using Evidently
    target_drift_score, target_drift_report_path = eval_target_drift(reference_data, production_data, target, artifact_path)

    # Log metrics using MLMonitor
    monitor.monitor("mse", mse)
    monitor.monitor("r2_score", r2)
    monitor.monitor("accuracy", accuracy)
    for feature, drift in drift_metrics.items():
        monitor.monitor(f"drift_{feature}", drift)
    monitor.monitor("target_drift", target_drift_score)

    # Start MLFlow run
    with mlflow.start_run(log_system_metrics=True) as run:
        mlflow.log_param("model_type", str(model.__class__.__name__))
        mlflow.log_metrics({"mse": mse, "r2_score": r2, "accuracy": accuracy})
        mlflow.log_metrics(drift_metrics)
        mlflow.log_metric("target_drift", target_drift_score)
        mlflow.sklearn.log_model(model, "model")
        mlflow.log_artifact(data_drift_report_path, artifact_path="drift_report")
        mlflow.log_artifact(target_drift_report_path, artifact_path="target_drift_report")

        # Push metrics to Prometheus Pushgateway
        push_metrics_to_gateway(mse, r2, accuracy, drift_metrics, target_drift_score)

        # Output artifact details
        artifacts = mlflow.artifacts.list_artifacts(run_id=run.info.run_id, artifact_path="drift_report")
        for artifact in artifacts:
            print(f"Artifact name: {artifact.path}, size: {artifact.file_size}")

    # Stop MLMonitor
    monitor.stop()

if __name__ == "__main__":
    main()
