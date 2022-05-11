from datetime import datetime
import requests 
import json 

import boto3 
import psycopg2
from lxml import html


def run_crawler(event, context):

    offset = int(event.get('offset'))
    conn = connect_to_rds()

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
    

    query ="""INSERT INTO crawling.crawled_matches(
        match_id,
        description,
        demo_id,
        match_played_at,                    
        created_at,
        updated_at,
        last_seen_at
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (match_id) DO UPDATE SET
        last_seen_at = EXCLUDED.last_seen_at;"""

    conn = connect_to_rds()
    print('total crawled matches amount:', len(item_list))

    cur = conn.cursor()
    cur.executemany(query, item_list)
    conn.commit()

def connect_to_rds():
    session = boto3.session.Session()
    
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )
    
    get_secret_value_response = client.get_secret_value(
    SecretId='RDSSecret3683CA93-EbWoCdWb5X7B'
    )
    
    secret = get_secret_value_response['SecretString']
    j = json.loads(secret)

    password = j['password']
    host = j['host']
    user = j['username']
    port = '5432'
    database = 'jazz-prod'
   
    conn = psycopg2.connect(
    database=database,
    user=user,
    password=password,
    host=host,
    port='5432'
    )
    return conn 
