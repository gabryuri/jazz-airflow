import logging
#import boto3
import json
import os
import sys
import psycopg2
import time

from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.settings import AIRFLOW_HOME
from airflow.contrib.hooks.aws_lambda_hook import AwsLambdaHook
#from botocore.exceptions import ClientError1

#from demoparser import DemoParser


dag = DAG('parse_dag', description='Hello World DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2021, 3, 20), catchup=False)


landing_bucket = 'jazz-landing'
output_bucket = 'jazz-processed'

demos_folder = 'tmp_demos'
processed_folder = 'tmp_processed'

def scan_for_demos(**kwargs):
    return ['pasta1/demo1.dem', 'pasta2/demo2.dem'] 


scan_for_demos = PythonOperator(
    task_id='scan_for_demos',
    python_callable=scan_for_demos,
    provide_context=True,
    dag=dag)


def parse_and_upload(**kwargs):
    time.sleep(30)
    ti = kwargs['ti']
    exec_date = kwargs['ds']

    s3_object_list = ti.xcom_pull(task_ids='scan_for_demos')

    hook = AwsLambdaHook( 
        function_name='jazz-ingest-parser',
        region_name='us-east-1',
        invocation_type='Event',
        )

    s3_json_objects = []
    for s3_object in s3_object_list:
        
        event = {"s3_object":s3_object,
                "object_prefix":"major_demos",
                "exec_date":exec_date}

        output_s3 = (os.path.join(event.get('object_prefix'), exec_date, os.path.basename(s3_object).strip('.dem')))+'.json'
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


def json_to_tables(**kwargs):
    time.sleep(60)
    ti = kwargs['ti']
    exec_date = kwargs['ds']

    s3_object_list = ti.xcom_pull(task_ids='parse_and_upload')
    #['major_demos/2022-05-09/demo1.json', 'major_demos/2022-05-09/demo2.json']# 

    rounds_hook = AwsLambdaHook( 
        function_name='jazz-etl-rounds',
        region_name='us-east-1',
        invocation_type='Event',
        )

    for s3_object in s3_object_list:
        event = {"s3_object":s3_object,
                "exec_date":exec_date}

        result = rounds_hook.invoke_lambda(payload= json.dumps(event))
        print(result)

json_to_tables = PythonOperator(
    task_id='json_to_tables',
    python_callable=json_to_tables, 
    provide_context=True,
    dag=dag)

scan_for_demos >> parse_and_upload >> json_to_tables

# def json_to_tables(**kwargs):
#     ti = kwargs['ti']

#     s3_object_list = ti.xcom_pull(task_ids='parse_and_upload')

#     print(s3_object_list)
    
#     with open(s3_object_list[1]) as f:
#         data = json.load(f)

#     match = data['matchID']
#     mapname = data['mapName']

#     columns = ['matchID', 'mapName', 'roundNum', 'isWarmup', 'tScore', 'ctScore', 
#             'endTScore', 'endCTScore', 'ctTeam', 'tTeam',
#             'winningSide', 'winningTeam', 'losingTeam', 
#             'roundEndReason', 'ctStartEqVal', 'ctRoundStartEqVal', 
#             'ctRoundStartMoney', 'ctBuyType', 'ctSpend', 'tStartEqVal', 
#             'tRoundStartEqVal', 'tRoundStartMoney', 'tBuyType', 'tSpend']

#     rounds = []
#     for round in data['gameRounds']:
#         round_info = []
#         for match_info in [match, mapname]:
#             round_info.append(match_info)
#         for field in round.keys():
#             if field in columns:
#                 round_info.append(round[field])
#         rounds.append(round_info)

#     query ="""INSERT INTO match_data.rounds(
#         "matchID",
#         "mapName",
#         "roundNum",
#         "isWarmup",
#         "tScore",
#         "ctScore",
#         "endTScore",
#         "endCTScore",
#         "ctTeam",
#         "tTeam",
#         "winningSide",
#         "winningTeam",
#         "losingTeam",
#         "roundEndReason",
#         "ctStartEqVal",
#         "ctRoundStartEqVal",
#         "ctRoundStartMoney",
#         "ctBuyType",
#         "ctSpend",
#         "tStartEqVal",
#         "tRoundStartEqVal",
#         "tRoundStartMoney",
#         "tBuyType",
#         "tSpend"
#         ) 
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s)
#         ON CONFLICT ("matchID","roundNum") DO NOTHING;"""

#     conn = psycopg2.connect(
#     database="jazz-prod",
#     user="postgres",
#     password=os.environ['PSYCOPG_PW'],
#     host=os.environ['PSYCOPG_HOST'],
#     port='5432'
#     )

#     print('total round amount:', len(rounds))

#     cur = conn.cursor()
#     cur.executemany(query, rounds)
#     conn.commit()

# # for json_element in json_objects: 
# #     trigger_lambda_rounds(json_element)
# #     trigger_lambda_tickrate(json_element)


# json_to_tables = PythonOperator(
#     task_id='json_to_tables',
#     python_callable=json_to_tables, 
#     provide_context=True,
# dag=dag)
