from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    App, RemovalPolicy, Stack
)


class RDSStack(Stack):
    def __init__(self, app: App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "MainVpc")

        rds.DatabaseInstance(
            self, "RDS",
            database_name="airflow",
            engine=rds.DatabaseInstanceEngine..postgres(version=rds.PostgresEngineVersion.VER_12_3),
            vpc=vpc,
            port=5432,
            instance_type=ec2.InstanceType("db.t2.micro"),
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False
        ),


