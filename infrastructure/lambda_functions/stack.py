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

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self,
            'rounds',
            function_name='jazz-lambdas-rounds',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('dags/lambda_codes'),
            handler='rounds.handler',
            role=role
        )