from aws_cdk import core

from ecs.stack import ECSCluster
from ecr.stack import ECRStack
from rds.stack import RdsStack
from basestack import BaseStack

app = core.App()
base = BaseStack(scope=app)
rds = RdsStack(scope=app, id='jazz-RDS-stack', basestack=base)
#ecs = ECSCluster(scope=app, id='Jazz-Ecs-RDS-Airflow')
#ecr = ECRStack(scope=app, id='EcrRepository')

app.synth() 

