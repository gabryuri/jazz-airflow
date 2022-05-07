import logging
import boto3
import json
import os
import sys
import psycopg2
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
    ti = kwargs['ti']
    exec_date = kwargs['ds']

    object_list = ti.xcom_pull(task_ids='scan_for_demos')

    s3_client = boto3.client('s3')

    s3_processed_objects = []

    for s3_object in object_list:
        print('PROCESSING FILE ', s3_object)
        
        demo_path = os.path.join(AIRFLOW_HOME, demos_folder, os.path.basename(s3_object))
        print('demo being saved to: ', demo_path)
        s3_client.download_file(landing_bucket, s3_object, demo_path)
        
        demo_name = os.path.basename(s3_object.strip('.dem'))
        print('demo name: ', demo_name)
        demo_parser = DemoParser(
            demofile=demo_path,
            demo_id=demo_name, 
            outpath=processed_folder,
            parse_rate=128)

        demo_parser.parse()

        local_json_path = os.path.join(processed_folder, demo_name)+".json"
        s3_object_name = os.path.join(exec_date, demo_name)+".json"

        s3_client.upload_file(local_json_path, output_bucket, s3_object_name)
        s3_processed_objects.append(local_json_path)

        #todo limpar os dados locais
    return s3_processed_objects
              

parse_and_upload = PythonOperator(
    task_id='parse_and_upload',
    python_callable=parse_and_upload, 
    provide_context=True,
    dag=dag)


def json_to_tables(**kwargs):
    ti = kwargs['ti']

    s3_object_list = ti.xcom_pull(task_ids='parse_and_upload')

    print(s3_object_list)
    
    with open(s3_object_list[1]) as f:
        data = json.load(f)

    match = data['matchID']
    mapname = data['mapName']

    columns = ['matchID', 'mapName', 'roundNum', 'isWarmup', 'tScore', 'ctScore', 
            'endTScore', 'endCTScore', 'ctTeam', 'tTeam',
            'winningSide', 'winningTeam', 'losingTeam', 
            'roundEndReason', 'ctStartEqVal', 'ctRoundStartEqVal', 
            'ctRoundStartMoney', 'ctBuyType', 'ctSpend', 'tStartEqVal', 
            'tRoundStartEqVal', 'tRoundStartMoney', 'tBuyType', 'tSpend']

    rounds = []
    for round in data['gameRounds']:
        round_info = []
        for match_info in [match, mapname]:
            round_info.append(match_info)
        for field in round.keys():
            if field in columns:
                round_info.append(round[field])
        rounds.append(round_info)

    query ="""INSERT INTO match_data.rounds(
        "matchID",
        "mapName",
        "roundNum",
        "isWarmup",
        "tScore",
        "ctScore",
        "endTScore",
        "endCTScore",
        "ctTeam",
        "tTeam",
        "winningSide",
        "winningTeam",
        "losingTeam",
        "roundEndReason",
        "ctStartEqVal",
        "ctRoundStartEqVal",
        "ctRoundStartMoney",
        "ctBuyType",
        "ctSpend",
        "tStartEqVal",
        "tRoundStartEqVal",
        "tRoundStartMoney",
        "tBuyType",
        "tSpend"
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s)
        ON CONFLICT ("matchID","roundNum") DO NOTHING;"""

    conn = psycopg2.connect(
    database="jazz-prod",
    user="postgres",
    password=os.environ['PSYCOPG_PW'],
    host=os.environ['PSYCOPG_HOST'],
    port='5432'
    )

    print('total round amount:', len(rounds))

    cur = conn.cursor()
    cur.executemany(query, rounds)
    conn.commit()

# for json_element in json_objects: 
#     trigger_lambda_rounds(json_element)
#     trigger_lambda_tickrate(json_element)


json_to_tables = PythonOperator(
    task_id='json_to_tables',
    python_callable=json_to_tables, 
    provide_context=True,
    dag=dag)


#go_operator >> hello_operator
scan_for_demos >> parse_and_upload >> json_to_tables