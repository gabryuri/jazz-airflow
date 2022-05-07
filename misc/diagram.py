from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.compute import ECR
#from diagrams.aws.database import RDS
#from diagrams.aws.network import ELB
#from diagrams.aws.analytics import DataPipeline
from diagrams.onprem.workflow import Airflow
from diagrams.aws.compute import ECS
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.language import Python

with Diagram("jazz-airflow", show=False, direction="TB"):
    #airflow = Airflow("Airflow")
    # Airflow("lb") >> [ECS("worker1"),
    #               EC2("worker2"),
    #               EC2("worker3"),
    #               EC2("worker4"),
    #               EC2("worker5"),
    #               Airflow("test2")] >> RDS("events")
    

    with Cluster("Deploy do Airflow no ECS (Via EC2)"):
        ecr = ECR("Imagem do airflow - ECR")
        airflow = Airflow("Airflow")
        cluster = ECS("Cluster")
        instancia = EC2("Instancia")

        cluster \
            - Edge(color="brown", style="dotted") \
            >> instancia  \
            >> Edge(label="") \
            >> airflow
        banco = PostgreSQL('metadata db')
        banco - Edge(color="black", style="dotted") - instancia
        ecr - Edge(color="black", style="dotted") - cluster

    
    with Cluster("Tasks do airflow"):
        pass

        # grpcsvc >> Edge(color="black") >> primary
