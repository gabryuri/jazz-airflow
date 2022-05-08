import json
import pyscopg2 

def handler(event, context):

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

    conn = psycopg2.connect(
    database="jazz-prod",
    user="postgres",
    password=os.environ['PSYCOPG_PW'],
    host=os.environ['PSYCOPG_HOST'],
    port='5432'
    )

    print('total round amount:', len(rounds))

    cur = conn.cursor()
    cur.executemany(query, rounds)
    conn.commit()

