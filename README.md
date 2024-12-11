# ML Monitoring with Evidently, MLflow, Prometheus, and Grafana along mlmonitor real time tracking

This project implements a comprehensive machine learning monitoring pipeline using **Evidently**, **MLflow**, **Prometheus Pushgateway**, and **Grafana**. It evaluates model performance, detects data drift, and enables real-time metric monitoring using ml_monitor.

---

## Features

1. **Drift Detection:**
   - Identify Data Drift and Target Drift using Evidently.
2. **Model Monitoring:**
   - Metrics include MSE, R² Score, Prediction Accuracy, and Drift Scores.
3. **Real-Time Metrics Push:**
   - Prometheus Pushgateway for exporting metrics.
4. **Visualization:**
   - Real-time dashboards via Grafana.
5. **Experiment Tracking:**
   - MLflow for artifact, parameter, and metric logging.
---

## File Structure

```
project/
├── ml_monitor                     # Stores configuration for monitoring and logging data to prometheus
├── reference_data.csv             # Reference dataset
├── current_data.csv               # Production dataset
├── requirements.txt               # Required Python packages
├── linearregression.py            # Main script                   
├── docker/                        # Pre-configured Grafana and Prometheus Docker setup
│   ├── docker-compose.yml         # Docker Compose file to launch Grafana and Prometheus
│   ├── prometheus/                # Prometheus configuration
│   │   └── prometheus.yml         # Prometheus configuration file
│   ├── grafana/                   # Grafana configuration
│       ├── provisioning/          # Grafana provisioning setup
│           ├── dashboard/         # Grafana dashboards
│           │   └── <dashboard_files>.json  # Dashboard files
│           └── datasource/        # Grafana datasource setup
│               └── <datasource_files>.yml  # Datasource configuration files
│         
└── setup.py                     # for installing and starting ml_monitor

```

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/045051Shalini/ml_pipeline_using_mlflow.git
   ```
2. Navigate to the project directory:
   ```bash
   cd project
   ```
3. Install mlflow in th rproject folder
   ```bash
   pip install mlflow
   mlflow server \
   --backend-store-uri sqlite:///mlflow.db \
   --default-artifact-root ./mlruns \
   --host 0.0.0.0 \
   --port 5000
   ```
2. Install ml_monitor
   ```bash
   pip install ml_monitor
   pip install .
   ```
3. Install requirements
   ```bash
   pip install -r requirements.txt
   ```

4. Install evidently ai
   ```bash
   pip install evidently
   pip install --upgrade evidently
   ```
5. Run docker compose up -d
   ```bash
    docker-compose up -d (in case it gives error than try docker compose up -d)
   ```
---

## Usage

1. **open terminal:**
   Ensure MLflow server is running on `http://localhost:5000`. To start:
   ```bash
   mlflow ui
   ```

2. **Open another terminal:**
Before running follwoing commnad replace the path of reference and production data with your path in linearregression.py file as following:
    reference_data = pd.read_csv('/home/user/project/reference_data.csv')
    production_data = pd.read_csv('/home/user/project/current_data.csv')
 Then run:  
  ```bash
   python linearregression.py --save-model
   ```
In case you are not able to see system metrics in mlflow ui then in terminal run following cmd and save model again
 ```bash
   export MLFLOW_ENABLE_SYSTEM_METRICS_LOGGING=true
   ```
4. **View Mlflow ui:**
   Mlflow user interface accessible at `http://localhost:5000`.
   
5. **View Prometheus Metrics:**
   Metrics are pushed to Prometheus   accessible at `http://localhost:9090`.

6. **View Prometheus Pushgateway Metrics:**
   Metrics are pushed to Prometheus Pushgateway and accessible at `http://localhost:9091`.   

7. **Visualize Metrics in Grafana:**
   - Access Grafana dashboard via `http://localhost:3000`.
   - Use Prometheus as the data source.
   - user: admin
   - password: ml_monitor
---



## Monitored Metrics

| **Metric**           | **Source**     |
|-----------------------|----------------|
| Data Drift Report    | Evidently      |
| Target Drift Report  | Evidently      |
| Model MSE            | MLflow         |
| Model R² Score       | MLflow         |
| Prediction Accuracy  | MLflow         |
| Feature Drift Scores | Evidently      |
| Target Drift Score   | Evidently      |

---

## Contributing

Feel free to fork this repository and submit a pull request with your updates.

---

## License

[MIT License](LICENSE)

---

## Contact

For queries or support, contact [Shalini Chauhan / 1shalinichauhan@gmail.com].

