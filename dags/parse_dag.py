import logging
import boto3
import json
import os
import sys
sys.path.append("/usr/local/airflow/dags/utils")

from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.settings import AIRFLOW_HOME
from botocore.exceptions import ClientError

from demoparser import DemoParser


dag = DAG('parse_dag', description='Hello World DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2021, 3, 20), catchup=False)


landing_bucket = 'jazz-landing'
output_bucket = 'jazz-processed'

def scan_for_demos(**kwargs):
    return ['pasta1/demo1.dem', 'pasta2/demo2.dem'] 


scan_for_demos = PythonOperator(
    task_id='scan_for_demos',
    python_callable=scan_for_demos,
    provide_context=True,
    dag=dag)


def parse_and_upload(**kwargs):
    ti = kwargs['ti']
    object_list = ti.xcom_pull(task_ids='scan_for_demos')

    s3_client = boto3.client('s3')

    #for s3_object in object_list:
    #print('PROCESSING FILE ', s3_object)
    # print('file', os.path.basename(s3_object))
    # print('file pure', os.path.basename(s3_object).strip('.dem'))

    # demofile = 'raw_tmp/demo_local.dem'

    s3_client.download_file(landing_bucket, object_list[1], 'demo_local.dem')

    #demofile = os.path.join(AIRFLOW_HOME, "raw_tmp", os.path.basename(s3_object))
    # outfile = os.path.join(AIRFLOW_HOME, "tmp", os.path.basename(s3_object))
    # print('demofile: ', demofile)
    # print('outfile: ', outfile)

    # demo_parser = DemoParser(demofile=demofile, demo_id=outfile, parse_rate=128)
    # demo_parser.parse()

    # object_name = os.path.join('output_folder', outfile)

    
    # try:
    #     response = s3_client.upload_file('tmp/'+ls+".json", output_bucket, object_name)
    # except ClientError as e:
    #     logging.error(e)
    #     return False
    return True

parse_and_upload = PythonOperator(
    task_id='parse_and_upload',
    python_callable=parse_and_upload, 
    provide_context=True,
    dag=dag)


#go_operator >> hello_operator
scan_for_demos >> parse_and_upload 