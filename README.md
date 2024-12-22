# Real-Time Logistics Data Pipeline Using Airflow, Pub/Sub and cloud function

## Overview
This project demonstrates a **real-time event-driven Big Data pipeline** using **Apache Airflow** and **Google Cloud Pub/Sub**. The pipeline processes logistics data uploaded to **Google Cloud Storage (GCS)**, runs Hive queries on a **Dataproc cluster**, and archives the processed files. 

## Features
- **Real-Time Automation**: Automatically triggers the pipeline when a new file is uploaded to the GCS bucket.
- **Data Processing**: Raw CSV files are processed into a Hive table.
- **File Archiving**: Processed files are moved to an archive bucket for backup.



## Prerequisites
1. **Google Cloud Platform (GCP) Setup**:
   - **GCS Buckets**:
     - `logistics-raw`: Stores raw input files.
     - `logistics-archive`: Stores processed/archived files.
   - **Dataproc Cluster**:
     - A single-node cluster with Hive installed.
   - **Pub/Sub Topic**:
     - `new-file-upload-topic`: Publishes messages when files are uploaded.
   - **IAM Roles**:
     Refer to [`iam/required_roles.txt`](iam/required_roles.txt) for a detailed list.

2. **Apache Airflow**:
   - A running Airflow environment with the required Python dependencies installed.

## Setup Instructions

### Step 1: Create GCS Buckets
```bash
gsutil mb -l us-central1 gs://logistics-raw
gsutil mb -l us-central1 gs://logistics-archive
```

### Step 2: Enable Pub/Sub Notifications
```bash
gcloud storage buckets notifications create gs://logistics-raw \
    --topic=new-file-upload-topic
```

### Step 3: Deploy the Cloud Function
```bash
gcloud functions deploy trigger_airflow_dag \
    --runtime python39 \
    --trigger-topic new-file-upload-topic \
    --region us-central1
```

### Step 4: Deploy the Airflow DAG

Copy pubsub_triggered_dag.py to your Airflow DAGs folder:
```bash
cp dags/pubsub_triggered_dag.py /path/to/airflow/dags/
```

Restart the Airflow scheduler and webserver:
```bash
airflow scheduler &
airflow webserver &
```


## Testing the Pipeline

### 1: Upload a file:
```bash
gsutil cp logistics_2023_09_01.csv gs://logistics-raw/input_data/
```

### 2. Check Cloud Function logs and Airflow DAG execution.