from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'Amy',
    'start_date': days_ago(1),
}

dag = DAG(
    'mlops_pipeline',
    default_args=default_args,
    description='MLOPs pipeline: data ingestion, data precessing, model training, model evaluation',
    schedule_interval=None
)

ingest_task = BashOperator(
    task_id='data_ingestion',
    bash_command='python /opt/airflow/python/data_ingestion.py',
    dag=dag,
)

process_task = BashOperator(
    task_id='data_processing',
    bash_command='python /opt/airflow/python/data_processing.py',
    dag=dag,
)

rf_train_task = BashOperator(
    task_id='model_training1',
    bash_command='python /opt/airflow/python/model_train_random_forest.py',
    dag=dag,
)

xgb_train_task = BashOperator(
    task_id='model_training2',
    bash_command='python /opt/airflow/python/model_train_xgboost.py',
    dag=dag,
)

dt_train_task = BashOperator(
    task_id='model_training3',
    bash_command='python /opt/airflow/python/model_train_decision_tree.py',
    dag=dag,
)

evaluate_task = BashOperator(
    task_id='model_evaluation',
    bash_command='python /opt/airflow/python/model_evaluation.py',
    dag=dag,
)

ingest_task >> process_task >> [rf_train_task, xgb_train_task, dt_train_task] >> evaluate_task