import logging
import boto3
import json
import os
import requests
from lxml import html
import psycopg2

# from datetime import datetime
# import time

from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.settings import AIRFLOW_HOME
from botocore.exceptions import ClientError

dag = DAG('crawling_for_matches',
          description='Hello World DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2022, 4, 24),
          catchup=False)



def get_matches():
    offset = 0 
    table_name = 'crawled_matches'
    url = f'https://www.hltv.org/results?offset={offset}'

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url=url, headers=headers)

    if r.status_code != 200: 
        print(f'request failed with status {r.status_code}')
        #todo raise for blablala

    tree = html.fromstring(r.content)
    matches = tree.xpath(f"//div[contains(@class, 'result-con')]/a/@href")

    print(f"Saving matches from offset {offset} ... into {table_name}", end="")
    created_at = datetime.now().__str__()
    matches_splitted = [ match.split('/') for match in matches ]

    item_list = []
    for match in matches_splitted:
        if len(match) > 3:
            item = (match[2], 
                    str(match[3]), 
                    1, 
                    str(created_at),
                    str(created_at), 
                    str(created_at),
                    str(created_at),
                    )
            item_list.append(item)
    
    print(item_list)


    # connection = ###
    # cursor = connection.cursor()
    # backslash = "\n"
    # insert_statement = (f"""INSERT INTO {table_name} 
    # VALUES {f", {backslash}".join([repr(tup) for tup in item_list])} 
    # ON CONFLICT DO NOTHING; """)

    # cursor.execute(insert_statement)
    # connection.commit()




    





 

get_matches = PythonOperator(task_id='get_matches', python_callable=get_matches, dag=dag)

#parser_operator = PythonOperator(task_id='parse_task', python_callable=demo_parse, dag=dag)

#go_operator >> hello_operator
#parser_operator >> upload_file



# class ScrapHLTV():
#     def __init__(self, offset=None):
#         self.offset = offset
#         self.matches = None
#         self.con = None
#         self.cur = None

#     def create_connection(self):
#         self.con = sqlite3.connect('database/demo_hltv.db')
#         self.cur = self.con.cursor()
#         return

#     def create_dir(self, dir_name=None):
#         try:
#             os.mkdir(dir_name)
#         except FileExistsError:
#             pass
#         return

#     def prepare(self):
#         list_dir = ['database']
#         for dir_name in list_dir:
#             self.create_dir(dir_name=dir_name)
#         return

#     def create_table(self):
#         self.cur.execute("""CREATE TABLE IF NOT EXISTS bronze_matches (
#                     match_id int,
#                     description text,
#                     demo_id int,
#                     created_at timestamp,
#                     updated_at timestamp,
#                     PRIMARY KEY (match_id) 
#                 )
#                 """)
#         self.con.commit()
#         return

#     def get_matches(self):
#         url = f'https://www.hltv.org/results?offset={self.offset}'
#         r = requests.get(url=url)
#         tree = html.fromstring(r.content)
#         self.matches = tree.xpath(f"//div[contains(@class, 'result-con')]/a/@href")
#         return
    
#     def save_matches(self):
#         print(f"Saving matches from offset {self.offset} ... ", end="")
#         created_at = datetime.now().__str__()
#         matches_splited = [ match.split('/') for match in self.matches ]
#         for match in matches_splited:
#             if len(match) > 3:
#                 self.cur.execute(f"""INSERT INTO bronze_matches 
#                                 VALUES (
#                                     {match[2]}, 
#                                     '{match[3]}', 
#                                     NULL, 
#                                     '{created_at}', 
#                                     '{created_at}' 
#                                 ) 
#                                 ON CONFLICT DO NOTHING;
#                                 """)
#                 self.con.commit()
#         print("Done")
#         return

#     def update_demos(self):
#         print("Updating Demos ... ", end="")
#         self.cur.execute("""SELECT * 
#                             FROM bronze_matches
#                             WHERE demo_id is NULL
#                         """)
#         results = self.cur.fetchall()

#         for match in results:
#             match_id = match[0]
#             description = match[1]
#             updated_at = datetime.now().__str__()

#             url = f'https://www.hltv.org/matches/{match_id}/{description}'
#             r = requests.get(url=url)

#             tree = html.fromstring(r.content)

#             demo = tree.xpath(f"//div[contains(@class, 'stream-box')]/a/@href")
            
#             if len(demo) > 0:
#                 if len(demo[0]) > 3:
#                     demo_id = demo[0].split('/')[3]

#                     self.cur.execute(f"""UPDATE bronze_matches 
#                                         SET demo_id =     {demo_id}, 
#                                             updated_at = '{updated_at}' 
#                                         WHERE match_id = {match_id}
#                                     """)
#                 self.con.commit()
#                 time.sleep(0.25)
#         print("Done")

#     def start(self):
#         print("Preparing scraping ...", end="")
#         self.prepare()
#         self.create_connection()
#         self.create_table()
#         self.get_matches()
#         print("OK")
#         self.save_matches()
#         self.update_demos()
#         return