from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

import json
#import boto3
import os
from awpy import DemoParser

def parse_demo():
    demofile = 'demo.dem'
    demo_parser = DemoParser(demofile=demofile, demo_id="test_parse", parse_rate=128)

    body = demo_parser.parse()

    print(body)
    return True 

lambda_handler('a','b')

dag = DAG('dag_parse', 
          description='Hello World DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2021, 3, 20), catchup=False)




hello_operator = PythonOperator(task_id='parse_task', python_callable=parse_demo, dag=dag)

hello_operator