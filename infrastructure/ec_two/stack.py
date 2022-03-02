from aws_cdk import core
from aws_cdk import (
    aws_ec2 as ec2
)
from constructs import Construct

class EC2Stack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, *kwargs)

        #IAM role

        #EC2 instance
        
