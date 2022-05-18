import os
import requests 
import boto3 
import psycopg2 
import json
from datetime import datetime

def lambda_handler(event, context):

    demo_id = event.get('demo_id')
    exec_date = event.get('exec_date')
    object_prefix = event.get('object_prefix')

    DEMOS_COMPRESSED_DIR = '/tmp'
    output_bucket = 'jazz-landing'

    print(f"Downloading match {demo_id}")
    url=f'https://www.hltv.org/download/demo/{str(demo_id)}'  
    resp = requests.get(url)

    # assuming the subdirectory tempdata has been created:
    zname = os.path.join(DEMOS_COMPRESSED_DIR, f"{str(demo_id)}.rar")
    zfile = open(zname, 'wb')
    zfile.write(resp.content)
    zfile.close()

    extract(f"{str(demo_id)}" ,DEMOS_COMPRESSED_DIR)
    
    downloaded_at = datetime.utcnow().__str__()
    file_count = 0 
    
    s3_client = boto3.client('s3')
    for file in os.listdir(DEMOS_COMPRESSED_DIR):
        if file.endswith(".dem"):
            file_count = file_count +1 
            local_json_path = (os.path.join(DEMOS_COMPRESSED_DIR, file))
            print('local_json_path:' , local_json_path)

            demo_name = str(demo_id)+'_'+str(file)
            print('demo_name: ', demo_name)

            s3_object_name = os.path.join(object_prefix, exec_date, demo_name)
            result = s3_client.upload_file(local_json_path, output_bucket, s3_object_name)
            print(f"{s3_object_name} yielded s3 upload result {result}")


    conn = connect_to_rds()
    cur = conn.cursor()

    cur.execute(f"""UPDATE crawling.crawled_matches 
                SET file_count =     {file_count}, 
                    downloaded_at = '{downloaded_at}' 
                WHERE demo_id = {demo_id}
            """)
    conn.commit()


def extract(demo_file, DEMOS_COMPRESSED_DIR):
    demo_file = os.path.join(DEMOS_COMPRESSED_DIR, demo_file)
    os.system(f'unrar x {demo_file}.rar {DEMOS_COMPRESSED_DIR}')
    return None


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