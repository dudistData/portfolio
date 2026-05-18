"""
This is a beginner-friendly Apache Airflow DAG (Directed Acyclic Graph).
A DAG is a collection of tasks you want to run, organized in a way that reflects their relationships and dependencies.

This DAG performs a very simple ETL (Extract, Transform, Load) pipeline:
1. Extract: Creates some dummy data and saves it as a CSV file.
2. Transform: Reads the CSV file, modifies the data, and saves it.
3. Load: Reads the transformed data and prints it out (a simple "load" for demonstration).
"""

import os
import pandas as pd
from datetime import datetime, timedelta

# Import the core Airflow components
from airflow import DAG
from airflow.operators.python import PythonOperator

# Define where our data will be saved.
# Because we mounted volumes in docker-compose.yaml, these paths inside the container
# map to the 'data/raw' and 'data/processed' folders on your local computer.
RAW_DATA_PATH = '/opt/airflow/data/raw/dummy_data.csv'
PROCESSED_DATA_PATH = '/opt/airflow/data/processed/clean_data.csv'

# --- Task 1: Extract ---
def extract_data(**kwargs):
    """
    Creates some dummy data and saves it to a CSV file.
    """
    print("Starting Extract phase...")
    data = {
        'id': [1, 2, 3, 4],
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'age': [25, 30, 35, 40]
    }
    df = pd.DataFrame(data)

    # Save the raw data
    df.to_csv(RAW_DATA_PATH, index=False)
    print(f"Data saved to {RAW_DATA_PATH}")

# --- Task 2: Transform ---
def transform_data(**kwargs):
    """
    Reads the raw CSV file, adds a new column, and saves it as processed data.
    """
    print("Starting Transform phase...")

    # Read the raw data
    df = pd.read_csv(RAW_DATA_PATH)

    # Transform: Let's add 5 years to everyone's age
    df['age_in_5_years'] = df['age'] + 5

    # Save the processed data
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Transformed data saved to {PROCESSED_DATA_PATH}")

# --- Task 3: Load ---
def load_data(**kwargs):
    """
    Reads the processed data and prints it to the logs.
    """
    print("Starting Load phase...")

    # Read the processed data
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # "Load" it by printing it out. In a real scenario, you might insert this into a database.
    print("Here is the final data:")
    print(df.to_string())


# --- DAG Definition ---

# Default arguments apply to all tasks in this DAG
default_args = {
    'owner': 'airflow',             # Who owns the DAG
    'depends_on_past': False,       # Should this run wait for previous runs to succeed?
    'email_on_failure': False,      # Turn off emails on failure for local learning
    'email_on_retry': False,
    'retries': 1,                   # How many times to retry if a task fails
    'retry_delay': timedelta(minutes=1), # How long to wait before retrying
}

# Define the DAG itself
with DAG(
    dag_id='hello_airflow_dag',                 # The unique name of the DAG
    default_args=default_args,
    description='A simple beginner ETL DAG',    # What this DAG does
    schedule_interval=timedelta(days=1),        # How often it runs (e.g., daily)
    start_date=datetime(2023, 1, 1),            # When it should "start" running (usually in the past so it can run immediately)
    catchup=False,                              # Don't try to run all the missed days between start_date and today
    tags=['beginner', 'etl'],                   # Tags to help find it in the UI
) as dag:

    # Define the tasks using PythonOperator
    # The PythonOperator runs a specific Python function.

    task_extract = PythonOperator(
        task_id='extract_data',      # Unique ID for the task
        python_callable=extract_data # The Python function to run
    )

    task_transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )

    task_load = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )

    # --- Define Task Dependencies ---
    # The bitshift operator (>>) tells Airflow the order tasks must run.
    # extract must finish before transform, and transform must finish before load.
    task_extract >> task_transform >> task_load
