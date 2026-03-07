from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Configurações básicas da automação
default_args = {
    'owner': 'ggcds',
    'depends_on_past': False,
    'start_date': datetime(2026, 3, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'pipeline_wealth_tech',
    default_args=default_args,
    description='Extração Yahoo Finance e Transformação dbt',
    schedule_interval=None, # Apenas gatilho manual
    catchup=False
) as dag:

    # Tarefa 1: Rodar o script Python de Ingestão (Bronze)
    extrair_dados = BashOperator(
        task_id='extrair_dados_yahoo',
        bash_command='python /opt/airflow/src/ingestion/ingestao_yahoo.py'
    )

    # Tarefa 2: Rodar o dbt (Silver e Gold)
    transformar_dados = BashOperator(
        task_id='dbt_run_gold_silver',
        bash_command='cd /opt/airflow/invest_analytics && dbt run'
    )

    # Tarefa 3: Rodar os testes de qualidade
    testar_dados = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/invest_analytics && dbt test'
    )

    # Definindo a ordem: Extrai -> Transforma -> Testa
    extrair_dados >> transformar_dados >> testar_dados