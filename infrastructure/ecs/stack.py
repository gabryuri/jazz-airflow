from aws_cdk import core
from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_rds as rds,
    aws_logs as logs
)
from constructs import Construct

class ECSCluster(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, *kwargs)

        vpc = ec2.Vpc(self, "MainVpc",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                name="public-subnet",
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            ec2.SubnetConfiguration(
                name="public-subnet2",
                subnet_type=ec2.SubnetType.ISOLATED
            ),
            ec2.SubnetConfiguration(
                name="public-subnet3",
                subnet_type=ec2.SubnetType.PRIVATE
            ),
            ]
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


        # asg = autoscaling.AutoScalingGroup(
        #     self, "MyFleet",
        #     instance_type=ec2.InstanceType("t2.micro"),
        #     machine_image=ecs.EcsOptimizedImage.amazon_linux2(),
        #     associate_public_ip_address=True,
        #     desired_capacity=1
        # )

        cluster = ecs.Cluster(
            self, 'EcsCluster',
            vpc=vpc
        )

        airflow_security_group = ec2.SecurityGroup(self, "SecurityGroup",
            vpc=vpc,
            description="Allow ssh access to ec2 instances",
            allow_all_outbound=True
        )
        airflow_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow ssh access from the world")
        airflow_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8080), "allow port 80")


        cluster.add_capacity("DefaultAutoScalingGroupCapacity",
        instance_type=ec2.InstanceType("t2.micro"),
        desired_capacity=1,
        key_name='ec2-key-pair'
        )


        task_definition_airflow = ecs.Ec2TaskDefinition(self,
        "TaskDef"#,
        #network_mode=ecs.NetworkMode.AWS_VPC
        )

        repo = ecr.Repository.from_repository_name(self, "repo", "ecr-airflow")

        container = task_definition_airflow.add_container("DefaultContainer",
            #image=ecs.ContainerImage.from_registry("puckel/docker-airflow"),
            image= ecs.EcrImage(repo, "prod"),
            memory_limit_mib=10000
        )
        
        container.add_port_mappings(
            ecs.PortMapping(
            container_port=8080,
            host_port=8080,
            protocol=ecs.Protocol.TCP
        ))

        container.add_port_mappings(
            ecs.PortMapping(
            container_port=5432,
            host_port=5432,
            protocol=ecs.Protocol.TCP
        ))


        ecs_service = ecs.Ec2Service(self, "Service",
        cluster=cluster,
        task_definition=task_definition_airflow#,
        #security_groups=[airflow_security_group]
    )   

