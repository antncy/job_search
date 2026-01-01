from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "job_scraper",
    default_args=default_args,
    description="Run job scraper every 3 hours",
    schedule=timedelta(hours=3),  # Every 3 hours
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:
    run_scraper = BashOperator(
        task_id="run_scraper",
        bash_command="python /home/ubuntu/mcp/embed_test/main.py",
    )