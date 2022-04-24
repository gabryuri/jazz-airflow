import os

from aws_cdk import core
from aws_cdk import aws_rds as rds, aws_ec2 as ec2


class BaseStack(core.Stack):
    def __init__(self, scope: core.Construct, **kwargs) -> None:
        super().__init__(scope, id=f"jazz-base-stack", **kwargs)


        self.vpc = ec2.Vpc(self, "MainVpc2",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                name="jazz-subnet",
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            ec2.SubnetConfiguration(
                name="jazz-subnet2",
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            ]
        )

        airflow_security_group = ec2.SecurityGroup(self, "SecurityGroup",
        vpc=self.vpc,
        description="Allow ssh access to ec2 instances",
        allow_all_outbound=True
        )
        airflow_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow ssh access from the world")
        airflow_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8080), "allow port 80")



        # self.custom_vpc = ec2.Vpc(self, f"vpc-{self.deploy_env}")

        # self.orders_rds_sg = ec2.SecurityGroup(
        #     self,
        #     f"orders-{self.deploy_env}-sg",
        #     vpc=self.custom_vpc,
        #     allow_all_outbound=True,
        #     security_group_name=f"orders-{self.deploy_env}-sg",
        # )

        # self.orders_rds_sg.add_ingress_rule(
        #     peer=ec2.Peer.ipv4("37.156.75.55/0"), connection=ec2.Port.tcp(5432)
        # )

        # for subnet in self.custom_vpc.private_subnets:
        #     self.orders_rds_sg.add_ingress_rule(
        #         peer=ec2.Peer.ipv4(subnet.ipv4_cidr_block),
        #         connection=ec2.Port.tcp(5432),
        #     )

        # self.orders_rds_parameter_group = rds.ParameterGroup(
        #     self,
        #     f"orders-{self.deploy_env}-rds-parameter-group",
        #     description="Parameter group to allow CDC from RDS using DMS.",
        #     engine=rds.DatabaseInstanceEngine.postgres(
        #         version=rds.PostgresEngineVersion.VER_12_4
        #     ),
        #     parameters={"rds.logical_replication": "1", "wal_sender_timeout": "0"},
        # )

        # self.orders_rds = rds.DatabaseInstance(
        #     self,
        #     f"orders-{self.deploy_env}-rds",
        #     engine=rds.DatabaseInstanceEngine.postgres(
        #         version=rds.PostgresEngineVersion.VER_12_4
        #     ),
        #     database_name="orders",
        #     instance_type=ec2.InstanceType("t3.micro"),
        #     vpc=self.custom_vpc,
        #     instance_identifier=f"rds-{self.deploy_env}-orders-db",
        #     port=5432,
        #     vpc_placement=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        #     subnet_group=rds.SubnetGroup(
        #         self,
        #         f"rds-{self.deploy_env}-subnet",
        #         description="place RDS on public subnet",
        #         vpc=self.custom_vpc,
        #         vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        #     ),
        #     parameter_group=self.orders_rds_parameter_group,
        #     security_groups=[self.orders_rds_sg],
        #     removal_policy=core.RemovalPolicy.DESTROY,
        #     **kwargs,
        # )