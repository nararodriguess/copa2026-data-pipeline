from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import json
import os
import logging
import sys

sys.path.insert(0, "/opt/airflow/scripts")
from transform_games import run as transform_and_load

API_KEY = os.getenv("API_KEY")
logger = logging.getLogger(__name__)

def get_games():
    url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": API_KEY}
    
    logger.info("Starting request to football-data.org API...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    matches = data.get("matches", [])
    
    logger.info(f"Successfully fetched {len(matches)} matches.")

    output_path = "/opt/airflow/data/raw/games.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Games data saved to {output_path}")

with DAG(
    dag_id="dag_get_games",
    start_date=datetime(2026, 6, 1),
    schedule_interval="@hourly",
    catchup=False,
) as dag:

    task_get = PythonOperator(
        task_id="get_games",
        python_callable=get_games,
    )

    task_transform = PythonOperator(
        task_id="transform_and_load",
        python_callable=transform_and_load,
    )

    task_get >> task_transform