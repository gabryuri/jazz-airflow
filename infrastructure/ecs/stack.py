from aws_cdk import core
from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_ecs as ecs
)
from constructs import Construct

class ECSCluster(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, *kwargs)

        #vpc = ec2.Vpc(
        #    self, "MyVpc",
        #    max_azs=2
        #)

        # asg = autoscaling.AutoScalingGroup(
        #     self, "MyFleet",
        #     instance_type=ec2.InstanceType("t2.micro"),
        #     machine_image=ecs.EcsOptimizedImage.amazon_linux2(),
        #     associate_public_ip_address=True,
        #     desired_capacity=1
        # )

        cluster = ecs.Cluster(
            self, 'EcsCluster'
        )

        cluster.add_capacity("DefaultAutoScalingGroupCapacity",
        instance_type=ec2.InstanceType("t2.micro"),
        desired_capacity=1
        )


        task_definition_airflow = ecs.Ec2TaskDefinition(self, "TaskDef")

        task_definition_airflow.add_container("DefaultContainer",
            image=ecs.ContainerImage.from_registry("apache/airflow"),
            memory_limit_mib=512
        )

        ecs_service = ecs.Ec2Service(self, "Service",
        cluster=cluster,
        task_definition=task_definition_airflow
    )

