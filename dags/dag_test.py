from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.settings import AIRFLOW_HOME
import json

import os
from operators.demoparser import DemoParser

def demo_parse():

    print("$AIRFLOW_HOME=", AIRFLOW_HOME)

    demofile = os.path.join(AIRFLOW_HOME, "demo.dem")
    outfile = 'demo_test'
    demo_parser = DemoParser(demofile="dags/demo.dem", demo_id=outfile, parse_rate=128)

    parsed_result = demo_parser.parse()

    with open(f'{outfile}.json') as json_file:
        data = json.load(json_file)
    print('data')
    print('data is',data)


def print_hello():
    return 'Hello world from first Airflow DAG!'

dag = DAG('parse_dag', description='Hello World DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2021, 3, 20), catchup=False)


command = ' '.join([
    'go',
    'version'
])

bo = BashOperator(
    task_id="load_collection",
    bash_command=command#,
    #env={'file_location': f'{AIRFLOW_HOME}/local_file.json'}
)

hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)
parser_operator = PythonOperator(task_id='parse_task', python_callable=demo_parse, dag=dag)

bo >> parser_operator >> hello_operator