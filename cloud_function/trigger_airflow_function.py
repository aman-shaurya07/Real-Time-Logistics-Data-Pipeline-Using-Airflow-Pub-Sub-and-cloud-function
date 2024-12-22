
import base64
import json
import requests

def trigger_airflow_dag(event, context):
    """
    Cloud Function to trigger an Airflow DAG when a Pub/Sub message is received.

    Args:
        event: The Pub/Sub event payload.
        context: Metadata for the event.

    Notes:
    - Replace <AIRFLOW_API_URL> with your Composer Airflow REST API URL.
        To get the URL, Go to you Airflow Webserver Home page from composer environments page. Copy the url.
        If you get "/home" at the end of the URL, then remove it from the URL.
        And add "/api/v1/dags/{dag_name}/dagRuns"
        replace dag_name with your dag name.
    - Use the command `gcloud auth print-access-token` to generate the Bearer Token.
    """

    pubsub_message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    dag_name = 'pubsub_triggered_dag'

    # Use your actual Airflow REST API URL (replace <YOUR_API_URL>)
    airflow_url = f'http://<AIRFLOW_WEBSERVER_URL>/api/v1/dags/{dag_name}/dagRuns'
    # ex:
    # airflow_url = f'https://a94c13e98l9844d48fd2eb5ydc1234u3-dot-us-central1.composer.googleusercontent.com/api/v1/dags/{dag_name}/dagRuns'


    # Get the Bearer Token using `gcloud auth print-access-token`
    token = '<YOUR_ACCESS_TOKEN>'  # Replace with your actual access token
    headers = {'Authorization': f'Bearer {token}'}

    # Optional: Pass the filename in the DAG configuration
    dag_run_conf = {"filename": pubsub_message['name']}

    # Trigger the Airflow DAG
    response = requests.post(airflow_url, headers=headers, json={"conf": dag_run_conf})

    # Log the result
    if response.status_code == 200:
        print('DAG triggered successfully.')
    else:
        print(f'Failed to trigger DAG: {response.text}')
