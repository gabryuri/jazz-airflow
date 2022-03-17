from aws_cdk import core

from common_stack import CommonStack
from data_lake.stack import DataLakeStack
from dms.stack import DmsStack
from kinesis.stack import KinesisStack
from ecs.stack import ECSCluster
#from ec_two.stack import EC2Stack

app = core.App()

#ec2_stack = EC2Stack(app)
#data_lake_stack = DataLakeStack(app)
# c  ommon_stack = CommonStack(app)
ecs = ECSCluster(scope=app, id='EcsStack')
ecr = ECRStack(scope=app, id='EcrRepository')

# test
#kinesis_stack = KinesisStack(
#    app, data_lake_raw_bucket=data_lake_stack.data_lake_raw_bucket
#)
#dms_stack = DmsStack(
#   app,
#    common_stack=common_stack,
#    data_lake_raw_bucket=data_lake_stack.data_lake_raw_bucket,
#)
app.synth() 

