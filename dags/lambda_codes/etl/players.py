import json
import psycopg2 
import boto3 
from datetime import datetime
#from utils.connector import connect_to_rds

def handler(event, context):

    s3_object = event.get('s3_object')
    exec_date = event.get('exec_date')
    print("processing s3 object, ", s3_object)

    data = get_object(s3_object)  
    #print(data)
    updated_at = datetime.utcnow().__str__()
    match = data['matchID']
    columns = ['tick','matchID','roundNum','steamID','hp','armor',
                'totalUtility','isAlive','isInBombZone','equipmentValue',
                'cash','hasHelmet','hasDefuse','hasBomb','created_at','updated_at']


    players = []
    for game_round in data['gameRounds']:
        print(game_round)
        for frame in game_round['frames']:
            for side in ['t', 'ct']:
                for player in frame[side]['players']:
                    players_info = []
                    players_info.append(frame['tick'])
                    players_info.append(match)
                    players_info.append(game_round['roundNum'])
                    for key in player.keys():
                        if key in columns:
                            players_info.append(player[key])   
                    players_info.append(updated_at)
                    players_info.append(updated_at)      
                    print(players_info)  
                    players.append(players_info)
               
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
    cur.executemany(query, players)
    conn.commit()


def get_object(s3_object):
    s3 = boto3.client('s3')   
    obj = s3.get_object(Bucket='jazz-processed', Key=s3_object)
    data = json.loads(obj['Body'].read())
    return data 
