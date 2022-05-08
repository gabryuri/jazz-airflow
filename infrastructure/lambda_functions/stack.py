from constructs import Construct
from aws_cdk import (
    core,
    aws_iam as iam,
    aws_lambda as _lambda,
)

class LambdaStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="jazz lambda roles"
        )

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))

        layer = _lambda.LayerVersion.from_layer_version_arn(
            self, 
            "Psycopg2Layer",
            layer_version_arn='arn:aws:lambda:us-east-1:898466741470:layer:psycopg2-py38:2')

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self,
            'rounds',
            function_name='jazz-lambda-rounds',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('dags/lambda_codes'),
            handler='rounds.handler',
            role=role,
            layer=layer,
            timeout=core.Duration.minutes(5)
        )

