from constructs import Construct
from aws_cdk import (
    core,
    aws_iam as iam,
    aws_lambda as _lambda,
)

class LambdaStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="jazz lambda roles"
        )

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))

        layer = _lambda.LayerVersion.from_layer_version_arn(
            self, 
            "Psycopg2Layer",
            layer_version_arn='arn:aws:lambda:us-east-1:898466741470:layer:psycopg2-py37:3')

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self,
            'rounds',
            function_name='jazz-lambda-rounds',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('dags/lambda_codes'),
            handler='rounds.handler',
            role=role,
            layers=[layer],
            timeout=core.Duration.minutes(5)
        )

import json
import boto3
import sys 
sys.path.insert(0, '/opt/parent')
import psycopg2

def handler(event, context):
    # client = boto3.client('s3')
    # response = client.put_object( 
    #     Bucket='s3-belisco-turma-6-develop-data-lake-curated',
    #     Body='bytes or seekable file-like object',
    #     Key='Object key for which the PUT operation was initiated'
    # )
    # return response 
    
        
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
    print(j)
    # password = j['password']
    # host = j['host']
    # user = j['user']
    # port = '5432'
    # database = 'jazz-prod'
    
    conn = psycopg2.connect(
    database=database,
    user=user,
    password=password,
    host=host,
    port='5432'
    )
    
        
    

# import json
# import pyscopg2 

# def handler(event, context):

#     match = data['matchID']
#     mapname = data['mapName']

#     columns = ['matchID', 'mapName', 'roundNum', 'isWarmup', 'tScore', 'ctScore', 
#             'endTScore', 'endCTScore', 'ctTeam', 'tTeam',
#             'winningSide', 'winningTeam', 'losingTeam', 
#             'roundEndReason', 'ctStartEqVal', 'ctRoundStartEqVal', 
#             'ctRoundStartMoney', 'ctBuyType', 'ctSpend', 'tStartEqVal', 
#             'tRoundStartEqVal', 'tRoundStartMoney', 'tBuyType', 'tSpend']

#     rounds = []
#     for round in data['gameRounds']:
#         round_info = []
#         for match_info in [match, mapname]:
#             round_info.append(match_info)
#         for field in round.keys():
#             if field in columns:
#                 round_info.append(round[field])
#         rounds.append(round_info)

#     query ="""INSERT INTO match_data.rounds(
#         "matchID",
#         "mapName",
#         "roundNum",
#         "isWarmup",
#         "tScore",
#         "ctScore",
#         "endTScore",
#         "endCTScore",
#         "ctTeam",
#         "tTeam",
#         "winningSide",
#         "winningTeam",
#         "losingTeam",
#         "roundEndReason",
#         "ctStartEqVal",
#         "ctRoundStartEqVal",
#         "ctRoundStartMoney",
#         "ctBuyType",
#         "ctSpend",
#         "tStartEqVal",
#         "tRoundStartEqVal",
#         "tRoundStartMoney",
#         "tBuyType",
#         "tSpend"
#         ) 
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s)
#         ON CONFLICT ("matchID","roundNum") DO NOTHING;"""

#     conn = psycopg2.connect(
#     database="jazz-prod",
#     user="postgres",
#     password=os.environ['PSYCOPG_PW'],
#     host=os.environ['PSYCOPG_HOST'],
#     port='5432'
#     )

#     print('total round amount:', len(rounds))

#     cur = conn.cursor()
#     cur.executemany(query, rounds)
#     conn.commit()

