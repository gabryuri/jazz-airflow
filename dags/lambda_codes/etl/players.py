import json
import psycopg2 
import boto3 
from datetime import datetime
import pandas as pd
#from utils.connector import connect_to_rds

def handler(event, context):

    #s3_object = event.get('s3_object')
    #exec_date = event.get('exec_date')

    #data = get_object(s3_object)  
    with open('demo1.json') as json_file:
        data = json.load(json_file)
    #print(data)

    match = data['matchID']
    columns = ['tick','matchID','roundNum','steamID','hp','armor',
                'totalUtility','isAlive','isInBombZone','equipmentValue',
                'cash','hasHelmet','hasDefuse','hasBomb','created_at','updated_at']

    updated_at = datetime.utcnow().__str__()
    players = []
    for round in data['gameRounds']:
        for frame in round['frames']:
            for side in ['t', 'ct']:
                for player in frame[side]['players']:
                    players_info = []
                    players_info.append(frame['tick'])
                    players_info.append(match)
                    players_info.append(round['roundNum'])
                    for key in player.keys():
                        if key in columns:
                            players_info.append(player[key])   
                    players_info.append(updated_at)
                    players_info.append(updated_at)        
                    players.append(players_info)
            

    print(players_info)
    #print(players)
    df_players = pd.DataFrame(players, columns=columns) 
    print(df_players)
    df_players.to_csv('Output.csv', index = False)
    
    query = """INSERT INTO match_data.players(
    tick,
    "matchID",
    "roundNum",
    "steamID",
    "hp",
    "armor",
    "totalUtility",
    "isAlive",
    "isInBombZone",
    "equipmentValue",
    "cash",
    "hasHelmet",
    "hasDefuse",
    "hasBomb",
    created_at,
    updated_at
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s)
    ON CONFLICT ("matchID", "tick", "steamID") DO UPDATE SET 
        "updated_at" = excluded."updated_at";
    """

    conn = connect_to_rds()
    print('total round amount:', len(players))

    cur = conn.cursor()
    cur.executemany(query, players[0:2])
    conn.commit()


def get_object(s3_object):
    s3 = boto3.client('s3')   
    obj = s3.get_object(Bucket='jazz-processed', Key=s3_object)
    data = json.loads(obj['Body'].read())
    return data 

def connect_to_rds():
    session = boto3.session.Session()
    
    # client = session.client(
    #     service_name='secretsmanager',
    #     region_name='us-east-1'
    # )
    
    # get_secret_value_response = client.get_secret_value(
    # SecretId='RDSSecret3683CA93-EbWoCdWb5X7B'
    # )
    
    # secret = get_secret_value_response['SecretString']
    # j = json.loads(secret)

    
   
    conn = psycopg2.connect(
    database=database,
    user=user,
    password=password,
    host=host,
    port='5432'
    )
    return conn 

handler('a','b')