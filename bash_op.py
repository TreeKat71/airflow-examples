from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'muller',
}

dag = DAG(
    'example_bash_operator',
    default_args=default_args,
    schedule_interval='0 0 * * *',
    start_date=datetime(1989, 6, 4),
    dagrun_timeout=timedelta(minutes=60),
    tags=['example']
)

# dummy
t1 = DummyOperator(
    task_id='t1',
    dag=dag,
)

# bash
for i in range(3):
    t2 = BashOperator(
        task_id=f'runme_{i}',
        bash_command='echo "{{ task_instance_key_str }}" && sleep 30',
        dag=dag,
    )
    t1 >> t2

t3 = BashOperator(
    task_id='t3',
    bash_command='echo 3',
    dag=dag,
)

t4 = BashOperator(
    task_id='t4',
    bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',
    dag=dag,
)

t2 >> t3 >> t4
