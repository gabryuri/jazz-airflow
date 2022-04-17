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

        vpc = ec2.Vpc(self, "MainVpc2",
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

        rds.DatabaseInstance(
            self, "RDS",
            instance_identifier="jazz-db",
            database_name="airflow",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_11_12),
            vpc=vpc,
            port=5432,
            publicly_accessible=True,
            instance_type=ec2.InstanceType("t2.micro"),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,
            vpc_placement=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
               )
        )

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
        instance_type=ec2.InstanceType("t2.small"),
        desired_capacity=1,
        key_name='ec2-key-pair'
        )

        volume = {
        # Use an Elastic FileSystem
        "name": "dags-volume",
        "efs_volume_configuration": {
            "file_system_id": "fs-0bf57c9e03f6fdbc3"
            }
        }

        task_definition_airflow = ecs.Ec2TaskDefinition(self,
        id="TaskDef",
        volumes = [volume]
        )


       
        repo = ecr.Repository.from_repository_name(self, "repo", "ecr-airflow")

        container = task_definition_airflow.add_container("DefaultContainer",
            image=ecs.ContainerImage.from_registry("puckel/docker-airflow:1.10.9"),
            #image= ecs.EcrImage(repo, "prod"),
            memory_limit_mib=1478,
            environment={'AIRFLOW__CORE__SQL_ALCHEMY_CONN':'postgresql+psycopg2://postgres:CwiNM6Fr,arcr3NUkX2aNNg^Z=lA4o@jazz-db.c6dsbzlok1sy.us-east-1.rds.amazonaws.com:5432/airflow',
                         'AIRFLOW__CORE__EXECUTOR':'LocalExecutor',
                         'AIRFLOW_USER_HOME':'usr/local/airflow',
                         'FERNET_KEY':'p2ipMzLuAmpasGAE-3qfiyyG_x-sAl25yR8YNJZvAZw='
                         }
        )    


        mount_point = ecs.MountPoint(
        container_path="/usr/local/airflow",
        read_only=True,
        source_volume="dags-volume"
        )

        container.add_mount_points(mount_point)
        
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

