import json
import psycopg2 
import boto3 
from datetime import datetime
from utils.connector import connect_to_rds

def handler(event, context):

    s3_object = event.get('s3_object')
    exec_date = event.get('exec_date')
    print("processing s3 object, ", s3_object)
    
    data = get_object(s3_object)  
    updated_at = datetime.utcnow().__str__()
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
        round_info.append(updated_at)
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
        "tSpend",
        updated_at
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s)
        ON CONFLICT ("matchID","roundNum") DO UPDATE SET 
        "updated_at" = excluded."updated_at";"""

    conn = connect_to_rds()
    print('total round amount:', len(rounds))

    cur = conn.cursor()
    cur.executemany(query, rounds)
    conn.commit()


def get_object(s3_object):
    s3 = boto3.client('s3')   
    obj = s3.get_object(Bucket='jazz-processed', Key=s3_object)
    data = json.loads(obj['Body'].read())
    return data 

