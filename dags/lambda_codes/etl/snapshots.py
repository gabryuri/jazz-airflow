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

    updated_at = datetime.utcnow().__str__()
    
    match = data['matchID']
    columns = ['matchID','roundNum','tick', 'seconds', 'clockTime', 'bombPlanted', 'bombsite']
    columns_side = ['side', 'teamEqVal', 'alivePlayers', 'totalUtility']

    rounds = []
    for round in data['gameRounds']:
        for frame in round['frames']:
            frame_info = []
            frame_info.append(match)
            frame_info.append(round['roundNum'])
            for field in frame.keys():
                if field in columns:
                    frame_info.append(frame[field])
            for side in ['t', 'ct']:
                for field in frame[side].keys():
                    if field in columns_side:
                        frame_info.append(frame[side][field])
            rounds.append(frame_info)

    columns_sides = [col + '_' + side for side in ['t', 'ct'] for col in columns_side]

    df_snapshots = pd.DataFrame(rounds, columns=[*columns, *columns_sides])
    print(df_snapshots)
    df_snapshots.to_csv('Output_snapshots.csv', index = False)        

    
    """
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
    updated_at
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s)
    ON CONFLICT ("matchID","roundNum") DO UPDATE SET 
        "updated_at" = excluded."updated_at";
    """


    # query ="""INSERT INTO match_data.rounds(
    #     "matchID",
    #     "mapName",
    #     "roundNum",
    #     "isWarmup",
    #     "tScore",
    #     "ctScore",
    #     "endTScore",
    #     "endCTScore",
    #     "ctTeam",
    #     "tTeam",
    #     "winningSide",
    #     "winningTeam",
    #     "losingTeam",
    #     "roundEndReason",
    #     "ctStartEqVal",
    #     "ctRoundStartEqVal",
    #     "ctRoundStartMoney",
    #     "ctBuyType",
    #     "ctSpend",
    #     "tStartEqVal",
    #     "tRoundStartEqVal",
    #     "tRoundStartMoney",
    #     "tBuyType",
    #     "tSpend",
    #     updated_at
    #     ) 
    #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    #             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    #             %s, %s, %s, %s, %s)
    #     ON CONFLICT ("matchID","roundNum") DO UPDATE SET 
    #     "updated_at" = excluded."updated_at";"""

    # conn = connect_to_rds()
    # print('total round amount:', len(rounds))

    # cur = conn.cursor()
    # cur.executemany(query, rounds)
    # conn.commit()


def get_object(s3_object):
    s3 = boto3.client('s3')   
    obj = s3.get_object(Bucket='jazz-processed', Key=s3_object)
    data = json.loads(obj['Body'].read())
    return data 

handler('a','b')