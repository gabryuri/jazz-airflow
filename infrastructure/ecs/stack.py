from aws_cdk import core
from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_rds as rds,
    aws_efs as efs
)
from constructs import Construct

from infrastructure.basestack import BaseStack


class ECSCluster(core.Stack):

    def __init__(
        self,
        scope: Construct,
        id: str,
        basestack: BaseStack,
        **kwargs
        ) -> None:
        self.basestack = basestack
        super().__init__(scope, id, *kwargs)


        cluster = ecs.Cluster(
            self, 'EcsCluster',
            vpc=self.basestack.vpc
        )

        cluster.add_capacity("DefaultAutoScalingGroupCapacity",
        instance_type=ec2.InstanceType("t2.micro"),
        desired_capacity=1,
        key_name='ec2-key-pair'
        )

        file_system = efs.FileSystem(self, "jazz-dags-file-system",
        vpc=self.basestack.vpc,
        lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,  
        performance_mode=efs.PerformanceMode.GENERAL_PURPOSE
        )


        efs_volume_configuration = ecs.EfsVolumeConfiguration(
        file_system_id="jazz-dags-file-system",
        # transit_encryption = "ENABLED",
        # authorization_config=ecs.AuthorizationConfig(
        #     access_point_id="fsap-022d4c28c6a91fd64"    
        # )
        )

        volume = ecs.Volume(
        name="dags-volume",
        efs_volume_configuration=efs_volume_configuration
        )
        

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
        read_only=False,
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

##TOdos
# 1- Adicionar EFS oficialmente aqui 
# 2- Adicionar instancia de sync aqui 
# 3- adicionar o scp lá no git actions? 
# 4- tentar plugar sec groups automaticamente
# 5- Adicionar load balancing e dns fixo? 

