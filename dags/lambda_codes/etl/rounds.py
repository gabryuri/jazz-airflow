import json
import psycopg2 
import boto3 

def handler(event, context):

    s3_object = event.get('s3_object')
    exec_date = event.get('exec_date')

    data = get_object(s3_object)  

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
        "tSpend"
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s)
        ON CONFLICT ("matchID","roundNum") DO NOTHING;"""

    conn = connect_to_rds()
    print('total round amount:', len(rounds))

    cur = conn.cursor()
    cur.executemany(query, rounds)
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

def get_object(s3_object):
    s3 = boto3.client('s3')   
    obj = s3.get_object(Bucket='jazz-processed', Key=s3_object)
    data = json.loads(obj['Body'].read())
    return data 
