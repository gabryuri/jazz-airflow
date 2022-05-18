from constructs import Construct
from aws_cdk import (
    core,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_ecr as ecr
)

class LambdaStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #Common resources 
        role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="jazz lambda roles"
        )

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))

        psycopg_layer = _lambda.LayerVersion.from_layer_version_arn(
        self, 
        "Psycopg2Layer",
        layer_version_arn='arn:aws:lambda:us-east-1:898466741470:layer:psycopg2-py38:2')

        lxml_layer = _lambda.LayerVersion.from_layer_version_arn(
        self, 
        "LxmlLayer",
        layer_version_arn='arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p38-lxml:1')

        requests_layer = _lambda.LayerVersion.from_layer_version_arn(
        self, 
        "RequestsLayer",
        layer_version_arn='arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p38-requests:2')
       

        # Ingest
        # Ingest - Crawling
        crawling_matches = _lambda.Function(
            self,
            'jazz-ingest-crawling_matches',
            function_name='jazz-ingest-crawling_matches',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('dags'),
            handler='lambda_codes/ingest/crawling_matches.handler',
            role=role,
            layers=[psycopg_layer, lxml_layer, requests_layer],
            timeout=core.Duration.minutes(5),
            memory_size=512
        )

        # Ingest - Finding demos from matches
        find_demos = _lambda.Function(
            self,
            'jazz-ingest-find_demos',
            function_name='jazz-ingest-find_demos',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('dags'),
            handler='lambda_codes/ingest/find_demos.handler',
            role=role,
            layers=[psycopg_layer, lxml_layer, requests_layer],
            timeout=core.Duration.minutes(15),
            memory_size=512
        )

        # Ingest - Downloading
        download_demos_repo = ecr.Repository.from_repository_name(self, "download_demos_repo", "lambda-downloader-repo")

        download_demos = _lambda.DockerImageFunction(
            self,
            'jazz-ingest-download_demos',
            function_name='jazz-ingest-download_demos',
            code=_lambda.DockerImageCode.from_ecr(download_demos_repo),
            role=role,
            timeout=core.Duration.minutes(15),
            memory_size=4096#,
            #ephemeral_storage_size=core.Size.mebibytes(2048)
        )

        print(vars(download_demos))
        print(vars(_lambda.DockerImageFunction))

        # Demo parser 
        repo = ecr.Repository.from_repository_name(self, "repo", "lambda-parser-repo")

        parser_lambda = _lambda.DockerImageFunction(
            self,
            'jazz-ingest-parser',
            function_name='jazz-ingest-parser',
            code=_lambda.DockerImageCode.from_ecr(repo),
            role=role,
            timeout=core.Duration.minutes(5),
            memory_size=2048#,
            #ephemeral_storage_size=core.Size.mebibytes(2048)
        )

        # ETL
        rounds_lambda = _lambda.Function(
            self,
            'jazz-etl-rounds',
            function_name='jazz-etl-rounds',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset('dags'),
            handler='lambda_codes/etl/rounds.handler',
            role=role,
            layers=[psycopg_layer],
            timeout=core.Duration.minutes(5),
            memory_size=512
        )

