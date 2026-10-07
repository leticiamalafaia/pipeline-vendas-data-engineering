from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="pipeline_vendas",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    testar_qualidade = BashOperator(
        task_id="testar_qualidade",
        bash_command="cd /opt/airflow/projeto-vendas && pytest tests/test_qualidade_dados.py",
    )

    executar_pipeline = BashOperator(
        task_id="executar_pipeline",
        bash_command="cd /opt/airflow/projeto-vendas && python src/tratamento.py",
    )

    testar_qualidade >> executar_pipeline
