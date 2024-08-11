FROM apache/airflow:latest

EXPOSE 8080
RUN pip install --no-cache-dir requests scikit-learn xgboost joblib matplotlib


