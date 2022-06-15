import boto3
import json
import os
import sys
import psycopg2
import time

sys.path.append("/usr/local/airflow/dags/utils")

from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.settings import AIRFLOW_HOME
from airflow.contrib.hooks.aws_lambda_hook import AwsLambdaHook

from connector import connect_to_rds


dag = DAG('parse_dag', description='Hello World DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2021, 3, 20), catchup=False)


landing_bucket = 'jazz-landing'
output_bucket = 'jazz-processed'

object_prefix = 'hltv'

def crawling_matches(**kwargs):
    offset = 0 

    hook = AwsLambdaHook( 
    function_name='jazz-ingest-crawling_matches',
    region_name='us-east-1',
    invocation_type='Event',
    )

    event = {"offset" : offset}

    result = hook.invoke_lambda(payload=json.dumps(event))
    print(result)

crawling_matches = PythonOperator(
    task_id='crawling_matches',
    python_callable=crawling_matches,
    provide_context=True,
    dag=dag)


def find_demo_ids(**kwargs):

    hook = AwsLambdaHook( 
    function_name='jazz-ingest-find_demos',
    region_name='us-east-1',
    invocation_type='Event',
    )

    event = {}

    result = hook.invoke_lambda(payload=json.dumps(event))
    print(result)

find_demo_ids = PythonOperator(
    task_id='find_demo_ids',
    python_callable=find_demo_ids,
    provide_context=True,
    dag=dag)


def download_demos(**kwargs):

    exec_date = kwargs['next_ds']
    conn = connect_to_rds()
    cur = conn.cursor()

    cur.execute("""SELECT demo_id
                        FROM crawling.crawled_matches
                        WHERE updated_at >= current_date - interval '1 day'
                        AND (demo_id <> 1 or demo_id is not null)
                     """)

    results = cur.fetchall()
    print('total amount of matches to download: ', len(results))

    hook = AwsLambdaHook( 
    function_name='jazz-ingest-download_demos',
    region_name='us-east-1',
    invocation_type='Event',
    )

    for demo in results:

        time.sleep(30)
        event = {"demo_id" : demo[0],
                "object_prefix" : object_prefix,
                "exec_date" : exec_date}

        print(event)

        result = hook.invoke_lambda(payload=json.dumps(event))
        print(result)

    time.sleep(400)
    return len(results)


download_demos = PythonOperator(
    task_id='download_demos',
    python_callable=download_demos,
    provide_context=True,
    dag=dag)


def parse_and_upload(**kwargs):
    time.sleep(30)
    ti = kwargs['ti']
    exec_date = kwargs['next_ds']

    hook = AwsLambdaHook( 
        function_name='jazz-ingest-parser',
        region_name='us-east-1',
        invocation_type='Event',
        )

    client = boto3.client('s3')
    result = client.list_objects(Bucket=landing_bucket,
                                 Prefix=os.path.join(object_prefix, exec_date)+'/',
                                 Delimiter='/')

 
    s3_json_objects = []
    for obj in result['Contents']:
        s3_object = obj['Key']

        event = {"s3_object":s3_object,
                "object_prefix":object_prefix,
                "exec_date":exec_date}

        output_s3 = (os.path.join(event.get('object_prefix'), exec_date, os.path.basename(s3_object).rstrip('.dem')))+'.json'
        print(output_s3)
        s3_json_objects.append(output_s3)

        result = hook.invoke_lambda(payload= json.dumps(event))
        print(result)
    return s3_json_objects
    
parse_and_upload = PythonOperator(
    task_id='parse_and_upload',
    python_callable=parse_and_upload, 
    provide_context=True,
    dag=dag)


def json_to_rounds(**kwargs):
    time.sleep(60)
    ti = kwargs['ti']
    exec_date = kwargs['next_ds']

    s3_object_list = ti.xcom_pull(task_ids='parse_and_upload')
    print(s3_object_list)

    rounds_hook = AwsLambdaHook( 
        function_name='jazz-etl-rounds',
        region_name='us-east-1',
        invocation_type='Event',
        )

    for s3_object in s3_object_list:
        event = {"s3_object" : s3_object,
                 "exec_date" : exec_date}

        result = rounds_hook.invoke_lambda(payload= json.dumps(event))
        print(result)

json_to_rounds = PythonOperator(
    task_id='json_to_rounds',
    python_callable=json_to_rounds, 
    provide_context=True,
    dag=dag)

def json_to_players(**kwargs):
    time.sleep(60)
    ti = kwargs['ti']
    exec_date = kwargs['next_ds']

    s3_object_list = ti.xcom_pull(task_ids='parse_and_upload')
    print(s3_object_list)

    rounds_hook = AwsLambdaHook( 
        function_name='jazz-etl-players',
        region_name='us-east-1',
        invocation_type='Event',
        )

    for s3_object in s3_object_list:
        event = {"s3_object" : s3_object,
                 "exec_date" : exec_date}

        result = rounds_hook.invoke_lambda(payload= json.dumps(event))
        print(result)

json_to_players = PythonOperator(
    task_id='json_to_players',
    python_callable=json_to_players, 
    provide_context=True,
    dag=dag)



def json_to_snapshots(**kwargs):
    time.sleep(60)
    ti = kwargs['ti']
    exec_date = kwargs['next_ds']

    s3_object_list = ti.xcom_pull(task_ids='parse_and_upload')
    print(s3_object_list)

    rounds_hook = AwsLambdaHook( 
        function_name='jazz-etl-snapshots',
        region_name='us-east-1',
        invocation_type='Event',
        )

    for s3_object in s3_object_list:
        event = {"s3_object" : s3_object,
                 "exec_date" : exec_date}

        result = rounds_hook.invoke_lambda(payload= json.dumps(event))
        print(result)

json_to_snapshots = PythonOperator(
    task_id='json_to_snapshots',
    python_callable=json_to_snapshots, 
    provide_context=True,
    dag=dag)

crawling_matches >> find_demo_ids >> download_demos >> parse_and_upload >> json_to_rounds
parse_and_upload >> json_to_players
parse_and_upload >> json_to_snapshots
