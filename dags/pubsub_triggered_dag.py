from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitHiveJobOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'pubsub_triggered_dag',
    default_args=default_args,
    description='Triggered by Pub/Sub for file processing',
    schedule_interval=None,  # No manual schedule
    start_date=datetime(2023, 12, 22),
    catchup=False,
)

# Create Hive Database if not exists
create_hive_database = DataprocSubmitHiveJobOperator(
    task_id="create_hive_database",
    query="CREATE DATABASE IF NOT EXISTS logistics_db;",
    cluster_name='logistics-cluster',
    region='us-central1',
    project_id='<PROJECT_ID>',
    dag=dag,
)

# Create Hive Table
create_hive_table = DataprocSubmitHiveJobOperator(
    task_id="create_hive_table",
    query="""
        CREATE EXTERNAL TABLE IF NOT EXISTS logistics_db.logistics_data (
            delivery_id INT,
            `date` STRING,
            origin STRING,
            destination STRING,
            vehicle_type STRING,
            delivery_status STRING,
            delivery_time STRING
        )
        ROW FORMAT DELIMITED
        FIELDS TERMINATED BY ','
        STORED AS TEXTFILE
        LOCATION 'gs://logistics-raw/input_data/'
        tblproperties('skip.header.line.count'='1');
    """,
    cluster_name='logistics-cluster',
    region='us-central1',
    project_id='<PROJECT_ID>',
    dag=dag,
)

# Archive processed file
archive_processed_file = BashOperator(
    task_id='archive_processed_file',
    bash_command="gsutil -m mv gs://logistics-raw/input_data/logistics_*.csv gs://logistics-archive/",
    dag=dag,
)

# Define task dependencies
create_hive_database >> create_hive_table >> archive_processed_file
