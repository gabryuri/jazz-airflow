import boto3 
import psycopg2 
import json 

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