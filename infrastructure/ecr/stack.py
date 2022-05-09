from aws_cdk import core
from aws_cdk import (
    aws_ecr as ecr
)
from constructs import Construct

class ECRStack(core.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, *kwargs)

        repository = ecr.Repository(self, "Repo",
            image_scan_on_push=True,
            repository_name='ecr-airflow'
        )

        repository.add_lifecycle_rule(tag_prefix_list=["prod"], max_image_count=150)
        repository.add_lifecycle_rule(max_image_age=core.Duration.days(30))

        parser_repo = ecr.Repository(self, "parser_repo",
            image_scan_on_push=True,
            repository_name='parser-repo'
        )

        parser_repo.add_lifecycle_rule(tag_prefix_list=["latest"], max_image_count=150)
        parser_repo.add_lifecycle_rule(max_image_age=core.Duration.days(30))