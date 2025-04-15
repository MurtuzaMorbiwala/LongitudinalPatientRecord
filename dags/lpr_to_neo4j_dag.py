from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lpr_data_generation.neo4j_pipeline import process_all_patient_files

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'lpr_to_neo4j',
    default_args=default_args,
    description='Load LPR data into Neo4j knowledge graph',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 4, 13),
    catchup=False,
    tags=['lpr', 'neo4j'],
)

def load_data_to_neo4j():
    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'lpr_data_generation'
    )
    process_all_patient_files(data_dir)

load_task = PythonOperator(
    task_id='load_lpr_data_to_neo4j',
    python_callable=load_data_to_neo4j,
    dag=dag,
)
