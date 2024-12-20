# ML Monitoring with Evidently AI, MLflow, Prometheus, and Grafana with ml_monitor real time tracking

This repository showcases a comprehensive machine learning pipeline designed for efficient experiment tracking, model monitoring, and performance visualization. The pipeline integrates state-of-the-art tools  **Evidently AI**, **MLflow**, **Prometheus**, and **Grafana** to ensure robust data drift detection, real-time metric logging, and insightful visualizations.

---

## Overview
**Experiment Tracking with MLflow**
MLflow is used to run and manage machine learning experiments. It tracks model parameters, metrics, and artifacts for reproducibility and comparison.

**Data Drift Detection with Evidently AI**
Evidently AI monitors and calculates data drift to ensure the model remains reliable in production.

**Metric Logging with Prometheus Pushgateway**
Performance metrics and drift data are pushed to Prometheus Pushgateway, ensuring a centralized and scalable logging mechanism.

**Visualization with Grafana**
Grafana is used to create real-time dashboards for visualizing metrics logged in Prometheus.

**Monitoring with ML Monitor**
ML Monitor provides a framework to track model health and operational metrics, ensuring the pipeline remains robust and production-ready.


![Screenshot 2024-12-17 181725 (1)](https://github.com/user-attachments/assets/f3b19d6e-53ce-4d31-a688-f609aa8d9f8f)

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
│           │   └── <dashboard_files>  # Dashboard files
│           └── datasource/        # Grafana datasource setup
│               └── <datasource_files> # Datasource configuration files
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
3. Install mlflow:
   ```bash
   pip install mlflow
   mlflow server \
   --backend-store-uri sqlite:///mlflow.db \
   --default-artifact-root ./mlruns \
   --host 0.0.0.0 \
   --port 5000
   ```
 ![Screenshot 2024-12-12 040023](https://github.com/user-attachments/assets/6d202b5c-7f5c-4247-9876-31514327d833)
  
2. Install ml_monitor
   ```bash
   pip install ml_monitor
   pip install .
   ```  
3. Install requirements
   ```bash
   pip install -r requirements.txt  ```

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
Before running follwoing commnad replace the path of reference and production data with your path in linearregression.py. The path will be found in these two lines:
    reference_data = pd.read_csv('/home/user/project/reference_data.csv')
    production_data = pd.read_csv('/home/user/project/current_data.csv')
 Then run:  
  ```bash
   python linearregression.py --save-model
   ```
Experiment will be seen as saved on terminal as following
![image](https://github.com/user-attachments/assets/15789e65-4f42-4ba6-b541-b44254c2e95f)


4. **View Mlflow ui:**
   Mlflow user interface accessible at `http://localhost:5000`.

Once the experiment will be saved following reports and metrics can be seen
  
  ![Screenshot 2024-12-12 041847](https://github.com/user-attachments/assets/d6ea204d-2b0d-4bbc-a5f3-0ba1e32a4601)
  ![Screenshot 2024-12-12 041938](https://github.com/user-attachments/assets/cebac03b-474c-4077-a5c2-05c85803b778)
  ![Screenshot 2024-12-12 042005](https://github.com/user-attachments/assets/7da0f877-a911-4529-9a55-6deb05977145)
  ![Screenshot 2024-12-12 042020](https://github.com/user-attachments/assets/03c3d526-46dc-4c6e-a178-d3bc6890af44)
   In case you are not able to see system metrics in mlflow ui then in terminal run following cmd and save model again
 ```bash
   export MLFLOW_ENABLE_SYSTEM_METRICS_LOGGING=true
   ```
  ![Screenshot 2024-12-12 042055](https://github.com/user-attachments/assets/45e73612-d497-4a4a-8504-aa4c5f3ba506)
  ![Screenshot 2024-12-12 042114](https://github.com/user-attachments/assets/b8f78a63-9388-4f17-b6e3-955b3608b60a)

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
![Screenshot 2024-12-12 042204](https://github.com/user-attachments/assets/97603680-4770-4cf4-9063-e95587fd43dd)



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
## Acknowledgments

I would like to extend my gratitude to the following resources that greatly helped in shaping this project:

- [Chamathka Deemanthi's Medium article](https://medium.com/@chamathka3deemanthi/implement-end-to-end-project-with-mlflow-evidently-ai-and-grafana-83175ea75c89) for providing a detailed guide on implementing an end-to-end project with MLflow, Evidently AI, and Grafana.
- [Sohini Roychowdhury's GitHub repository](https://github.com/sohiniroych/ML-Monitoring-with-Grafana) for an excellent example of ML monitoring with Grafana.

These resources were invaluable in understanding and implementing the core aspects of this project.

---

## Contributing

Feel free to fork this repository and submit a pull request with your updates.

---

## License

[MIT License](https://github.com/045051Shalini/ml_pipeline_using_mlflow/blob/main/LICENSE)

---

## Contact

For queries or support, contact [Shalini Chauhan / 1shalinichauhan@gmail.com].

