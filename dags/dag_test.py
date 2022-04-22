from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.settings import AIRFLOW_HOME
import json

import os
#from awpy import DemoParser
#from lightawpy.demoparser import DemoParser
from operators.demoparser import DemoParser



dag = DAG('parse_dag', description='Hello World DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2021, 3, 20), catchup=False)


outfilename = 'temp_demo3'

def demo_parse():

    print("$AIRFLOW_HOME=", AIRFLOW_HOME)

    demofile = os.path.join(AIRFLOW_HOME, "demo.dem")
    outfile = 'tmp/'+outfilename
    demo_parser = DemoParser(demofile="dags/demo.dem", demo_id=outfile, parse_rate=128)

    demo_parser.parse()

import logging
import boto3
from botocore.exceptions import ClientError
import os
def upload_file():
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    object_name = 'testezinho.json'
    bucket = 's3-belisco-turma-6-develop-data-lake-curated'

    # If S3 object_name was not specified, use file_name
    # if object_name is None:
    #     object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file('tmp/'+outfilename+".json", bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True





#go_operator = PythonOperator(task_id='go_task', python_callable=sprocess, dag=dag)
upload_file = PythonOperator(task_id='upload_file', python_callable=upload_file, dag=dag)
parser_operator = PythonOperator(task_id='parse_task', python_callable=demo_parse, dag=dag)

#go_operator >> hello_operator
parser_operator >> upload_file