from aws_cdk import core
from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds
)
from constructs import Construct

from infrastructure.basestack import BaseStack

class RdsStack(core.Stack):

    def __init__(
        self,
        scope: Construct,
        id: str,
        basestack: BaseStack,
        **kwargs
        ) -> None:
        self.basestack = basestack
        super().__init__(scope, id, *kwargs)

        rds.DatabaseInstance(
            self, "RDS",
            instance_identifier="jazz-db",
            database_name="airflow",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_11_12),
            vpc=self.basestack.vpc,
            port=5432,
            publicly_accessible=True,
            instance_type=ec2.InstanceType("t2.micro"),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,
            vpc_placement=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
               )
        )