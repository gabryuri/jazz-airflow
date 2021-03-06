from aws_cdk import core

from ecs.stack import ECSCluster
from ecr.stack import ECRStack
from rds.stack import RdsStack
from storage.stack import S3StorageStack
from lambda_functions.stack import LambdaStack
from basestack import BaseStack


app = core.App()

base = BaseStack(scope=app)
rds = RdsStack(scope=app, id='jazz-RDS-stack', basestack=base)
ecs = ECSCluster(scope=app, id='Jazz-Ecs-Airflow', basestack=base)
s3_storage = S3StorageStack(scope=app)
ecr = ECRStack(scope=app, id='Jazz-Ecr-Repository')
lambdas = LambdaStack(scope=app, id='Jazz-Lambda-Functions')
app.synth() 

