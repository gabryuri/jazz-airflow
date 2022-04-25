import os

from aws_cdk import core
from aws_cdk import (
    aws_s3 as s3,
)

from storage.base import S3StorageBaseBucket, StorageLayer


class S3StorageStack(core.Stack):
    def __init__(self, scope: core.Construct, **kwargs):
        #self.deploy_env = os.environ["ENVIRONMENT"]
        super().__init__(scope, id=f"jazz-s3-storage-stack", **kwargs)

        self.s3_storage_landing = S3StorageBaseBucket(self, layer=StorageLayer.LANDING)

        # self.s3_storage_landing.add_lifecycle_rule(
        #     transitions=[
        #         s3.Transition(
        #             storage_class=s3.StorageClass.INTELLIGENT_TIERING,
        #             transition_after=core.Duration.days(90),
        #         ),
        #         s3.Transition(
        #             storage_class=s3.StorageClass.GLACIER,
        #             transition_after=core.Duration.days(360),
        #         ),
        #     ],
        #     enabled=True,
        # )

        # self.s3_storage_landing.add_lifecycle_rule(
        #     expiration=core.Duration.days(360),
        #     enabled=True,
        # )

        # self.s3_storage_processed = S3StorageBaseBucket(self, layer=StorageLayer.PROCESSED)

        # self.s3_storage_metadata = S3StorageBaseBucket(self, layer=StorageLayer.METADATA)
