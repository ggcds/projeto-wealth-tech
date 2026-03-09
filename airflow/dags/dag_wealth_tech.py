from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "ggcds",
    "depends_on_past": False,
    "start_date": datetime(2026, 3, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "pipeline_wealth_tech",
    default_args=default_args,
    description="Extração Yahoo Finance e Transformação dbt",
    schedule_interval=None,  # gatilho manual
    catchup=False,
) as dag:

    # 1) Ingestão (Bronze)
    extrair_dados = BashOperator(
        task_id="extrair_dados_yahoo",
        bash_command="python /opt/airflow/src/ingestion/ingestao_yahoo.py",
    )

    # 2) dbt build (Seeds + Models + Tests)
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="cd /opt/airflow/invest_analytics && dbt build --profiles-dir .",
    )

    extrair_dados >> dbt_build
