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
            frame_info.append(updated_at)
            frame_info.append(updated_at)
            rounds.append(frame_info)

    columns_sides = [col + '_' + side for side in ['t', 'ct'] for col in columns_side]


    query = """INSERT INTO match_data.snapshots(
    "matchID",
    "roundNum",
    tick,
    seconds,
    "clockTime",
    "bombPlanted",
    bombsite,
    side_t,
    "teamEqVal_t",
    "alivePlayers_t",
    "totalUtility_t",
    side_ct,
    "teamEqVal_ct",
    "alivePlayers_ct",
    "totalUtility_ct",
    created_at,
    updated_at
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT ("matchID", tick) DO UPDATE SET 
        "updated_at" = excluded."updated_at";
    """

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
