from aws_cdk import core
from aws_cdk import (
    aws_ec2 as ec2
)
from constructs import Construct

class RawEC2Role(iam.Role):
    def __init__(
        self,
        scope: core.Construct,
        **kwargs,
    ) -> None:
        self.deploy_env = os.environ["ENVIRONMENT"]
        super().__init__(
            scope,
            id=f"iam-{self.deploy_env}-ec2-to-ecr-role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            description="Role to allow ec2 to access ecr",
        )
        self.add_policy()

    def add_policy(self):
        policy = iam.Policy(
            self,
            id=f"iam-{self.deploy_env}-ec2-to-ecr-policy",
            policy_name=f"iam-{self.deploy_env}-ec2-to-ecr-policy",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "s3:PutObjectTagging",
                        "s3:DeleteObject",
                        "s3:ListBucket",
                        "s3:PutObject",
                        "ecr:*",
                        "cloudtrail:LookupEvents"
                    ],
                    resources=[
                        "*"
                    ],
                )
            ],
        )
        self.attach_inline_policy(policy)

        return policy

class EC2Stack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, *kwargs)

        #IAM role

        #EC2 instance

