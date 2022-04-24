from aws_cdk import core

from ecs.stack import ECSCluster
from ecr.stack import ECRStack

app = core.App()

ecs = ECSCluster(scope=app, id='Jazz-Ecs-RDS-Airflow')
ecr = ECRStack(scope=app, id='EcrRepository')

app.synth() 

