
from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_rds as rds
)
from constructs import Construct

class RDSStack(core.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, *kwargs)

        vpc = ec2.Vpc(self, "MainVpc2",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                name="public-subnet2",
                subnet_type=ec2.SubnetType.PUBLIC
            )],
        )

        rds.DatabaseInstance(
            self, "RDS",
            database_name="airflow",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_12_3),
            vpc=vpc,
            port=5432,
            instance_type=ec2.InstanceType("db.t2.micro"),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False
        )


