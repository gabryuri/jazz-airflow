import requests 
import json 
import boto3
import psycopg2
from datetime import datetime
from lxml import html
import time 

    
def handler(event, context):

    conn = connect_to_rds()
    cur = conn.cursor()

    cur.execute("""SELECT match_id, description
                        FROM crawling.crawled_matches
                        WHERE demo_id is NULL or demo_id = 1
                    """)

    results = cur.fetchall()
    print(f"Updating demos for {len(results)} matches")

    demos_to_download = []
    for match in results:
        match_id = match[0]
        
        description = match[1]
        updated_at = datetime.utcnow().__str__()

        url = f'https://www.hltv.org/matches/{match_id}/{description}'
        r = requests.get(url=url)

        tree = html.fromstring(r.content)

        demo = tree.xpath(f"//div[contains(@class, 'stream-box')]/a/@href")
        
        if len(demo) > 0:
            if len(demo[0]) > 3:
                demo_id = demo[0].split('/')[3]
                demos_to_download.append(demo_id)

                cur.execute(f"""UPDATE crawling.crawled_matches 
                                    SET demo_id =     {demo_id}, 
                                        updated_at = '{updated_at}' 
                                    WHERE match_id = {match_id}
                                """)
            conn.commit()
            time.sleep(5.25)
    print("Done")
    return demos_to_download

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

