from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG("electricity_etl", start_date=datetime(2024,1,1), schedule="@hourly") as dag:

    t1 = BashOperator(
        task_id="bronze",
        bash_command="python src/ingestion.py"
    )

    t2 = BashOperator(
        task_id="silver",
        bash_command="python src/silver.py"
    )

    t3 = BashOperator(
        task_id="gold",
        bash_command="python src/gold.py"
    )

    t1 >> t2 >> t3