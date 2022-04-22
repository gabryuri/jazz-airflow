from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.settings import AIRFLOW_HOME
import json

import os
#from awpy import DemoParser
from lightawpy.demoparser import DemoParser
#from operators.demoparser import DemoParser

def demo_parse():

    print("$AIRFLOW_HOME=", AIRFLOW_HOME)

    demofile = os.path.join(AIRFLOW_HOME, "demo.dem")
    outfile = 'tmp/demo_testes'
    demo_parser = DemoParser(demofile="dags/demo.dem", demo_id=outfile, parse_rate=128)

    parsed_result = demo_parser.parse()
    print('parsed_result:', parsed_result)
    with open(AIRFLOW_HOME+'/'+outfile+".json") as json_file:
        data = json.load(json_file)
    print('data')
    print('data is',data)

def sprocess():
    import subprocess


    command = ['go', 'run', 'plugins/operators/parse_demo.go',
     '-demo', '/usr/local/airflow/dags/demo.dem',
     '-parserate', '128', '-tradetime', '5',
     '-buystyle', 'hltv', '-demoid',
     'tmp/demo_testes', '-out', '/usr/local/airflow',
     '--parseframes']

    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        #cwd='path'
    )
    process_output, second_output =  proc.communicate()

    print(process_output)


def print_hello():
    return 'Hello world from first Airflow DAG!'

dag = DAG('parse_dag', description='Hello World DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2021, 3, 20), catchup=False)


command = ' '.join([
    'ls'
])

bo = BashOperator(
    task_id="load_collection",
    bash_command=command#,
    #env={'file_location': f'{AIRFLOW_HOME}/local_file.json'}
)

go_operator = PythonOperator(task_id='go_task', python_callable=sprocess, dag=dag)
hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)
parser_operator = PythonOperator(task_id='parse_task', python_callable=demo_parse, dag=dag)

go_operator >>  bo >> hello_operator
parser_operator  >> bo 