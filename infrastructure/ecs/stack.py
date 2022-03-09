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

        vpc = ec2.Vpc(self, "MainVpc",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                name="public-subnet",
                subnet_type=ec2.SubnetType.PUBLIC
            )],
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

        # my_security_group = ec2.SecurityGroup(self, "SecurityGroup",
        #     vpc=vpc,
        #     description="Allow ssh access to ec2 instances",
        #     allow_all_outbound=True
        # )
        # my_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow ssh access from the world")


        cluster.add_capacity("DefaultAutoScalingGroupCapacity",
        instance_type=ec2.InstanceType("t2.micro"),
        desired_capacity=1,
        key_name='ec2-key-pair'
        )


        task_definition_airflow = ecs.Ec2TaskDefinition(self, "TaskDef")

        port_mapping = ecs.PortMapping(container_port=80,host_port=8080,protocol=ecs.Protocol.TCP)


        task_definition_airflow.add_container("DefaultContainer",
            image=ecs.ContainerImage.from_registry("apache/airflow"),
            memory_limit_mib=512,
            port_mappings=port_mapping
        )

        ecs_service = ecs.Ec2Service(self, "Service",
        cluster=cluster,
        task_definition=task_definition_airflow
    )   

